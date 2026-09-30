"""D120 division-free fast transport of a truncated moment functional.

Prototype, not a replacement moment solver.  Arithmetic uses Python integers
and a proved carry-free Kronecker product, including at precisions beyond
the frozen NumPy implementation's int64 limit.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
FP = [2, 0, -16, 0, 20, 0, -8, 0]
ZERO = (0,)*8
ONE = (1,)+(0,)*7


def source(p):
    p = Path(p).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


class Ring:
    def __init__(self, bits):
        self.bits = bits
        self.mod = 1 << bits
        self.product_count = 0
        self.maximum_packed_bytes = 0

    def add(self, a, b):
        return tuple((x+y) % self.mod for x, y in zip(a, b))

    def neg(self, a):
        return tuple(-x % self.mod for x in a)

    def padd(self, a, b):
        n = max(len(a), len(b))
        return [self.add(a[i] if i < len(a) else ZERO,
                         b[i] if i < len(b) else ZERO) for i in range(n)]

    def mul(self, a, b):
        return self.pmul([a], [b])[0]

    def pmul(self, a, b, limit=None):
        if not a or not b:
            return []
        if limit is not None:
            a, b = a[:limit], b[:limit]
        n = len(a)+len(b)-1
        # Every unreduced bivariate convolution coefficient has at most
        # 8*min(len(a),len(b)) products, each < 2^(2*bits).
        # The b-exponent is <=14, so a stride of 15 prevents row overlap.
        width = (2*self.bits+(8*min(len(a), len(b))).bit_length()+7)//8
        def pack(poly):
            buf = bytearray(len(poly)*15*width)
            for i, row in enumerate(poly):
                for j, c in enumerate(row):
                    offset = (15*i+j)*width
                    buf[offset:offset+width] = c.to_bytes(width, 'little')
            return int.from_bytes(buf, 'little')
        size = n*15*width
        self.maximum_packed_bytes = max(self.maximum_packed_bytes, size)
        self.product_count += 1
        raw = (pack(a)*pack(b)).to_bytes(size, 'little')
        result = []
        for i in range(n if limit is None else min(n, limit)):
            row = [int.from_bytes(raw[(15*i+j)*width:(15*i+j+1)*width], 'little') for j in range(15)]
            for k in range(14, 7, -1):
                for j in (0, 2, 4, 6):
                    row[k-8+j] -= row[k]*FP[j]
            result.append(tuple(c % self.mod for c in row[:8]))
        return result

    def ppow(self, a, n, limit):
        result = [ONE]
        while n:
            if n & 1:
                result = self.pmul(result, a, limit)
            n >>= 1
            if n:
                a = self.pmul(a, a, limit)
        return result

    def transform(self, moments, a, b, c, rows):
        """Return coefficients of sum m_k [(a*x+b)/(c*x+1)]^n.

        For the polynomial moment sequence (zero beyond the input), set
        A=a*T-c, D=1-b*T, Delta=a-b*c and K(S)=sum m_(k+1) S^k.
        The generating series is m0/D+Delta*T*K(A/D)/D^2.
        Homogenization, then unit-series inversion, avoids division by a,
        c, Delta or factorials.  Only the constant term 1 is inverted.
        """
        assert moments and rows > 0
        A, D = [self.neg(c), a], [ONE, self.neg(b)]
        geometric = [ONE]
        for _ in range(1, rows):
            geometric.append(self.mul(geometric[-1], b))
        result = self.pmul([moments[0]], geometric, rows)
        if len(moments) == 1 or rows == 1:
            return result
        cache = {}
        def power(which, n):
            key = which, n
            if key not in cache:
                cache[key] = self.ppow(A if which == 'A' else D, n, rows)
            return cache[key]
        def homogeneous(coeff):
            if len(coeff) == 1:
                return [coeff[0]]
            middle = len(coeff)//2
            # The two children have prescribed degrees middle-1 and
            # len(coeff)-middle-1; keep leading zero coefficients.
            lo, hi = homogeneous(coeff[:middle]), homogeneous(coeff[middle:])
            return self.padd(self.pmul(power('D', len(coeff)-middle), lo, rows),
                             self.pmul(power('A', middle), hi, rows))
        # H has prescribed degree len(moments)-2.  Thus D^2 K(A/D)
        # in the denominator is D^len(moments), without any cancellation.
        H = homogeneous(moments[1:])
        inverse = self.ppow(geometric, len(moments), rows-1)
        delta = self.add(a, self.neg(self.mul(b, c)))
        correction = self.pmul([delta], self.pmul(H, inverse, rows-1), rows-1)
        return self.padd(result, [ZERO]+correction)[:rows]


def slow_product(a, b, mod):
    result = [[0]*15 for _ in range(len(a)+len(b)-1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            for k, u in enumerate(x):
                for l, v in enumerate(y):
                    result[i+j][k+l] += u*v
    for row in result:
        for k in range(14, 7, -1):
            for j in range(8):
                row[k-8+j] -= row[k]*FP[j]
    return [tuple(x % mod for x in row[:8]) for row in result]


def controls():
    count = 0
    for bits in (3, 25, 129, 1536):
        r = Ring(bits)
        x = [tuple((r.mod-1-17*i-31*j) % r.mod for j in range(8)) for i in range(5)]
        y = [tuple((r.mod-3-19*i-13*j) % r.mod for j in range(8)) for i in range(7)]
        assert r.pmul(x, y) == slow_product(x, y, r.mod)
        # Compare the entire generating transform to an independent
        # coefficient recurrence, including nonunits and a zero determinant.
        for a, b, c in ((x[0], y[0], x[1]), (ZERO, ONE, ZERO), (ONE, ZERO, ONE)):
            moments = x
            got = r.transform(moments, a, b, c, 9)
            powers = [[ONE]+[ZERO]*4]
            for n in range(1, 9):
                row = [r.mul(b, powers[-1][0])]
                for k in range(1, 5):
                    row.append(r.add(r.add(r.mul(b, powers[-1][k]), r.mul(a, powers[-1][k-1])),
                                     r.neg(r.mul(c, row[-1]))))
                powers.append(row)
            expected = []
            for row in powers:
                acc = ZERO
                for q, m in zip(row, moments):
                    acc = r.add(acc, slow_product([q], [m], r.mod)[0])
                expected.append(acc)
            assert got == expected
            count += 1
    return {'arbitrary_precision_product_bits': [3, 25, 129, 1536],
            'independent_recurrence_controls': count,
            'integer_arithmetic_has_no_fixed_width_overflow': True}


def build():
    control = controls()
    bank_path = DATA/'dyadic_precision200_d115.json'
    transport_path = DATA/'dyadic_moment_transports_refined_d115.json'
    bank = json.loads(bank_path.read_text())
    packet = json.loads(transport_path.read_text())
    P = bank['working_precision_pi']
    assert P == 200
    r = Ring(P//8)
    def params(row):
        assert row['normalized_error_pi'] >= P
        return [tuple((q := Fraction(c)).numerator*pow(q.denominator, -1, r.mod) % r.mod for c in x)
                for x in row['normalized_center'][:3]]
    # Cover every state, both children and every distinct child map on one
    # actual harmonic basis column.  The prototype does not recompute a bank.
    state = [[tuple(m[0]) for m in row[:P]] for row in bank['state_moments_power_basis']]
    timings = []
    start = time.monotonic()
    unique = set()
    for edge, row in enumerate(packet['transitions']):
        total = [ZERO]*P
        for child in row['children']:
            pars = params(child)
            unique.add(tuple(pars))
            then = time.monotonic()
            got = r.transform(state[child['target_edge']], *pars, P)
            timings.append(time.monotonic()-then)
            total = r.padd(total, got)
        assert total == state[edge], ('state residual', edge)
        if edge % 30 == 0:
            print(f'MOBIUS_STATES|{edge+1}/174; seconds={time.monotonic()-start:.3f}', flush=True)
    state_seconds = time.monotonic()-start
    # The CM charts have a different input length: independently compare all
    # 17 against their frozen chart moments, still on the selected column.
    full = [[tuple(m[0]) for m in row] for row in bank['state_moments_power_basis']]
    chart_start = time.monotonic()
    cm = [row for row in packet['CM_charts'] if row['chart'] == 'A']
    for i, row in enumerate(cm):
        got = r.transform(full[row['target_edge']], *params(row), bank['CM_cutoff']+1)
        expected = [tuple(m[0]) for m in bank['CM_A_chart_moments'][i]['moments_power_basis']]
        assert got == expected, ('CM chart', i)
    result = {'status': 'pass', 'milestone': 'D120', 'controls': control,
        'frozen_working_precision_pi': P, 'basis_columns_checked': [0],
        'state_equations_checked': len(state), 'child_actions_checked': len(timings),
        'distinct_child_maps_checked': len(unique), 'CM_charts_checked': len(cm),
        'state_coefficients_checked': len(state)*P*8,
        'CM_coefficients_checked': len(cm)*(bank['CM_cutoff']+1)*8,
        'state_sweep_wall_seconds': state_seconds,
        'CM_charts_wall_seconds': time.monotonic()-chart_start,
        'median_child_wall_seconds': sorted(timings)[len(timings)//2],
        'maximum_packed_product_bytes': r.maximum_packed_bytes,
        'polynomial_products': r.product_count,
        'dense_operator_table_allocated': False,
        'actual_moment_precision_increased': False,
        'full_precision_solver_implemented': False,
        'candidate_identification_proved': False,
        'sources': [source(p) for p in (Path(__file__), bank_path, transport_path)]}
    print('MOBIUS_CONTROL|'+json.dumps({k:v for k,v in result.items() if k != 'sources'}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if args.controls:
        print(json.dumps(controls()), flush=True)
    else:
        out = DATA/'dyadic_mobius_transform_d120.json'
        assert not out.exists()
        out.write_text(json.dumps(build(), indent=2)+'\n')
    print('PASS|459_DYADIC_MOBIUS_TRANSFORM', flush=True)

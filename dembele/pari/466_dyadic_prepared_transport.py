"""D121 reusable transport plans with power-of-two reductions.

Exact arithmetic only.  The ring modulus is a power of two, so bit masks
replace general integer remainder operations, including on negative values.
Plans retain map-dependent powers across harmonic columns.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
s = importlib.util.spec_from_file_location('gmp', ROOT/'dembele/pari/463_dyadic_gmp_transport.py')
g = importlib.util.module_from_spec(s); s.loader.exec_module(g)
f = g.f


class Ring(g.Ring):
    def __init__(self, bits):
        super().__init__(bits)
        self.mask = self.mod-1

    def add(self, a, b):
        return tuple((x+y) & self.mask for x, y in zip(a, b))

    def neg(self, a):
        return tuple(-x & self.mask for x in a)

    def pmul(self, a, b, limit=None):
        if not a or not b: return []
        if limit is not None: a, b = a[:limit], b[:limit]
        n = len(a)+len(b)-1
        width = (2*self.bits+(8*min(len(a), len(b))).bit_length()+7)//8
        def pack(poly):
            buf = bytearray(len(poly)*15*width)
            for i, row in enumerate(poly):
                for j, c in enumerate(row):
                    offset = (15*i+j)*width
                    buf[offset:offset+width] = c.to_bytes(width, 'little')
            return buf
        size = n*15*width
        self.maximum_packed_bytes = max(self.maximum_packed_bytes, size)
        self.product_count += 1
        raw = g.G.product(pack(a), pack(b), size)
        result = []
        for i in range(n if limit is None else min(n, limit)):
            row = [int.from_bytes(raw[(15*i+j)*width:(15*i+j+1)*width], 'little') for j in range(15)]
            for k in range(14, 7, -1):
                for j in (0, 2, 4, 6): row[k-8+j] -= row[k]*f.FP[j]
            result.append(tuple(c & self.mask for c in row[:8]))
        return result

    def transform(self, moments, a, b, c, rows):
        return Plan(self, a, b, c, len(moments), rows).apply(moments)


class Plan:
    def __init__(self, ring, a, b, c, count, rows):
        assert count >= 1 and rows >= 1
        self.ring, self.count, self.rows = ring, count, rows
        self.delta = ring.add(a, ring.neg(ring.mul(b, c)))
        self.geometric = [f.ONE]
        for _ in range(1, rows): self.geometric.append(ring.mul(self.geometric[-1], b))
        self.A = [ring.neg(c), a]
        self.cache = {}
        self.scalar_powers = [[f.ONE], [f.ONE]]
        for i, x in enumerate(self.A):
            for _ in range(count): self.scalar_powers[i].append(ring.mul(self.scalar_powers[i][-1], x))
        self.inverse = []
        binomial = 1
        for j in range(rows-1):
            reduced = binomial & ring.mask
            self.inverse.append(tuple(reduced*x & ring.mask for x in self.geometric[j]))
            numerator = binomial*(count+j)
            assert numerator % (j+1) == 0
            binomial = numerator//(j+1)

    def power(self, which, n):
        key = which, n
        if key not in self.cache:
            r = self.ring
            ans, binomial = [], 1
            for k in range(n+1):
                if which == 'D':
                    # D=1-b*T.  The same powers also supplied the inverse.
                    value = self.geometric[k] if k % 2 == 0 else r.neg(self.geometric[k])
                else:
                    value = r.mul(self.scalar_powers[0][n-k], self.scalar_powers[1][k])
                reduced = binomial & r.mask
                ans.append(tuple(reduced*x & r.mask for x in value))
                if k < n:
                    numerator = binomial*(n-k)
                    assert numerator % (k+1) == 0
                    binomial = numerator//(k+1)
            self.cache[key] = ans[:self.rows]
        return self.cache[key]

    def apply(self, moments):
        r, count, rows = self.ring, self.count, self.rows
        assert len(moments) == count
        result = r.pmul([moments[0]], self.geometric, rows)
        if count == 1 or rows == 1: return result
        def homogeneous(coeff):
            if len(coeff) == 1: return [coeff[0]]
            middle = len(coeff)//2
            return r.padd(r.pmul(self.power('D', len(coeff)-middle), homogeneous(coeff[:middle]), rows),
                          r.pmul(self.power('A', middle), homogeneous(coeff[middle:]), rows))
        H = homogeneous(moments[1:])
        correction = r.pmul([self.delta], r.pmul(H, self.inverse, rows-1), rows-1)
        return r.padd(result, [f.ZERO]+correction)[:rows]


def build(target=False):
    original = f.Ring; f.Ring = Ring
    try: controls = f.controls()
    finally: f.Ring = original
    # Additional independent products exercise the GMP branch at large bits.
    ring = Ring(1536)
    x = [tuple((ring.mod-17*i-31*j-1) & ring.mask for j in range(8)) for i in range(5)]
    y = [tuple((ring.mod-13*i-19*j-3) & ring.mask for j in range(8)) for i in range(7)]
    assert ring.pmul(x, y) == f.slow_product(x, y, ring.mod)
    benchmarks = []
    previous = None
    for P in ([10552] if target else [200, 400, 800, 1600]):
        ring = Ring(P//8)
        pi = (0, 1, 0, 0, 0, 0, 0, 0)
        unit = tuple((ring.mod-7-19*j) & ring.mask for j in range(8))
        b = tuple((ring.mod-3-11*j) & ring.mask for j in range(8))
        c = ring.mul(pi, unit); a = ring.add(pi, ring.mul(b, c))
        values = [tuple((ring.mod-1-17*i-31*j) & ring.mask for j in range(8)) for i in range(P)]
        begin = time.monotonic(); plan = Plan(ring, a, b, c, P, P)
        prepare_seconds = time.monotonic()-begin
        begin = time.monotonic(); answer = plan.apply(values)
        first_seconds = time.monotonic()-begin
        begin = time.monotonic(); doubled = plan.apply([ring.add(x, x) for x in values])
        reused_seconds = time.monotonic()-begin
        assert doubled == [ring.add(x, x) for x in answer]
        if previous:
            oldP, old = previous; mask = (1 << (oldP//8))-1
            assert [tuple(x & mask for x in row) for row in answer[:oldP]] == old
        previous = P, answer
        small = g.Ring(25)
        check = small.transform([tuple(x % small.mod for x in v) for v in values[:200]],
            *[tuple(x % small.mod for x in z) for z in (a, b, c)], 200)
        assert [tuple(x % small.mod for x in row) for row in answer[:200]] == check
        row = {'synthetic_P':P, 'modulus_bits':P//8, 'prepare_seconds':prepare_seconds,
               'first_apply_seconds':first_seconds, 'reused_apply_seconds':reused_seconds,
               'first_total_seconds':prepare_seconds+first_seconds,
               'maximum_packed_product_bytes':ring.maximum_packed_bytes,
               'cached_polynomial_coefficient_count':sum(map(len, plan.cache.values()))}
        benchmarks.append(row)
        print('PREPARED_TRANSPORT|'+json.dumps(row), flush=True)
    return {'status':'pass', 'milestone':'D121', 'arithmetic_controls':controls,
        'independent_large_product_checked':True, 'synthetic_benchmarks':benchmarks,
        'reused_plan_linearity_control_passed':True,
        'actual_moment_precision_increased':False,
        'sources':[f.source(p) for p in [Path(__file__), Path(g.__file__), Path(f.__file__),
            g.LIB, g.HEADER, DATA/'dyadic_gmp_target_cost_d120.json']]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--target', action='store_true')
    args = parser.parse_args()
    out = DATA/('dyadic_prepared_target_d121.json' if args.target else 'dyadic_prepared_transport_d121.json')
    assert not out.exists()
    out.write_text(json.dumps(build(args.target), indent=2)+'\n')
    print('PASS|466_DYADIC_PREPARED_TRANSPORT', flush=True)

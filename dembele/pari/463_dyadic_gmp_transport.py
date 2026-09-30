"""D120 GMP acceleration and integral binomial linear-form powers.

No package installation, new Hecke data or new arithmetic moments.  The
local GMP ABI is recorded and checked against its installed public header.
"""
import argparse
import ctypes as C
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
s = importlib.util.spec_from_file_location('prototype', ROOT/'dembele/pari/459_dyadic_mobius_transform.py')
f = importlib.util.module_from_spec(s)
s.loader.exec_module(f)
LIB = Path('/opt/homebrew/lib/libgmp.dylib').resolve()
HEADER = Path('/opt/homebrew/opt/gmp/include/gmp.h').resolve()


class Mpz(C.Structure):
    _fields_ = [('alloc', C.c_int), ('size', C.c_int), ('limbs', C.c_void_p)]


class GMP:
    def __init__(self):
        header = HEADER.read_text()
        assert 'int _mp_alloc;' in header and 'int _mp_size;' in header and 'mp_limb_t *_mp_d;' in header
        lib = C.CDLL(str(LIB))
        ptr = C.POINTER(Mpz)
        def bind(name, args, result=None):
            fun = getattr(lib, '__gmpz_'+name)
            fun.argtypes, fun.restype = args, result
            return fun
        self.init = bind('init', [ptr])
        self.clear = bind('clear', [ptr])
        self.imp = bind('import', [ptr, C.c_size_t, C.c_int, C.c_size_t, C.c_int, C.c_size_t, C.c_void_p])
        self.exp = bind('export', [C.c_void_p, C.POINTER(C.c_size_t), C.c_int, C.c_size_t, C.c_int, C.c_size_t, ptr], C.c_void_p)
        self.mul = bind('mul', [ptr, ptr, ptr])
        self.sizeinbase = bind('sizeinbase', [ptr, C.c_int], C.c_size_t)
        self.version = C.c_char_p.in_dll(lib, '__gmp_version').value.decode()

    def product(self, a, b, size):
        if max(len(a), len(b)) < 4096:
            return (int.from_bytes(a, 'little')*int.from_bytes(b, 'little')).to_bytes(size, 'little')
        x, y, z = Mpz(), Mpz(), Mpz()
        for value in (x, y, z):
            self.init(C.byref(value))
        try:
            abuf = (C.c_ubyte*len(a)).from_buffer(a)
            bbuf = (C.c_ubyte*len(b)).from_buffer(b)
            self.imp(C.byref(x), len(a), -1, 1, 0, 0, abuf)
            self.imp(C.byref(y), len(b), -1, 1, 0, 0, bbuf)
            self.mul(C.byref(z), C.byref(x), C.byref(y))
            assert (self.sizeinbase(C.byref(z), 2)+7)//8 <= size
            buf = C.create_string_buffer(size)
            count = C.c_size_t()
            self.exp(buf, C.byref(count), -1, 1, 0, 0, C.byref(z))
            assert count.value <= size
            return buf.raw
        finally:
            for value in (x, y, z):
                self.clear(C.byref(value))


G = GMP()


class Ring(f.Ring):
    def pmul(self, a, b, limit=None):
        if not a or not b:
            return []
        if limit is not None:
            a, b = a[:limit], b[:limit]
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
        raw = G.product(pack(a), pack(b), size)
        result = []
        for i in range(n if limit is None else min(n, limit)):
            row = [int.from_bytes(raw[(15*i+j)*width:(15*i+j+1)*width], 'little') for j in range(15)]
            for k in range(14, 7, -1):
                for j in (0, 2, 4, 6):
                    row[k-8+j] -= row[k]*f.FP[j]
            result.append(tuple(c % self.mod for c in row[:8]))
        return result

    def transform(self, moments, a, b, c, rows):
        assert moments and rows > 0
        count = len(moments)
        geometric = [f.ONE]
        for _ in range(1, rows):
            geometric.append(self.mul(geometric[-1], b))
        result = self.pmul([moments[0]], geometric, rows)
        if count == 1 or rows == 1:
            return result
        A, D = [self.neg(c), a], [f.ONE, self.neg(b)]
        cache = {}
        def power(which, n):
            key = which, n
            if key not in cache:
                x, y = A if which == 'A' else D
                xp, yp = [f.ONE], [f.ONE]
                for _ in range(n):
                    xp.append(self.mul(xp[-1], x))
                    yp.append(self.mul(yp[-1], y))
                ans, binomial = [], 1
                for k in range(n+1):
                    value = self.mul(xp[n-k], yp[k])
                    ans.append(tuple(binomial*u % self.mod for u in value))
                    # Division is exact in Z, before reduction in the ring.
                    if k < n:
                        numerator = binomial*(n-k)
                        assert numerator % (k+1) == 0
                        binomial = numerator//(k+1)
                cache[key] = ans[:rows]
            return cache[key]
        def homogeneous(coeff):
            if len(coeff) == 1:
                return [coeff[0]]
            middle = len(coeff)//2
            return self.padd(self.pmul(power('D', len(coeff)-middle), homogeneous(coeff[:middle]), rows),
                             self.pmul(power('A', middle), homogeneous(coeff[middle:]), rows))
        H = homogeneous(moments[1:])
        # (1-b*T)^(-count) uses integral binomial coefficients. No field
        # division by an even integer, a determinant or a map parameter.
        inverse, binomial = [], 1
        for j in range(rows-1):
            inverse.append(tuple(binomial*u % self.mod for u in geometric[j]))
            numerator = binomial*(count+j)
            assert numerator % (j+1) == 0
            binomial = numerator//(j+1)
        delta = self.add(a, self.neg(self.mul(b, c)))
        correction = self.pmul([delta], self.pmul(H, inverse, rows-1), rows-1)
        return self.padd(result, [f.ZERO]+correction)[:rows]


def build(target=False):
    # Large-buffer import/export and carries are checked against Python's
    # independent arbitrary integers, including zero and unequal lengths.
    for na, nb in ((0, 5000), (5001, 4096), (8193, 4127)):
        a = bytearray((17*i+23) % 256 for i in range(na))
        b = bytearray((13*i+31) % 256 for i in range(nb))
        if na == 0:
            a = bytearray(5000)
        got = G.product(a, b, len(a)+len(b))
        assert int.from_bytes(got, 'little') == int.from_bytes(a, 'little')*int.from_bytes(b, 'little')
    original = f.Ring
    f.Ring = Ring
    try:
        controls = f.controls()
        actual = None if target else f.build()
    finally:
        f.Ring = original
    bench, previous = [], None
    sizes = [10552] if target else [200, 400, 800, 1600]
    for P in sizes:
        ring = Ring(P//8)
        pi = (0, 1, 0, 0, 0, 0, 0, 0)
        unit = tuple((ring.mod-7-19*j) % ring.mod for j in range(8))
        bb = tuple((ring.mod-3-11*j) % ring.mod for j in range(8))
        cc = ring.mul(pi, unit)
        aa = ring.add(pi, ring.mul(bb, cc))
        moments = [tuple((ring.mod-1-17*i-31*j) % ring.mod for j in range(8)) for i in range(P)]
        start = time.monotonic()
        result = ring.transform(moments, aa, bb, cc, P)
        elapsed = time.monotonic()-start
        if previous:
            oldP, old = previous
            modulus = 1 << (oldP//8)
            assert [tuple(c % modulus for c in row) for row in result[:oldP]] == old
        previous = P, result
        # Independently agree with the original Python implementation at
        # P=200, including for the target-size synthetic calculation.
        if P == sizes[0]:
            small = original(25)
            pars = [tuple(x % small.mod for x in z) for z in (aa, bb, cc)]
            vals = [tuple(x % small.mod for x in z) for z in moments[:200]]
            check = small.transform(vals, *pars, 200)
            assert [tuple(x % small.mod for x in z) for z in result[:200]] == check
        row = {'synthetic_P': P, 'coefficient_modulus_bits': P//8,
               'single_action_wall_seconds': elapsed,
               'maximum_packed_product_bytes': ring.maximum_packed_bytes,
               'polynomial_products': ring.product_count}
        bench.append(row)
        print('GMP_COST|'+json.dumps(row), flush=True)
    return {'status': 'pass', 'milestone': 'D120', 'GMP_version': G.version,
        'public_ABI_header_checked': True, 'large_buffer_python_integer_controls': 3,
        'arithmetic_controls': controls, 'actual_frozen_bank_checks': actual,
        'synthetic_benchmarks': bench,
        'all_binomial_divisions_exact_in_Z_before_reduction': True,
        'actual_moment_precision_increased': False,
        'full_precision_solver_implemented': False,
        'target_synthetic_action_is_not_an_actual_refinement': target,
        'sources': [f.source(p) for p in [Path(__file__), Path(f.__file__), LIB, HEADER,
            DATA/'dyadic_precision_design_d120.json']]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', action='store_true')
    args = parser.parse_args()
    out = DATA/('dyadic_gmp_target_cost_d120.json' if args.target else 'dyadic_gmp_transport_d120.json')
    assert not out.exists()
    out.write_text(json.dumps(build(args.target), indent=2)+'\n')
    print('PASS|463_DYADIC_GMP_TRANSPORT', flush=True)

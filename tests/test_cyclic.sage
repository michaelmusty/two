# Tests for belyi/cyclic.sage (M2), verified through belyi/verify.sage (M1).
load("belyi/verify.sage")
load("belyi/cyclic.sage")
from sage.all import GF, Infinity

PASS = 0; FAIL = 0
def check(name, fn):
    global PASS, FAIL
    try:
        fn(); print(f"  ok   {name}"); PASS += 1
    except Exception as e:
        print(f"  FAIL {name}: {e}"); FAIL += 1

# C16 y^16 = (x-1)  (thesis oracle f16T1-1,16,16-g0, up to unit): passport (1,16,16) genus 0
def c16():
    L, x, f = cyclic_absolute(GF(7), 4, 0, 1)
    r = verify_belyi(L, x, expected_passport=(1, 16, 16), expected_genus=0, name="C16")
    assert cyclic_passport(4, 0, 1) == (1, 16, 16), cyclic_passport(4, 0, 1)

# C16 y^16 = x(x-1): predicted passport (16,16,8); confirm Belyi + passport formula matches verifier
def c16_ab():
    L, x, f = cyclic_absolute(GF(7), 4, 1, 1)
    r = verify_belyi(L, x, name="C16 x(x-1)")
    assert tuple(sorted(r['passport'])) == tuple(sorted(cyclic_passport(4, 1, 1))), \
        (r['passport'], cyclic_passport(4, 1, 1))
    assert cyclic_passport(4, 1, 1) == (16, 16, 8)

# C8 y^8 = x^3(x-1): passport formula vs verifier, and genus consistency
def c8():
    L, x, f = cyclic_absolute(GF(5), 3, 3, 1)
    r = verify_belyi(L, x, name="C8 x^3(x-1)")
    assert tuple(sorted(r['passport'])) == tuple(sorted(cyclic_passport(3, 3, 1)))

# C4 y^4 = x(x-1): passport (4,4,2)
def c4():
    L, x, f = cyclic_absolute(GF(3), 2, 1, 1)
    r = verify_belyi(L, x, expected_passport=(4, 4, 2), name="C4 x(x-1)")

for nm, fn in [("C16 (1,16,16)", c16), ("C16 x(x-1)", c16_ab),
               ("C8 x^3(x-1)", c8), ("C4 x(x-1)", c4)]:
    check(nm, fn)
print(f"\n{PASS} passed, {FAIL} failed")

# Tests for belyi/verify.sage against explicit thesis oracle equations.
load("belyi/verify.sage")
from sage.all import FunctionField, GF, QQ, Infinity, PolynomialRing

PASS = 0; FAIL = 0
def check(name, fn):
    global PASS, FAIL
    try:
        fn(); print(f"  ok   {name}"); PASS += 1
    except Exception as e:
        print(f"  FAIL {name}: {e}"); FAIL += 1

def make(field, poly_in_xy):
    K = FunctionField(field, 'x'); x = K.gen()
    R = PolynomialRing(K, 'Y'); Y = R.gen()
    F = poly_in_xy(x, Y)
    L = K.extension(F, 'y')
    return L, x

# --- Oracle 1: y^16 = 1 - x   (f16T1-1,16,16-g0): deg16 genus0 passport {1,16,16}
def o1():
    L, x = make(QQ, lambda x, Y: Y**16 - (1 - x))
    r = verify_belyi(L, x, expected_passport=(1, 16, 16), expected_genus=0, name="C16 y^16=1-x")
    assert r['degree'] == 16

# --- Oracle 2: y^16 + (4x-2)y^8 + 1  (f16T13-2,2,8-g0): deg16 genus0 passport {2,2,8}
def o2():
    L, x = make(GF(7), lambda x, Y: Y**16 + (4*x - 2)*Y**8 + 1)
    verify_belyi(L, x, expected_passport=(2, 2, 8), expected_genus=0, name="16T13 y^16+(4x-2)y^8+1")

# --- Oracle 3: y^16 = -x^2 (x-1)^7  (f16T1-8,16,16-g7): deg16 genus7 passport {8,16,16}
def o3():
    L, x = make(GF(5), lambda x, Y: Y**16 + x**2 * (x - 1)**7)
    verify_belyi(L, x, expected_passport=(8, 16, 16), expected_genus=7, name="16T1 y^16=-x^2(x-1)^7")

# --- Oracle 4: y^8 + 2x^6+2x^5+2x^4+x^3+x^2+x  over F_3 (8T1-8,8,4-g3): deg8 genus3
def o4():
    L, x = make(GF(3), lambda x, Y: Y**8 + 2*x**6 + 2*x**5 + 2*x**4 + x**3 + x**2 + x)
    verify_belyi(L, x, expected_passport=(8, 8, 4), expected_genus=3, name="8T1 deg8/F3")

# --- Negative control: y^2 = x(x-1)(x-2) over F_5 ramifies over x=2 -> NOT Belyi
def neg():
    L, x = make(GF(5), lambda x, Y: Y**2 - x*(x - 1)*(x - 2))
    threw = False
    try:
        verify_belyi(L, x, name="neg control (should fail)")
    except AssertionError:
        threw = True
    assert threw, "verifier failed to reject a non-Belyi cover"

for nm, fn in [("oracle1 C16", o1), ("oracle2 16T13", o2), ("oracle3 g7", o3),
               ("oracle4 deg8/F3", o4), ("negative control", neg)]:
    check(nm, fn)

print(f"\n{PASS} passed, {FAIL} failed")

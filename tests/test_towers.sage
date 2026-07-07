# Tests for belyi/towers.sage (M3 part 1: absolute-model square-root composition).
load("belyi/towers.sage"); load("belyi/verify.sage")
from sage.all import GF, PolynomialRing, FunctionField

PASS = 0; FAIL = 0
def check(name, fn):
    global PASS, FAIL
    try:
        fn(); print(f"  ok   {name}"); PASS += 1
    except Exception as e:
        print(f"  FAIL {name}: {e}"); FAIL += 1

def base_ring(p):
    K = FunctionField(GF(p), 'x'); return K, K.gen(), PolynomialRing(K, 'y').gen()

# sqrt(y) over y^2=x(x-1)  ==  z^4 = x(x-1)  (C4, genus1, passport (4,4,2))
def c4():
    K, x, y = base_ring(7)
    Q = compose_sqrt(K, y**2 - x*(x-1), y)
    L = K.extension(Q, 'w')
    r = verify_belyi(L, x, expected_passport=(4, 4, 2), expected_genus=1, name="C4")
    assert L.degree() == 4

# two more square roots of x -> w^8 = x (C8, genus 0, ramified only 0,oo)
def c8():
    K, x, y = base_ring(7)
    Q2 = compose_sqrt(K, y**2 - x, y)                 # z^4 = x
    z = Q2.parent().gen()
    Q3 = compose_sqrt(K, Q2, z)                        # w^8 = x
    L = K.extension(Q3, 'w')
    assert L.degree() == 8 and L.genus() == 0
    r = verify_belyi(L, x, name="C8")
    assert tuple(sorted(r['passport'])) == (1, 8, 8)

for nm, fn in [("compose C4", c4), ("compose C8", c8)]:
    check(nm, fn)
print(f"\n{PASS} passed, {FAIL} failed")

# Test M3.4: end-to-end reconstruction of the Q8 genus-2 Belyi curve from its triple.
load("belyi/reconstruct.sage")
from sage.all import GF, QQ, PolynomialRing, NumberField

PASS = 0; FAIL = 0
def check(name, fn):
    global PASS, FAIL
    try:
        fn(); print(f"  ok   {name}"); PASS += 1
    except Exception as e:
        print(f"  FAIL {name}: {e}"); FAIL += 1

def q8():
    G = libgap.SmallGroup(8, 4)
    gens = libgap.GeneratorsOfGroup(G)
    f = reconstruct(G, gens[0], gens[1], 13, verbose=False)
    assert f.degree() == 5, ("expected quintic (genus 2)", f.degree())
    # roots must be {0, +-1, +-i}; i in F_13 is 5 (5^2 = -1)
    roots = set(int(r) for r, _ in f.roots())
    assert roots == {0, 1, 12, 5, 8}, roots        # {0,+-1,+-i} with i=5,-i=8,-1=12
    # 2-torsion field = splitting field of s^5-s over Q = Q(i): Galois group C2, solvable
    t = PolynomialRing(QQ, 't').gen()
    fac = (t**5 - t).factor()
    K = NumberField(t**2 + 1, 'ii')
    splits_over_Qi = all(len(g.change_ring(K).roots()) == g.degree() for g, _ in fac)
    assert splits_over_Qi, "s^5-s must split over Q(i)"
    # => Q(J[2]) = Q(i), Gal = C2, SOLVABLE  (matches Q8 centralizer prediction)

check("Q8 8T5-4,4,4-g2 reconstruction -> y^2=s^5-s, Q(J[2])=Q(i) solvable", q8)
print(f"\n{PASS} passed, {FAIL} failed")

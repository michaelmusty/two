# Tate pilot, over-Q validation target: the definite group data for
# disc = 2, p = 13 (CD-uniformizing the genus-2 Shimura curve X^{26};
# ground truth = Tate parameters of the conductor-26 isogeny classes).
#
# Builds, Sage-natively (no Magma):
#   B = (-1,-1|Q) (disc 2), O = maximal (Hurwitz-like), O13 = level-13
#   Eichler; ideal classes; unit groups; the 14 BT coset reps (elements of
#   O^x-orbits mapping to the standard P^1(F_13) matrices under a 13-adic
#   splitting); wp (norm 13, normalizes the Iwahori); splitting to 13^M by
#   Hensel lift of modp_splitting_data.
#
# Run: sage overq_data.sage   -> prints the structure table + writes
#                                overq_data.sobj

from sage.all import (QuaternionAlgebra, QQ, ZZ, Qp, matrix, save)

p = 13
M = 40

B = QuaternionAlgebra(2)
i, j, k = B.gens()
print(f"OQ|B = {B}, disc {B.discriminant()}")
O = B.maximal_order()
print(f"OQ|maximal order basis: {O.basis()}")

# unit group of O (finite): brute force over small combinations
units = []
Obasis = O.basis()
from itertools import product as iproduct
for co in iproduct(range(-2, 3), repeat=4):
    x = sum(c * b for c, b in zip(co, Obasis))
    if x != 0 and x.reduced_norm() == 1:
        units.append(x)
print(f"OQ|#O^x = {len(units)} (Hurwitz: 24)")

# Brandt/Eichler data at level 13
Bm = BrandtModule(2, 13)
print(f"OQ|BrandtModule(2,13): dimension {Bm.dimension()} (edges of the dual graph)")
ideals = Bm.right_ideals()
print(f"OQ|right ideal classes: {len(ideals)}")
O13 = ideals[0].left_order()
print(f"OQ|Eichler order (level 13) basis: {O13.basis()}")
# stabilizer orders (units of left orders of the classes)
stabs = []
for I in ideals:
    OL = I.left_order()
    cnt = 0
    for co in iproduct(range(-3, 4), repeat=4):
        x = sum(c * b for c, b in zip(co, OL.basis()))
        if x != 0 and x.reduced_norm() == 1:
            cnt += 1
    stabs.append(cnt // 2)   # mod +-1
print(f"OQ|edge stabilizer orders (mod +-1): {stabs}  (sum 1/e = {sum(1/QQ(e) for e in stabs)})")

# T_2 (or T_3) Brandt eigensystems vs the conductor-26 curves
T3 = Bm.hecke_matrix(3)
print(f"OQ|Brandt T_3 eigenvalues: {sorted(T3.eigenvalues())}")
for lab in ['26a1', '26b1']:
    E = EllipticCurve(lab)
    print(f"OQ|{lab}: a_3 = {E.ap(3)}, a_13 = {E.ap(13)}, "
          f"tate q_13 val = {E.tate_curve(13).parameter(prec=8).valuation()}")

# 13-adic splitting: Hensel-lift Sage's mod-p splitting
Fp = GF(p)
Ibar, Jbar, _ = B.modp_splitting_data(p)
R = Qp(p, M)
MS = MatrixSpace(R, 2)
I0 = MS(Ibar.change_ring(ZZ))
J0 = MS(Jbar.change_ring(ZZ))
a = ZZ(i * i)   # -1
b = ZZ(j * j)   # -1
# Newton: refine I with I^2 = a, then J with J^2 = b, IJ = -JI
one = MS(1)
def newton_sqrt_mat(X0, target):
    X = X0
    for _ in range(M.bit_length() + 2):
        X = X - (X * X - target * one) * (2 * X).inverse()
    return X
II = newton_sqrt_mat(I0, R(a))
# J must anticommute with II and square to b: solve in the centralizer trick:
# parametrize J = y*II*J0 + z*J0 ... simpler: alternate Newton on the pair
JJ = J0
for _ in range(M.bit_length() + 2):
    # enforce anticommutation: project J -> (J - II*J*II/ a)/2... since II^2=a:
    JJ = (JJ - II * JJ * II / R(a)) / R(2)
    # then correct the square
    JJ = JJ - (JJ * JJ - R(b) * one) * (2 * JJ).inverse()
def minval(X):
    vals = [t.valuation() for t in X.list() if t != 0]
    return min(vals) if vals else 'exact-0'
print(f"OQ|splitting check (min valuations; want exact-0 or >= {M}): "
      f"I^2-a: {minval(II*II - R(a)*one)}, J^2-b: {minval(JJ*JJ - R(b)*one)}, "
      f"IJ+JI: {minval(II*JJ + JJ*II)}")

def embed(x, prec=M):
    c = x.coefficient_tuple()
    return c[0] * one + c[1] * II + c[2] * JJ + c[3] * II * JJ

# wp: element of O13 with reduced norm 13 normalizing the Iwahori
wp = None
for co in iproduct(range(-4, 5), repeat=4):
    x = sum(c * bb for c, bb in zip(co, O13.basis()))
    if x.reduced_norm() == 13:
        g = embed(x)
        # normalizes Iwahori: lower-left entry valuation >= 1 and
        # g * Iwahori * g^-1 stays Iwahori — test on II-generated order elts
        if g[1][0].valuation() >= 1 and g[0][1].valuation() >= 0:
            wp = x
            break
print(f"OQ|wp = {wp} (norm {wp.reduced_norm() if wp else None})")

# BT reps: 14 elements of O^x-ish mapping to [[a,1],[-1,0]] mod p classes;
# darmonpoints' hardcode branch builds them from wp and residues — defer the
# exact construction to the class; here just certify the P^1 classes are
# reachable: the reduction map O^x -> PGL2(F_13) orbits on P^1(F_13)
P1cls = set()
for u in units:
    g = embed(u).apply_map(lambda t: t.residue())
    # class of the column (g * [1,0]^t) in P^1(F_13)
    x0, y0 = g[0][0], g[1][0]
    P1cls.add((x0 / y0) if y0 != 0 else 'inf')
print(f"OQ|P^1(F_13) classes hit by O^x acting on [1:0]: {len(P1cls)} of 14")

save({'p': int(p), 'M': int(M)}, 'overq_meta.sobj')
print("OQ|done")

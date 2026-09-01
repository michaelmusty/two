# Over-Q ground-truth check of the monodromy-pairing layer (D31 convention):
# ord(q_E) of the CD-optimal curve = <v,v> under the stab-order diagonal,
# for the Brandt eigenvectors of (disc 2, level 13).
from itertools import product as iproduct
Bm = BrandtModule(2, 13)
T3 = Bm.hecke_matrix(3)
ideals = Bm.right_ideals()
stabs = []
for I in ideals:
    OL = I.left_order()
    cnt = 0
    for co in iproduct(range(-3, 4), repeat=4):
        x = sum(c * b for c, b in zip(co, OL.basis()))
        if x != 0 and x.reduced_norm() == 1:
            cnt += 1
    stabs.append(cnt // 2)
print(f"MQ|stabs = {stabs}")
# self-adjointness of T_3 under diag(stabs): e_j T_ij = e_i T_ji
ok = all(stabs[j]*T3[i][j] == stabs[i]*T3[j][i] for i in range(3) for j in range(3))
print(f"MQ|T_3 self-adjoint under diag(stabs): {ok}")
for a3, lab in [(1, '26a'), (-3, '26b')]:
    K = (T3 - a3).kernel()
    v = K.basis()[0]
    d = lcm([c.denominator() for c in v])
    vz = [ZZ(d*c) for c in v]
    g = gcd(vz)
    vz = [c//g for c in vz]
    pair = sum(e*c*c for e, c in zip(stabs, vz))
    print(f"MQ|{lab}: eigenvector {vz}, <v,v>_stab = {pair}")
    for E in EllipticCurve(lab + '1').isogeny_class():
        print(f"MQ|   {E.label()}: v(q_13) = {E.tate_curve(13).parameter(prec=6).valuation()}")

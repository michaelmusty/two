# Pin the normalization: <v,v>_stab vs 2*v(q_optimal) across several (D,p).
from itertools import product as iproduct
def check(D, p, iso_labels):
    Bm = BrandtModule(D, p)
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
    ell = next(l for l in [3,5,7,11] if D*p % l != 0)
    T = Bm.hecke_matrix(ell)
    print(f"NM|(D,p)=({D},{p}) dim {Bm.dimension()} stabs {stabs} using T_{ell}")
    for lab in iso_labels:
        E0 = EllipticCurve(lab)
        a = E0.ap(ell)
        K = (T - a).kernel()
        if K.dimension() != 1:
            print(f"NM| {lab}: eigenspace dim {K.dimension()} != 1, skip")
            continue
        v = K.basis()[0]
        d = lcm([c.denominator() for c in v]); vz = [ZZ(d*c) for c in v]
        g = gcd(vz); vz = [c//g for c in vz]
        pair = sum(e*c*c for e, c in zip(stabs, vz))
        vals = sorted(set(E.tate_curve(p).parameter(prec=6).valuation()
                          for E in E0.isogeny_class()))
        print(f"NM| {lab}: <v,v> = {pair}, halves = {pair/2}, class v(q)s = {vals}, "
              f"match/2: {pair/2 in vals}")
check(2, 13, ['26a1', '26b1'])
check(2, 7, ["14a1"])
check(3, 5, ["15a1"])
check(2, 7, ['14a1'])
check(5, 11, ["55a1"])

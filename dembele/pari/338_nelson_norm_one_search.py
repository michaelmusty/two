"""D92: complete bounded enumeration after fixing reduced norm to one.

At the seven compact places Nrd=1. An anisotropic rational majorant
therefore avoids the large all-norm central-unit covering ellipsoid.
Every positive unit is a square, certified by full unit signature rank.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time
from sage.all import (AA, GF, QQ, ZZ, NumberField, PolynomialRing, QuaternionAlgebra,
                      RealBallField, RealField, matrix, vector)

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"


def source(p):
    return {"path":str(p.relative_to(ROOT)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}


def rows(m):return [[str(c) for c in row] for row in m.rows()]


def setup():
    paths=[DATA/"cm_orbit.json",DATA/"nelson_cm_lattice_d90.json",DATA/"nelson_primitive_classes_d91.json"]
    raw,local,old=[json.loads(p.read_text()) for p in paths]
    P=PolynomialRing(QQ,"s");s=P.gen();F=NumberField(s**8-8*s**6+20*s**4-16*s*s+2,"b");b=F.gen()
    B=QuaternionAlgebra(F,b-b*b,-1)
    def quat(v):return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    def coords(q):return vector(QQ,sum([list(c.vector()) for c in q.coefficient_tuple()],[]))
    basis=[quat(v) for v in raw["quaternion_export"]["order_basis"]]
    beta=quat(local["arithmetic"]["CM_beta_power_coordinates"])
    par=[(q+beta*q*beta**(-1))/2 for q in basis]
    perp=[q-p for q,p in zip(basis,par)]
    pair=lambda q,r:(q*r.conjugate()).reduced_trace()/2
    Gpar=matrix(F,[[pair(q,r) for r in par] for q in par])
    Gperp=matrix(F,[[pair(q,r) for r in perp] for q in perp])
    places=sorted(F.embeddings(AA),key=lambda p:p(b));RB=RealBallField(256)
    # These eight signatures span the entire possible signature space.
    cosines=[F(2),b]
    for _ in range(2,8):cosines.append(b*cosines[-1]-cosines[-2])
    units=[F(-1)]+[1+sum(cosines[1:j+1]) for j in range(1,8)]
    signatures=[]
    for u in units:
        assert u.is_integral() and (1/u).is_integral() and abs(u.norm())==1
        values=[RB(p(u)) for p in places];assert all(not v.contains_zero() for v in values)
        signatures.append([int(v.upper()<0) for v in values])
    assert matrix(GF(2),signatures).rank()==8
    signature_proof={"units_power_coordinates":[list(map(str,u.vector())) for u in units],
                     "signatures":signatures,"rank_over_F2":8,
                     "consequence":"Every totally positive unit is a square: signature map on O_F^*/O_F^{*2} has size 2^8."}
    roots=[[str(QQ(RB(p(b)).lower())),str(QQ(RB(p(b)).upper()))] for p in places]
    return locals()


def search(d,T):
    started=time.monotonic()
    F,B,b=d["F"],d["B"],d["b"];places=d["places"];RF=RealField(200);RB=d["RB"]
    vandermonde=matrix(RF,[[RF(p(b))**j for j in range(8)] for p in places])
    weights=[];bounds=[];epsilon=QQ(1)/1000
    for sign in [1,-1]:
        target=vector(RF,[RF(QQ(sign)/(2*T)) if i==4 else RF(1) for i in range(8)])
        approximation=vandermonde.solve_right(target)
        coeff=[QQ((x*10**15).round())/10**15 for x in approximation]
        w=F(coeff);intervals=[]
        for i,p in enumerate(places):
            value=RB(p(w));expected=QQ(sign)/(2*T) if i==4 else QQ(1)
            assert value.lower()>expected-abs(expected)*epsilon
            assert value.upper()<expected+abs(expected)*epsilon
            intervals.append([str(QQ(value.lower())),str(QQ(value.upper()))])
        weights.append(w);bounds.append(intervals)
    gamma,eta=weights
    G=matrix(QQ,[[((gamma*d["Gpar"][i,j]+eta*d["Gperp"][i,j]).trace()) for j in range(32)] for i in range(32)])
    assert G.is_positive_definite()
    # Seven compact contributions <=1+eps, split contribution at most
    # (1+eps)*(2*T-1)/(2*T). This covers every norm-one point with A<=T.
    cutoff=(1+epsilon)*(8-QQ(1)/(2*T))
    denominator=G.denominator();integral=matrix(ZZ,denominator*G)
    change=matrix(ZZ,integral.__pari__().qflllgram(1));assert abs(change.det())==1
    reduced=change.transpose()*integral*change
    print("ENUM_START",T,"bound",cutoff,"elapsed",round(time.monotonic()-started,3),flush=True)
    result=reduced.__pari__().qfminim((denominator*cutoff).floor(),250000,0)
    V=matrix(ZZ,result[2]);count=int(result[0]);assert V.ncols()*2==count,"enumeration output cap exceeded"
    print("ENUM_DONE",T,"vectors",count,"elapsed",round(time.monotonic()-started,3),flush=True)
    rb=[sum((change[j,k]*d["basis"][j] for j in range(32)),B(0)) for k in range(32)]
    classes=[];others=Counter();seen=set();old_matches={r["index"]:[] for r in d["old"]["primitive_classes"] if r["norm_ideal_norm"]==1}
    old_quats={r["index"]:d["quat"](r["quaternion_power_coordinates"]) for r in d["old"]["primitive_classes"] if r["norm_ideal_norm"]==1}
    beta=d["beta"]
    for j,v in enumerate(V.columns()):
        q=sum((v[i]*rb[i] for i in range(32) if v[i]),B(0))
        n=q.reduced_norm()
        if n!=F(1):others["reduced_norm_not_one"]+=1;continue
        parallel=(q+beta*q*beta**(-1))/2;A=parallel.reduced_norm()
        value=places[4](A)
        if value>T:others["norm_one_above_A_cutoff"]+=1;continue
        assert value>=1
        coordinates=tuple(d["coords"](q));assert coordinates not in seen and tuple(-c for c in coordinates) not in seen;seen.add(coordinates)
        av=RB(value);matches=[]
        for index,old in old_quats.items():
            ratio=q*old**(-1)
            cs=ratio.coefficient_tuple()
            if all(not c for c in cs[1:]):
                u=cs[0];assert u.is_integral() and (1/u).is_integral() and abs(u.norm())==1
                old_matches[index].append(len(classes));matches.append(index)
        classes.append({"index":len(classes),"enumeration_index":j,
                        "quaternion_power_coordinates":list(map(str,coordinates)),
                        "order_coordinates":list(map(int,change*v)),
                        "A_field_coefficients":list(map(str,A.vector())),
                        "A_interval":[str(QQ(av.lower())),str(QQ(av.upper()))],
                        "A_display":str(av),"old_primitive_indices":matches})
    assert all(len(matches)==1 for matches in old_matches.values()),old_matches
    return {"status":"pass: complete reduced-norm-one classes through invariant cutoff",
            "invariant_A_cutoff":T,"classes":classes,"class_count_modulo_sign":len(classes),
            "old_norm_one_classes":old_matches,"discarded_signed_pairs":dict(others),
            "majorant":{"gamma_coefficients":list(map(str,gamma.vector())),"eta_coefficients":list(map(str,eta.vector())),
                         "weight_real_intervals":bounds,"relative_weight_error":"1/1000",
                         "gram":rows(G),"cutoff":str(cutoff),"reduction_change":rows(change)},
            "enumeration":{"vectors_including_both_signs":count,"complete_returned_list":True,
                           "representatives_reduced_coordinates":[list(map(int,v)) for v in V.columns()],
                           "algorithm":"PARI qfminim flag 0 on exact integral Gram, all vectors retained"},
            "unit_signature_proof":d["signature_proof"],"real_root_intervals":d["roots"],
            "complete_for_norm_ideal_one":True,"other_norm_ideals_enumerated":False,
            "infinite_norm_one_tail_bounded":False,"Shimura_derivative_computed":False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--bound",type=int,default=400);args=p.parse_args()
    assert args.bound>=400
    out=DATA/f"nelson_norm_one_d92_T{args.bound}.json";assert not out.exists()
    d=setup();result=search(d,args.bound)
    result["sources"]=[source(p) for p in [Path(__file__)]+d["paths"]]
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("NORM_ONE_CLASSES",result["class_count_modulo_sign"],flush=True)
    print("PASS|338_nelson_norm_one_search")


if __name__=="__main__":main()

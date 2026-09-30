"""D93: fixed reduced norm at the saved Hecke prime (31,b-27).

Normalizing by a central unit reduces every positive-norm class at this
prime to Nrd(alpha)=n. Full positive-unit square coverage is proved in
D92. Enumeration coverage is certified separately by script 345.
"""
import argparse
from collections import Counter
import importlib.util
from itertools import product
import json
from pathlib import Path
import time
from sage.all import GF, QQ, ZZ, RealField, matrix, vector

spec=importlib.util.spec_from_file_location("norm_one",Path(__file__).with_name("339_nelson_norm_one_search.py"))
norm_one=importlib.util.module_from_spec(spec);spec.loader.exec_module(norm_one)
ROOT,DATA=norm_one.ROOT,norm_one.DATA


def norm_generator(d):
    F,b,places=d["F"],d["b"],d["places"];RF=RealField(200)
    g=1+2*b-4*b**3+b**5
    assert abs(g.norm())==31 and g.is_integral()
    roots=[r for r in range(31) if (r**8-8*r**6+20*r**4-16*r*r+2)%31==0]
    zeros=[r for r in roots if (1+2*r-4*r**3+r**5)%31==0];assert zeros==[27]
    target=vector(GF(2),[int(p(g)<0) for p in places])
    exponents=matrix(GF(2),d["signatures"]).transpose().solve_right(target)
    correction=F(1)
    for u,e in zip(d["units"],exponents):correction*=u**int(e)
    n=g*correction;assert all(p(n)>0 for p in places)
    # Choose a smaller positive generator within the square-unit orbit.
    path=DATA/"nelson_unit_cutoff_d91.json";old=json.loads(path.read_text())
    units=[F([QQ(c) for c in v]) for v in next(v for v in old["alternatives"] if v["name"]=="LLL")["units_power_coordinates"]]
    logs=matrix(RF,[[2*abs(RF(p(u))).log() for u in units] for p in places])
    displacement=vector(RF,[RF(31).log()/8-RF(p(n)).log() for p in places])
    solution=(logs.transpose()*logs).solve_right(logs.transpose()*displacement)
    floors=[x.floor() for x in solution]
    options=[vector(ZZ,[f+e for f,e in zip(floors,bits)]) for bits in product([0,1],repeat=7)]
    chosen=min(options,key=lambda v:max(abs(x) for x in logs*v-displacement))
    for u,e in zip(units,chosen):correction*=u**(2*e)
    n=g*correction
    assert n.norm()==31 and n.is_integral() and correction.is_integral() and (1/correction).is_integral()
    assert all(p(n)>0 for p in places)
    proof={"saved_generator_coefficients":list(map(str,g.vector())),
           "totally_positive_generator_coefficients":list(map(str,n.vector())),
           "unit_correction_coefficients":list(map(str,correction.vector())),
           "initial_signature_unit_exponents":list(map(int,exponents)),
           "square_unit_balance_exponents":list(map(int,chosen)),
           "prime_norm":31,"prime_b_residue":27,
           "positive_real_intervals":[[str(QQ(d["RB"](p(n)).lower())),str(QQ(d["RB"](p(n)).upper()))] for p in places]}
    return n,proof,path


def search(d,n,T):
    started=time.monotonic();F,B,b=d["F"],d["B"],d["b"];places=d["places"];RB=d["RB"];RF=RealField(200)
    V=matrix(RF,[[RF(p(b))**j for j in range(8)] for p in places]);weights=[];normalized=[];intervals=[]
    eps=QQ(1)/1000
    for sign in [1,-1]:
        target=vector(RF,[RF(QQ(sign*31)/(2*T)) if i==4 else RF(1) for i in range(8)])
        coeff=[QQ((x*10**15).round())/10**15 for x in V.solve_right(target)]
        w=F(coeff);balls=[]
        for i,p in enumerate(places):
            val=RB(p(w));expected=QQ(sign*31)/(2*T) if i==4 else QQ(1)
            assert expected-abs(expected)*eps<val.lower()<=val.upper()<expected+abs(expected)*eps
            balls.append([str(QQ(val.lower())),str(QQ(val.upper()))])
        normalized.append(w);weights.append(w/n);intervals.append(balls)
    gamma,eta=weights
    G=matrix(QQ,[[((gamma*d["Gpar"][i,j]+eta*d["Gperp"][i,j]).trace()) for j in range(32)] for i in range(32)])
    assert G.is_positive_definite()
    cutoff=(1+eps)*(8-QQ(31)/(2*T));den=G.denominator();integral=matrix(ZZ,den*G)
    change=matrix(ZZ,integral.__pari__().qflllgram(1));assert abs(change.det())==1
    reduced=change.transpose()*integral*change
    print("ENUM_START",T,"bound",cutoff,flush=True)
    result=reduced.__pari__().qfminim((den*cutoff).floor(),250000,2,precision=256)
    vectors=matrix(ZZ,result[2]);count=int(result[0]);assert count==2*vectors.ncols()
    print("ENUM_DONE",T,"vectors",count,"elapsed",round(time.monotonic()-started,3),flush=True)
    rb=[sum((change[j,k]*d["basis"][j] for j in range(32)),B(0)) for k in range(32)]
    classes=[];others=Counter();seen=set();beta=d["beta"]
    for j,v in enumerate(vectors.columns()):
        q=sum((v[i]*rb[i] for i in range(32) if v[i]),B(0))
        if q.reduced_norm()!=n:others["reduced_norm_not_selected_generator"]+=1;continue
        parallel=(q+beta*q*beta**(-1))/2;A=31*parallel.reduced_norm()/n;val=places[4](A)
        if val>T:others["selected_norm_above_A_cutoff"]+=1;continue
        assert val>=31
        coords=tuple(d["coords"](q));assert coords not in seen and tuple(-c for c in coords) not in seen;seen.add(coords)
        av=RB(val)
        classes.append({"index":len(classes),"enumeration_index":j,"quaternion_power_coordinates":list(map(str,coords)),
                        "order_coordinates":list(map(int,change*v)),"A_field_coefficients":list(map(str,A.vector())),
                        "A_interval":[str(QQ(av.lower())),str(QQ(av.upper()))],"A_display":str(av)})
    return {"status":"pass: fixed-norm search; rigorous interval coverage is a separate artifact",
            "invariant_A_cutoff":T,"prime_norm":31,"prime_b_residue":27,
            "classes":classes,"class_count_modulo_sign":len(classes),"discarded_signed_pairs":dict(others),
            "majorant":{"gamma_coefficients":list(map(str,gamma.vector())),"eta_coefficients":list(map(str,eta.vector())),
                         "normalized_weight_coefficients":[list(map(str,w.vector())) for w in normalized],
                         "normalized_weight_real_intervals":intervals,"relative_weight_error":"1/1000",
                         "gram":norm_one.rows(G),"cutoff":str(cutoff),"reduction_change":norm_one.rows(change)},
            "enumeration":{"vectors_including_both_signs":count,"complete_returned_list":True,
                           "representatives_reduced_coordinates":[list(map(int,v)) for v in vectors.columns()],
                           "algorithm":"PARI qfminim flag 2 at 256 bits; coverage checked separately",
                           "rigorous_roundoff_tracking":False},
            "unit_signature_proof":d["signature_proof"],"real_root_intervals":d["roots"],
            "infinite_prime_family_tail_bounded":False,"Shimura_derivative_computed":False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--bound",type=int,default=6400);args=p.parse_args();assert args.bound>=400
    out=DATA/f"nelson_prime31_b27_d93_T{args.bound}.json";assert not out.exists()
    d=norm_one.setup();n,proof,unit_path=norm_generator(d)
    print("NORM_GENERATOR",n,"real_values",[str(d["RB"](p(n))) for p in d["places"]],flush=True)
    result=search(d,n,args.bound);result["norm_generator"]=proof
    paths=[Path(__file__),Path(norm_one.__file__),unit_path,ROOT/"dembele/magma/60_f16_steinberg.m",DATA/"f16_steinberg.out"]+d["paths"]
    result["sources"]=[norm_one.source(p) for p in paths]
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PRIME_CLASSES",result["class_count_modulo_sign"],flush=True)
    print("PASS|344_nelson_prime31_search")


if __name__=="__main__":main()

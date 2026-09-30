"""D92: exhaustive interval Fincke--Pohst replay, independent of qfminim.

An exact rational LDL decomposition and outward Arb bounds give integer
branch ranges containing every possible vector. Exact leaf tests remove
the harmless excess. This certifies coverage, rather than just checking
the vectors returned by the floating-point PARI enumeration.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
from sage.all import QQ, ZZ, RealBallField, matrix, vector

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"
RB=RealBallField(256)


def source(p):
    return {"path":str(p.relative_to(ROOT)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}


def canonical(v):
    # Last nonzero entry positive, the convention used by our recursion.
    if not any(v):return None
    return tuple(v) if next(x for x in reversed(v) if x)>0 else tuple(-x for x in v)


def enumerate_exact(G,bound):
    n=G.nrows();U=matrix.identity(QQ,n);D=[]
    for j in range(n):
        D.append(G[j,j]-sum(D[k]*U[k,j]**2 for k in range(j)))
        assert D[-1]>0
        for k in range(j+1,n):
            U[j,k]=(G[j,k]-sum(D[i]*U[i,j]*U[i,k] for i in range(j)))/D[j]
    assert U.transpose()*matrix.diagonal(QQ,D)*U==G
    d=[RB(c) for c in D];u=[[RB(c) for c in row] for row in U.rows()]
    assert all(x.lower()>0 for x in d)
    x=[0]*n;found=set();visits=[0]*n;leaf_tests=0;extras=0;started=time.monotonic()
    def walk(j,partial,fixed):
        nonlocal leaf_tests,extras
        visits[j]+=1
        remaining=RB(bound)-partial
        if remaining.upper()<0:return
        center=-sum((u[j][k]*x[k] for k in range(j+1,n) if x[k]),RB(0))
        radius=(RB(remaining.upper())/RB(d[j].lower())).sqrt().upper()
        lo=ZZ((center-RB(radius)).lower().ceil())
        hi=ZZ((center+RB(radius)).upper().floor())
        if not fixed:lo=max(lo,0)
        for value in range(int(lo),int(hi)+1):
            x[j]=value
            new_partial=partial+d[j]*(RB(value)-center)**2
            if new_partial.lower()>bound:continue
            if j:
                walk(j-1,new_partial,fixed or value!=0)
            elif fixed or value:
                leaf_tests+=1;v=vector(QQ,x)
                if v*G*v<=bound:
                    key=canonical(x);assert key==tuple(x) and key not in found
                    found.add(key)
                else:extras+=1
        x[j]=0
    walk(n-1,RB(0),False)
    print("INTERVAL_ENUM_DONE",len(found),"pairs",sum(visits),"nodes",round(time.monotonic()-started,3),"seconds",flush=True)
    return found,{"LDL_diagonal":list(map(str,D)),"LDL_upper":[list(map(str,row)) for row in U.rows()],
                  "nodes_by_coordinate":visits,"exact_leaf_tests":leaf_tests,"excess_interval_leaves":extras}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--bound",type=int,default=400);args=p.parse_args()
    path=DATA/f"nelson_norm_one_d92_T{args.bound}.json";packet=json.loads(path.read_text())
    out=DATA/f"nelson_norm_one_coverage_d92_T{args.bound}.json";assert not out.exists()
    majorant=packet["majorant"];G=matrix(QQ,majorant["gram"]);change=matrix(ZZ,majorant["reduction_change"])
    assert abs(change.det())==1
    reduced=change.transpose()*G*change;bound=QQ(majorant["cutoff"])
    print("INTERVAL_ENUM_START",args.bound,flush=True)
    found,proof=enumerate_exact(reduced,bound)
    expected={canonical(v) for v in packet["enumeration"]["representatives_reduced_coordinates"]}
    assert None not in expected and len(expected)*2==packet["enumeration"]["vectors_including_both_signs"]
    assert found==expected,(len(found),len(expected),len(found-expected),len(expected-found))
    # The equality assertion must also detect a deliberately omitted vector.
    corrupt=set(expected);corrupt.pop();assert corrupt!=found
    result={"status":"pass: exhaustive interval enumeration equals saved list",
            "invariant_A_cutoff":args.bound,"interval_precision_bits":256,
            "signed_pair_count":len(found),"proof":proof,
            "coverage_method":"exact rational LDL; outward Arb integer ranges; exact rational leaf tests",
            "depends_on_qfminim_roundoff_guarantee":False,"omitted_vector_control_rejected":True,
            "sources":[source(Path(__file__)),source(path)]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|340_nelson_norm_one_coverage")


if __name__=="__main__":main()

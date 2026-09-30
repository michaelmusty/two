"""Independent standard-Python replay of D90's exact finite certificates.

The numerical Mellin calibration is hash-bound, not promoted to an
interval certificate. No candidate curve or differential bank is read.
"""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
from math import lcm
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"dembele/data/computed"
OUTPUT=DATA/"nelson_d90.json"


def source(path):
    path=Path(path).resolve()
    return {"path":str(path.relative_to(ROOT)),
            "sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def matrix(rows):
    return [[F(x) for x in row] for row in rows]


def transpose(a):
    return [list(v) for v in zip(*a)]


def multiply(a,b):
    bt=transpose(b)
    return [[sum(x*y for x,y in zip(row,col) if x and y) for col in bt] for row in a]


def identity(n,scale=1):
    return [[scale*int(i==j) for j in range(n)] for i in range(n)]


def determinant(a):
    a=matrix(a);det=F(1)
    for i in range(len(a)):
        pivot=next(j for j in range(i,len(a)) if a[j][i])
        if pivot!=i:
            a[i],a[pivot]=a[pivot],a[i];det=-det
        d=a[i][i];det*=d
        for j in range(i+1,len(a)):
            c=a[j][i]/d
            if c:
                a[j]=[u-c*v for u,v in zip(a[j],a[i])]
    return det


def inverse(a):
    n=len(a);a=[row+ident for row,ident in zip(matrix(a),identity(n))]
    for i in range(n):
        j=next(j for j in range(i,n) if a[j][i])
        a[i],a[j]=a[j],a[i]
        d=a[i][i];a[i]=[v/d for v in a[i]]
        for j in range(n):
            if j!=i and a[j][i]:
                c=a[j][i];a[j]=[u-c*v for u,v in zip(a[j],a[i])]
    return [row[n:] for row in a]


def polynomial(text):
    def add(a,b):
        result=a.copy()
        for key,v in b.items(): result[key]=result.get(key,0)+v
        return {k:v for k,v in result.items() if v}
    def mul(a,b):
        out={}
        for (i,j),x in a.items():
            for (k,l),y in b.items():
                key=(i+k,j+l);out[key]=out.get(key,0)+x*y
        return {k:v for k,v in out.items() if v}
    def parse(node):
        if isinstance(node,ast.Constant) and type(node.value)==int:
            return {(0,0):node.value} if node.value else {}
        if isinstance(node,ast.Name):
            return { {"y":(1,0),"yb":(0,1)}[node.id]:1}
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):
            return {k:-v for k,v in parse(node.operand).items()}
        if isinstance(node,ast.BinOp):
            left=parse(node.left)
            if isinstance(node.op,ast.Pow):
                assert isinstance(node.right,ast.Constant)
                out={(0,0):1}
                for _ in range(node.right.value): out=mul(out,left)
                return out
            right=parse(node.right)
            if isinstance(node.op,ast.Add):return add(left,right)
            if isinstance(node.op,ast.Sub):return add(left,{k:-v for k,v in right.items()})
            if isinstance(node.op,ast.Mult):return mul(left,right)
        raise ValueError("unexpected polynomial syntax")
    return parse(ast.parse(text.replace("^","**"),mode="eval").body)


def exact_checks(local, finite, shell):
    a=local["arithmetic"]
    G=matrix(a["relative_pairing_gram"])
    H=matrix(a["relative_dual_in_order_coordinates"])
    assert multiply(G,H)==identity(32) and abs(determinant(G))==4
    assert all(G[i][i].denominator==1 and G[i][i]%2==0 for i in range(32))
    packet=finite["finite_pairing"]
    representatives=matrix(packet["discriminant_representatives"])
    bilinear=multiply(multiply(representatives,G),transpose(representatives))
    qvalues=[(bilinear[i][i]/2)%1 for i in range(4)]
    assert qvalues==[F(0),F(1,2),F(1,2),F(1,2)]
    signs=[[1 if x%1==0 else -1 for x in row] for row in bilinear]
    assert signs==packet["Fourier_numerator_matrix"]
    assert multiply(signs,signs)==identity(4,4)
    assert sum(1 if q==0 else -1 for q in qvalues)/2==-1
    damaged=[row[:] for row in signs];damaged[0][0]*=-1
    assert multiply(damaged,damaged)!=identity(4,4)
    polynomials=local["derivatives"]["polynomials"]
    for n in [1,3,5]:
        assert polynomial(polynomials[f"{n},1"])=={(1,n):-1,(0,n-1):n}
    assert polynomial(polynomials["1,1"])!={(1,1):-1}
    split=local["CM_lattice_split"]
    A=matrix(split["integral_CM_involution"])
    plus=matrix(split["parallel_lattice_basis"])
    minus=matrix(split["perpendicular_lattice_basis"])
    assert multiply(A,A)==identity(32)
    assert multiply(A,plus)==plus
    assert multiply(A,minus)==[[-c for c in row] for row in minus]
    direct=[p+m for p,m in zip(plus,minus)]
    assert abs(determinant(direct))==65536
    Q=matrix(a["majorant_gram"])
    assert multiply(multiply(transpose(plus),Q),minus)==[[0]*16 for _ in range(16)]
    change=matrix(local["enumeration_pilot"]["reduction_change"])
    reduced=multiply(multiply(transpose(change),Q),change)
    den=lcm(*(x.denominator for row in reduced for x in row))
    reduced=[[int(x*den) for x in row] for row in reduced]
    def integral(mat):
        assert all(F(x).denominator==1 for row in mat for x in row)
        return [[int(x) for x in row] for row in mat]
    Ap=[[x-int(i==j) for j,x in enumerate(row)] for i,row in enumerate(A)]
    Am=[[x+int(i==j) for j,x in enumerate(row)] for i,row in enumerate(A)]
    par=integral(multiply(Ap,change));perp=integral(multiply(Am,change))
    glue=integral([[2*x for x in row] for row in multiply(inverse(direct),change)])
    purepar=pureperp=mixed=outside=0
    seen=set()
    for v in shell["all_representatives_reduced_coordinates"]:
        assert tuple(v) not in seen and tuple(-x for x in v) not in seen
        seen.add(tuple(v))
        nz=[(i,x) for i,x in enumerate(v) if x]
        norm=sum(x*y*reduced[i][j] for i,x in nz for j,y in nz)
        assert 0<F(norm,den)<=F(shell["majorant_bound"])
        pp=all(sum(row[i]*x for i,x in nz)==0 for row in par)
        pm=all(sum(row[i]*x for i,x in nz)==0 for row in perp)
        purepar+=2*pp;pureperp+=2*pm;mixed+=2*(not pp and not pm)
        outside+=2*any(sum(row[i]*x for i,x in nz)%2 for row in glue)
    assert 2*len(seen)==shell["vectors_count_both_signs"]==9910
    assert (purepar,pureperp,mixed,outside)==(452,98,9360,9360)
    for key,value in [("pure_parallel_count",purepar),("pure_perpendicular_count",pureperp),
                      ("mixed_count",mixed),("outside_CM_direct_sum_count",outside)]:
        assert shell[key]==value
    return {"dual_Gram_and_finite_Fourier_replayed":True,
            "CM_lattice_glue_index_replayed":65536,
            "second_shell_vectors_replayed":2*len(seen),
            "mixed_vectors_replayed":mixed,
            "Fourier_sign_corruption_rejected":True,
            "missing_derivative_constant_rejected":True,
            "enumeration_completeness":"PARI qfminim; independent replay validates every saved vector and classification",
            "numerical_Mellin_values":"hash-bound calibration, no interval certificate"}


def compute():
    names=["nelson_cm_lattice_d90.json","nelson_finite_mellin_d90.json","nelson_cm_shell_d90.json"]
    objects=[json.loads((DATA/n).read_text()) for n in names]
    checks=exact_checks(*objects)
    paths={Path(__file__).resolve(),*(DATA/n for n in names)}
    jobs=[]
    for path in sorted(DATA.glob("nelson_*_d90_attempt*.job.json")):
        job=json.loads(path.read_text());jobs.append(job)
        assert job["wall_seconds"]<job["timeout_seconds"]==180
        paths.add(path)
        for item in job["sources"]+[job["log"]]:
            p=ROOT/item["path"]
            assert hashlib.sha256(p.read_bytes()).hexdigest()==item["sha256"]
            paths.add(p)
    assert len(jobs)==6 and [j["status"] for j in jobs].count("pass")==3
    for obj in objects:
        for item in obj["sources"]:
            p=ROOT/item["path"]
            assert source(p)==item;paths.add(p)
    # Bind the specific historical Hecke identification used by the report.
    paths.add(DATA/"f16_steinberg.out")
    return {"status":"pass: D90 local evaluator components",
            "independent_replay":checks,
            "jobs":{"count":len(jobs),"successful":3,"retained_failed":3,
                    "maximum_wall_seconds":max(j["wall_seconds"] for j in jobs)},
            "sources":[source(p) for p in sorted(paths)],
            "Shimura_tangent_computed":False,
            "global_Hilbert_theta_lift_evaluated":False,
            "next":"justify the Hilbert cusp/unit unfolding and evaluate one Hecke eigenform with a truncation bound"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args();result=compute()
    if args.check:assert result==json.loads(OUTPUT.read_text())
    else:
        assert not OUTPUT.exists()
        OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: D90 finite kernel, CM lattice and 9,910 shell vectors;",len(result["sources"]),"hashes")


if __name__=="__main__":main()

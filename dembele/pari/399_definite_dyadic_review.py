"""Independent rational replay of D109, with no Sage or Magma dependency.

The defining Hensel inequality proves an exact K-valued splitting. Integer
lattice, residue-spanning and arithmetic edge-transport checks are replayed.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "definite_dyadic_review_d109.json"
REPORT = ROOT / "dembele/certificates/definite-dyadic-d109.md"
spec = importlib.util.spec_from_file_location("d91_field", ROOT/"dembele/pari/334_nelson_unfolding_audit.py")
ar = importlib.util.module_from_spec(spec); spec.loader.exec_module(ar)
mat = ar.mat
ZERO, ONE = ar.ZERO, ar.ONE
add, mul, scale, inv = ar.fadd, ar.fmul, ar.fscale, ar.finverse
PI = (Q(0),Q(1))+(Q(0),)*6
E = (ONE,ZERO,ZERO,ONE)


def source(path):
    path = Path(path).resolve()
    return {"path":str(path), "sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def checked(rows):
    paths=[]
    for row in rows:
        path=ROOT/row["path"]
        assert source(path)["sha256"]==row["sha256"], str(path)
        paths.append(path)
    return paths


def f(row): return tuple(map(Q,row))
def fm(row): return tuple(f(c) for c in row)
def neg(x): return scale(x,-1)
def sub(x,y): return add(x,neg(y))
def v2(x):
    def vp(n): return (abs(n)&-abs(n)).bit_length()-1
    return vp(x.numerator)-vp(x.denominator)
def val(x): return min((8*v2(c)+i for i,c in enumerate(x) if c),default=10**9)
def madd(a,b): return tuple(add(x,y) for x,y in zip(a,b))
def mscale(a,x): return tuple(mul(c,x) for c in a)
def mmul(a,b):
    return tuple(add(mul(a[2*i],b[j]),mul(a[2*i+1],b[2+j])) for i in range(2) for j in range(2))
def mdet(a): return sub(mul(a[0],a[3]),mul(a[1],a[2]))
def minv(a): return mscale((a[3],neg(a[1]),neg(a[2]),a[0]),inv(mdet(a)))
def mval(a): return min(map(val,a))
def qmul(q,r):
    out=[ZERO]*4
    for i,u in enumerate(q):
        for j,w in enumerate(r):
            a,b=i%2,i//2; c,d=j%2,j//2
            term=mul(u,w)
            if (b*c+(a+c)//2+(b+d)//2)%2: term=neg(term)
            k=(a+c)%2+2*((b+d)%2)
            out[k]=add(out[k],term)
    return tuple(out)
def qnorm(q):
    result=ZERO
    for c in q: result=add(result,mul(c,c))
    return result
def flatten(q): return sum((list(c) for c in q),[])


def computations():
    raw=json.loads((DATA/"definite_dyadic_export_d109.json").read_text())
    p=json.loads((DATA/"definite_dyadic_certificate_d109.json").read_text())
    assert raw["field_polynomial_ascending"]==ar.POLY+[1]
    assert [f(c) for c in raw["quaternion_parameters"]]==[neg(ONE),neg(ONE)]
    assert val(PI)==1 and val(scale(ONE,2))==8
    # Eisenstein gives both the completion and the exact valuation formula.
    assert ar.POLY[0]%4==2 and all(c%2==0 for c in ar.POLY)
    basis=[fm(q) for q in raw["order_Z_basis"]]
    Z=mat.transpose([flatten(q) for q in basis]); Zi=mat.inverse(Z)
    def coords(q): return ar.mv(Zi,flatten(q))
    def integral(q): return all(c.denominator==1 for c in coords(q))
    assert len(basis)==32 and integral((ONE,ZERO,ZERO,ZERO))
    assert all(integral(tuple(mul(PI,c) for c in q)) for q in basis)
    assert all(integral(qmul(q,r)) for q in basis for r in basis)
    traces=[]
    for j in range(8):
        m=ar.fmatrix(tuple(Q(i==j) for i in range(8)))
        traces.append(sum(m[i][i] for i in range(8)))
    def trace(x): return sum(c*t for c,t in zip(x,traces))
    gram=[[2*trace(qmul(q,r)[0]) for r in basis] for q in basis]
    disc=mat.determinant(gram)
    assert disc==Q(p["absolute_reduced_trace_discriminant"]) and abs(disc)==2**124
    OF=mat.matrix(raw["OF_Z_basis"])
    assert abs(mat.determinant(OF))==1
    # Independent monogenic field trace discriminant.
    powers=[tuple(Q(i==j) for i in range(8)) for j in range(8)]
    assert mat.determinant([[trace(mul(x,y)) for y in powers] for x in powers])==2**31

    h=p["Hensel"]; x0,y=f(h["x0"]),f(h["y"])
    residual=add(add(mul(x0,x0),mul(y,y)),ONE)
    n,s=val(residual),val(scale(x0,2)); d=n-s
    assert residual==f(h["residual"]) and n==h["residual_valuation"]
    assert s==h["derivative_valuation"] and n>2*s and d==h["root_error_valuation"]
    C=fm(p["conjugating_matrix"]); Ci=minv(C)
    I=mmul(mmul(C,(ZERO,neg(ONE),ONE,ZERO)),Ci)
    Jc=mmul(mmul(C,(ZERO,y,y,ZERO)),Ci)
    Jt=mmul(mmul(C,(ONE,ZERO,ZERO,neg(ONE))),Ci)
    assert [I,Jc,Jt]==[fm(p[k]) for k in ["I_exact","J_constant","J_slope"]]
    assert mmul(I,I)==mscale(E,neg(ONE))
    zero=(ZERO,)*4
    assert madd(mmul(I,Jc),mmul(Jc,I))==zero
    assert madd(mmul(I,Jt),mmul(Jt,I))==zero
    assert mmul(Jt,Jt)==E and madd(mmul(Jc,Jt),mmul(Jt,Jc))==zero
    assert mmul(Jc,Jc)==mscale(E,mul(y,y))
    def image(q):
        const=madd(madd(mscale(E,q[0]),mscale(I,q[1])),madd(mscale(Jc,q[2]),mscale(mmul(I,Jc),q[3])))
        slope=madd(mscale(Jt,q[2]),mscale(mmul(I,Jt),q[3]))
        return madd(const,mscale(slope,x0)),slope
    reductions=[]; error_bounds=[]
    for j,q in enumerate(basis):
        center,slope=image(q); bound=d+mval(slope)
        assert center==fm(p["order_image_centers"][j]) and mval(center)>=0 and bound>=1
        assert bound==p["order_image_error_lower_bounds"][j]
        reductions.append([int(val(c)==0) for c in center]); error_bounds.append(bound)
    assert reductions==p["order_image_reductions"]
    pivot=p["residue_basis_Z_indices"]
    assert len(set(pivot))==4
    assert int(mat.determinant([reductions[i] for i in pivot]))%2==1
    assert p["residue_rank"]==4

    t=p["transport"]; q=fm(t["quaternion"])
    assert qnorm(q)==ONE and integral(q)
    qi=(q[0],)+tuple(neg(c) for c in q[1:])
    assert integral(qi) and qmul(q,qi)==(ONE,ZERO,ZERO,ZERO)
    assert coords(q)==list(map(Q,t["unit_order_coordinates"]))
    center,slope=image(q)
    assert center==fm(t["matrix_center"]) and slope==fm(t["matrix_slope"])
    assert mval(center)>=0 and d+mval(slope)>=1
    red=[int(val(c)==0) for c in center]
    assert red==t["mod_pi_matrix"]
    lines=[(1,0),(0,1),(1,1)]
    perm=[lines.index(tuple(sum(red[2*i+j]*l[j] for j in range(2))%2 for i in range(2))) for l in lines]
    assert perm==t["neighbor_permutation"]
    a,b=t["source_neighbor"],t["target_neighbor"]
    assert a!=b and perm[a]==b
    lattices=[(ONE,ZERO,ZERO,PI),(PI,ZERO,ZERO,ONE),(ONE,ZERO,ONE,PI)]
    assert lattices[a]==fm(t["source_lattice"]) and lattices[b]==fm(t["target_lattice"])
    U=mmul(mmul(minv(lattices[b]),center),lattices[a])
    V=mmul(mmul(minv(lattices[b]),slope),lattices[a])
    assert U==fm(t["conjugated_center"]) and V==fm(t["conjugated_slope"])
    assert mval(U)>=0 and d+mval(V)>=1
    assert d+mval(V)==t["conjugated_error_lower_bound"]
    assert mul(mul(qnorm(q),mdet(lattices[a])),inv(mdet(lattices[b])))==ONE

    # Negative controls reject a wrong Hensel root and a wrong target edge.
    wrong_x=add(x0,ONE)
    bad_n=val(add(add(mul(wrong_x,wrong_x),mul(y,y)),ONE))
    bad_s=val(scale(wrong_x,2))
    assert not bad_n>2*bad_s
    wrong_transition=mmul(mmul(minv(lattices[a]),center),lattices[a])
    assert mval(wrong_transition)<0
    assert d+mval(mmul(mmul(minv(lattices[a]),slope),lattices[a]))>=0
    return {"order_rank":32,"exact_order_closure_products_checked":1024,
            "absolute_trace_discriminant":str(disc),"local_valuation_ramification":8,
            "Hensel_residual_valuation":n,"Hensel_derivative_valuation":s,
            "Hensel_root_error_valuation":d,"minimum_order_image_error":min(error_bounds),
            "local_order_image_mod_pi_rank":4,"exact_integral_splitting_certified":True,
            "norm_one_arithmetic_edge_transport_verified":True,
            "neighbor_permutation":perm,"transport_fixes_base_vertex":True,
            "wrong_Hensel_root_rejected":True,"wrong_target_neighbor_rejected":True,
            "full_tree_quotient_or_harmonic_cocycle_computed":False}


def build():
    result=computations()
    prior_path=DATA/"shimura_evaluator_review_d108.json"
    prior=json.loads(prior_path.read_text())
    assert prior["status"]=="pass" and len(prior["sources"])==606
    paths=checked(prior["sources"])+[prior_path,Path(__file__),REPORT,DATA/"definite_dyadic_sources_d109.json"]
    for name in ["definite_dyadic_export_d109.json","definite_dyadic_certificate_d109.json"]:
        path=DATA/name; record=json.loads(path.read_text()); paths+=[path]+checked(record.get("sources",[]))
    # Bind every attempt, retaining snapshots for unsuccessful drivers.
    attempts=list(DATA.glob("definite_dyadic_export_d109_attempt*.job.json"))
    attempts+=list(DATA.glob("definite_dyadic_certificate_d109_attempt*.job.json"))
    for path in sorted(attempts):
        job=json.loads(path.read_text())
        assert job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
        paths+=checked(job["sources"]+[job["log"]])+[path]
        if job["status"]=="pass":
            assert job["wall_seconds"]<180
            paths+=checked([job["driver"]])
        else:
            assert job["status"] in ["failed","timeout"]
            ext=Path(job["driver"]["path"]).suffix
            snapshot=path.with_name(path.name.replace(".job.json","_failed"+ext))
            assert source(snapshot)["sha256"]==job["driver"]["sha256"]
            paths.append(snapshot)
    probe=DATA/"definite_dyadic_review_d109_probe_attempt01.job.json"
    if probe.exists():
        job=json.loads(probe.read_text());assert job["status"]=="pass"
        paths+=checked(job["sources"]+[job["driver"],job["log"]])+[probe]
    paths+=[Path("/Users/musty/hilbertmodularforms/ModFrmHil/hackobj.m"),
            Path("/Users/musty/hilbertmodularforms/ModFrmHil/precompute.m"),
            ROOT/"dembele/pari/334_nelson_unfolding_audit.py",ROOT/"dembele/pari/325_nelson_d90_audit.py"]
    return {"status":"pass","milestone":"D109","certificates":result,
            "D108_source_hashes_checked_unchanged":606,
            "actual_definite_order_exported":True,"integral_dyadic_splitting_certified":True,
            "one_arithmetic_edge_transport_verified":True,
            "full_arithmetic_group_or_normalizer_quotient_constructed":False,
            "actual_Shimura_tangent_or_jet_evaluated":False,
            "actual_dyadic_CM_matching_proved":False,"candidate_identification_proved":False,
            "target_field_polynomial_constructed":False,
            "sources":[source(p) for p in sorted(set(p.resolve() for p in paths))]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument("--check",action="store_true");group.add_argument("--probe",action="store_true")
    args=parser.parse_args()
    if args.probe:
        print(json.dumps(computations(),indent=2),flush=True)
        print("PASS|D109_DYADIC_PROBE",flush=True);return
    if args.check:
        old=json.loads(OUT.read_text());checked(old["sources"])
    result=build()
    if args.check: assert result==old
    else:
        assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","source_hashes":len(result["sources"]),
                      "D108_hashes_unchanged":606,"actual_Shimura_jet_evaluated":False}),flush=True)
    print("PASS|D109_DYADIC_REVIEW",flush=True)


if __name__=="__main__":main()

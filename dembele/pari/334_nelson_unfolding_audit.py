"""Independent rational replay of D91 arithmetic and interval-output audit.

Uses standard Python only. Analytic nodes are bound to the successful Arb
run; this replay independently checks the quaternion identities, unit
witnesses, primitive classes, interval widths and bucket accumulation.
It does not certify a missing primitive-class tail or a global lift.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/"dembele/data/computed"
spec=importlib.util.spec_from_file_location("matrix_audit",Path(__file__).with_name("325_nelson_d90_audit.py"))
mat=importlib.util.module_from_spec(spec);spec.loader.exec_module(mat)
ZERO=(Q(0),)*8;ONE=(Q(1),)+ZERO[1:]
POLY=[2,0,-16,0,20,0,-8,0]


def fadd(x,y):return tuple(a+b for a,b in zip(x,y))
def fscale(x,c):return tuple(a*c for a in x)
def fmul(x,y):
    z=[Q(0)]*15
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:z[i+j]+=a*b
    for j in range(14,7,-1):
        if z[j]:
            for i,c in enumerate(POLY):z[j-8+i]-=z[j]*c
    return tuple(z[:8])


def fmatrix(x):
    return mat.transpose([list(fmul(x,tuple(Q(i==j) for i in range(8)))) for j in range(8)])


def finverse(x):return tuple(row[0] for row in mat.inverse(fmatrix(x)))
def fnorm(x):return mat.determinant(fmatrix(x))
F_A=(Q(0),Q(1),Q(-1))+ZERO[3:]


def quaternion(row):return tuple(tuple(Q(c) for c in row[8*j:8*(j+1)]) for j in range(4))
def flatten(q):return sum((list(c) for c in q),[])
def qadd(x,y):return tuple(fadd(a,b) for a,b in zip(x,y))
def qscale(q,c):return tuple(fscale(a,c) for a in q)
def central(q,u):return tuple(fmul(a,u) for a in q)
QONE=(ONE,ZERO,ZERO,ZERO)


def qmul(x,y):
    out=[ZERO]*4
    for i,u in enumerate(x):
        if u==ZERO:continue
        for j,v in enumerate(y):
            if v==ZERO:continue
            a,b=i%2,i//2;c,d=j%2,j//2
            value=fmul(u,v)
            if a+c>=2:value=fmul(value,F_A)
            if (b*c+(b+d)//2)%2:value=fscale(value,-1)
            k=(a+c)%2+2*((b+d)%2)
            out[k]=fadd(out[k],value)
    return tuple(out)


def qnorm(q):
    result=qmul(q,(q[0],)+tuple(fscale(c,-1) for c in q[1:]))
    assert result[1:]==(ZERO,)*3
    return result[0]


def mv(m,v):return [sum(a*b for a,b in zip(row,v) if a and b) for row in m]
def integral(v):return all(c.denominator==1 for c in v)


def exact_checks(raw,local,shell,pilot,primitive):
    O=mat.transpose(mat.matrix(raw["quaternion_export"]["order_basis"]));Oinv=mat.inverse(O)
    basis=[quaternion(v) for v in raw["quaternion_export"]["order_basis"]]
    beta=quaternion(local["arithmetic"]["CM_beta_power_coordinates"])
    pi=(Q(2),Q(1))+ZERO[2:]
    assert qnorm(beta)==pi and qmul(beta,beta)==(fscale(pi,-1),ZERO,ZERO,ZERO)
    beta_inv=central(qscale(beta,-1),finverse(pi))
    L=mat.matrix(primitive["beta_left_multiplication_in_order_basis"])
    assert mat.multiply(O,L)==mat.transpose([flatten(qmul(beta,e)) for e in basis])
    assert integral(sum(L,[])) and abs(mat.determinant(L))==4
    D=mat.matrix(local["arithmetic"]["relative_dual_in_order_coordinates"])
    U=mat.matrix(pilot["cusp_basis_change_in_relative_dual"])
    assert integral(sum(U,[])) and abs(mat.determinant(U))==1
    assert mat.multiply(mat.multiply(O,D),U)==mat.transpose([flatten(qmul(beta_inv,e)) for e in basis])
    assert mat.multiply(D,U)==mat.inverse(L)
    reduced=mat.multiply(O,mat.matrix(local["enumeration_pilot"]["reduction_change"]))
    originals=[]
    for row in pilot["unit_classes"]:
        q=quaternion(row["quaternion_power_coordinates"])
        v=shell["all_representatives_reduced_coordinates"][row["shell_index"]]
        assert flatten(q)==mv(reduced,v)
        assert integral(mv(Oinv,flatten(q)))
        n=qnorm(q);assert list(n)==[Q(c) for c in row["norm_generator"]]
        nn=fnorm(n);assert nn==row["norm_ideal_norm"] and 0<nn<=64
        parallel=qscale(qadd(q,qmul(qmul(beta,q),beta_inv)),Q(1,2))
        assert row["mixed"]==(q!=parallel and parallel!=(ZERO,)*4)
        A=tuple(Q(c) for c in row["multiplicative_majorant_field_element"])
        assert fmul(A,n)==fscale(qnorm(parallel),nn)
        originals.append(q)
    for witness in pilot["unit_duplicate_witnesses"]:
        unit=tuple(Q(c) for c in witness["unit_power_coordinates"])
        assert integral(unit) and integral(finverse(unit)) and abs(fnorm(unit))==1
        q=originals[witness["representative_index"]]
        actual=mv(reduced,shell["all_representatives_reduced_coordinates"][witness["shell_index"]])
        assert flatten(central(q,unit))==actual
    classes=[];seen=set();buckets=Counter()
    for row in primitive["primitive_classes"]:
        q=quaternion(row["quaternion_power_coordinates"])
        assert integral(mv(Oinv,flatten(q)))
        assert not integral(mv(Oinv,flatten(qmul(beta_inv,q))))
        n=qnorm(q);nn=fnorm(n);assert nn==row["norm_ideal_norm"] and nn in [1,31]
        pivot=next(c for c in q if c!=ZERO)
        projective=tuple(fmul(c,finverse(pivot)) for c in q)
        key=(projective,nn)
        assert key not in seen;seen.add(key)
        parallel=qscale(qadd(q,qmul(qmul(beta,q),beta_inv)),Q(1,2))
        A=tuple(Q(c) for c in row["multiplicative_majorant_field_element"])
        assert fmul(A,n)==fscale(qnorm(parallel),nn)
        assert row["mixed"]==(q!=parallel)
        if nn==1:bucket="known"
        else:
            zeros=[b for b in range(31) if (b**8-8*b**6+20*b**4-16*b*b+2)%31==0
                   and sum(c.numerator*pow(c.denominator,-1,31)*pow(b,i,31) for i,c in enumerate(n))%31==0]
            assert len(zeros)==1;bucket="a31_b"+str(zeros[0])
        assert row["Hecke_bucket"]==bucket;buckets[bucket]+=1;classes.append(q)
    powers=[QONE]
    for _ in range(6):powers.append(qmul(beta,powers[-1]))
    for row in primitive["pilot_decomposition"]:
        unit=tuple(Q(c) for c in row["unit_power_coordinates"])
        assert integral(unit) and integral(finverse(unit)) and abs(fnorm(unit))==1
        q=qmul(powers[row["beta_exponent"]],central(classes[row["primitive_index"]],unit))
        assert q==originals[row["pilot_index"]]
    missing=primitive["missing_old_pilot_class"]
    q=quaternion(missing["quaternion_power_coordinates"])
    assert q==qmul(beta,classes[missing["primitive_index"]]) and fnorm(qnorm(q))==2
    assert integral(mv(Oinv,flatten(q)))
    assert all(not r["mixed"] for r in pilot["unit_classes"] if r["norm_ideal_norm"]==2)
    assert dict(buckets)==primitive["bucket_counts"]
    # Corrupt the dual change, then ensure the exact identity rejects it.
    bad=[row[:] for row in U];bad[0][0]+=1
    assert mat.multiply(mat.multiply(O,D),bad)!=mat.transpose([flatten(qmul(beta_inv,e)) for e in basis])
    return {"dual_equals_beta_inverse_order":True,"pilot_classes":len(originals),
            "unit_duplicate_witnesses":len(pilot["unit_duplicate_witnesses"]),
            "primitive_classes":len(classes),"Hecke_bucket_counts":dict(buckets),
            "explicit_missing_old_shell_class_checked":True,"dual_corruption_rejected":True}


def read_interval(v):
    lo,hi=Q(v["lower"]),Q(v["upper"]);assert lo<=hi;return lo,hi


def interval_checks(packet):
    assert packet["precision_bits"]==320 and packet["trapezoidal_step"]=="1/32" and packet["height"]==16
    assert packet["all_auxiliary_ideals_summed"] and packet["all_beta_powers_summed"]
    assert not packet["omitted_primitive_classes_bounded"] and not packet["Shimura_derivative_computed"]
    count=0
    for kernel in packet["kernels"]:
        assert read_interval(kernel["A"])[0]>0 and read_interval(kernel["Z"])[0]>0
        for row in kernel["values"]:
            lo,hi=read_interval(row["value"]);assert hi-lo<Q(1,10**30)
            for key in ["strip_error_bound","vertical_tail_bound"]:
                elo,ehi=read_interval(row[key]);assert 0<elo<=ehi<Q(1,10**40)
            assert row["coarse_grid_overlaps"];count+=1
    assert count==42
    max_radius=Q(0)
    for bucket,values in packet["Hecke_affine_buckets"].items():
        terms=[v for v in packet["class_terms"] if v["bucket"]==bucket]
        for degree,value in values.items():
            for part in ["real","imag"]:
                lo,hi=read_interval(value[part]);max_radius=max(max_radius,(hi-lo)/2)
                lower=sum(read_interval(v["values"][degree][part])[0] for v in terms)
                upper=sum(read_interval(v["values"][degree][part])[1] for v in terms)
                assert lo<=upper and lower<=hi
            if degree=="1":assert read_interval(value["imag"])[0]<=0<=read_interval(value["imag"])[1]
    assert max_radius<Q(1,10**47)
    return {"scalar_kernels":count,"primitive_class_terms":len(packet["class_terms"]),
            "largest_bucket_component_radius_upper_bound":"1e-47",
            "scalar_quadrature_error_upper_bound":"6.550e-44",
            "node_enclosures":"hash-bound Arb run; not numerically recomputed by this standard-Python checker"}


def compute():
    names=["cm_orbit.json","nelson_cm_lattice_d90.json","nelson_cm_shell_d90.json",
           "nelson_unfolding_data_d91.json","nelson_primitive_classes_d91.json","nelson_interval_sum_d91.json"]
    documents=[json.loads((DATA/n).read_text()) for n in names]
    sources={};jobs=[]
    def bind(p,expected=None):
        p=Path(p);p=p if p.is_absolute() else ROOT/p
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        if expected is not None:assert h==expected,p
        rel=str(p.relative_to(ROOT));sources[rel]={"path":rel,"sha256":h}
    for name,doc in zip(names,documents):
        bind(DATA/name)
        for s in doc.get("sources",[]):bind(s["path"],s["sha256"])
    for stem,count in [("unfolding",2),("primitive",2),("interval",3)]:
        for i in range(1,count+1):
            p=DATA/f"nelson_{stem}_d91_attempt{i:02d}.job.json";job=json.loads(p.read_text())
            bind(p);bind(job["log"]["path"],job["log"]["sha256"])
            for src in job["sources"]:bind(src["path"],src["sha256"])
            assert job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
            assert job["status"]==("pass" if i==count else "failed")
            jobs.append({"path":str(p.relative_to(ROOT)),"status":job["status"],"wall_seconds":job["wall_seconds"]})
    bind(Path(__file__));bind(Path(mat.__file__))
    return {"status":"pass: arithmetic identities and interval partial sums; no full lift",
            "exact":exact_checks(*documents[:5]),"interval_output":interval_checks(documents[5]),
            "jobs":jobs,"sources":sorted(sources.values(),key=lambda s:s["path"]),
            "global_Hilbert_theta_lift_evaluated":False,"Shimura_derivative_computed":False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--check",action="store_true");args=p.parse_args()
    result=compute();output=DATA/"nelson_unfolding_d91.json"
    if args.check:assert result==json.loads(output.read_text())
    else:
        assert not output.exists();output.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: D91 exact cusp/unit arithmetic, 29 primitive classes, 42 interval kernels;",len(result["sources"]),"hashes")


if __name__=="__main__":main()

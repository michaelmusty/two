"""D92 independent rational audit and manifest (standard Python only).

Replays the majorants, unit signatures, every enumerated norm/class,
the rational LDL identities, nested cutoffs and disk-average series.
Exhaustive interval recursion and analytic Arb bounds are hash-bound to
their bounded runs, rather than silently attributed to this replay.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import lcm
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"
spec=importlib.util.spec_from_file_location("arithmetic",Path(__file__).with_name("334_nelson_unfolding_audit.py"))
ar=importlib.util.module_from_spec(spec);spec.loader.exec_module(ar);mat=ar.mat


def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(x,y):
    v=[a*b for a in x for b in y];return min(v),max(v)
def poly(coeffs,x):
    r=(Q(0),Q(0))
    for c in reversed(coeffs):r=add(mul(r,x),(Q(c),Q(c)))
    return r
def read_interval(row):return Q(row["lower"]),Q(row["upper"])
def overlap(x,y):return max(x[0],y[0])<=min(x[1],y[1])
def canonical(v):
    assert any(v)
    return tuple(v) if next(x for x in v if x)>0 else tuple(-x for x in v)
def rank2(rows):
    basis={}
    for row in rows:
        x=sum(int(v)<<i for i,v in enumerate(row))
        while x:
            pivot=x.bit_length()-1
            if pivot in basis:x^=basis[pivot]
            else:basis[pivot]=x;break
    return len(basis)
def imul(x,y):
    z=[0]*15
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:z[i+j]+=a*b
    for j in range(14,7,-1):
        if z[j]:
            for i,c in enumerate(ar.POLY):z[j-8+i]-=z[j]*c
    return z[:8]
def norm_numerator(q):
    a,b,c,d=[q[8*j:8*(j+1)] for j in range(4)]
    pos=[x+y for x,y in zip(imul(a,a),imul(c,c))]
    neg=imul([0,1,-1,0,0,0,0,0],[x+y for x,y in zip(imul(b,b),imul(d,d))])
    return [x-y for x,y in zip(pos,neg)]
def integral_matrix(m):
    den=lcm(*(v.denominator for row in m for v in row))
    return [[int(v*den) for v in row] for row in m],den
def pair(q,r):
    pos=ar.fadd(ar.fmul(q[0],r[0]),ar.fmul(q[2],r[2]))
    neg=ar.fmul(ar.F_A,ar.fadd(ar.fmul(q[1],r[1]),ar.fmul(q[3],r[3])))
    return ar.fadd(pos,ar.fscale(neg,-1))


def prepare(raw,local):
    basis=[ar.quaternion(v) for v in raw["quaternion_export"]["order_basis"]]
    O=mat.transpose(mat.matrix(raw["quaternion_export"]["order_basis"]))
    M=mat.matrix(local["CM_lattice_split"]["integral_CM_involution"])
    assert mat.multiply(M,M)==mat.identity(32)
    beta=ar.quaternion(local["arithmetic"]["CM_beta_power_coordinates"])
    beta_inv=ar.central(ar.qscale(beta,-1),ar.finverse(ar.qnorm(beta)))
    assert mat.multiply(O,M)==mat.transpose([ar.flatten(ar.qmul(ar.qmul(beta,q),beta_inv)) for q in basis])
    P=[[Q(int(i==j)+M[i][j],2) for j in range(32)] for i in range(32)]
    C=[[Q(int(i==j)-M[i][j],2) for j in range(32)] for i in range(32)]
    pairs=[[pair(q,r) for r in basis] for q in basis]
    fbas=[tuple(Q(i==j) for i in range(8)) for j in range(8)]
    def trace(x):return sum(ar.fmatrix(x)[i][i] for i in range(8))
    traces=[[trace(ar.fmul(x,y)) for y in fbas] for x in fbas]
    return O,M,P,C,pairs,traces


def check_packet(packet,coverage,prepared):
    O,M,P,C,pairs,traces=prepared;T=packet["invariant_A_cutoff"]
    roots=[tuple(Q(x) for x in row) for row in packet["real_root_intervals"]]
    for i,(lo,hi) in enumerate(roots):
        assert lo<hi and poly(ar.POLY+[1],(lo,lo))[0]*poly(ar.POLY+[1],(hi,hi))[0]<0
        if i:assert roots[i-1][1]<lo
        a=poly(ar.F_A,(lo,hi));assert (a[0]>0) if i==4 else (a[1]<0)
    sig=packet["unit_signature_proof"];signs=[]
    for row in sig["units_power_coordinates"]:
        u=tuple(Q(c) for c in row)
        assert ar.integral(u) and ar.integral(ar.finverse(u)) and abs(ar.fnorm(u))==1
        values=[poly(u,r) for r in roots];assert all(v[0]>0 or v[1]<0 for v in values)
        signs.append([int(v[1]<0) for v in values])
    assert signs==sig["signatures"] and rank2(signs)==sig["rank_over_F2"]==8
    majorant=packet["majorant"];weighted=[]
    for name,sign in [("gamma_coefficients",1),("eta_coefficients",-1)]:
        w=[Q(c) for c in majorant[name]]
        for i,r in enumerate(roots):
            lo,hi=poly(w,r);target=Q(sign,2*T) if i==4 else Q(1);error=abs(target)/1000
            assert target-error<lo<=hi<target+error
        tw=[sum(w[j]*traces[j][k] for j in range(8)) for k in range(8)]
        weighted.append([[sum(a*b for a,b in zip(tw,v)) for v in row] for row in pairs])
    gp=mat.multiply(mat.multiply(mat.transpose(P),weighted[0]),P)
    gc=mat.multiply(mat.multiply(mat.transpose(C),weighted[1]),C)
    G=[[a+b for a,b in zip(x,y)] for x,y in zip(gp,gc)]
    assert G==mat.matrix(majorant["gram"])
    cutoff=Q(1001,1000)*(8-Q(1,2*T));assert cutoff==Q(majorant["cutoff"])
    change=mat.matrix(majorant["reduction_change"]);assert abs(mat.determinant(change))==1
    assert ar.integral(sum(change,[]))
    reduced=mat.multiply(mat.multiply(mat.transpose(change),G),change)
    D=[Q(c) for c in coverage["proof"]["LDL_diagonal"]];U=mat.matrix(coverage["proof"]["LDL_upper"])
    assert all(d>0 for d in D)
    assert all(U[i][j]==int(i==j) for i in range(32) for j in range(i+1))
    assert all(sum(D[k]*U[k][i]*U[k][j] for k in range(i+1))==reduced[i][j]
               for i in range(32) for j in range(i,32))
    assert not coverage["depends_on_qfminim_roundoff_guarantee"] and coverage["omitted_vector_control_rejected"]
    Gint,gden=integral_matrix(reduced)
    B,bden=integral_matrix(mat.multiply(O,change))
    BP,pden=integral_matrix(mat.multiply(mat.multiply(O,P),change))
    listed={v["enumeration_index"]:v for v in packet["classes"]}
    vectors=packet["enumeration"]["representatives_reduced_coordinates"]
    seen=set();classes=set();discard=Counter();field_values=[];classified=0
    for index,v in enumerate(vectors):
        key=canonical(v);assert key not in seen;seen.add(key)
        nz=[(i,x) for i,x in enumerate(v) if x]
        energy=sum(x*y*Gint[i][j] for i,x in nz for j,y in nz)
        assert 0<Q(energy,gden)<=cutoff
        q=[sum(row[i]*x for i,x in nz) for row in B]
        n=norm_numerator(q)
        if n!=[bden*bden]+[0]*7:
            assert index not in listed;discard["reduced_norm_not_one"]+=1;continue
        qp=[sum(row[i]*x for i,x in nz) for row in BP]
        A=[Q(x,pden*pden) for x in norm_numerator(qp)];lo,hi=poly(A,roots[4])
        assert hi<T or lo>T
        if lo>T:
            assert index not in listed;discard["norm_one_above_A_cutoff"]+=1;continue
        row=listed[index];classified+=1;field_values.append((A,lo,hi))
        assert A==[Q(x) for x in row["A_field_coefficients"]]
        raw=[Q(x,bden) for x in q];assert raw==[Q(x) for x in row["quaternion_power_coordinates"]]
        assert ar.mv(change,v)==row["order_coordinates"]
        key=canonical(raw);assert key not in classes;classes.add(key)
    assert dict(discard)==packet["discarded_signed_pairs"]
    assert classified==len(listed)==packet["class_count_modulo_sign"]
    assert 2*len(seen)==packet["enumeration"]["vectors_including_both_signs"]==2*coverage["signed_pair_count"]
    assert all(canonical(q[:8]+tuple(-x for x in q[8:])) in classes for q in classes)
    identity=[v for v in field_values if v[0]==list(ar.ONE)]
    assert len(identity)==1 and canonical([Q(1)]+[Q(0)]*31) in classes
    assert all(lo>64 for a,lo,hi in field_values if a!=list(ar.ONE))
    return {"cutoff":T,"signed_pairs_checked":len(seen),"norm_one_classes":len(classes),
            "interval_recursion_nodes":sum(coverage["proof"]["nodes_by_coordinate"]),
            "positive_weight_proofs":16,"unit_signature_rank":8,"inverse_pairing_checked":True},classes


def analytic_checks(packet,packing,sets):
    assert packet["complete_norm_one_family_bounded"] and packing["complete_norm_one_family_bounded"]
    assert not packet["other_norm_ideal_families_bounded"] and not packing["Shimura_derivative_computed"]
    terms={r["class_index"]:r for r in packet["class_terms"]};assert len(terms)==541
    for k in packet["kernels"]:
        for r in k["values"]:
            lo,hi=read_interval(r["value"]);assert hi-lo<Q(1,10**30)
            assert 0<read_interval(r["strip_error_bound"])[1]<Q(1,10**40)
            assert 0<read_interval(r["vertical_tail_bound"])[1]<Q(1,10**40)
    records=[]
    for row,better in zip(packet["cutoffs"],packing["cutoffs"]):
        T=row["cutoff"];assert T==better["cutoff"] and row["class_count"]==len(sets[T])
        assert row["partial_sums"]==better["partial_sums"]
        for ptext,v in better["moment_bounds"].items():
            p=Q(ptext);u=Q(7,9);w2=1-Q(1,T);coefficient=Q(1);total=Q(0)
            for n in range(129):
                if n:coefficient*=((p+n)/n)**2
                total+=coefficient*w2**n*u**(n+1)/(n+1)
            assert v["angular_series_terms"]==129 and total==Q(v["angular_series_lower_sum"])
            lo,hi=read_interval(v["outside_A"])
            # Exact squaring verifies the radical enclosure for cosh((R-r)/2)^2.
            center=Q(8*(2*T-1)+1,2);square=Q(63*T*(T-1))
            assert lo>1 and 0<center-hi and (center-hi)**2<=square<=(center-lo)**2
            wl,wh=read_interval(v["radial_weight_lower_bound"])
            if p<=1:assert wl==wh==1
            else:
                power=p-1
                assert 0<wl and wl**power.denominator<=Q(2,9)**power.numerator<=wh**power.denominator
            ml,mh=read_interval(v["sum_A_to_minus_p_minus_one_upper_bound"])
            assert ml>0
            # This is an exact rational check of the saved fractional-power
            # upper bound, with no floating-point evaluation in this audit.
            assert (mh*p*wl*total)**p.denominator*lo**p.numerator>=1
        for a in ["1","3","5"]:
            tail=better["infinite_norm_one_tail"][a];elo,ehi=read_interval(tail["absolute_error_bound"])
            assert 0<elo<=ehi<read_interval(row["infinite_norm_one_tail"][a]["absolute_error_bound"])[0]
            assert ehi==min(read_interval(v["bound"])[1] for v in tail["alternatives"])
            for part in ["real","imag"]:
                lo,hi=read_interval(better["full_norm_one_family_enclosures"][a][part])
                pl,ph=read_interval(row["partial_sums"][a][part])
                if a=="1" and part=="imag":assert lo==hi==0 and pl<=0<=ph
                else:assert lo<=pl-ehi and ph+ehi<=hi
        records.append({"cutoff":T,"S11_partial":row["partial_sums"]["1"]["real"]["display"],
                        "S11_tail_bound":better["infinite_norm_one_tail"]["1"]["absolute_error_bound"]["display"]})
    last=packing["cutoffs"][-1]
    assert read_interval(last["full_norm_one_family_enclosures"]["1"]["real"])[0]>0
    return {"kernel_count":sum(len(v["values"]) for v in packet["kernels"]),"class_terms":541,
            "cutoffs":records,"full_norm_one_S11_proved_positive":True,
            "analytic_scope":"Arb gamma/zeta nodes and analytic bounds hash-bound; rational disk-average series replayed"}


def compute():
    sources={};jobs=[]
    def bind(p,expected=None):
        p=Path(p);p=p if p.is_absolute() else ROOT/p
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        if expected is not None:assert h==expected,p
        rel=str(p.relative_to(ROOT));sources[rel]={"path":rel,"sha256":h}
    def read(name):
        p=DATA/name;doc=json.loads(p.read_text());bind(p)
        for v in doc.get("sources",[]):bind(v["path"],v["sha256"])
        return doc
    raw=read("cm_orbit.json");local=read("nelson_cm_lattice_d90.json");prepared=prepare(raw,local)
    exact=[];sets={}
    for T in [400,1600,6400,25600]:
        packet=read(f"nelson_norm_one_d92_T{T}.json");coverage=read(f"nelson_norm_one_coverage_d92_T{T}.json")
        record,classes=check_packet(packet,coverage,prepared)
        if sets:assert sets[max(sets)]<classes
        exact.append(record);sets[T]=classes
        print("EXACT_CUTOFF_PASS",T,len(classes),flush=True)
    packet=read("nelson_norm_one_sum_d92_T25600.json");packing=read("nelson_norm_one_packing_tail_d92.json")
    old=read("nelson_norm_one_sum_d92_T6400.json")
    assert old["tail_constants"]==packet["tail_constants"]
    for left,right in zip(old["cutoffs"],packet["cutoffs"]):
        assert left["cutoff"]==right["cutoff"] and left["class_count"]==right["class_count"]
        for a in ["1","3","5"]:
            for part in ["real","imag"]:
                assert overlap(read_interval(left["partial_sums"][a][part]),read_interval(right["partial_sums"][a][part]))
    analytic=analytic_checks(packet,packing,sets)
    for p in sorted(DATA.glob("nelson_norm_one*_d92*attempt*.job.json")):
        job=json.loads(p.read_text());bind(p);bind(job["log"]["path"],job["log"]["sha256"])
        for v in job["sources"]:bind(v["path"],v["sha256"])
        assert job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
        jobs.append({"path":str(p.relative_to(ROOT)),"status":job["status"],"wall_seconds":job["wall_seconds"]})
    assert len(jobs)==12 and Counter(v["status"] for v in jobs)=={"pass":11,"failed":1}
    for p in [Path(__file__),Path(ar.__file__),Path(mat.__file__)]:bind(p)
    return {"status":"pass: complete bounded norm-one enumeration and an infinite-family enclosure",
            "exact":exact,"analytic":analytic,"jobs":jobs,"sources":sorted(sources.values(),key=lambda v:v["path"]),
            "complete_norm_one_family_bounded":True,"global_Hilbert_theta_lift_evaluated":False,
            "Shimura_derivative_computed":False,
            "next":"extend fixed-norm enumeration to matched Hecke ideals; prove an all-ideal tail and identify the global test vector"}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--check",action="store_true");args=p.parse_args()
    result=compute();out=DATA/"nelson_norm_one_d92.json"
    if args.check:assert result==json.loads(out.read_text())
    else:assert not out.exists();out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: D92 complete norm-one cutoffs, bounded infinite norm-one family;",len(result["sources"]),"hashes")


if __name__=="__main__":main()

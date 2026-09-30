"""D93 standard-Python replay, with refined algebraic coefficient bounds.

Continuation of frozen 349, whose endpoint-product assertion was too
strong: a saved enclosing interval can be wider than the live Arb ball.
Exact bisection tightens the isolated Hecke roots before certification.

Checks fixed-norm coverage inputs, every vector classification, the
32 local ideal orbits, their exact norm-one witnesses, Hecke root
isolation, rational moment bounds and saved interval containment.
Arb recursion, Gamma/zeta nodes and the all-ideal analytic proof remain
explicitly separate from this rational replay.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"
spec=importlib.util.spec_from_file_location("norm_one",Path(__file__).with_name("343_nelson_norm_one_audit.py"))
prev=importlib.util.module_from_spec(spec);spec.loader.exec_module(prev)
ar,mat=prev.ar,prev.mat


def bareiss(a):
    a=[list(map(int,r)) for r in a];n=len(a);previous=1;sign=1
    for k in range(n-1):
        pivot=next(i for i in range(k,n) if a[i][k])
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        value=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=a[i][j]*value-a[i][k]*a[k][j];assert v%previous==0;a[i][j]=v//previous
            a[i][k]=0
        previous=value
    return sign*a[-1][-1]


def rank_mod(a,p=31):
    a=[[int(v)%p for v in r] for r in a];rank=0
    for j in range(len(a[0])):
        k=next((k for k in range(rank,len(a)) if a[k][j]),None)
        if k is None:continue
        a[rank],a[k]=a[k],a[rank];v=pow(a[rank][j],-1,p);a[rank]=[x*v%p for x in a[rank]]
        for k in range(len(a)):
            if k!=rank:
                v=a[k][j];a[k]=[(x-v*y)%p for x,y in zip(a[k],a[rank])]
        rank+=1
        if rank==len(a):break
    return rank


def packet_checks(packet,coverage,prepared):
    O,M,P,C,pairs,traces=prepared;T=packet["invariant_A_cutoff"]
    assert packet["prime_norm"]==31 and packet["prime_b_residue"]==27
    roots=[tuple(Q(v) for v in r) for r in packet["real_root_intervals"]]
    for i,(lo,hi) in enumerate(roots):
        assert lo<hi and prev.poly(ar.POLY+[1],(lo,lo))[0]*prev.poly(ar.POLY+[1],(hi,hi))[0]<0
        if i:assert roots[i-1][1]<lo
    generator=packet["norm_generator"];n=tuple(Q(c) for c in generator["totally_positive_generator_coefficients"])
    g=tuple(Q(c) for c in generator["saved_generator_coefficients"]);unit=tuple(Q(c) for c in generator["unit_correction_coefficients"])
    assert g==tuple(map(Q,[1,2,0,-4,0,1,0,0])) and ar.fmul(g,unit)==n
    assert ar.integral(n) and ar.fnorm(n)==31 and ar.integral(unit) and ar.integral(ar.finverse(unit)) and abs(ar.fnorm(unit))==1
    assert all(prev.poly(n,r)[0]>0 for r in roots)
    zeros=[r for r in range(31) if sum(c*pow(r,j) for j,c in enumerate(ar.POLY+[1]))%31==0
           and sum(int(c)*pow(r,j) for j,c in enumerate(g))%31==0]
    assert zeros==[27]
    sig=packet["unit_signature_proof"];signs=[]
    for row in sig["units_power_coordinates"]:
        u=tuple(Q(c) for c in row);assert ar.integral(u) and ar.integral(ar.finverse(u)) and abs(ar.fnorm(u))==1
        values=[prev.poly(u,r) for r in roots];assert all(v[0]>0 or v[1]<0 for v in values)
        signs.append([int(v[1]<0) for v in values])
    assert signs==sig["signatures"] and prev.rank2(signs)==8
    majorant=packet["majorant"];weighted=[]
    for index,(name,sign) in enumerate([("gamma_coefficients",1),("eta_coefficients",-1)]):
        w=tuple(Q(c) for c in majorant[name]);normalized=ar.fmul(w,n)
        assert list(normalized)==[Q(c) for c in majorant["normalized_weight_coefficients"][index]]
        for i,r in enumerate(roots):
            lo,hi=prev.poly(normalized,r);target=Q(sign*31,2*T) if i==4 else Q(1);error=abs(target)/1000
            assert target-error<lo<=hi<target+error
        tw=[sum(w[j]*traces[j][k] for j in range(8)) for k in range(8)]
        weighted.append([[sum(x*y for x,y in zip(tw,v)) for v in row] for row in pairs])
    gp=mat.multiply(mat.multiply(mat.transpose(P),weighted[0]),P);gc=mat.multiply(mat.multiply(mat.transpose(C),weighted[1]),C)
    G=[[a+b for a,b in zip(x,y)] for x,y in zip(gp,gc)];assert G==mat.matrix(majorant["gram"])
    cutoff=Q(1001,1000)*(8-Q(31,2*T));assert cutoff==Q(majorant["cutoff"])
    change=mat.matrix(majorant["reduction_change"]);assert ar.integral(sum(change,[])) and abs(mat.determinant(change))==1
    reduced=mat.multiply(mat.multiply(mat.transpose(change),G),change)
    D=[Q(v) for v in coverage["proof"]["LDL_diagonal"]];U=mat.matrix(coverage["proof"]["LDL_upper"])
    assert all(d>0 for d in D) and all(U[i][j]==int(i==j) for i in range(32) for j in range(i+1))
    assert all(sum(D[k]*U[k][i]*U[k][j] for k in range(i+1))==reduced[i][j] for i in range(32) for j in range(i,32))
    assert not coverage["depends_on_qfminim_roundoff_guarantee"] and coverage["omitted_vector_control_rejected"]
    Gint,gden=prev.integral_matrix(reduced);B,bden=prev.integral_matrix(mat.multiply(O,change))
    BP,pden=prev.integral_matrix(mat.multiply(mat.multiply(O,P),change));ninv=ar.finverse(n)
    listed={r["enumeration_index"]:r for r in packet["classes"]};seen=set();classes=set();discard=Counter();count=0
    for index,v in enumerate(packet["enumeration"]["representatives_reduced_coordinates"]):
        key=prev.canonical(v);assert key not in seen;seen.add(key);nz=[(i,x) for i,x in enumerate(v) if x]
        energy=sum(x*y*Gint[i][j] for i,x in nz for j,y in nz);assert 0<Q(energy,gden)<=cutoff
        q=[sum(row[i]*x for i,x in nz) for row in B]
        if prev.norm_numerator(q)!=[int(c*bden*bden) for c in n]:
            assert index not in listed;discard["reduced_norm_not_selected_generator"]+=1;continue
        qp=[sum(row[i]*x for i,x in nz) for row in BP]
        A=ar.fscale(ar.fmul(tuple(Q(x,pden*pden) for x in prev.norm_numerator(qp)),ninv),31)
        lo,hi=prev.poly(A,roots[4]);assert hi<T or lo>T
        if lo>T:
            assert index not in listed;discard["selected_norm_above_A_cutoff"]+=1;continue
        assert lo>31 or A==ar.fscale(ar.ONE,31)
        row=listed[index];count+=1;raw=[Q(x,bden) for x in q]
        assert raw==[Q(x) for x in row["quaternion_power_coordinates"]] and list(A)==[Q(c) for c in row["A_field_coefficients"]]
        assert ar.mv(change,v)==row["order_coordinates"]
        key=prev.canonical(raw);assert key not in classes;classes.add(key)
    assert dict(discard)==packet["discarded_signed_pairs"] and count==len(listed)==packet["class_count_modulo_sign"]
    assert 2*len(seen)==packet["enumeration"]["vectors_including_both_signs"]==2*coverage["signed_pair_count"]
    assert all(prev.canonical(q[:8]+tuple(-x for x in q[8:])) in classes for q in classes)
    return {"cutoff":T,"ellipsoid_signed_pairs":len(seen),"prime_classes":len(classes),
            "interval_recursion_nodes":sum(coverage["proof"]["nodes_by_coordinate"]),"unit_signature_rank":8,
            "conjugation_pairing_checked":True},classes


def coset_checks(packet,cosets,raw):
    O=mat.transpose(mat.matrix(raw["quaternion_export"]["order_basis"]));basis=[ar.quaternion(v) for v in raw["quaternion_export"]["order_basis"]]
    n=tuple(Q(c) for c in packet["norm_generator"]["totally_positive_generator_coefficients"])
    E=cosets["finite_embedding"];ii=[E["i"][:2],E["i"][2:]];jj=[E["j"][:2],E["j"][2:]]
    def mod(m):return [[v%31 for v in row] for row in m]
    def product(x,y):return mod(mat.multiply(x,y))
    assert product(ii,ii)==[[11,0],[0,11]] and product(jj,jj)==[[30,0],[0,30]]
    assert product(ii,jj)==mod([[-v for v in row] for row in product(jj,ii)])
    four=[[[1,0],[0,1]],ii,jj,product(ii,jj)]
    def field_reduce(v):return sum(c.numerator*pow(c.denominator,-1,31)*pow(27,j,31) for j,c in enumerate(v))%31
    def rho(q):
        values=[field_reduce(c) for c in q]
        return [sum(v*four[k][i][j] for k,v in enumerate(values))%31 for i in range(2) for j in range(2)]
    reduction=mat.transpose([rho(q) for q in basis]);assert reduction==E["reduction_matrix"] and rank_mod(reduction)==4
    N=cosets["norm_scalar_matrix"];assert bareiss(N)==31**4 and mod(mat.multiply(reduction,N))==[[0]*32 for _ in range(4)]
    assert mat.multiply(O,N)==mat.transpose([ar.flatten(ar.central(q,n)) for q in basis])
    assert cosets["all_32_orbits_exhibited"] and cosets["realized_lines"]==list(range(32))
    by_index={r["index"]:r for r in packet["classes"]};representatives={}
    for row in cosets["coset_representatives"]:
        label=row["line_label"];r=by_index[row["representative_class_index"]];q=ar.quaternion(r["quaternion_power_coordinates"])
        assert ar.mv(O,row["order_coordinates"])==ar.flatten(q)
        bar=(q[0],)+tuple(ar.fscale(c,-1) for c in q[1:]);assert ar.mv(O,row["conjugate_order_coordinates"])==ar.flatten(bar)
        L=row["left_matrix"];Lbar=row["conjugate_left_matrix"]
        assert bareiss(L)==31**2 and mat.multiply(L,Lbar)==N and mat.multiply(Lbar,L)==N
        assert mat.multiply(O,L)==mat.transpose([ar.flatten(ar.qmul(q,e)) for e in basis])
        assert mat.multiply(O,Lbar)==mat.transpose([ar.flatten(ar.qmul(bar,e)) for e in basis])
        image=mod(mat.multiply(reduction,L));assert rank_mod(image)==2
        if label<31:assert all((image[2][j]-label*image[0][j])%31==0 and (image[3][j]-label*image[1][j])%31==0 for j in range(32))
        else:assert all(v==0 for row in image[:2] for v in row)
        assert label not in representatives;representatives[label]=q
    counts=Counter();seen=set()
    for row in cosets["class_witnesses"]:
        index=row["class_index"];assert index not in seen;seen.add(index);label=row["line_label"];counts[str(label)]+=1
        gamma=ar.quaternion(ar.mv(O,row["right_norm_one_order_coordinates"]));assert ar.qnorm(gamma)==ar.ONE
        q=ar.quaternion(by_index[index]["quaternion_power_coordinates"]);assert ar.qmul(representatives[label],gamma)==q
        a,b,c,d=rho(q);assert (a*d-b*c)%31==0 and any([a,b,c,d])
        assert (c-label*a)%31==(d-label*b)%31==0 if label<31 else a==b==0
    assert len(seen)==len(by_index) and dict(counts)==cosets["coset_counts"]
    # A wrong finite prime label must fail the saved generator test.
    assert sum(c*pow(10,j) for j,c in enumerate([1,2,0,-4,0,1,0,0]))%31!=0
    return {"right_orbits":32,"ideal_index":31**2,"kernel_index":31**4,
            "exact_class_witnesses":len(seen),"finite_ring_rank":4,"wrong_prime_label_rejected":True}


def moment_check(row):
    t=Q(row["displacement_cutoff"]);p=Q(row["exponent_p"]);u=Q(7,9);w2=1-1/t;assert t>Q(9,2)
    total=Q(0);coefficient=Q(1)
    for j in range(129):
        if j:coefficient*=((p+j)/j)**2
        total+=coefficient*w2**j*u**(j+1)/(j+1)
    assert row["angular_series_terms"]==129 and total==Q(row["angular_series_lower_sum"])
    lo,hi=prev.read_interval(row["outside_A"]);center=(8*(2*t-1)+1)/2;square=63*t*(t-1)
    assert 1<lo<=hi<center and (center-hi)**2<=square<=(center-lo)**2
    wl,wh=prev.read_interval(row["radial_weight_lower_bound"])
    if p<=1:assert wl==wh==1
    else:
        power=p-1;assert 0<wl and wl**power.denominator<=Q(2,9)**power.numerator<=wh**power.denominator
    ml,mh=prev.read_interval(row["orbit_moment_bound"]);assert 0<ml<=mh
    assert (mh*p*wl*total)**p.denominator*lo**p.numerator>=1


def analytic_checks(packet,series,global_bounds,old_constants,z0):
    assert series["complete_prime_family_bounded"] and series["all_auxiliary_ideals_summed"] and series["all_beta_powers_summed"]
    assert not series["Shimura_derivative_computed"]
    classes=packet["classes"];terms={r["class_index"]:r for r in series["class_terms"]};assert len(terms)==len(classes)==586
    for row in series["cutoffs"]:
        T=row["cutoff"];chosen=[v for v in classes if Q(v["A_interval"][1])<T];assert len(chosen)==row["class_count"]
        for m in row["moment_bounds"].values():assert Q(m["displacement_cutoff"])==Q(T,31);moment_check(m)
        for a in ["1","3","5"]:
            for part in ["real","imag"]:
                combined=(sum(prev.read_interval(terms[v["index"]]["values"][a][part])[0] for v in chosen),
                          sum(prev.read_interval(terms[v["index"]]["values"][a][part])[1] for v in chosen))
                assert prev.overlap(combined,prev.read_interval(row["partial_sums"][a][part]))
            tail=row["infinite_prime_family_tail"][a];e=prev.read_interval(tail["absolute_error_bound"])[1]
            assert e==min(prev.read_interval(v["bound"])[1] for v in tail["alternatives"])
            for option in tail["alternatives"]:
                c=Q(option["contour"]);const=next(v for v in old_constants if Q(v["contour"])==c)["constants"][a]
                b1=prev.read_interval(const["2"]["bound"])[1];b2=prev.read_interval(const[str(int(a)+2)]["bound"])[1]
                m1=prev.read_interval(row["moment_bounds"][str(c)]["orbit_moment_bound"])[1]
                m2=prev.read_interval(row["moment_bounds"][str(c+1)]["orbit_moment_bound"])[1]
                error=prev.read_interval(option["bound"])[1]
                assert (error*31/(32*(b1*m1+b2*m2)))**c.denominator*(31*z0[0])**c.numerator>=1
            for part in ["real","imag"]:
                lo,hi=prev.read_interval(row["full_unweighted_prime_family_enclosures"][a][part]);pl,ph=prev.read_interval(row["partial_sums"][a][part])
                if a=="1" and part=="imag":assert lo==hi==0 and pl<=0<=ph
                else:assert lo<=pl-e and ph+e<=hi
    polynomial=[-899,433,-36,-8,1];roots=[];refined_roots=[]
    assert series["Hecke_polynomial_coefficients"]==polynomial and series["selected_root_index"]==0 and series["U_p2"]==1
    for row in series["weighted_first_quartic_orbit"]:
        lo,hi=prev.read_interval(row["Hecke_eigenvalue"]);assert prev.poly(polynomial,(lo,lo))[0]*prev.poly(polynomial,(hi,hi))[0]<0
        if roots:assert roots[-1][1]<lo
        roots.append((lo,hi))
        # Four disjoint sign-changing intervals exhaust this quartic's
        # roots. Exact bisection preserves the unique root, and avoids
        # requiring an output ball to contain the product of two wider
        # serialized endpoint boxes.
        for _ in range(32):
            mid=(lo+hi)/2
            if prev.poly(polynomial,(lo,lo))[0]*prev.poly(polynomial,(mid,mid))[0]<0:hi=mid
            else:lo=mid
        assert prev.poly(polynomial,(lo,lo))[0]*prev.poly(polynomial,(hi,hi))[0]<0
        refined_roots.append([str(lo),str(hi)])
        for a in ["1","3","5"]:
            v=row["weighted_prime_family"][a];error=prev.read_interval(v["absolute_error_bound"])[1]
            assert error>=max(abs(lo),abs(hi))*prev.read_interval(series["cutoffs"][-1]["infinite_prime_family_tail"][a]["absolute_error_bound"])[1]
    assert len(roots)==4
    # x^4+x+1 has no factor of degree one or two over F2.
    for f in [2,3,4,5,6,7]:
        r=19
        while r and r.bit_length()>=f.bit_length():r^=f<<(r.bit_length()-f.bit_length())
        assert r!=0
    assert global_bounds["all_ideal_absolute_convergence_proved"] and global_bounds["all_uncomputed_norm_ideal_families_bounded"]
    assert not global_bounds["complete_A_cutoff_evaluated"] and not global_bounds["useful_CM_accuracy_reached"]
    assert not global_bounds["Shimura_derivative_computed"]
    # Independently replay the Euler numerator identity D-X*D'=1-q*X^2.
    for q in [2,3,31,97]:
        D=[1,-(q+1),q];assert [D[j]-j*D[j] for j in range(3)]==[1,0,-q]
        for e in range(9):assert (e+1)*sum(q**j for j in range(e+1))>0
    for a in ["1","3","5"]:
        omitted=global_bounds["uncomputed_norm_ideal_bounds"][a]
        assert prev.read_interval(omitted["absolute_error_bound"])[1]==min(prev.read_interval(v["bound"])[1] for v in omitted["alternatives"])
        for option in omitted["alternatives"]:
            c=option["contour"];assert c>Q(3,2)
            bs=next(v for v in global_bounds["constants"] if v["contour"]==c)["constants"][a]
            bsum=prev.read_interval(bs["2"]["bound"])[1]+prev.read_interval(bs[str(int(a)+2)]["bound"])[1]
            mass=prev.read_interval(option["omitted_divisor_mass"])[1];bound=prev.read_interval(option["bound"])[1]
            assert bound*z0[0]**c>=bsum*mass/(1-Q(2,9)**c)
    for row in global_bounds["hypothetical_complete_cutoff_bounds"]:
        assert not row["cutoff_enumerated"]
        for values in row["bounds"].values():
            for option in values["alternatives"]:assert Q(3,2)<Q(option["moment_exponent"])<option["contour"]
            assert prev.read_interval(values["absolute_error_bound"])[1]==min(prev.read_interval(v["bound"])[1] for v in values["alternatives"])
    return {"scalar_kernels":sum(len(k["values"]) for k in series["kernels"]),"prime_class_terms":len(terms),
            "Hecke_roots_isolated":4,"refined_Hecke_root_intervals":refined_roots,"prime_S11_partial":series["cutoffs"][-1]["partial_sums"]["1"]["real"]["display"],
            "prime_S11_tail_bound":series["cutoffs"][-1]["infinite_prime_family_tail"]["1"]["absolute_error_bound"]["display"],
            "uncomputed_norm_ideal_S11_bound":global_bounds["uncomputed_norm_ideal_bounds"]["1"]["absolute_error_bound"]["display"],
            "scope":"rational arithmetic and interval-output replay; Arb nodes and exhaustive recursion bound to runs; analytic proofs in report"}


def compute():
    sources={};jobs=[]
    def bind(p,expected=None):
        p=Path(p);p=p if p.is_absolute() else ROOT/p;h=hashlib.sha256(p.read_bytes()).hexdigest()
        if expected is not None:assert h==expected,p
        rel=str(p.relative_to(ROOT));sources[rel]={"path":rel,"sha256":h}
    def read(name):
        p=DATA/name;doc=json.loads(p.read_text());bind(p)
        for src in doc.get("sources",[]):bind(src["path"],src["sha256"])
        return doc
    raw=read("cm_orbit.json");local=read("nelson_cm_lattice_d90.json");read("nelson_norm_one_d92.json")
    prepared=prev.prepare(raw,local);exact=[];sets={}
    for T in [6400,25600]:
        packet=read(f"nelson_prime31_b27_d93_T{T}.json");coverage=read(f"nelson_prime31_coverage_d93_T{T}.json")
        record,classes=packet_checks(packet,coverage,prepared)
        if sets:assert sets[max(sets)]<classes
        exact.append(record);sets[T]=classes;print("EXACT_PRIME_CUTOFF_PASS",T,len(classes),flush=True)
    small_cosets=read("nelson_prime31_cosets_d93_T6400.json");assert small_cosets["all_32_orbits_exhibited"]
    cosets=read("nelson_prime31_cosets_d93_T25600.json");orbit=coset_checks(packet,cosets,raw)
    print("EXACT_COSETS_PASS",orbit["right_orbits"],orbit["exact_class_witnesses"],flush=True)
    series=read("nelson_prime31_sum_d93.json");global_bounds=read("nelson_all_ideal_bounds_d93.json")
    old=read("nelson_norm_one_sum_d92_T25600.json");d91=read("nelson_interval_sum_d91.json")
    z0=prev.read_interval(next(v for v in d91["kernels"] if v["majorant_field_element"]==["1"]+["0"]*7)["Z"])
    analytic=analytic_checks(packet,series,global_bounds,old["tail_constants"]["contours"],z0)
    text=(DATA/"f16_steinberg.out").read_text();assert "z^4 - 8*z^3 - 36*z^2 + 433*z - 899" in text
    assert re.search(r"R60\|orbit 1 \(dim 4\): U_p2 charpoly \[\s*<z - 1, 4>\s*\]",text)
    for p in sorted(DATA.glob("nelson_*_d93*attempt*.job.json")):
        if p.name.startswith("nelson_d93_audit"):continue
        job=json.loads(p.read_text());bind(p);bind(job["log"]["path"],job["log"]["sha256"])
        for src in job["sources"]:bind(src["path"],src["sha256"])
        assert job["status"]=="pass" and job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
        jobs.append({"path":str(p.relative_to(ROOT)),"status":job["status"],"wall_seconds":job["wall_seconds"]})
    assert len(jobs)==8
    # Preserve and bind the first audit attempt; its failure was a
    # checker endpoint-comparison issue, with no rejected source data.
    failed_path=DATA/"nelson_d93_audit_attempt01.job.json"
    failed=read(failed_path.name)
    bind(failed["log"]["path"],failed["log"]["sha256"])
    assert failed["status"]=="failed" and failed["exit_code"]==1
    assert failed["timeout_seconds"]==180 and failed["timeout_terminates_process_group"]
    for p in [Path(__file__),Path(prev.__file__),Path(ar.__file__),Path(mat.__file__)]:bind(p)
    return {"status":"pass: complete norm-31 family and explicit but loose all-ideal bounds",
            "exact_cutoffs":exact,"cosets":orbit,"analytic":analytic,"jobs":jobs,
            "preserved_audit_failure":str(failed_path.relative_to(ROOT)),
            "sources":sorted(sources.values(),key=lambda v:v["path"]),
            "all_ideal_absolute_convergence_proved":True,"useful_CM_accuracy_reached":False,
            "global_Shimizu_test_vector_identification_proved":False,"Shimura_derivative_computed":False,
            "next":"review global kernel/summation and test-vector identification before extending the Hecke bank or cutoff"}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--check",action="store_true");args=p.parse_args()
    result=compute();out=DATA/"nelson_prime31_d93.json"
    if args.check:assert result==json.loads(out.read_text())
    else:assert not out.exists();out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: D93 prime-norm enumeration, 32 cosets, weighted family and all-ideal cost gate;",len(result["sources"]),"hashes")


if __name__=="__main__":main()

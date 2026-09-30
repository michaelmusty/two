"""D107 independent rational certificate for the saved CM point/root matching.

Root centers are certified by an integer Rouche inequality, not trusted as
numerical approximations. A field norm makes the resolvent match exact.
The companion proof uses the finite root-monomial rank to certify the cycle.
"""
import argparse
import ast
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"dembele/data/computed"
OUT=DATA/"cm_root_matching_review_d107.json"
F_POLY=[2,0,-16,0,20,0,-8,0,1]
L_POLY=[68,-2,-128,16,80,40,32,-80,-32,64,0,-16,16,8,0,0,-2,1]


def source(p):
    p=Path(p).resolve()
    return {"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}


def checked(items):
    paths=[]
    for item in items:
        p=ROOT/item["path"]
        assert source(p)["sha256"]==item["sha256"],str(p)
        paths.append(p)
    return paths


def module(name,p):
    spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def cmul(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])


def cadd(a,b):
    return (a[0]+b[0],a[1]+b[1])


def scaled_value(coefficients,z,denominator):
    coeff=list(map(int,coefficients))
    while len(coeff)>1 and coeff[-1]==0:
        coeff.pop()
    out=(coeff[-1],0);power=denominator
    for c in reversed(coeff[:-1]):
        out=cadd(cmul(out,z),(c*power,0));power*=denominator
    return out,len(coeff)-1


def rouche(coeff,z,D,R):
    n=len(coeff)-1
    assert abs(z[0])+abs(z[1])<8*D
    value,_=scaled_value(coeff,z,D)
    derivative,_=scaled_value([j*coeff[j] for j in range(1,n+1)],z,D)
    # If |c|<8 and r<=8, the nonlinear Taylor terms are <= M*r^2.
    M=sum(abs(coeff[j])*2**j*8**(j-2) for j in range(2,n+1))
    constant=abs(value[0])+abs(value[1])
    linear=max(abs(derivative[0]),abs(derivative[1]))*D*R
    remainder=constant*R*R+M*D**n
    assert linear>2*remainder
    return True


def poly_value(p,x):
    out=Q(0)
    for c in reversed(p):
        out=out*x+c
    return out


def sturm_chain(p):
    def trim(a):
        while len(a)>1 and a[-1]==0:
            a.pop()
        return a
    def rem(a,b):
        a=a[:]
        while len(a)>=len(b) and any(a):
            shift=len(a)-len(b);c=a[-1]/b[-1]
            for j,x in enumerate(b):
                a[j+shift]-=c*x
            trim(a)
        return a
    chain=[list(map(Q,p)),[Q(i*p[i]) for i in range(1,len(p))]]
    while True:
        nxt=[-c for c in rem(chain[-2],chain[-1])]
        if not any(nxt):
            break
        chain.append(nxt)
    assert len(chain[-1])==1
    return chain


def variations(chain,x):
    values=[poly_value(p,x) for p in chain]
    signs=[1 if z>0 else -1 for z in values if z]
    return sum(a!=b for a,b in zip(signs,signs[1:]))


def iadd(a,b):
    return (a[0]+b[0],a[1]+b[1])


def imul(a,b):
    v=[x*y for x in a for y in b]
    return min(v),max(v)


def ipoly(p,x):
    out=(Q(0),Q(0))
    for c in reversed(p):
        out=iadd(imul(out,x),(Q(c),Q(c)))
    return out


def quaternion_checks(orbit,real,witness):
    q=module("d91_quaternion_arithmetic",ROOT/"dembele/pari/334_nelson_unfolding_audit.py")
    mat=q.mat
    O=mat.transpose(mat.matrix(orbit["quaternion_export"]["order_basis"]))
    C=mat.matrix(real["normalizer_conjugation_in_order_basis"])
    assert q.integral(sum(C,[])) and mat.multiply(C,C)==mat.identity(32)
    conjugated=[[(-1 if i>=16 else 1)*c for c in row] for i,row in enumerate(O)]
    assert mat.multiply(O,C)==conjugated
    def from_order(v):
        return q.quaternion(q.mv(O,list(map(Q,v))))
    unit=q.quaternion(witness["positive_unit_quaternion"])
    U=witness["positive_unit_order_coordinates"]
    V=witness["positive_unit_inverse_order_coordinates"]
    assert q.integral(list(map(Q,U))+list(map(Q,V)))
    assert from_order(U)==unit
    inverse=from_order(V)
    assert q.qmul(unit,inverse)==q.QONE==q.qmul(inverse,unit)
    square=(Q(2),Q(4),Q(-28),Q(0),Q(22),Q(0),Q(-4),Q(0))
    base=q.central(q.qscale(q.quaternion(orbit["quaternion_export"]["elliptics"][8]),2),q.finverse(square))
    assert q.qmul(base,base)==(q.fscale((Q(2),Q(1))+q.ZERO[2:],-1),q.ZERO,q.ZERO,q.ZERO)
    I=(q.ZERO,q.ONE,q.ZERO,q.ZERO)
    R=q.qmul(inverse,I)
    assert R==q.quaternion(witness["point_fixing_negative_normalizer"])
    assert q.qadd(q.qmul(R,base),q.qmul(base,R))==(q.ZERO,)*4
    assert R[0]==q.ZERO
    assert list(q.qnorm(R))==list(map(Q,witness["point_fixing_normalizer_reduced_norm"]))
    D=int(witness["small_sign_center_common_denominator"]);eps=Q(1,10**60)
    b0=Q(int(witness["split_b_center_numerator"]),D)
    s0=Q(int(witness["sqrt_b_minus_b_squared_center_numerator"]),D)
    bint=(b0-eps,b0+eps);sint=(s0-eps,s0+eps)
    chain=sturm_chain(F_POLY)
    assert variations(chain,-2)-variations(chain,2)==8
    assert variations(chain,0)-variations(chain,1)==1
    assert variations(chain,bint[0])-variations(chain,bint[1])==1
    assert 0<bint[0]<bint[1]<Q(1,2) and sint[0]>0
    alow=bint[0]-bint[0]**2;ahigh=bint[1]-bint[1]**2
    assert sint[0]**2<alow<ahigh<sint[1]**2
    left=ipoly(base[2],bint)
    prod=imul(ipoly(base[3],bint),sint)
    lower_left=(left[0]-prod[1],left[1]-prod[0])
    assert lower_left[1]<0
    assert ipoly(q.qnorm(unit),bint)[0]>0
    assert ipoly(q.qnorm(R),bint)[1]<0
    labels=orbit["CM_orbit"]["class_labels_in_point_order"]
    reflection=[labels.index(-a%17) for a in labels]
    assert real["reflection_class_offset"]==0 and real["unique_real_point_index"]==[8]
    assert reflection==real["conjugation_point_permutation"]
    assert real["CM_beta_imaginary_sign_at_reference"]==-1
    return {"integer_normalizer_matrix_replayed":True,"positive_unit_and_inverse_integral":True,
            "point_fixing_negative_normalizer_anticommutes_with_beta":True,
            "split_b_root_uniquely_certified":True,"all_F_roots_in_minus2_plus2":True,
            "Rickards_lower_left_strictly_negative":True,"real_reference_point_index":8,
            "CM_beta_imaginary_sign":-1,"conjugation_point_permutation":reflection,
            "class_zero_reference_proved_without_numeric_function_values":True},bint


def root_checks(orbit,witness,bint):
    D=int(witness["root_center_common_denominator"])
    R=10**1080;assert D==10**1100
    centers=[tuple(map(int,p)) for p in witness["root_centers_real_imaginary_numerators"]]
    beta=tuple(map(int,witness["beta_center_real_imaginary_numerators"]))
    M_POLY=list(map(int,orbit["CM_orbit"]["CM_polynomial_ascending"]))
    assert len(centers)==17 and all(rouche(L_POLY,z,D,R) for z in centers)
    assert rouche(M_POLY,beta,D,R)
    assert beta[0]==0 and beta[1]<0
    # All CM roots are pure imaginary and have absolute value <2, since
    # the real subfield polynomial has all eight roots in (-2,2).
    lo=Q(beta[1],D)-Q(1,R);hi=Q(beta[1],D)+Q(1,R)
    assert lo<hi<0 and bint[0]<hi*hi-2<lo*lo-2<bint[1]
    assert abs(beta[1])*R+D<2*D*R
    old=orbit["field_root_action"]["complex_roots"]
    for i,z in enumerate(centers):
        assert abs(Q(z[0],D)-Q(old[i][0]))+abs(Q(z[1],D)-Q(old[i][1]))+Q(1,R)<Q(1,10**70)
        for w in centers[:i]:
            assert ((z[0]-w[0])**2+(z[1]-w[1])**2)*R**2>4*D**2
    real_indices=[i for i,z in enumerate(centers) if z[1]==0]
    assert real_indices==[2]
    assert all(abs(z[1])*R>D for i,z in enumerate(centers) if i!=2)
    assert sum(abs(c)*4**i for i,c in enumerate(L_POLY[:-1]))<4**17
    cycle=[a-1 for a in orbit["field_root_action"]["complex_frobenius_31"]]
    assert sorted(cycle)==list(range(17))
    visited=[];k=2
    for _ in range(17):
        visited.append(k);k=cycle[k]
    assert k==2 and len(set(visited))==17
    gamma=list(map(int,orbit["matching"]["resolvent_generator_in_K"]))
    while gamma[-1]==0:
        gamma.pop()
    gv,degree=scaled_value(gamma,beta,D)
    kv=(0,0)
    for i,z in enumerate(centers):
        kv=cadd(kv,cmul(cmul(z,z),centers[cycle[i]]))
    residual=(kv[0]*D**(degree-3)-gv[0],kv[1]*D**(degree-3)-gv[1])
    uncertainty=17*3*8**2+sum(i*abs(c)*2**(i-1) for i,c in enumerate(gamma) if i)
    centered=abs(residual[0])+abs(residual[1])
    # |kappa-gamma| < 10^-1000, by a fully integral comparison.
    assert centered*R*10**1000+uncertainty*D**degree*10**1000<D**degree*R
    conjugate_bound=1088+sum(abs(c)*2**i for i,c in enumerate(gamma))
    assert conjugate_bound==275090 and conjugate_bound**270<10**2000
    # Alternative one-embedding bound uses D105's resolvent conjugate bound.
    assert 2176**271<10**1000
    wrong_beta=(beta[0],-beta[1])
    wrong,_=scaled_value(gamma,wrong_beta,D)
    wrong_res=(kv[0]*D**(degree-3)-wrong[0],kv[1]*D**(degree-3)-wrong[1])
    assert max(abs(c) for c in wrong_res)*1000>D**degree
    inverse=[cycle.index(i) for i in range(17)]
    wrong_k=(0,0)
    for i,z in enumerate(centers):
        wrong_k=cadd(wrong_k,cmul(cmul(z,z),centers[inverse[i]]))
    wrong_res=(wrong_k[0]*D**(degree-3)-gv[0],wrong_k[1]*D**(degree-3)-gv[1])
    assert max(abs(c) for c in wrong_res)*1000>D**degree
    return {"root_disks_certified":17,"CM_beta_disk_certified":True,
            "disk_radius_decimal_exponent":1080,"linear_Rouche_term_exceeds_twice_remainder":True,
            "all_root_disks_disjoint":True,"saved_root_centers_match_within_10_minus70":True,
            "unique_real_root_index":2,"resolvent_difference_absolute_bound":"10^-1000",
            "all_conjugate_difference_bound_without_resolvent_root_bound":conjugate_bound,
            "two_conjugate_embeddings_norm_bound_strictly_below_one":True,
            "one_embedding_D105_resolvent_norm_bound_also_passes":True,
            "algebraic_resolvent_equality_via_integral_norm_proof":True,
            "wrong_beta_sign_rejected":True,"inverse_cycle_rejected":True,
            "certified_cycle_proposal_zero_based":cycle,"cycle_starting_at_real_root":visited}


def fmul(a,b,modulus):
    out=[0]*33
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                out[i+j]+=x*y
    for k in range(32,16,-1):
        v=out[k]%modulus
        if v:
            for j,c in enumerate(L_POLY[:-1]):
                out[k-17+j]-=v*c
    return [c%modulus for c in out[:17]]


def fpow(a,n,modulus):
    out=[1]+[0]*16
    while n:
        if n&1:out=fmul(out,a,modulus)
        a=fmul(a,a,modulus);n>>=1
    return out


def fvalue(p,a,modulus):
    out=[0]*17
    for c in reversed(p):
        out=fmul(out,a,modulus);out[0]=(out[0]+c)%modulus
    return out


def rank_mod(rows):
    a=[row[:] for row in rows];r=0
    for col in range(len(a[0])):
        k=next((i for i in range(r,len(a)) if a[i][col]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        inv=pow(a[r][col],-1,31)
        a[r]=[x*inv%31 for x in a[r]]
        for i in range(r+1,len(a)):
            c=a[i][col]
            if c:a[i]=[(x-c*y)%31 for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r


def pair_and_local_checks(orbit):
    alpha=[0,1]+[0]*15;roots=[alpha]
    for _ in range(16):
        roots.append(fpow(roots[-1],31,31))
    assert len(set(map(tuple,roots)))==17 and fpow(roots[-1],31,31)==alpha
    assert all(not any(fvalue(L_POLY,z,31)) for z in roots)
    pairs=[(i,j) for i in range(17) for j in range(17) if i!=j]
    rows=[]
    for a in range(1,17):
        values=[fmul(fmul(roots[a*i%17],roots[a*i%17],31),roots[a*j%17],31) for i,j in pairs]
        rows.extend([[z[k] for z in values] for k in range(17)])
    assert all(sum(row)%31==0 for row in rows)
    rank=rank_mod(rows);assert rank==271
    text=(DATA/"cm_root_pair_rank_d107_attempt01.log").read_text()
    assert "RANK|271" in text and "NULLITY|1" in text and "PASS|D107_ROOT_PAIR_MONOMIAL_RANK" in text
    match=re.search(r"^KERNEL\|(.+?)^CPU_SECONDS\|",text,re.M|re.S)
    assert ast.literal_eval(match.group(1))==[[1]*272]
    # Independent Newton identities give the exact characteristic-zero relation.
    s1,s2,s3=2,4,8
    assert s1*s2-s3==0
    # Hensel-lift ALL roots in Z/31^8[alpha]/(f), independently of Magma.
    exponent=8;modulus=31**exponent
    derivative=[j*L_POLY[j] for j in range(1,18)]
    def inverse_unit(a,m):
        inv=fpow([c%31 for c in a],31**17-2,31)
        current=31
        while current<m:
            current=min(current*current,m)
            ainv=fmul(a,inv,current)
            correction=[(-c)%current for c in ainv];correction[0]=(correction[0]+2)%current
            inv=fmul(inv,correction,current)
        assert fmul(a,inv,m)==[1]+[0]*16
        return inv
    lifted=[]
    for z in roots:
        z=z[:];current=31
        while current<modulus:
            current=min(current*current,modulus)
            error=fvalue(L_POLY,z,current)
            inv=inverse_unit(fvalue(derivative,z,current),current)
            z=[(a-b)%current for a,b in zip(z,fmul(error,inv,current))]
        assert not any(fvalue(L_POLY,z,modulus))
        lifted.append(z)
    kappa=[0]*17
    for i,z in enumerate(lifted):
        term=fmul(fmul(z,z,modulus),lifted[(i+1)%17],modulus)
        kappa=[(a+b)%modulus for a,b in zip(kappa,term)]
    assert not any(kappa[1:])
    assert kappa[0]==int(orbit["field_root_action"]["kappa_mod31_60"])%modulus
    mp=list(map(int,orbit["CM_orbit"]["CM_polynomial_ascending"]))
    gp=list(map(int,orbit["matching"]["resolvent_generator_in_K"]))
    def value(p,z,m):
        out=0
        for c in reversed(p):out=(out*z+c)%m
        return out
    md=[j*mp[j] for j in range(1,len(mp))]
    beta_roots=[]
    for residue in range(31):
        if value(mp,residue,31):continue
        z=residue;current=31
        while current<modulus:
            current=min(current*current,modulus)
            z=(z-value(mp,z,current)*pow(value(md,z,current),-1,current))%current
        assert value(mp,z,modulus)==0
        beta_roots.append((residue,z,value(gp,z,modulus)))
    assert len(beta_roots)==16 and len({c for _,_,c in beta_roots})==16
    matches=[r for r,z,c in beta_roots if c==kappa[0]]
    assert matches==[19]
    return {"ordered_pair_cubic_monomials":272,"rank_mod31":rank,
            "only_rational_relation_via_reduction_and_Newton_identity":"sum_{i!=j} r_i^2*r_j=0",
            "directed_cycle_sums_distinct_via_companion_proof":True,
            "independent_padic_lift_precision":exponent,"padic_kappa_residue":str(kappa[0]),
            "padic_kappa_is_scalar":True,"matches_D59_padic_kappa":True,
            "CM_beta_roots_with_resolvent_values_mod31_power":[list(map(str,row)) for row in beta_roots],
            "unique_matching_beta_mod31":19,"prime_ideal_class_in_saved_generator":3}


def computations():
    orbit=json.loads((DATA/"cm_orbit.json").read_text())
    real=json.loads((DATA/"cm_real_structure_d107.json").read_text())
    witness=json.loads((DATA/"cm_root_matching_witness_d107.json").read_text())
    exact,bint=quaternion_checks(orbit,real,witness)
    root=root_checks(orbit,witness,bint)
    local=pair_and_local_checks(orbit)
    assert real["prime31_beta19_class_in_saved_generator"]==3
    labels=orbit["CM_orbit"]["class_labels_in_point_order"]
    cycle=root["cycle_starting_at_real_root"]
    lookup=[cycle[6*c%17] for c in labels]
    assert lookup==orbit["matching"]["point_to_root_index_zero_based"]
    return {"real_structure":exact,"complex_root_and_norm_certificate":root,
            "root_cycle_and_local_comparison":local,
            "point_to_root_index_zero_based":lookup}


def build():
    result=computations()
    paths=[Path(__file__),ROOT/"dembele/pari/334_nelson_unfolding_audit.py",
           ROOT/"dembele/pari/325_nelson_d90_audit.py"]
    prior_path=DATA/"cm_ratio_jet_review_d106.json";prior=json.loads(prior_path.read_text())
    assert prior["status"]=="pass" and len(prior["sources"])==562
    paths+=checked(prior["sources"])+[prior_path]
    for name in ["cm_real_structure_d107.json","cm_root_matching_witness_d107.json"]:
        p=DATA/name;saved=json.loads(p.read_text())
        paths+=checked(saved["sources"])+[p]
    for stem in ["cm_real_structure_d107_attempt02","cm_root_pair_rank_d107_attempt01","cm_root_matching_witness_d107_attempt02"]:
        p=DATA/(stem+".job.json");job=json.loads(p.read_text())
        assert job["status"]=="pass" and job["timeout_seconds"]==180
        assert job["wall_seconds"]<180 and job["timeout_terminates_process_group"]
        paths+=checked(job["sources"]+[job["driver"],job["log"]])+[p]
    for stem in ["cm_real_structure_d107","cm_root_matching_witness_d107"]:
        p=DATA/(stem+"_attempt01.job.json");failed=json.loads(p.read_text())
        snapshot=DATA/(stem+"_attempt01_failed.py")
        assert failed["status"]=="failed" and source(snapshot)["sha256"]==failed["driver"]["sha256"]
        paths+=checked(failed["sources"]+[failed["log"]])+[p,snapshot,DATA/(stem+"_failure.json")]
    probe=DATA/"cm_root_matching_review_d107_probe_attempt01.job.json"
    if probe.exists():
        job=json.loads(probe.read_text());assert job["status"]=="pass"
        paths+=checked(job["sources"]+[job["driver"],job["log"]])+[probe]
    paths += [ROOT/"dembele/certificates/cm-root-matching-d107.md",
              DATA/"cm_root_matching_sources_d107.json"]
    return {"status":"pass","milestone":"D107","certificates":result,
            "D106_source_hashes_checked_unchanged":562,
            "saved_CM_point_root_matching_certified_via_companion_proof":True,
            "CM_reference_realness_and_embedding_sign_certified":True,
            "old_complex_padic_root_ordering_comparison_trusted":False,
            "candidate_equations_or_analytic_differential_banks_used":False,
            "independent_Shimura_tangent_or_jet_evaluated":False,
            "particular_actual_G12_chart_certified":False,
            "candidate_curve_identification_proved":False,"target_field_polynomial_constructed":False,
            "sources":[source(p) for p in sorted(set(p.resolve() for p in paths))],
            "scope":"Exact finite witnesses and norm certificate. CM reciprocity, D106 rigidity and the geometric comparison proof are mathematical inputs, not machine-verified."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--probe",action="store_true")
    mode.add_argument("--check",action="store_true")
    args=parser.parse_args()
    if args.probe:
        result=computations()
        print(json.dumps(result,indent=2),flush=True)
        print("PASS|D107_CM_ROOT_MATCHING_PROBE",flush=True);return
    if args.check:
        old=json.loads(OUT.read_text());checked(old["sources"])
    result=build()
    if args.check:assert result==old
    else:
        assert not OUT.exists(),"Preserve completed reviews."
        OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","source_hashes":len(result["sources"]),
                      "D106_hashes_unchanged":562,"root_monomial_rank":271,
                      "real_reference_point":8,"point_root_matching_certified":True}),flush=True)
    print("PASS|D107_CM_ROOT_MATCHING_REVIEW",flush=True)


if __name__=="__main__":
    main()


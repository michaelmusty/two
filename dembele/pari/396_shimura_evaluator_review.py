"""D108 rational replay of the spectral rejection and conditional dyadic interface.

Arb quadrature centers and Sage field controls are bound to successful runs.
This independently reconstructs more conservative rational quadrature errors,
the method floor, all local valuation formulas and formal coordinate changes.
It does not claim an actual Shimura cocycle, moment bank, or tangent.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
OUT = DATA/"shimura_evaluator_review_d108.json"
REPORT = ROOT/"dembele/certificates/shimura-evaluator-d108.md"
spec = importlib.util.spec_from_file_location("d97_intervals", ROOT/"dembele/pari/367_nelson_signed_orbit_audit.py")
ar = importlib.util.module_from_spec(spec); spec.loader.exec_module(ar)


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def checked(rows):
    paths = []
    for row in rows:
        path = ROOT/row["path"]
        assert source(path)["sha256"] == row["sha256"], str(path)
        paths.append(path)
    return paths


def pmul(a,b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j] += x*y
    return out


def padd(a,b):
    return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]


def gamma_polynomial(c):
    out = [Q(1)]
    for _ in range(8): out = pmul(out,[1,8])
    for limit,power in [(c-1,8),(c,8)]:
        for j in range(1,limit+1):
            for _ in range(power): out = pmul(out,[j,1])
    out = pmul(out,[2*c-1,2])
    assert len(out)-1 == 16*c+1
    return out


def integral_tail(poly,T):
    return sum(a*sum(Q(comb(j,v)*T**(j-v)*factorial(v),24**(v+1)) for v in range(j+1)) for j,a in enumerate(poly))


def quadrature_error(zlow,n):
    # e > 8/3, so replace every decaying exponential by a rational upper bound.
    def boundary(c,T=0):
        constant = zlow**(-c)*Q(2*c,2*c-1)**8*Q(1+2**c)/(1-Q(1,2**(c+1)))
        return constant*2*integral_tail(gamma_polynomial(c),T)*Q(3,8)**(24*T)
    return (boundary(1)+boundary(3))/(6*(Q(8,3)**(6*n)-1))+boundary(2,16)/6


def pi_interval():
    def atan_inverse(q,n):
        total = sum(Q((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(n))
        following = Q((-1)**n,(2*n+1)*q**(2*n+1))
        return min(total,total+following),max(total,total+following)
    a,b = atan_inverse(5,64),atan_inverse(239,20)
    # Machin identity; standard alternating-series bounds.
    return 16*a[0]-4*b[1],16*a[1]-4*b[0]


def spectral_replay(packet):
    pi = pi_interval(); ar.overlap(pi,ar.box(packet["pi"]))
    root6 = ar.radical(Q(6),2)
    maximum = ar.mul(ar.scale(pi,4),(5-2*root6[1],5-2*root6[0]))
    ar.overlap(maximum,ar.box(packet["maximum_comparison_transform_D2"]))
    # In Q(sqrt(6)): t*p*(p+1)-(p-2) = t*(p-a)^2.
    def mul6(x,y): return x[0]*y[0]+6*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
    t,a = (5,-2),(2,1)
    assert mul6(t,mul6(a,a)) == (2,0)
    assert tuple(-2*x for x in mul6(t,a)) == (t[0]-1,t[1])
    assert maximum[0]>0
    norm31 = None
    for row in packet["rows"]:
        N = row["norm"]
        z = ar.box(row["argument"]); center = ar.box(row["finite_quadrature"])
        error = quadrature_error(z[0],packet["mesh_denominator"])
        value = center[0]-error,center[1]+error
        assert value[1]-value[0]<Q(1,10**40)
        ar.overlap(value,ar.box(row["K1"]))
        ar.overlap(ar.box(row["coarse_K1"]),value)
        H = ar.scale(ar.mul(pi,value),Q(8,N))
        ar.overlap(H,ar.box(row["H_N_mu1"]))
        assert H[0]>0
        if N==31: norm31=H
    assert norm31 and Q('462.9997152485')<norm31[0]<norm31[1]<Q('462.9997152486')
    # Eight distinct degree-one primes; only one was included in D93.
    fp = [2,0,-16,0,20,0,-8,0,1]
    roots = [x for x in range(31) if sum(c*x**j for j,c in enumerate(fp))%31==0]
    assert len(roots)==8
    assert all(sum(j*c*x**(j-1) for j,c in enumerate(fp) if j)%31 for x in roots)
    weight = ar.scale(ar.radical(Q(31)**71,64),28)
    floor = ar.divide(ar.mul(weight,norm31),maximum)
    lower0 = ar.divide(ar.scale(norm31,28*31),maximum)
    partial = ar.box(packet["saved_partial"])
    ratio = ar.divide(floor,partial)
    ar.overlap(floor,ar.box(packet["comparison_method_floor_from_norm31"]))
    ar.overlap(lower0,ar.box(packet["comparison_method_floor_with_exponent_zero"]))
    assert floor[0]>Q('460891.49') and lower0[0]>Q('316578.20')
    assert ratio[0]>Q('60.32') and lower0[0]>41*partial[1]
    assert ar.box(packet["saved_two_family_error"])[0]>partial[1]
    return {"independent_rational_quadrature_error_bound":True,
            "independent_pi_and_radical_bounds":True,"global_h_p_mu1_maximum_identity":True,
            "norm31_primes":roots,"omitted_primes":7,
            "method_floor_lower":str(floor[0]),"method_floor_with_delta_zero_lower":str(lower0[0]),
            "method_floor_over_partial_lower":str(ratio[0]),
            "scope":"Uniform per-ideal h_p comparison, or positive mixtures, with absolute Hecke envelopes and the unsigned geometric diagonal bound. Not the actual remainder."}


def dyadic_replay(packet):
    fp = list(map(Q,packet["F_polynomial_ascending"]))
    mp = list(map(Q,packet["CM_polynomial_ascending"]))
    out = [Q(0)]
    for c in reversed(fp):
        out = padd(pmul(out,[-2,0,-1]),[c])
    while out[-1]==0:out.pop()
    assert out==mp
    for p in [fp,mp]:
        assert p[-1]==1 and p[0]%4==2 and all(c%2==0 for c in p[:-1])
    assert len(fp)==9 and len(mp)==17
    # Formal coordinate transformation, independently multiplying finite series.
    # Factoring beta^(k+1) leaves 2^k*w^k*(1-w)^(-k-2).
    geometric = [Q(1)]*8
    for k in range(6):
        series = [Q(1)]
        for _ in range(k+2):series=pmul(series,geometric)[:8]
        for j in range(3):
            power=2*j+1-k
            coefficient=0 if power<0 else 2**k*series[power]
            assert coefficient==(0 if power<0 else 2**k*comb(2*j+2,k+1))
    # For each Taylor order the omitted chart exponents are
    # E0=(J-k)/2-d, E1=J+1-d, Einf=3J/2-k/2+1-d.
    # Differences E1-E0=(J+k)/2+1 and Einf-E0=J+1 are nonnegative.
    controls=packet["synthetic_measure_controls"]
    for row in controls:
        J,d,P=[row[k] for k in ["highest_moment_index","measure_denominator_exponent","input_moment_absolute_precision"]]
        assert J>=5
        for k in range(6):
            e0,e1,ei=Q(J-k,2)-d,Q(J+1-d),Q(3*J-k,2)+1-d
            assert e1-e0==Q(J+k,2)+1 and ei-e0==J+1
            local=min(e0,P-Q(k+1,2))
            coefficient=Q(1+17*k,2)
            assert e0+coefficient==Q(J+1,2)-d+8*k
            assert P-Q(k+1,2)+coefficient==P+8*k
            assert Q(row["Taylor_tail_valuations"][k])>=e0
            assert Q(row["Taylor_with_moment_error_valuations"][k])>=local
        bound=min(Q(J+1,2)-d,P)
        assert Q(row["proved_coarse_lower_bound"])==bound
        assert all(Q(v)>=bound for v in row["coarse_coefficient_error_valuations"])
        assert row["wrong_infinity_sign_detected_at_requested_precision"]==(J==31)
        assert row["omitted_infinity_chart_rejected"]
    assert not packet["actual_Shimura_jet_evaluated"] and not packet["actual_moments_computed"]
    return {"Eisenstein_and_field_relation_checks":True,"ramification_index_F_at_2":8,
            "ramification_index_CM_at_2":16,"coarse_coordinate_identity_checked":True,
            "three_chart_tail_exponents_replayed":True,"synthetic_controls":len(controls),
            "coarse_error_bound":"min((J+1)/2-d,P)",
            "sign_flip_requires_sufficient_dyadic_precision":True,
            "actual_measure_moments_supplied":False}


def computations():
    spectral=json.loads((DATA/"nelson_discrete_multiplier_d108.json").read_text())
    dyadic=json.loads((DATA/"dyadic_poisson_jet_interface_d108.json").read_text())
    return {"spectral":spectral_replay(spectral),"dyadic":dyadic_replay(dyadic)}


def build():
    result=computations()
    paths=[Path(__file__),ROOT/"dembele/pari/367_nelson_signed_orbit_audit.py"]
    prior_path=DATA/"cm_root_matching_review_d107.json"
    prior=json.loads(prior_path.read_text())
    assert prior["status"]=="pass" and len(prior["sources"])==588
    paths+=checked(prior["sources"])+[prior_path]
    for name in ["nelson_discrete_multiplier_d108.json","dyadic_poisson_jet_interface_d108.json"]:
        p=DATA/name;record=json.loads(p.read_text());paths+=checked(record["sources"])+[p]
    for stem in ["nelson_discrete_multiplier_d108_attempt01","dyadic_poisson_jet_interface_d108_attempt02"]:
        p=DATA/(stem+".job.json");job=json.loads(p.read_text())
        assert job["status"]=="pass" and job["timeout_seconds"]==180 and job["wall_seconds"]<180
        assert job["timeout_terminates_process_group"]
        paths+=checked(job["sources"]+[job["driver"],job["log"]])+[p]
    p=DATA/"dyadic_poisson_jet_interface_d108_attempt01.job.json"
    failed=json.loads(p.read_text());snapshot=DATA/"dyadic_poisson_jet_interface_d108_attempt01_failed.py"
    assert failed["status"]=="failed" and source(snapshot)["sha256"]==failed["driver"]["sha256"]
    paths+=checked(failed["sources"]+[failed["log"]])+[p,snapshot,DATA/"dyadic_poisson_jet_interface_d108_failure.json"]
    probe=DATA/"shimura_evaluator_review_d108_probe_attempt01.job.json"
    if probe.exists():
        job=json.loads(probe.read_text());assert job["status"]=="pass"
        paths+=checked(job["sources"]+[job["driver"],job["log"]])+[probe]
    paths+=[REPORT,DATA/"shimura_evaluator_sources_d108.json",
            Path("/Users/musty/hilbertmodularforms/ModFrmHil/definite.m")]
    return {"status":"pass","milestone":"D108","certificates":result,
            "D107_source_hashes_checked_unchanged":588,
            "completed_per_ideal_absolute_comparison_rejected":True,
            "full_spectrum_upper_bound_constructed":False,
            "dyadic_moment_to_coarse_jet_interface_proved_conditionally":True,
            "actual_Shimura_tangent_or_jet_evaluated":False,"actual_dyadic_CM_matching_proved":False,
            "candidate_identification_proved":False,"target_field_polynomial_constructed":False,
            "sources":[source(p) for p in sorted(set(p.resolve() for p in paths))],
            "scope":"Rational replay and provenance; the proof establishes the analytic implications. No actual moments or new harmonic cocycles. Transcendental centers and exact CM-field controls are bound, not independently recomputed."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument("--check",action="store_true");group.add_argument("--probe",action="store_true")
    args=parser.parse_args()
    if args.probe:
        result=computations();print(json.dumps(result,indent=2),flush=True)
        print("PASS|D108_EVALUATOR_PROBE",flush=True);return
    if args.check:
        old=json.loads(OUT.read_text());checked(old["sources"])
    result=build()
    if args.check:assert result==old
    else:
        assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","source_hashes":len(result["sources"]),
                      "D107_hashes_unchanged":588,"actual_Shimura_jet_evaluated":False}),flush=True)
    print("PASS|D108_EVALUATOR_REVIEW",flush=True)


if __name__=="__main__":main()

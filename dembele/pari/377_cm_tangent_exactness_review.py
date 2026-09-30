"""Bind D101 and replay candidate arithmetic plus elementary exactness controls."""
import argparse
from fractions import Fraction
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"dembele/data/computed"
OUT=DATA/"cm_tangent_exactness_review_d101.json"
SPEC=importlib.util.spec_from_file_location("d101_tangent",ROOT/"dembele/pari/376_cm_tangent_exactness.py")
T=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(T)


def build():
    candidate=T.load(T.OUTPUT)
    for item in candidate["sources"]:
        assert T.source(item["path"])==item,item["path"]
    assert T.audit(candidate["job"])==candidate
    receipt=T.load(DATA/"cm_tangent_exactness_d101_recheck.job.json")
    assert receipt["status"]=="pass" and receipt["timeout_seconds"]==180
    for item in receipt["sources"]+[receipt["driver"],receipt["log"]]:
        assert T.source(item["path"])==item,item["path"]
    f=[2,0,-16,0,20,0,-8,0,1]
    e=T.compose(f,[-2,0,-1])
    assert e==[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]
    assert all(poly[-1]==1 and poly[0]%4==2 and all(c%2==0 for c in poly[:-1]) for poly in [f,e])
    counterexamples=[]
    for degree in [17,136]:
        for n in [32,256,1024]:
            delta=Fraction(1,2**n)
            assert delta>0 and delta<Fraction(1,2**(n-1))
            assert delta.denominator==2**n
            assert (2**n*delta)**degree==1
            counterexamples.append({"degree":degree,"n":n,"nonzero":True,
                                    "norm_power_of_two":-n*degree,
                                    "cleared_norm":1,"strict_threshold_rejects":True})
    g=16
    assert g*(g-1)//2==120 and 5*g-5==75 and 3*(2*g-2)==90
    paths=[Path(__file__),ROOT/"dembele/certificates/cm-tangent-exactness-d101.md",
           DATA/"cm_tangent_exactness_sources_d101.json",T.OUTPUT,
           DATA/"cm_tangent_candidate_height_d101_attempt01.job.json",
           DATA/"cm_tangent_exactness_d101_recheck.job.json",
           Path(receipt["log"]["path"]),Path(candidate["job"]["log"]["path"])]
    paths += [Path(item["path"]) for item in candidate["sources"]]
    paths += [Path(item["path"]) for item in candidate["job"]["sources"]]
    manifest=[T.source(p) for p in sorted(set(p.resolve() for p in paths))]
    return {"status":"pass","milestone":"D101","sources":manifest,
            "candidate_replay":"pass","S_unit_counterexamples":counterexamples,
            "relative_CM_ramification_at_2":True,"ramification_reason":"Both absolute polynomials are 2-Eisenstein; degrees 8 and 16.",
            "Yuan_Theorem_1_2_no_common_ramification_hypothesis_satisfied":False,
            "Zhao_Theorem_1_1_finite_ramification_pattern_satisfied":True,
            "Zhao_full_application_instantiated":False,
            "Gaussian_dimensions":{"domain":120,"target":75,"degree":90},
            "actual_arithmetic_clearing_bound_proved":False,
            "independent_Shimura_tangent_obtained":False,
            "spectral_pilot_gate_passed":False,
            "scope":"Elementary proofs and candidate computations; no arithmetic identification or effective target height bound."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    if args.check:
        old=T.load(OUT)
        for item in old["sources"]:
            assert T.source(item["path"])==item,item["path"]
    result=build()
    if args.check:
        assert result==old
    else:
        assert not OUT.exists(),"Preserve the completed audit."
        OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","source_hashes":len(result["sources"]),
                      "candidate_replay":"pass","arithmetic_identification":False}),flush=True)


if __name__=="__main__":
    main()

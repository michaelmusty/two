"""Final D91 manifest, adding derivative calibration and a unit cutoff.

The independent rational checks in 334 are replayed. Arb nodes and the
unit logarithm/vertex enclosures are hash-bound to their bounded runs.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

spec=importlib.util.spec_from_file_location("unfolding_audit",Path(__file__).with_name("334_nelson_unfolding_audit.py"))
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
DATA=audit.DATA;ROOT=audit.ROOT


def compute():
    result=audit.compute()
    previous=DATA/"nelson_unfolding_d91.json"
    assert result==json.loads(previous.read_text())
    sources={s["path"]:s for s in result["sources"]}
    def bind(p,expected=None):
        p=Path(p);p=p if p.is_absolute() else ROOT/p
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        if expected is not None:assert h==expected,p
        relative=str(p.relative_to(ROOT));sources[relative]={"path":relative,"sha256":h}
    bind(Path(__file__));bind(previous)
    for name,stem in [("nelson_derivative_calibration_d91.json","derivative"),("nelson_unit_cutoff_d91.json","unit_cutoff")]:
        p=DATA/name;packet=json.loads(p.read_text());bind(p)
        for src in packet["sources"]:bind(src["path"],src["sha256"])
        job_path=DATA/f"nelson_{stem}_d91_attempt01.job.json";job=json.loads(job_path.read_text());bind(job_path)
        bind(job["log"]["path"],job["log"]["sha256"])
        for src in job["sources"]:bind(src["path"],src["sha256"])
        assert job["status"]=="pass" and job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
        result["jobs"].append({"path":str(job_path.relative_to(ROOT)),"status":job["status"],"wall_seconds":job["wall_seconds"]})
        if stem=="derivative":
            assert packet["arxiv_v1_display_11_scale_discrepancy"]
            assert not packet["published_2015_display_checked"]
            assert all(Fraction(t["Mellin_relative_error"])<Fraction(1,10**40) for t in packet["tests"])
            result["derivative_calibration"]={"points":3,"relative_error_bound":"1e-40",
                "arxiv_v1_scale_discrepancy_recorded":True,"published_2015_formula_checked":False}
        else:
            assert packet["unit_rank_certified"]==7 and packet["C"]==2126
            assert not packet["complete_cutoff_enumerated"]
            for option in packet["alternatives"]:
                T=option["unit_exponent_change"]
                assert abs(audit.mat.determinant(T))==1
                for coeffs in option["units_power_coordinates"]:
                    u=tuple(Fraction(c) for c in coeffs)
                    assert audit.integral(u) and audit.integral(audit.finverse(u)) and abs(audit.fnorm(u))==1
            assert next(v for v in packet["cost_diagnostics"] if v["invariant_A_bound"]==359)["sufficient_Q_bound"]==333
            result["unit_cutoff"]={"unit_rank":7,"cover_constant":2126,
                "A_359_sufficient_Q_bound":333,"complete_cutoff_enumerated":False,
                "scope":"rational unit arithmetic replayed; logarithm and vertex balls bound to Sage run"}
    result["sources"]=sorted(sources.values(),key=lambda s:s["path"])
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--check",action="store_true");args=p.parse_args()
    result=compute();out=DATA/"nelson_hilbert_d91.json"
    if args.check:assert result==json.loads(out.read_text())
    else:
        assert not out.exists();out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: D91 cusp/unit identities, 29 primitive classes, 42 interval kernels, derivative calibration and cutoff;",len(result["sources"]),"hashes")


if __name__=="__main__":main()

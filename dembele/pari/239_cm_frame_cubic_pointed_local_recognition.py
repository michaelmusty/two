"""Apply the held-out-digit Q/F recognition pilot to normalized local coefficients."""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


prior = module("local_recognition_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
checks = prior.checks


def worker(n):
    from sage.all import GF, ZZ, PolynomialRing
    rec = module("local_recognition_methods", ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py")
    path = DATA / f"cm_frame_cubic_pointed_{n}_local_invariants.json"
    controls = DATA / f"cm_frame_cubic_pointed_{n}_recognition.json"
    record = json.loads(path.read_text()); checks.verify_records(record)
    checks.verify_records(json.loads(controls.read_text()))
    train, valid = n//2, n
    U = PolynomialRing(ZZ, "t"); f = U([2, 0, -16, 0, 20, 0, -8, 0, 1])
    roots = [(int(x), rec.hensel_root(f, int(x), valid)) for x, m in f.change_ring(GF(31)).roots() if m == 1]
    values = dict(zip(("alpha", "beta", "gamma", "delta"), record["data"]["normalized_coefficients"]))
    values.update({f"a_local_{j+81}": v for j, v in enumerate(record["data"]["a_coefficients"])})
    results = []
    for label, value in values.items():
        rational = rec.rational_candidate(value, train, valid)
        fields = [{"root_mod31": initial, "candidates": rec.field_candidates(value, root, train, valid)} for initial, root in roots]
        results.append({"label": label, "rational_candidate": rational, "field_candidates": fields})
    rq = [r["label"] for r in results if r["rational_candidate"] and r["rational_candidate"]["validates_unused_digits"]]
    rf = [r["label"] for r in results if any(c["validates_unused_digits"] for row in r["field_candidates"] for c in row["candidates"])]
    report = {"status": "pass", "sources": [checks.source(p) for p in (Path(__file__), Path(rec.__file__), path, controls)],
              "precision_digits": n, "training_digits": train, "validation_digits": valid-train,
              "results": results, "rational_survivors": rq, "field_survivors": rf,
              "exact_recognition_certified": False, "coefficient_field_excluded": False}
    (DATA / f"cm_frame_cubic_pointed_{n}_local_recognition.json").write_text(json.dumps(report, indent=2)+"\n")
    print("LOCAL_RECOGNITION", n, "Q", rq, "F", rf, flush=True)
    print("PASS|239_CM_FRAME_CUBIC_POINTED_LOCAL_RECOGNITION", n, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(8, 16, 32), required=True)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.worker: worker(args.digits); return
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    base = DATA / f"cm_frame_cubic_pointed_{args.digits}_local_recognition"
    job = prior.jobs.run_job([prior.jobs.SAGE, "-python", str(Path(__file__)), "--digits", str(args.digits), "--worker"],
        base.with_suffix(".out"), 180, "PASS|239_CM_FRAME_CUBIC_POINTED_LOCAL_RECOGNITION", env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"] = [checks.source(Path(__file__)), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = Path(str(base)+"_job.json"); jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"local recognition: {job['status']}")
    report = json.loads(base.with_suffix(".json").read_text()); report["sources"].append(checks.source(jpath))
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n"); checks.verify_records(report)
    print("PASS|239_CM_FRAME_CUBIC_POINTED_LOCAL_RECOGNITION_JOB", args.digits, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()

# D86 precision adapter of 271; original SHA256 1d3836ab18a554bef23970ce5c592aac873a1782dd9e656defc009f5939c011f
"""D86: exact height exclusion using the integral scaled inverse of a lattice basis.

For D=31^train and K=D*B^-1 integral, put S=max_j sum_i |K_ij|.
If v=z*B has coefficient height H, then D*|z_j| <= H*S. Thus H*S<D
forces z=0. The saved integer matrix identity B*K=D*I certifies the bound.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("dual_height_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks
spec = importlib.util.spec_from_file_location("dual_height128_jobs", ROOT / "dembele/pari/272_cm_frame_bounded_jobs.py")
jobs = importlib.util.module_from_spec(spec); spec.loader.exec_module(jobs)


def worker(train, index):
    from sage.all import QQ, ZZ, identity_matrix, matrix
    source = DATA / f"cm_frame_cubic_adjoint_joint_128_{train}_{index}.json"
    record = json.loads(source.read_text()); checks.verify_records(record)
    assert record["result"]["determinant_verified"]
    B = matrix(ZZ, record["result"]["rows"]); assert B.nrows() == B.ncols() == 200
    D = ZZ(31)**train
    K = (D*B.change_ring(QQ).inverse()).change_ring(ZZ)
    assert B*K == D*identity_matrix(ZZ, 200)
    sums = [sum(abs(x) for x in K.column(j)) for j in range(200)]
    S = max(sums); H = (D-1)//S
    assert H*S < D <= (H+1)*S
    report = {"status": "pass", "milestone": "D86", "date": "2026-09-23",
        "sources": [checks.source(p) for p in (Path(__file__), source)],
        "precision_digits": 128, "training_digits": train, "root_mod31": record["root_mod31"],
        "lattice_rank": 200, "scaled_inverse_rows": [[int(x) for x in row] for row in K],
        "scale": int(D), "column_absolute_sums": [int(x) for x in sums],
        "maximum_column_absolute_sum": int(S), "integer_matrix_identity_verified": True,
        "excluded_integral_coefficient_height_through": int(H),
        "scope": "All nonzero integral homogeneous representatives in the 25 fixed A2 coordinates and the degree-eight power basis of F, including arbitrary common F-valued scaling.",
        "coefficient_field_excluded": False, "exact_curve_equation_certified": False,
        "proof": "dembele/certificates/cm-frame-cubic-128-chatelet.md"}
    base = DATA / f"cm_frame_cubic_adjoint_dual_height_128_{train}_{index}"
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|301_DUAL_RECOGNITION_HEIGHT", train, index, "excluded height <=", H, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", type=int, default=112)
    parser.add_argument("--root-index", type=int, choices=range(8), default=0)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.worker: worker(args.train, args.root_index); return
    base = DATA / f"cm_frame_cubic_adjoint_dual_height_128_{args.train}_{args.root_index}"
    result_path, job_path = base.with_suffix(".json"), Path(str(base)+"_job.json")
    if result_path.exists() or job_path.exists():
        assert result_path.exists() and job_path.exists(), "Preserve incomplete attempts"
        checks.read_job(job_path, "PASS|301_DUAL_RECOGNITION_HEIGHT")
        checks.verify_records(json.loads(result_path.read_text()))
        print("PASS|301_EXISTING_HEIGHT_BOUND", args.root_index, flush=True); return
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    job = jobs.run_job([jobs.SAGE, "-python", str(Path(__file__)), "--train", str(args.train),
        "--root-index", str(args.root_index), "--worker"], base.with_suffix(".out"), 180,
        "PASS|301_DUAL_RECOGNITION_HEIGHT", env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"] += [checks.source(Path(__file__)), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = Path(str(base)+"_job.json"); jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"dual height bound: {job['status']}")
    report = json.loads(base.with_suffix(".json").read_text()); report["sources"].append(checks.source(jpath))
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n"); checks.verify_records(report)
    print("PASS|301_DUAL_RECOGNITION_HEIGHT_JOB", args.root_index, round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

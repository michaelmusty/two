"""Exact coefficient-height exclusion from a saved joint-recognition lattice.

For an integral row v=z*B, let k be the last nonzero coefficient of z.
Projection orthogonal to the first k-1 rows has length |z_k|*|b_k^*|.
Thus ||v||_2^2 >= min |b_i^*|^2. Since there are 200 coefficients,
200*H^2 below this minimum excludes every nonzero row of height <= H.
This is a bound in the specified power/coefficient bases, not a field exclusion.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("recognition_height_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def worker(train, index):
    from sage.all import QQ, ZZ, matrix
    path = DATA / f"cm_frame_cubic_adjoint_joint_64_{train}_{index}.json"
    record = json.loads(path.read_text()); checks.verify_records(record)
    assert record["result"]["determinant_verified"]
    B = matrix(QQ, record["result"]["rows"])
    assert B.nrows() == B.ncols() == 200
    G, M = B.gram_schmidt(orthonormal=False)
    assert M*G == B and all(M[i,i] == 1 for i in range(200))
    assert all(M[i,j] == 0 for i in range(200) for j in range(i+1,200))
    diagonal = G*G.transpose()
    assert diagonal.is_diagonal()
    norms = diagonal.diagonal(); assert all(x > 0 for x in norms)
    least = min(norms)
    H = ZZ(least.numerator()//(200*least.denominator())).isqrt()
    if 200*H**2 >= least: H -= 1
    assert 200*H**2 < least <= 200*(H+1)**2
    assert all(max(abs(x) for x in row) > H for row in B)
    report = {"status": "pass", "milestone": "D83", "date": "2026-09-22",
        "sources": [checks.source(p) for p in (Path(__file__), path)],
        "precision_digits": 64, "training_digits": train, "root_mod31": record["root_mod31"],
        "lattice_rank": 200, "exact_orthogonalization_verified": True,
        "minimum_squared_orthogonal_length": [int(least.numerator()), int(least.denominator())],
        "excluded_integral_coefficient_height_through": int(H),
        "scope": "All nonzero integral homogeneous representatives in the 25 fixed A2 coordinates and the degree-eight power basis of F, including arbitrary common F-valued scaling.",
        "coefficient_field_excluded": False, "exact_curve_equation_certified": False,
        "proof": "dembele/certificates/cm-frame-cubic-64.md",
        "api_reference": "https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.gram_schmidt"}
    base = DATA / f"cm_frame_cubic_adjoint_height_64_{train}_{index}"
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|270_RECOGNITION_HEIGHT", train, index, "excluded height <=", H, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", type=int, default=48)
    parser.add_argument("--root-index", type=int, choices=range(8), default=0)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.worker: worker(args.train, args.root_index); return
    base = DATA / f"cm_frame_cubic_adjoint_height_64_{args.train}_{args.root_index}"
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    job = prior.jobs.run_job([prior.jobs.SAGE, "-python", str(Path(__file__)), "--train", str(args.train),
        "--root-index", str(args.root_index), "--worker"], base.with_suffix(".out"), 180,
        "PASS|270_RECOGNITION_HEIGHT", env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"] = [checks.source(Path(__file__)), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = Path(str(base)+"_job.json"); jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"height bound: {job['status']}")
    report = json.loads(base.with_suffix(".json").read_text()); report["sources"].append(checks.source(jpath))
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n"); checks.verify_records(report)
    print("PASS|270_RECOGNITION_HEIGHT_JOB", args.root_index, round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

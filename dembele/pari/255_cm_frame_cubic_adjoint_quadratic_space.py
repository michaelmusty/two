"""Saturate and reduce the exactly certified rational quadratic coefficient space."""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("adjoint_quadratic_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks
BASE = DATA / "cm_frame_cubic_adjoint_quadratic_space"


def worker():
    from sage.all import GF, QQ, ZZ, matrix, vector
    jpath = Path(str(BASE)+"_job.json")
    job = checks.read_job(jpath, "PASS|254_CM_FRAME_CUBIC_ADJOINT_QUADRATIC_SPACE")
    output = Path(job["log"]["path"]).read_text()
    rows = prior.helpers.field(output, "ADJOINT_QUADRATIC_SPACE_INTEGER_ROWS")
    weights = prior.helpers.field(output, "ADJOINT_QUADRATIC_SPACE_LEADING_WEIGHTS")
    B = matrix(ZZ, rows); assert B.rank() == 25 and B.ncols() == 45
    C = B.saturation().LLL()
    assert C.change_ring(QQ).row_space() == B.change_ring(QQ).row_space()
    assert C.change_ring(GF(31)).rank() == 25
    pivots = list(C.change_ring(GF(31)).pivots()); assert len(pivots) == 25
    det = C.matrix_from_columns(pivots).det(); assert det % 31 != 0
    lead = C*vector(QQ, [QQ(a)/b for a, b in weights])
    data = {"integer_basis_rows": [[int(x) for x in row] for row in C.rows()],
            "leading_weights": weights,
            "basis_leading_weights": [[int(x.numerator()), int(x.denominator())] for x in lead],
            "unit_pivot_indices_zero_based": pivots}
    report = {"status": "pass", "sources": [checks.source(p) for p in (Path(__file__), jpath)],
              "data": data, "space": "H0(2*K_C-D17-3*P32)", "dimension": 25,
              "exact_rational_space_certified": True, "saturated_integer_lattice": True,
              "unit_pivot_minor_at_31": True,
              "maximum_basis_coefficient": max(abs(int(x)) for x in C.list()),
              "maximum_basis_height_digits": len(str(max(abs(int(x)) for x in C.list())))}
    BASE.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("ADJOINT_QUADRATIC_BASIS_HEIGHT_DIGITS", report["maximum_basis_height_digits"], flush=True)
    print("PASS|255_CM_FRAME_CUBIC_ADJOINT_QUADRATIC_SPACE", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.worker: worker(); return
    # The Magma certificate can be resumed without repeating the exact calculation.
    script = ROOT / "dembele/magma/254_cm_frame_cubic_adjoint_quadratic_space.m"
    prior.run(script, BASE, "PASS|254_CM_FRAME_CUBIC_ADJOINT_QUADRATIC_SPACE",
        [DATA / "cm_frame_cubic_adjoint_1_check.json"], "", False)
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    logbase = DATA / "cm_frame_cubic_adjoint_quadratic_basis"
    job = prior.jobs.run_job([prior.jobs.SAGE, "-python", str(Path(__file__)), "--worker"],
        logbase.with_suffix(".out"), 180, "PASS|255_CM_FRAME_CUBIC_ADJOINT_QUADRATIC_SPACE", env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"] = [checks.source(Path(__file__)), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = Path(str(logbase)+"_job.json"); jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"quadratic basis: {job['status']}")
    report = json.loads(BASE.with_suffix(".json").read_text()); report["sources"].append(checks.source(jpath))
    BASE.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n"); checks.verify_records(report)
    print("PASS|255_CM_FRAME_CUBIC_ADJOINT_QUADRATIC_SPACE_JOB", round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()

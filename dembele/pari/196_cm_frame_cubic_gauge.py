"""Fix an algebraic representative gauge that preserves the D81 lift."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("gauge_prior", ROOT / "dembele/pari/189_cm_frame_cubic_lift_third.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, jobs, checks = prior.helpers, prior.jobs, prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    old = DATA / "cm_frame_cubic_lift_check.json"
    checks.verify_records(json.loads(old.read_text()))
    script = ROOT / "dembele/magma/195_cm_frame_cubic_gauge.m"
    job_path = DATA / "cm_frame_cubic_gauge_job.json"
    if not args.collect_only:
        job = jobs.run_job(jobs.magma_command(script), DATA / "cm_frame_cubic_gauge.out", 180,
                           "PASS|195_CM_FRAME_CUBIC_GAUGE")
        job["sources"] = [checks.source(p) for p in (Path(__file__), script, old,
            ROOT / "dembele/magma/186_cm_frame_cubic_lift_arithmetic.m",
            ROOT / "dembele/magma/187_cm_frame_cubic_lift_model.m",
            ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
        job_path.write_text(json.dumps(job, indent=2)+"\n")
        if job["status"] != "pass":
            raise RuntimeError(f"gauge calculation: {job['status']}")
    job = checks.read_job(job_path, "PASS|195_CM_FRAME_CUBIC_GAUGE")
    output = Path(job["log"]["path"]).read_text()
    names = ("pin_indices", "pin_values", "divisor_pivots", "jacobian_mod31",
             "jacobian_determinant_mod31", "q_free_indices", "q_free_values", "u_pivot", "f_pivot")
    data = {key: helpers.field(output, "GAUGE_"+key.upper()) for key in names}
    assert len(data["pin_indices"]) == len(data["pin_values"]) == 80
    assert data["jacobian_determinant_mod31"] % 31 != 0
    mpath = DATA / "cm_frame_cubic_gauge.m"
    mpath.write_text("// D82 fixed algebraic normalization conditions, independent of precision.\n"+
        "\n".join(f"gauge_{key} := {helpers.magma(value)};" for key, value in data.items())+"\n")
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), job_path, old)],
              "magma_artifact": checks.source(mpath), "data": data,
              "representative_parameters": 80, "unit_derivative_minor_verified": True,
              "equivalent_representative_control_passed": True, "preserves_D81_mod961": True,
              "higher_precision_computed": False}
    (DATA / "cm_frame_cubic_gauge.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|196_CM_FRAME_CUBIC_GAUGE")


if __name__ == "__main__":
    main()

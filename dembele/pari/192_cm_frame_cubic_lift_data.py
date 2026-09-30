"""Construct and collect the normalized cubic modulo 31^2."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("lift_cubic_third", ROOT / "dembele/pari/189_cm_frame_cubic_lift_third.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, jobs, checks = prior.helpers, prior.jobs, prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    third_path = DATA / "cm_frame_cubic_lift_third.json"
    third = json.loads(third_path.read_text()); checks.verify_records(third)
    job_path = DATA / "cm_frame_cubic_lift_function_job.json"
    script = ROOT / "dembele/magma/191_cm_frame_cubic_lift_function.m"
    if not args.collect_only:
        job = jobs.run_job(jobs.magma_command(script), DATA / "cm_frame_cubic_lift_function.out",
                           180, "PASS|191_CM_FRAME_CUBIC_LIFT_FUNCTION")
        job["sources"] = [checks.source(p) for p in (Path(__file__), script, third_path,
            DATA / "cm_frame_cubic_lift_sections.json", DATA / "cm_frame_cubic_check.json",
            ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m",
            ROOT / "dembele/magma/186_cm_frame_cubic_lift_arithmetic.m",
            ROOT / "dembele/magma/187_cm_frame_cubic_lift_model.m",
            ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
        job_path.write_text(json.dumps(job, indent=2)+"\n")
        if job["status"] != "pass":
            raise RuntimeError(f"cubic lift function construction: {job['status']}")
    job = checks.read_job(job_path, "PASS|191_CM_FRAME_CUBIC_LIFT_FUNCTION")
    output = Path(job["log"]["path"]).read_text()
    names = ("descended_divisor_coordinates", "moving_coefficients", "q_coefficients", "u_coefficients",
             "f_coefficients", "norm_scalar", "a_coefficients", "denominator_coefficients",
             "trace_numerator_coefficients")
    data = {key: helpers.field(output, "LIFT_"+key.upper()) for key in names}
    old = json.loads((DATA / "cm_frame_cubic.json").read_text())["data"]
    for key in names:
        if key in ("descended_divisor_coordinates", "moving_coefficients"):
            continue
        oldkey = ("cubic_" if key in names[-3:] else "kummer_")+key
        if key == "norm_scalar":
            assert data[key] % 31 == old[oldkey]
        else:
            assert [c % 31 for c in data[key]] == old[oldkey]
            assert all(0 <= c < 961 for c in data[key])
    mpath = DATA / "cm_frame_cubic_lift.m"
    mpath.write_text("// D81 normalized cubic modulo 31^2, in the D79 gauge.\n"+
        "\n".join(f"cubic961_{key} := {helpers.magma(value)};" for key, value in data.items())+"\n")
    report = {"status": "pass", "milestone": "D81", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), job_path, DATA / "cm_frame_cubic.json")],
              "magma_artifact": checks.source(mpath), "data": data, "modulus": 961,
              "precision_digits": 2, "coefficientwise_reduction_verified": True,
              "weighted_equation": "Q4*T^3-3*A4*Q4*T-P10=0, weight(T)=2",
              "kummer_function_constructed": True, "cubic_lift_computed": True,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False}
    (DATA / "cm_frame_cubic_lift.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|192_CM_FRAME_CUBIC_LIFT_DATA")


if __name__ == "__main__":
    main()

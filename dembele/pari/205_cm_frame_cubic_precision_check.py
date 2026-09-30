"""Independently verify a normalized higher-precision cubic and digit controls."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("precision_check_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, jobs, checks = prior.helpers, prior.jobs, prior.checks


def run(script, base, marker, inputs, wrapper_text, expected_failure=None):
    wrapper = Path(str(base)+"_run.m")
    wrapper.write_text("SetQuitOnError(true);\n"+wrapper_text+prior.loadline(script))
    job = jobs.run_job(jobs.magma_command(wrapper), base.with_suffix(".out"), 180,
                       marker, expected_failure=expected_failure)
    job["sources"] = [checks.source(p) for p in [Path(__file__), script, wrapper,
        ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"]+inputs]
    Path(str(base)+"_job.json").write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass":
        raise RuntimeError(f"{base.name}: {job['status']}")
    return job


def check_section_reduction(n):
    current = json.loads(prior.stem(n, "_sections").with_suffix(".json").read_text())["data"]
    previous = json.loads(prior.previous_sections(n).with_suffix(".json").read_text())["data"]
    modulus = 31**(n//2)
    def reduce(value):
        return [reduce(x) for x in value] if isinstance(value, list) else value % modulus
    for key in ("odd_section_rows", "point_coordinates", "branch_plus_values", "branch_minus_values"):
        assert reduce(current[key]) == previous[key]
    assert current["point_indices"] == previous["point_indices"]
    assert len(current["odd_support_components"]) == len(previous["odd_support_components"])
    for a, b in zip(current["odd_support_components"], previous["odd_support_components"]):
        assert a[:2] == b[:2] and a[3] == b[3] and reduce(a[2]) == b[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args(); n = args.digits
    result = prior.stem(n, "_check").with_suffix(".json")
    if args.collect_only:
        report = json.loads(result.read_text()); checks.verify_records(report)
        assert report["independent_verification_completed"] and report["persistent_gauge_verified"]
        print("PASS|205_CM_FRAME_CUBIC_PRECISION_CHECK_PROVENANCE", n)
        return
    data_paths = [prior.stem(n).with_suffix(".json"), prior.stem(n, "_sections").with_suffix(".json"),
                  prior.stem(n, "_third").with_suffix(".json"), DATA / "cm_frame_cubic_gauge.json"]
    prev_path = prior.previous_cubic(n).with_suffix(".json")
    previous_root = DATA / "cm_frame_cubic_lift_check.json" if n == 4 else prior.stem(n//2, "_check").with_suffix(".json")
    for path in [*data_paths, prev_path, previous_root]:
        checks.verify_records(json.loads(path.read_text()))
    check_section_reduction(n)
    previous = json.loads(prev_path.read_text())["data"].copy()
    previous["modulus"] = 31**(n//2)
    wrapper = f"precision_digits := {n};\n"+prior.loadline(prior.stem(n, "_sections").with_suffix(".m"))
    wrapper += prior.loadline(prior.stem(n, "_third").with_suffix(".m"))
    wrapper += prior.loadline(prior.stem(n).with_suffix(".m"))+prior.binding("previous_cubic_", previous)
    script = ROOT / "dembele/magma/204_cm_frame_cubic_precision_check.m"
    marker = "PASS|204_CM_FRAME_CUBIC_PRECISION_CHECK"
    inputs = prior.CORE+[ROOT / "dembele/magma/202_cm_frame_cubic_gauge_arithmetic.m",
                        ROOT / "dembele/pari/201_cm_frame_cubic_precision.py", previous_root, prev_path]+data_paths
    positive = run(script, prior.stem(n, "_check"), marker, inputs, wrapper)
    controls = {}
    for name, mutation, assertion in (
        ("norm", "precision_cubic_norm_scalar := (precision_cubic_norm_scalar+31^(precision_digits-1)) mod 31^precision_digits;", "assert norm_ok;"),
        ("trace", "precision_cubic_trace_numerator_coefficients[1] := (precision_cubic_trace_numerator_coefficients[1]+31^(precision_digits-1)) mod 31^precision_digits;", "assert trace_ok;"),
    ):
        controls[name] = run(script, prior.stem(n, f"_{name}_control"), marker,
                             inputs, wrapper+mutation+"\n", expected_failure=assertion)
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), previous_root, *data_paths,
                  Path(str(prior.stem(n, "_check"))+"_job.json"),
                  Path(str(prior.stem(n, "_norm_control"))+"_job.json"),
                  Path(str(prior.stem(n, "_trace_control"))+"_job.json")]],
              "precision_digits": n, "modulus": 31**n,
              "persistent_gauge_verified": True, "independent_verification_completed": True,
              "points_sections_branch_values_verified": True, "compatible_reduction_verified": True,
              "three_division_verified": True, "frobenius_descent_verified": True,
              "function_divisors_and_norm_verified": True, "cubic_coefficients_verified": True,
              "class_number_assumed": False, "reflection_quotient_genus": 64,
              "positive_check": positive, "highest_digit_norm_control": controls["norm"],
              "highest_digit_trace_control": controls["trace"],
              "characteristic_zero_cubic_constructed": False, "arithmetic_identification_certified": False,
              "target_field_constructed": False, "proof": "dembele/certificates/cm-frame-cubic-precision.md"}
    result.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|205_CM_FRAME_CUBIC_PRECISION_CHECK", n, "both highest-digit controls rejected")


if __name__ == "__main__":
    main()

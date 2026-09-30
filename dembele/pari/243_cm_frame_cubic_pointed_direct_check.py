"""Verify pointed cubics in separate bounded geometry, class and function jobs."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed_check_function", ROOT / "dembele/pari/241_cm_frame_cubic_pointed_direct_function.py")
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
spec = importlib.util.spec_from_file_location("pointed_check_runner", ROOT / "dembele/pari/205_cm_frame_cubic_precision_check.py")
runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
prior, checks, stem = build.prior, build.checks, build.stem


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(16, 32), required=True)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args(); n = args.digits
    result = stem(n, "_direct_check").with_suffix(".json")
    if args.collect_only:
        report = json.loads(result.read_text()); checks.verify_records(report)
        assert report["independent_verification_completed"]
        print("PASS|243_CM_FRAME_CUBIC_POINTED_DIRECT_CHECK_PROVENANCE", n)
        return
    paths, wrapper, previous = build.inputs_and_wrapper(n)
    cubic_path = stem(n, "_direct").with_suffix(".json")
    checks.verify_records(json.loads(cubic_path.read_text()))
    previous_root = DATA / "cm_frame_cubic_lift_check.json" if n == 1 else stem(n//2, "_check").with_suffix(".json")
    checks.verify_records(json.loads(previous_root.read_text()))
    wrapper += prior.loadline(stem(n, "_direct").with_suffix(".m"))
    inputs = prior.CORE+[Path(__file__), Path(build.__file__), Path(build.jets.__file__), previous_root, cubic_path]+paths
    positive = {}; positive_paths = []
    stages = (("geometry", "233_cm_frame_cubic_pointed_geometry_check", "233_CM_FRAME_CUBIC_POINTED_GEOMETRY_CHECK"),
              ("class", "234_cm_frame_cubic_pointed_class_check", "234_CM_FRAME_CUBIC_POINTED_CLASS_CHECK"),
              ("functions", "242_cm_frame_cubic_pointed_direct_function_check", "242_CM_FRAME_CUBIC_POINTED_DIRECT_FUNCTION_CHECK"))
    for label, filename, endmarker in stages:
        script = ROOT / ("dembele/magma/"+filename+".m"); marker = "PASS|"+endmarker
        base = stem(n, "_direct_"+label+"_check")
        positive[label] = runner.run(script, base, marker, inputs, wrapper)
        positive_paths.append(Path(str(base)+"_job.json"))
        print("POINTED_INDEPENDENT_STAGE_PASS", n, label, round(positive[label]["wall_seconds"], 3), flush=True)
    controls = {}
    for name, mutation, assertion in (
        ("norm", "pointed_cubic_norm_scalar := (pointed_cubic_norm_scalar+31^(precision_digits-1)) mod 31^precision_digits;", "assert norm_ok;"),
        ("septic", "pointed_cubic_trace_septic_coefficients[1] := (pointed_cubic_trace_septic_coefficients[1]+31^(precision_digits-1)) mod 31^precision_digits;", "assert septic_ok;"),
    ):
        controls[name] = runner.run(script, stem(n, f"_direct_{name}_control"), marker,
            inputs, wrapper+mutation+"\n", expected_failure=assertion)
        print("POINTED_DIGIT_CONTROL_REJECTED", n, name, round(controls[name]["wall_seconds"], 3), flush=True)
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), previous_root, cubic_path,
                  *positive_paths,
                  Path(str(stem(n, "_direct_norm_control"))+"_job.json"),
                  Path(str(stem(n, "_direct_septic_control"))+"_job.json")]],
              "precision_digits": n, "modulus": 31**n,
              "independent_verification_completed": True, "points_sections_branch_values_verified": True,
              "three_division_verified": True, "actual_pointed_divisor_verified": True,
              "pointed_condition_rank": 80, "function_divisors_and_norm_verified": True,
              "fixed_linear_denominator_verified": True, "leading_coefficients_verified": [1, 2],
              "compatible_reduction_verified": n > 1, "positive_check": positive,
              "highest_digit_norm_control": controls["norm"], "highest_digit_septic_control": controls["septic"],
              "characteristic_zero_cubic_constructed": False, "arithmetic_identification_certified": False,
              "target_field_constructed": False, "proof": "dembele/certificates/cm-frame-cubic-precision.md"}
    result.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|243_CM_FRAME_CUBIC_POINTED_DIRECT_CHECK", n, "both highest-digit controls rejected", flush=True)


if __name__ == "__main__":
    main()

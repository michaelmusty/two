"""D83: check pointed functions, reusing the separately certified exact class matrix."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


build = module("pointed64_check_build", "241_cm_frame_cubic_pointed_direct_function.py")
runner = module("pointed64_check_runner", "205_cm_frame_cubic_precision_check.py")
prior, checks, stem = build.prior, build.checks, build.stem


def main():
    n = 64
    paths, wrapper, previous = build.inputs_and_wrapper(n)
    cubic_path = stem(n, "_direct").with_suffix(".json")
    class_path = stem(n, "_newton_third").with_suffix(".json")
    previous_root = stem(32, "_check").with_suffix(".json")
    cubic, cls, prev = [json.loads(p.read_text()) for p in (cubic_path, class_path, previous_root)]
    for report in (cubic, cls, prev): checks.verify_records(report)
    assert cls["actual_divisor_verified"] and cls["three_division_verified"]
    assert cls["frobenius_fixed"] and cls["antiinvariant"]
    assert cubic["data"]["descended_divisor_coordinates"] == cls["data"]["coordinates"]
    wrapper += prior.loadline(stem(n, "_direct").with_suffix(".m"))
    inputs = prior.CORE+[Path(__file__), Path(build.__file__), Path(build.jets.__file__),
                         previous_root, cubic_path, class_path]+paths
    positive = {"class": {"verified_by": checks.source(class_path), "exact_matrix_equality_verified": True}}
    jobs = []
    for label, filename, marker in (
        ("geometry", "233_cm_frame_cubic_pointed_geometry_check.m", "PASS|233_CM_FRAME_CUBIC_POINTED_GEOMETRY_CHECK"),
        ("functions", "242_cm_frame_cubic_pointed_direct_function_check.m", "PASS|242_CM_FRAME_CUBIC_POINTED_DIRECT_FUNCTION_CHECK"),
    ):
        script = ROOT / "dembele/magma" / filename
        base = stem(n, "_direct_"+label+"_check")
        positive[label] = runner.run(script, base, marker, inputs, wrapper)
        jobs.append(Path(str(base)+"_job.json"))
        print("POINTED64_INDEPENDENT_CHECK_PASS", label, round(positive[label]["wall_seconds"], 3), flush=True)
    controls = {}
    for name, mutation, assertion in (
        ("norm", "pointed_cubic_norm_scalar := (pointed_cubic_norm_scalar+31^63) mod 31^64;", "assert norm_ok;"),
        ("septic", "pointed_cubic_trace_septic_coefficients[1] := (pointed_cubic_trace_septic_coefficients[1]+31^63) mod 31^64;", "assert septic_ok;"),
    ):
        base = stem(n, "_direct_"+name+"_control")
        controls[name] = runner.run(script, base, marker, inputs, wrapper+mutation+"\n", expected_failure=assertion)
        jobs.append(Path(str(base)+"_job.json"))
        print("POINTED64_DIGIT_CONTROL_REJECTED", name, round(controls[name]["wall_seconds"], 3), flush=True)
    report = {"status": "pass", "milestone": "D83", "date": "2026-09-22",
        "sources": [checks.source(p) for p in [Path(__file__), previous_root, cubic_path, class_path, *jobs]],
        "precision_digits": n, "modulus": 31**n, "independent_verification_completed": True,
        "points_sections_branch_values_verified": True, "three_division_verified": True,
        "actual_pointed_divisor_verified": True, "pointed_condition_rank": 80,
        "function_divisors_and_norm_verified": True, "fixed_linear_denominator_verified": True,
        "leading_coefficients_verified": [1, 2], "compatible_reduction_verified": True,
        "positive_check": positive, "highest_digit_norm_control": controls["norm"],
        "highest_digit_septic_control": controls["septic"], "characteristic_zero_cubic_constructed": False,
        "arithmetic_identification_certified": False, "target_field_constructed": False,
        "proof": "dembele/certificates/cm-frame-cubic-64.md"}
    stem(n, "_direct_check").with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|265_CM_FRAME_CUBIC_POINTED64_CHECK", flush=True)


if __name__ == "__main__":
    main()

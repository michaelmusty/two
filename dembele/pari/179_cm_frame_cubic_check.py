"""Verify D79's saved F31 cubic, its divisor witnesses and two corruptions.

Default rechecks saved data; --rebuild also reconstructs the functions.
--collect-only verifies the existing certificate and recursive hashes.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


helpers = module("cubic_check_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
jobs = module("cubic_check_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = helpers.checks


def run(script, stem, marker, inputs, expected_failure=None):
    job = jobs.run_job(jobs.magma_command(script), DATA / f"{stem}.out", 180,
                       marker, expected_failure=expected_failure)
    job["sources"] = [checks.source(p) for p in [script, Path(__file__),
                      ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"]+inputs]
    (DATA / f"{stem}_job.json").write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass":
        raise RuntimeError(f"{stem}: {job['status']}")
    return job


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--collect-only", action="store_true")
    mode.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    report_path = DATA / "cm_frame_cubic_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        checks.verify_records(report)
        assert report["status"] == "pass" and report["independent_verification_completed"]
        assert report["genus64_curve_constructed_modulo31"] and not report["arithmetic_identification_certified"]
        print("PASS|179_CM_FRAME_CUBIC_CHECK_PROVENANCE")
        return
    old_path = DATA / "cm_frame_cover_check.json"
    old = json.loads(old_path.read_text()); checks.verify_records(old)
    assert old["three_division_verified"]
    inputs = [old_path, ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m"]
    inputs += [DATA / name for name in ("cm_frame_cover_makdisi.m", "cm_frame_cover_sections.m",
               "cm_frame_cover_third_check_input.m", "cm_frame_B3_rational_model.m",
               "cm_frame_B3_fiber.m", "cm_frame_B3_fiber_structure.m", "cm_frame_curve_candidate.m")]
    if args.rebuild:
        run(ROOT / "dembele/magma/176_cm_frame_kummer_function.m", "cm_frame_kummer_function",
            "PASS|176_CM_FRAME_KUMMER_FUNCTION", inputs)
        subprocess.run([sys.executable, str(ROOT / "dembele/pari/177_cm_frame_cubic_data.py")],
                       cwd=ROOT, check=True, timeout=30)
    cubic_path = DATA / "cm_frame_cubic.json"
    cubic = json.loads(cubic_path.read_text()); checks.verify_records(cubic)
    inputs.append(cubic_path)
    script = ROOT / "dembele/magma/178_cm_frame_cubic_check.m"
    marker = "PASS|178_CM_FRAME_CUBIC_CHECK"
    positive = run(script, "cm_frame_cubic_check", marker, inputs)
    controls = {}
    needle = 'load "dembele/data/computed/cm_frame_cubic.m";'
    content = script.read_text(); assert content.count(needle) == 1
    for name, mutation, assertion in (
        ("norm", "kummer_norm_scalar := (kummer_norm_scalar+1) mod 31;", "assert norm_ok;"),
        ("trace", "cubic_trace_numerator_coefficients[1] := (cubic_trace_numerator_coefficients[1]+1) mod 31;", "assert trace_ok;"),
    ):
        control = DATA / f"cm_frame_cubic_{name}_control.m"
        control.write_text(content.replace(needle, needle+"\n"+mutation))
        controls[name] = run(control, f"cm_frame_cubic_{name}_control", marker,
                             inputs+[script], expected_failure=assertion)
    report = {
        "status": "pass", "milestone": "D79", "date": "2026-09-21",
        "sources": [checks.source(p) for p in (Path(__file__), old_path, cubic_path,
                    DATA / "cm_frame_cubic_check_job.json", DATA / "cm_frame_cubic_norm_control_job.json",
                    DATA / "cm_frame_cubic_trace_control_job.json")],
        # Historical jobs bind the discovery files as they were then. A
        # rebuild replaces those files legitimately; retain immutable logs
        # and script snapshots without treating old inputs as proof inputs.
        "historical_failures": [
            {"record_path": str(DATA / f"{stem}_job.json"),
             "log": checks.source(DATA / f"{stem}.out"),
             "source_snapshot": checks.source(DATA / f"{stem}.m"),
             "role": "archived failed run, not an arithmetic proof dependency"}
            for stem in ("cm_frame_kummer_function_monomial_syntax_failure",
                         "cm_frame_cubic_check_matrix_universe_failure")],
        "characteristic": 31, "evaluation_count": 1024, "injectivity_bound": 960,
        "base_divisor_degree": 120, "section_dimensions": [81, 201, 321, 441],
        "representative_defined_over_F31": True,
        "function_divisor": "D+-D-+3E_R-3D0", "norm_scalar": cubic["data"]["kummer_norm_scalar"],
        "norm_identity": "h*tau(h)=a^3, h=c*u/q, a=c*f, tau(a)=a",
        "weighted_equation": "Q4*T^3-3*A4*Q4*T-P10=0, weight(T)=2",
        "geometric_galois_group": "S3", "base_genus": 16,
        "quadratic_resolvent_genus": 40, "cyclic_cover_genus": 136,
        "reflection_quotient_genus": 64, "branch_degrees": {"transposition": 18, "three_cycle": 9},
        "kummer_function_constructed": True, "cyclic_cubic_constructed": True,
        "genus64_curve_constructed_modulo31": True, "independent_verification_completed": True,
        "coefficient_check": positive, "wrong_norm_control": controls["norm"],
        "wrong_trace_coefficient_control": controls["trace"],
        "characteristic_zero_cubic_constructed": False, "arithmetic_identification_certified": False,
        "prescribed_Fuchsian_monodromy_matched": False, "third_uniqueness_certified": False,
        "target_field_constructed": False,
        "proof": "dembele/certificates/cm-frame-cubic-cover.md",
    }
    report_path.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|179_CM_FRAME_CUBIC_CHECK: genus-64 cubic verified; both corruptions rejected")


if __name__ == "__main__":
    main()

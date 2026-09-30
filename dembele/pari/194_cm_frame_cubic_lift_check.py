"""Verify the genuine cubic modulo 961 and reject highest-digit corruptions.

Default rechecks the saved construction; --rebuild repeats all D81 stages.
--collect-only audits the saved recursive certificate without Magma.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("lift_check_prior", ROOT / "dembele/pari/189_cm_frame_cubic_lift_third.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, jobs, checks = prior.helpers, prior.jobs, prior.checks


def run(script, stem, marker, inputs, expected_failure=None):
    job = jobs.run_job(jobs.magma_command(script), DATA / f"{stem}.out", 180,
                       marker, expected_failure=expected_failure)
    job["sources"] = [checks.source(p) for p in [script, Path(__file__),
        ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"]+inputs]
    (DATA / f"{stem}_job.json").write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass":
        raise RuntimeError(f"{stem}: {job['status']}")
    return job


def python_stage(name, *args):
    subprocess.run([sys.executable, str(ROOT / "dembele/pari" / name), *args], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--collect-only", action="store_true")
    modes.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    result_path = DATA / "cm_frame_cubic_lift_check.json"
    if args.collect_only:
        report = json.loads(result_path.read_text()); checks.verify_records(report)
        assert report["status"] == "pass" and report["independent_verification_completed"]
        assert report["modulus"] == 961 and report["coefficientwise_reduction_verified"]
        print("PASS|194_CM_FRAME_CUBIC_LIFT_CHECK_PROVENANCE")
        return
    old_path = DATA / "cm_frame_cubic_point_check.json"
    old = json.loads(old_path.read_text()); checks.verify_records(old)
    model_inputs = [ROOT / "dembele/magma/186_cm_frame_cubic_lift_arithmetic.m",
                    ROOT / "dembele/magma/187_cm_frame_cubic_lift_model.m"]
    old_inputs = [old_path]+[DATA / name for name in (
        "cm_frame_curve_candidate.m", "cm_frame_marks.m", "cm_frame_B3_rational_model.m",
        "cm_frame_B3_veronese.m", "cm_frame_B3_fiber.m", "cm_frame_B3_fiber_structure.m",
        "cm_frame_cover_sections.m", "cm_frame_cover_makdisi.m", "cm_frame_cubic.m")]
    if args.rebuild:
        run(ROOT / "dembele/magma/184_cm_frame_cubic_lift_sections.m", "cm_frame_cubic_lift_sections",
            "PASS|184_CM_FRAME_CUBIC_LIFT_SECTIONS", old_inputs)
        python_stage("185_cm_frame_cubic_lift_section_data.py")
        run(ROOT / "dembele/magma/188_cm_frame_cubic_lift_pilot.m", "cm_frame_cubic_lift_pilot",
            "PASS|188_CM_FRAME_CUBIC_LIFT_PILOT", model_inputs+
            [DATA / "cm_frame_cubic_lift_sections.json", old_path])
        python_stage("189_cm_frame_cubic_lift_third.py", "--rebuild")
        python_stage("192_cm_frame_cubic_lift_data.py")
    cubic_path = DATA / "cm_frame_cubic_lift.json"
    cubic = json.loads(cubic_path.read_text()); checks.verify_records(cubic)
    inputs = model_inputs+old_inputs+[cubic_path, DATA / "cm_frame_cubic_lift_third.json",
                                    DATA / "cm_frame_cubic_lift_sections.json"]
    script = ROOT / "dembele/magma/193_cm_frame_cubic_lift_check.m"
    marker = "PASS|193_CM_FRAME_CUBIC_LIFT_CHECK"
    positive = run(script, "cm_frame_cubic_lift_check", marker, inputs)
    needle = 'load "dembele/data/computed/cm_frame_cubic_lift.m";'
    content = script.read_text(); assert content.count(needle) == 1
    controls = {}
    for name, mutation, assertion in (
        ("norm", "cubic961_norm_scalar := (cubic961_norm_scalar+31) mod 961;", "assert norm_ok;"),
        ("trace", "cubic961_trace_numerator_coefficients[1] := (cubic961_trace_numerator_coefficients[1]+31) mod 961;", "assert trace_ok;"),
    ):
        control = DATA / f"cm_frame_cubic_lift_{name}_control.m"
        control.write_text(content.replace(needle, needle+"\n"+mutation))
        controls[name] = run(control, f"cm_frame_cubic_lift_{name}_control", marker,
                             inputs+[script], expected_failure=assertion)
    historical = []
    for stem, suffix in (("cm_frame_cubic_lift_sections_linear_factor_failure", ".m"),
                         ("cm_frame_cubic_lift_sections_linear_root_failure", ".m"),
                         ("cm_frame_cubic_lift_sections_division_api_failure", ".m"),
                         ("cm_frame_cubic_lift_pilot_data_syntax_failure", ".py")):
        historical.append({"record_path": str(DATA / f"{stem}_job.json"),
                           "log": checks.source(DATA / f"{stem}.out"),
                           "source_snapshot": checks.source(DATA / f"{stem}{suffix}"),
                           "role": "archived implementation failure, not a proof dependency"})
    report = {"status": "pass", "milestone": "D81", "date": "2026-09-22",
        "sources": [checks.source(p) for p in (Path(__file__), old_path, cubic_path,
                    DATA / "cm_frame_cubic_lift_check_job.json",
                    DATA / "cm_frame_cubic_lift_norm_control_job.json",
                    DATA / "cm_frame_cubic_lift_trace_control_job.json")],
        "historical_failures": historical, "modulus": 961, "precision_digits": 2,
        "evaluation_count": 1024, "auxiliary_count": 111, "injectivity_bound": 960,
        "section_dimensions": [81, 201, 321, 441], "odd_support_degrees": [18, 21],
        "points_sections_and_branch_values_verified": True,
        "three_division_verified": True, "frobenius_descent_verified": True,
        "antiinvariant_verified": True, "class_number_assumed": False,
        "norm_scalar": cubic["data"]["norm_scalar"],
        "norm_identity": "h*tau(h)=a^3, h=c*u/q, a=c*f, tau(a)=a",
        "weighted_equation": cubic["weighted_equation"],
        "coefficientwise_reduction_verified": True, "reflection_quotient_genus": 64,
        "cubic_lift_computed": True, "independent_verification_completed": True,
        "positive_check": positive, "highest_digit_norm_control": controls["norm"],
        "highest_digit_trace_control": controls["trace"],
        "characteristic_zero_cubic_constructed": False, "arithmetic_identification_certified": False,
        "prescribed_Fuchsian_monodromy_matched": False, "third_uniqueness_certified": False,
        "target_field_constructed": False, "proof": "dembele/certificates/cm-frame-cubic-lift.md"}
    result_path.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|194_CM_FRAME_CUBIC_LIFT_CHECK: cubic mod961 verified; highest-digit corruptions rejected")


if __name__ == "__main__":
    main()

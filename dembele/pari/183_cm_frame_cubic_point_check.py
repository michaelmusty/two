"""Independently check D80's cubic point counts and a corrupted fibre count.

Default checks saved point lists without repeating the point search.
--rebuild also repeats the two bounded point searches and collection.
--collect-only verifies the existing certificate and source hashes.
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
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


helpers = module("cubic_point_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
jobs = module("cubic_point_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
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
    report_path = DATA / "cm_frame_cubic_point_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text()); checks.verify_records(report)
        assert report["status"] == "pass" and report["independent_fiber_verification_completed"]
        assert report["point_counts"] == report["hecke_predictions"]
        assert not report["arithmetic_identification_certified"]
        print("PASS|183_CM_FRAME_CUBIC_POINT_CHECK_PROVENANCE")
        return
    inputs = [DATA / n for n in ("cm_frame_cubic_check.json", "cm_frame_curve_verification.json",
              "cm_frame_curve_candidate.m", "cm_frame_marks.m", "cm_frame_B3_rational_model.m",
              "cm_frame_B3_fiber_structure.m", "cm_frame_cover_sections.m", "cm_frame_cover_makdisi.m",
              "cm_frame_cubic.m", "levelraise_p2k_charpolys.m")]
    if args.rebuild:
        script = ROOT / "dembele/magma/180_cm_frame_cubic_point_count.m"
        for degree, stem in ((1, "cm_frame_cubic_point_count_F31"), (2, "cm_frame_cubic_point_count_F31_squared")):
            wrapper = DATA / f"{stem}_run.m"
            wrapper.write_text(f'extension_degree := {degree};\nload "dembele/magma/180_cm_frame_cubic_point_count.m";\n')
            run(wrapper, stem, "PASS|180_CM_FRAME_CUBIC_POINT_COUNT", inputs+[script])
        subprocess.run([sys.executable, str(ROOT / "dembele/pari/181_cm_frame_cubic_point_data.py")],
                       cwd=ROOT, check=True, timeout=30)
    data_path = DATA / "cm_frame_cubic_point_counts.json"
    data = json.loads(data_path.read_text()); checks.verify_records(data)
    inputs.append(data_path)
    script = ROOT / "dembele/magma/182_cm_frame_cubic_point_check.m"
    marker = "PASS|182_CM_FRAME_CUBIC_POINT_CHECK"
    positives = []
    for degree in (1, 2):
        wrapper = DATA / f"cm_frame_cubic_point_check_{degree}_run.m"
        suffix = "F31" if degree == 1 else "F31_squared"
        wrapper.write_text(f'extension_degree := {degree};\n'
                           f'load "dembele/data/computed/cm_frame_cubic_point_count_{suffix}_input.m";\n'
                           'load "dembele/magma/182_cm_frame_cubic_point_check.m";\n')
        positives.append(run(wrapper, f"cm_frame_cubic_point_check_{degree}", marker, inputs+[script]))
    needle = "assert point_count_extension_degree eq extension_degree;"
    content = script.read_text(); assert content.count(needle) == 1
    negative = DATA / "cm_frame_cubic_point_fiber_control.m"
    negative.write_text('load "dembele/data/computed/cm_frame_cubic_point_count_F31_input.m";\n'+content.replace(needle, needle+
        "\npoint_count_fiber_counts[1][3] := (point_count_fiber_counts[1][3]+1) mod 4;"))
    control = run(negative, "cm_frame_cubic_point_fiber_control", marker,
                  inputs+[script], expected_failure="assert fiber_ok;")
    point_counts = [r["cubic_point_count"] for r in data["point_counts"]]
    predictions = [r["hecke_expected_point_count"] for r in data["point_counts"]]
    traces = [32-point_counts[0], 962-point_counts[1]]
    report = {
        "status": "pass", "milestone": "D80", "date": "2026-09-22",
        "sources": [checks.source(p) for p in (Path(__file__), data_path,
                    DATA / "cm_frame_cubic_point_check_1_job.json", DATA / "cm_frame_cubic_point_check_2_job.json",
                    DATA / "cm_frame_cubic_point_fiber_control_job.json")],
        "historical_runs": [
            {"record_path": str(DATA / f"{stem}_job.json"),
             "log": checks.source(DATA / f"{stem}.out"),
             "source_snapshots": [checks.source(DATA / n) for n in snapshots],
             "role": "archived run, not an arithmetic proof dependency"}
            for stem, snapshots in (
                ("cm_frame_cubic_point_count_parameter_scope_failure",
                 ["cm_frame_cubic_point_count_parameter_scope_failure.m"]),
                ("cm_frame_cubic_point_check_load_syntax_failure",
                 ["cm_frame_cubic_point_check_load_syntax_failure_0.m",
                  "cm_frame_cubic_point_check_load_syntax_failure_1.py",
                  "cm_frame_cubic_point_check_load_syntax_failure_2.m"]),
                ("cm_frame_cubic_point_count_F31_pilot",
                 ["cm_frame_cubic_point_count_F31_pilot.m"]))],
        "field_cardinalities": [31, 961], "base_point_counts": [50, 1400],
        "point_counts": point_counts, "hecke_predictions": predictions,
        "Frobenius_power_traces": traces,
        "Euler_polynomial_initial_coefficients": [1, -traces[0], (traces[0]**2-traces[1])//2],
        "independent_fiber_verification_completed": True,
        "independent_checks": positives, "wrong_fiber_count_control": control,
        "comparison_scope": "first two power traces at the single split prime 31",
        "full_Euler_factor_computed": False, "arithmetic_identification_certified": False,
        "prescribed_Fuchsian_monodromy_matched": False,
        "characteristic_zero_cubic_constructed": False, "target_field_constructed": False,
        "proof": "dembele/certificates/cm-frame-cubic-frobenius.md",
    }
    assert point_counts == predictions
    report_path.write_text(json.dumps(report, indent=2)+"\n"); checks.verify_records(report)
    print("PASS|183_CM_FRAME_CUBIC_POINT_CHECK:", point_counts, "match Hecke; wrong fibre rejected")


if __name__ == "__main__":
    main()

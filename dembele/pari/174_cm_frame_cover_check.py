"""Check D78's genus-40 section model and saved 3-division class.

Default repeats the saved-space and saved-relation checks and corruption
controls. --relation-only reuses the completed section checks. --rebuild
also constructs sections, evaluates them and repeats the scalar search.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


helpers = module("cover_check_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
jobs = module("cover_check_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = helpers.checks


def run_magma(script, stem, marker, inputs, expected_failure=None):
    job = jobs.run_job(jobs.magma_command(script), DATA / f"{stem}.out", 180,
                       marker, expected_failure=expected_failure)
    job["sources"] = [checks.source(p) for p in [script, Path(__file__),
                      ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"]+inputs]
    (DATA / f"{stem}_job.json").write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass":
        raise RuntimeError(f"{stem}: {job['status']}")
    return job


def python_step(name):
    script = ROOT / "dembele/pari" / name
    import subprocess
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True, timeout=200)


def section_checks(recheck=False):
    script = ROOT / "dembele/magma/168_cm_frame_cover_makdisi_check.m"
    inputs = [DATA / "cm_frame_cover_makdisi.json", DATA / "cm_frame_cover_sections.json",
              DATA / "cm_frame_B3_rational_model.m", DATA / "cm_frame_B3_fiber.m",
              DATA / "cm_frame_B3_fiber_structure.m", DATA / "cm_frame_marks.m",
              DATA / "cm_frame_curve_candidate.m"]
    stem = "cm_frame_cover_makdisi_recheck" if recheck else "cm_frame_cover_makdisi_check"
    control_stem = "cm_frame_cover_makdisi_recheck_value_control" if recheck else "cm_frame_cover_makdisi_value_control"
    run_magma(script, stem, "PASS|168_CM_FRAME_COVER_MAKDISI_CHECK", inputs)
    negative = DATA / f"{control_stem}.m"
    needle = 'load "dembele/data/computed/cm_frame_cover_makdisi.m";'
    text = script.read_text()
    assert text.count(needle) == 1
    negative.write_text(text.replace(needle, needle+
        '\nmakdisi_v1_evaluations[1][46] := (makdisi_v1_evaluations[1][46]+1) mod 961;'))
    run_magma(negative, control_stem, "PASS|168_CM_FRAME_COVER_MAKDISI_CHECK",
              inputs+[script], expected_failure="assert V1 eq DecodeMatrix(makdisi_v1_evaluations,k);")


def rebuild():
    # Rebuild in dependency order; unchanged old arithmetic inputs are retained.
    sources = [DATA / n for n in ("cm_frame_curve_candidate.m", "cm_frame_marks.m",
               "cm_frame_B3_rational_model.m", "cm_frame_B3_fiber.m",
               "cm_frame_B3_fiber_structure.m", "cm_frame_B3_branch_class.json")]
    run_magma(ROOT / "dembele/magma/164_cm_frame_cover_sections.m", "cm_frame_cover_sections",
              "PASS|164_CM_FRAME_COVER_SECTIONS", sources)
    python_step("165_cm_frame_cover_section_data.py")
    run_magma(ROOT / "dembele/magma/166_cm_frame_cover_makdisi.m", "cm_frame_cover_makdisi",
              "PASS|166_CM_FRAME_COVER_MAKDISI", [DATA / "cm_frame_cover_sections.json"]+sources)
    python_step("167_cm_frame_cover_makdisi_data.py")
    section_checks()
    run_magma(ROOT / "dembele/magma/171_cm_frame_cover_class_check.m", "cm_frame_cover_class_check",
              "PASS|171_CM_FRAME_COVER_CLASS_CHECK", [DATA / "cm_frame_cover_makdisi_check_job.json",
              ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m", DATA / "cm_frame_cover_makdisi.json"])
    python_step("172_cm_frame_cover_third.py")


def check_negative(path, expected, marker):
    job = json.loads(path.read_text())
    checks.verify_records(job)
    assert job["status"] == "pass" and job["exit_code"] != 0
    output = Path(job["log"]["path"]).read_text()
    assert expected in output and "Assertion failed" in output and marker not in output
    return job


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--collect-only", action="store_true")
    mode.add_argument("--relation-only", action="store_true")
    mode.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    report_path = DATA / "cm_frame_cover_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        checks.verify_records(report)
        assert report["three_division_verified"] and not report["cyclic_cubic_constructed"]
        print("PASS|174_CM_FRAME_COVER_CHECK_PROVENANCE")
        return
    if args.rebuild:
        rebuild()
    elif not args.relation_only:
        section_checks(recheck=True)
    # A routine recheck gets new filenames: the discovery chain continues
    # to bind the original section-check job rather than a changed timestamp.
    recheck = not args.rebuild and not args.relation_only
    section_path = DATA / ("cm_frame_cover_makdisi_recheck_job.json" if recheck else "cm_frame_cover_makdisi_check_job.json")
    value_path = DATA / ("cm_frame_cover_makdisi_recheck_value_control_job.json" if recheck else "cm_frame_cover_makdisi_value_control_job.json")
    section_job = checks.read_job(section_path,
                                  "PASS|168_CM_FRAME_COVER_MAKDISI_CHECK")
    value_control = check_negative(value_path,
                                   "assert V1 eq DecodeMatrix(makdisi_v1_evaluations,k);",
                                   "PASS|168_CM_FRAME_COVER_MAKDISI_CHECK")
    third_path = DATA / "cm_frame_cover_third.json"
    third = json.loads(third_path.read_text()); checks.verify_records(third)
    assert third["three_division_computed"]
    class_job = checks.read_job(DATA / "cm_frame_cover_class_check_job.json",
                                "PASS|171_CM_FRAME_COVER_CLASS_CHECK")
    delta = helpers.field(Path(class_job["log"]["path"]).read_text(), "DELTA_SECTION_ROWS")
    input_path = DATA / "cm_frame_cover_third_check_input.m"
    input_path.write_text("// D78: saved third for verification without a class-number assumption.\n"+
                          "third_check_delta_rows := "+helpers.magma(delta)+";\n"+
                          "third_check_candidate_rows := "+helpers.magma(third["candidate_rows"])+";\n")
    script = ROOT / "dembele/magma/175_cm_frame_cover_third_check.m"
    sources = [input_path, third_path, ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m",
               DATA / "cm_frame_cover_makdisi.json"]
    relation = run_magma(script, "cm_frame_cover_third_check", "PASS|175_CM_FRAME_COVER_THIRD_CHECK", sources)
    negative = DATA / "cm_frame_cover_third_class_control.m"
    needle = "candidate:=Dec(third_check_candidate_rows,k);"
    text = script.read_text(); assert text.count(needle) == 1
    negative.write_text(text.replace(needle, needle+"\ncandidate:=AddClass(candidate,D);"))
    control = run_magma(negative, "cm_frame_cover_third_class_control", "PASS|175_CM_FRAME_COVER_THIRD_CHECK",
                         sources+[script], expected_failure="assert EqualClass(threeA,NegClass(D));")
    report = {"status": "pass", "milestone": "D78", "date": "2026-09-21",
              "sources": [checks.source(p) for p in (__file__, DATA / "cm_frame_cover_sections.json",
                          DATA / "cm_frame_cover_makdisi.json", third_path,
                          section_path, value_path,
                          DATA / "cm_frame_cover_class_check_job.json",
                          DATA / "cm_frame_cover_third_check_job.json",
                          DATA / "cm_frame_cover_third_class_control_job.json",
                          DATA / "cm_frame_cover_sections_matrix_api_failure_job.json")],
              "genus": 40, "base_divisor_degree": 120,
              "available_good_points_F31_squared": 2048, "evaluation_count": 640,
              "section_dimensions": [81, 201, 321], "auxiliary_divisor_degree": 111,
              "delta_nonzero": True, "delta_killed_by_three": False,
              "three_division_verified": True, "relation": "3[A]=-[D+-D-]",
              "third_fixed_by_Frobenius": True, "third_negated_by_cover_involution": True,
              "scalar_used_only_for_discovery": third["proposed_scalar"],
              "jacobian_or_prym_order_certified": False,
              "third_uniqueness_certified": False,
              # This unsuccessful historical probe is not an input to the
              # proof. Its old JSON binds the discovery files as they were
              # then; --rebuild legitimately replaces those D78 files.
              "historical_gp_probe": {
                  "record_path": str(DATA / "cm_frame_cover_class_job.json"),
                  "log": checks.source(DATA / "cm_frame_cover_class.out"),
                  "status": "timeout", "timeout_seconds": 180,
                  "role": "archived comparison, not an arithmetic proof dependency"},
              "section_check": section_job, "value_control": value_control,
              "relation_check": relation, "wrong_class_control": control,
              "kummer_function_constructed": False, "cyclic_cubic_constructed": False,
              "genus64_curve_constructed": False, "arithmetic_identification_certified": False,
              "proof": "dembele/certificates/cm-frame-cover-class-arithmetic.md"}
    report_path.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|174_CM_FRAME_COVER_CHECK: verified Frobenius-fixed anti-invariant third; both corruptions rejected")


if __name__ == "__main__":
    main()

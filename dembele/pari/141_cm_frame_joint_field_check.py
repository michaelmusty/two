"""D75: reproduce or independently certify joint F recognition and bounds.

Default checks the saved rows, exact control and coefficient-box bounds in
Magma, then rejects a changed unused digit. --search repeats the Sage work.
--collect-only checks saved provenance without running the arithmetic.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


jobs = module("joint_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = module("joint_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
source = checks.source


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--search", action="store_true")
    mode.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    report_path = DATA / "cm_frame_joint_field_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        checks.verify_records(report)
        assert report["status"] == report["independent_check"]["status"] == report["negative_control"]["status"] == "pass"
        print("PASS: D75 joint F recognition, exact controls and coefficient-box exclusions.")
        return
    definitions = [
        ("138_cm_frame_joint_field_recognition.py", "cm_frame_joint_field_recognition", 300,
         "PASS|138_CM_FRAME_JOINT_FIELD_RECOGNITION"),
        ("139_cm_frame_joint_height_bounds.py", "cm_frame_joint_height_bounds", 180,
         "PASS|139_CM_FRAME_JOINT_HEIGHT_BOUNDS")]
    if args.search:
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d75-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        for filename, name, timeout, marker in definitions:
            script = ROOT / "dembele/pari" / filename
            job = jobs.run_job([jobs.SAGE, "-python", str(script)], DATA / (name+".out"), timeout, marker, env=env)
            job["sources"] = [source(script), source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
            job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
            write_json(DATA / (name+"_job.json"), job)
            print(name, job["status"], round(job["wall_seconds"], 3), flush=True)
            if job["status"] != "pass":
                raise RuntimeError(f"{name}: {job['status']}")
    for filename, name, timeout, marker in definitions:
        checks.read_job(DATA / (name+"_job.json"), marker)
    fit_path = DATA / "cm_frame_joint_field_recognition.json"
    bound_path = DATA / "cm_frame_joint_height_bounds.json"
    fit, bounds = [json.loads(p.read_text()) for p in (fit_path, bound_path)]
    checks.verify_records(fit)
    checks.verify_records(bounds)
    assert fit["status"] == bounds["status"] == "pass"
    assert [b["root_mod31"] for b in bounds["denominator_bounds"]] == fit["all_roots_mod31"]
    trials = [fit["control"]]+fit["denominator_trials"]
    targets = [fit["control"]["target_residues"]]+[fit["denominator_target_residues"] for _ in fit["denominator_trials"]]
    all_bounds = [bounds["control"]]+bounds["denominator_bounds"]
    tuples = []
    for trial, bound in zip(trials, all_bounds):
        matches = [-1]*136
        for c in trial["candidates"]:
            matches[c["row_index_zero_based"]] = c["matching_digits"]
        vals = [trial["root_mod_validation"], trial["projective_anchor_index_zero_based"]+1,
                trial["reduced_rows"], matches, sorted(i+1 for i in trial["survivor_row_indices"]),
                int(bound["maximum_inverse_column_l1_norm"]), bound["coefficient_box_excluded_through"]]
        tuples.append("<"+",".join(str(x) for x in vals)+">")
    bindings = {
        "joint_training_digits": fit["training_digits"], "joint_validation_digits": fit["validation_digits"],
        "joint_field_polynomial": fit["field_polynomial_ascending"], "joint_targets": targets,
        "joint_control_coefficients": fit["control"]["exact_control_coefficients"],
        "joint_negative_coordinate": fit["control"]["negative_control_coordinate"]+1}
    data_path = DATA / "cm_frame_joint_field_data.m"
    data_path.write_text("// D75: saved fit rows and claimed bounds; independently checked by Magma 140.\n"
                        +"\n".join(f"{key} := {value};" for key, value in bindings.items())
                        +"\njoint_trials := [*\n"+",\n".join(tuples)+"\n*];\n")
    script = ROOT / "dembele/magma/140_cm_frame_joint_field_check.m"
    inputs = [script, data_path, DATA / "cm_frame_denominator_space_coordinates.m"]
    check = jobs.run_job(jobs.magma_command(script), DATA / "cm_frame_joint_field_check.out", 180,
                         "PASS|140_CM_FRAME_JOINT_FIELD_CHECK")
    check["sources"] = [source(p) for p in inputs]
    report = {"status": check["status"], "milestone": "D75", "date": "2026-09-18",
              "independent_check": check,
              "sources": [source(p) for p in (__file__, ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py", fit_path, bound_path,
                          DATA / "cm_frame_joint_field_recognition_job.json", DATA / "cm_frame_joint_height_bounds_job.json")],
              "provisional_survivor_count": fit["provisional_survivor_count"],
              "uniform_coefficient_box_excluded_through": bounds["uniform_coefficient_box_excluded_through"],
              "number_field_cover_obtained": False, "nonmembership_in_F_proved": False}
    write_json(report_path, report)
    print("joint field certificate", check["status"], round(check["wall_seconds"], 3), flush=True)
    if check["status"] != "pass":
        print(Path(check["log"]["path"]).read_text()[-4000:])
        raise RuntimeError("independent joint field check failed")
    negative_path = DATA / "cm_frame_joint_field_negative_control.m"
    needle = 'load "dembele/data/computed/cm_frame_joint_field_data.m";'
    text = script.read_text().replace(needle, needle
            +"\njoint_targets[1][joint_negative_coordinate] +:= 31^joint_training_digits;")
    assert text != script.read_text()
    negative_path.write_text(text)
    negative = jobs.run_job(jobs.magma_command(negative_path), negative_path.with_suffix(".out"), 180,
                            "PASS|140_CM_FRAME_JOINT_FIELD_CHECK", expected_failure="assert matching eq trial[4]")
    negative["sources"] = [source(negative_path)]+[source(p) for p in inputs]
    negative["mutation"] = "add 31^64 to one non-anchor control coordinate; all fitting digits unchanged"
    report["negative_control"] = negative
    report["status"] = negative["status"]
    write_json(report_path, report)
    if negative["status"] != "pass":
        raise RuntimeError("unused-digit corruption was not rejected")
    checks.verify_records(report)
    print("PASS: independently checked joint F rows, exact control, coefficient bounds and digit corruption.")


if __name__ == "__main__":
    main()

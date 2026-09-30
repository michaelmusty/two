"""D77: reproduce or independently certify the normalized B3 fibre.

Default repeats the independent verifier and unit-corruption control.
--rebuild first repeats 157--160. --control-only checks the saved
positive job and runs its missing control. --collect-only validates
the completed provenance without repeating arithmetic.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


jobs = module("fiber_runner_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
collect = module("fiber_runner_data", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
checks = collect.checks


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--rebuild", action="store_true")
    mode.add_argument("--control-only", action="store_true")
    mode.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    report_path = DATA / "cm_frame_B3_fiber_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        checks.verify_records(report)
        assert report["status"] == report["positive_job"]["status"] == report["negative_job"]["status"] == "pass"
        print("PASS: normalized B3 fibre K(sqrt(-3)), oriented degree-nine branches, corrupted unit rejected.")
        return
    env = dict(os.environ, DOT_SAGE="/private/tmp/dembele-d77-sage", OPENBLAS_NUM_THREADS="1")
    if args.rebuild:
        stages = [
            ("magma/157_cm_frame_B3_fiber.m", "cm_frame_B3_fiber", "PASS|157_CM_FRAME_B3_FIBER",
             ["cm_frame_curve_candidate.m", "cm_frame_marks.m", "cm_frame_B3_rational_model.m",
              "cm_frame_B3_rational_check.json", "cm_frame_marks_check.json"]),
            ("pari/158_cm_frame_B3_fiber_data.py", "cm_frame_B3_fiber_data", "PASS|158_CM_FRAME_B3_FIBER_DATA", []),
            ("magma/159_cm_frame_B3_fiber_squareclass.m", "cm_frame_B3_fiber_squareclass",
             "PASS|159_CM_FRAME_B3_FIBER_SQUARECLASS", ["cm_frame_B3_fiber.m", "cm_frame_B3_fiber.json"]),
            ("pari/160_cm_frame_B3_fiber_structure.py", "cm_frame_B3_fiber_structure",
             "PASS|160_CM_FRAME_B3_FIBER_STRUCTURE", []),
        ]
        for relative, name, marker, inputs in stages:
            script = ROOT / "dembele" / relative
            command = jobs.magma_command(script) if script.suffix == ".m" else (
                [sys.executable, str(script)] if relative.startswith("pari/158_")
                else [jobs.SAGE, "-python", str(script)])
            job = jobs.run_job(command, DATA / (name+".out"), 180, marker, env=env)
            job["sources"] = [checks.source(script), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
            job["sources"] += [checks.source(DATA / p) for p in inputs]
            if relative.startswith("pari/160_"):
                job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
            write_json(DATA / (name+"_job.json"), job)
            print(name, job["status"], round(job["wall_seconds"], 3), flush=True)
            if job["status"] != "pass":
                raise RuntimeError("fiber reconstruction failed")
    job_records = [
        ("cm_frame_B3_fiber_job.json", "PASS|157_CM_FRAME_B3_FIBER"),
        ("cm_frame_B3_fiber_squareclass_job.json", "PASS|159_CM_FRAME_B3_FIBER_SQUARECLASS"),
        ("cm_frame_B3_fiber_structure_job.json", "PASS|160_CM_FRAME_B3_FIBER_STRUCTURE"),
    ]
    for name, marker in job_records:
        checks.read_job(DATA / name, marker)
    for name, prefix in (("cm_frame_B3_fiber", "fiber_"), ("cm_frame_B3_fiber_structure", "branch_")):
        record = json.loads((DATA / (name+".json")).read_text())
        checks.verify_records(record)
        mtext = (DATA / (name+".m")).read_text()
        for key, value in record["data"].items():
            assert prefix+key+" := "+collect.magma(value)+";" in mtext
    template = ROOT / "dembele/magma/161_cm_frame_B3_fiber_check.m"
    inputs = [template, ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"]
    inputs += [DATA / name for name in ("cm_frame_B3_fiber.m", "cm_frame_B3_fiber_structure.m",
               "cm_frame_B3_fiber_structure.json", "cm_frame_B3_fiber_structure_job.json",
               "cm_frame_B3_rational_model.m", "cm_frame_curve_candidate.m", "cm_frame_marks.m")]
    positive_path = DATA / "cm_frame_B3_fiber_check_job.json"
    marker = "PASS|161_CM_FRAME_B3_FIBER_CHECK"
    if not args.control_only:
        positive = jobs.run_job(jobs.magma_command(template), DATA / "cm_frame_B3_fiber_check.out", 180, marker)
        positive["sources"] = [checks.source(p) for p in inputs]
        write_json(positive_path, positive)
    positive = checks.read_job(positive_path, marker)
    print("independent fiber", positive["status"], round(positive["wall_seconds"], 3), flush=True)
    negative_script = DATA / "cm_frame_B3_fiber_unit_control.m"
    needle = 'load "dembele/data/computed/cm_frame_B3_fiber.m";'
    text = template.read_text().replace(needle, needle+"\nfiber_unit[1] +:= 1;")
    assert text != template.read_text()
    negative_script.write_text(text)
    negative = jobs.run_job(jobs.magma_command(negative_script), negative_script.with_suffix(".out"), 180,
                            marker, expected_failure="assert n2 eq d0*alpha")
    negative["sources"] = [checks.source(negative_script)]+[checks.source(p) for p in inputs]
    negative["mutation"] = "add 1 to the constant coefficient of the normalized unit; point and zero orders unchanged"
    write_json(DATA / "cm_frame_B3_fiber_unit_control_job.json", negative)
    if negative["status"] != "pass":
        raise RuntimeError("corrupted normalized fibre unit was not rejected")
    output = (DATA / "cm_frame_B3_fiber_check.out").read_text()
    report = {"status": "pass", "milestone": "D77", "date": "2026-09-19",
              "sources": [checks.source(p) for p in (__file__, ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          DATA / "cm_frame_B3_fiber.json", DATA / "cm_frame_B3_fiber_structure.json",
                          DATA / "cm_frame_B3_rational_check.json")]
                         +[checks.source(DATA / name) for name, _ in job_records],
              "positive_job": positive, "negative_job": negative,
              "fiber_is_field": True, "fiber_field_degree": 18,
              "fiber_presentation": "K(sqrt(-3)), [K:Q]=9", "squareclass": -3,
              "oriented_branch_degrees": [9, 9],
              "B3_factor_degrees_mod31": collect.field(output, "B3_FACTOR_DEGREES_MOD31"),
              "branch_plus_values_mod31": collect.field(output, "BRANCH_PLUS_VALUES_MOD31"),
              "branch_minus_values_mod31": collect.field(output, "BRANCH_MINUS_VALUES_MOD31"),
              "selected_sqrt_minus3_mod31": 11,
              "constant_C3_inertia_condition_passed": True,
              "scalar_twist_uniqueness": "necessary condition singles out this F-scalar twist for the fixed geometric half",
              "arithmetic_curve_or_half_identified": False,
              "cyclic_cubic_constructed": False, "genus64_cover_constructed": False,
              "proof": "dembele/certificates/cm-frame-B3-fiber.md"}
    write_json(report_path, report)
    checks.verify_records(report)
    print("corrupted unit", negative["status"], round(negative["wall_seconds"], 3), flush=True)
    print("PASS: exact normalized fibre K(sqrt(-3)) and two oriented degree-nine branches.")


if __name__ == "__main__":
    main()

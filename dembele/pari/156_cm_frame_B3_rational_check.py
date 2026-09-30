"""D76: independently certify or reproduce the rational B3 double cover.

Default runs Magma 155 and a wrong-twist control. --reconstruct first
repeats scripts 150--154 against the saved certified lifts. To rebuild
those lifts too, run script 148 with --rebuild before this runner.
--collect-only recursively validates the saved provenance and outcomes.
"""
import argparse
import ast
import importlib.util
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


jobs = module("rational_check_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = module("rational_check_hashes", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")


def write_json(path, record):
    path.write_text(json.dumps(record, indent=2)+"\n")


STAGES = (
    (150, "pari/150_cm_frame_B3_space_recognition.py", "cm_frame_B3_space_recognition", 300,
     "PASS|150_CM_FRAME_B3_SPACE_RECOGNITION", []),
    (151, "magma/151_cm_frame_B3_exact_product_relations.m", "cm_frame_B3_exact_product_relations", 180,
     "PASS|151_CM_FRAME_B3_EXACT_PRODUCT_RELATIONS",
     ["cm_frame_curve_candidate.m", "cm_frame_marks.m", "cm_frame_B3_space_recognition.m",
      "cm_frame_B3_space_recognition.json", "cm_frame_B3_space_recognition_job.json"]),
    (152, "pari/152_cm_frame_B3_veronese.py", "cm_frame_B3_veronese", 180,
     "PASS|152_CM_FRAME_B3_VERONESE", []),
    (153, "magma/153_cm_frame_B3_rational_cover.m", "cm_frame_B3_rational_cover", 180,
     "PASS|153_CM_FRAME_B3_RATIONAL_COVER",
     ["cm_frame_curve_candidate.m", "cm_frame_marks.m", "cm_frame_B3_veronese.m",
      "cm_frame_B3_veronese.json", "cm_frame_B3_veronese_job.json", "cm_frame_B3_transfer.m",
      "cm_frame_B3_numerator.m", "cm_frame_B3_moving_128.m"]),
    (154, "pari/154_cm_frame_B3_rational_model.py", "cm_frame_B3_rational_model", 180,
     "PASS|154_CM_FRAME_B3_RATIONAL_MODEL", []),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--reconstruct", action="store_true")
    modes.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    path = DATA / "cm_frame_B3_rational_check.json"
    if args.collect_only:
        report = json.loads(path.read_text())
        checks.verify_records(report)
        assert report["status"] == report["independent_check"]["status"] == report["negative_control"]["status"] == "pass"
        print("PASS: exact rational genus-40 cover, 128-digit square map, wrong twist rejected.")
        return
    lift_path = DATA / "cm_frame_B3_lift_check.json"
    lift = json.loads(lift_path.read_text())
    checks.verify_records(lift)
    assert lift["status"] == "pass"
    env = dict(os.environ, DOT_SAGE="/private/tmp/dembele-d76-sage", OPENBLAS_NUM_THREADS="1")
    for number, relative, name, timeout, marker, inputs in STAGES:
        script = ROOT / "dembele" / relative
        job_path = DATA / (name+"_job.json")
        if args.reconstruct:
            command = jobs.magma_command(script) if script.suffix == ".m" else [jobs.SAGE, "-python", str(script)]
            job = jobs.run_job(command, DATA / (name+".out"), timeout, marker, env=env)
            job["sources"] = [checks.source(p) for p in (script, ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
            job["sources"] += [checks.source(DATA / name) for name in inputs]
            if script.suffix == ".py":
                job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
            write_json(job_path, job)
            print(number, job["status"], round(job["wall_seconds"], 3), flush=True)
        checks.read_job(job_path, marker)
    model_path = DATA / "cm_frame_B3_rational_model.json"
    model = json.loads(model_path.read_text())
    checks.verify_records(model)
    model_m = DATA / "cm_frame_B3_rational_model.m"
    for binding, key in (("rational_numerator", "numerator_coefficients"),
                         ("rational_denominator", "denominator_coefficients"),
                         ("rational_square_g", "square_numerator_coefficients"),
                         ("rational_square_q", "square_denominator_coefficients")):
        raw = re.search(r"^"+binding+r" := (.*);$", model_m.read_text(), re.M).group(1)
        assert ast.literal_eval(raw) == model[key]
    assert model["branch_degree"] == 18 and model["genus"] == 40
    template = ROOT / "dembele/magma/155_cm_frame_B3_rational_check.m"
    inputs = [template, model_m, DATA / "cm_frame_B3_veronese.m", DATA / "cm_frame_B3_transfer.m",
              DATA / "cm_frame_doubling_128.m", DATA / "cm_frame_curve_candidate.m", DATA / "cm_frame_marks.m"]
    report = {"status": "incomplete", "milestone": "D76", "date": "2026-09-18",
              "sources": [checks.source(p) for p in (__file__, lift_path, model_path,
                          DATA / "cm_frame_B3_check.json", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")]
                         +[checks.source(DATA / (name+"_job.json")) for _, _, name, _, _, _ in STAGES],
              "rational_cover_obtained": True, "genus": 40, "branch_degree": 18,
              "square_map_precision_digits": 128, "arithmetic_identification_obtained": False,
              "global_twist_identified": False}
    job = jobs.run_job(jobs.magma_command(template), DATA / "cm_frame_B3_rational_check.out", 180,
                       "PASS|155_CM_FRAME_B3_RATIONAL_CHECK")
    job["sources"] = [checks.source(p) for p in inputs]
    report["independent_check"] = job
    write_json(path, report)
    print("independent rational cover", job["status"], round(job["wall_seconds"], 3), flush=True)
    if job["status"] != "pass":
        raise RuntimeError("independent rational cover check failed")
    negative = DATA / "cm_frame_B3_rational_twist_control.m"
    needle = 'load "dembele/data/computed/cm_frame_B3_rational_model.m";'
    text = template.read_text().replace(needle, needle
        +"\nrational_denominator := [-x:x in rational_denominator];\nrational_veronese_scale := -rational_veronese_scale;")
    assert text != template.read_text()
    negative.write_text(text)
    job = jobs.run_job(jobs.magma_command(negative), negative.with_suffix(".out"), 180,
                       "PASS|155_CM_FRAME_B3_RATIONAL_CHECK", expected_failure="assert cover_left eq cover_right")
    job["sources"] = [checks.source(negative)]+[checks.source(p) for p in inputs]
    job["mutation"] = "negate the rational denominator and its Veronese scale; exact divisors unchanged"
    report["negative_control"] = job
    report["status"] = job["status"]
    write_json(path, report)
    if job["status"] != "pass":
        raise RuntimeError("wrong global twist was not rejected by the saved local square map")
    checks.verify_records(report)
    print("wrong twist control", job["status"], round(job["wall_seconds"], 3), flush=True)
    print("PASS: exact Q cover on C with branch degree 18 and genus 40; local scalar checked through 31^128.")


if __name__ == "__main__":
    main()

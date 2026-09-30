"""D74: certify the reduced denominator space and collect recognition evidence.

Default runs the independent space check and a newest-digit error control.
--recognize also repeats the bounded recognition and basis computations.
--collect-only validates the saved arithmetic/provenance without recomputation.
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


jobs = module("job_helpers", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = module("check_helpers", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
source = checks.source


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--recognize", action="store_true")
    modes.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    report_path = DATA / "cm_frame_arithmetic_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        checks.verify_records(report)
        assert report["status"] == report["space_check"]["status"] == report["negative_control"]["status"] == "pass"
        print("PASS: D74 lift to 31^128, reduced 17-dimensional space and bounded recognition records.")
        return
    definitions = [
        ("pari/132_cm_frame_denominator_recognition.py", "cm_frame_denominator_recognition", 240,
         "PASS|132_CM_FRAME_DENOMINATOR_RECOGNITION"),
        ("pari/133_cm_frame_projective_denominator.py", "cm_frame_projective_denominator", 300,
         "PASS|133_CM_FRAME_PROJECTIVE_DENOMINATOR"),
        ("magma/134_cm_frame_denominator_space.m", "cm_frame_denominator_space", 180,
         "PASS|134_CM_FRAME_DENOMINATOR_SPACE"),
        ("pari/135_cm_frame_denominator_space_reduction.py", "cm_frame_denominator_space_reduced", 300,
         "PASS|135_CM_FRAME_DENOMINATOR_SPACE_REDUCTION")]
    if args.recognize:
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d74-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        for relative, name, timeout, marker in definitions:
            script = ROOT / "dembele" / relative
            command = jobs.magma_command(script) if script.suffix == ".m" else [jobs.SAGE, "-python", str(script)]
            job = jobs.run_job(command, DATA / (name+".out"), timeout, marker,
                               env=env if script.suffix == ".py" else None)
            job["sources"] = [source(script)]
            if script.suffix == ".m":
                job["sources"] += [source(DATA / p) for p in (
                    "cm_frame_curve_candidate.m", "cm_frame_numerator_lattice.m", "cm_frame_normalized_resolvent.m")]
            else:
                job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
            write_json(DATA / (name+"_job.json"), job)
            print(name, job["status"], round(job["wall_seconds"], 3), flush=True)
            if job["status"] != "pass":
                raise RuntimeError(f"{name}: {job['status']}")
    job_records = []
    for relative, name, timeout, marker in definitions:
        job_path = DATA / (name+"_job.json")
        checks.read_job(job_path, marker)
        job_records.append(source(job_path))
    space_path = DATA / "cm_frame_denominator_space_reduced.json"
    space = json.loads(space_path.read_text())
    checks.verify_records(space)
    assert space["status"] == "pass" and space["space_dimension"] == 17
    coordinates = space["denominator_basis_coefficients"]["128"]
    coordinates_path = DATA / "cm_frame_denominator_space_coordinates.m"
    coordinates_path.write_text("// D74 denominator coordinates modulo 31^128 in the exact reduced space.\n"
                                +"space_denominator_coordinates := "+str(coordinates)+";\n")
    script = ROOT / "dembele/magma/136_cm_frame_denominator_space_check.m"
    job = jobs.run_job(jobs.magma_command(script), DATA / "cm_frame_denominator_space_check.out", 180,
                       "PASS|136_CM_FRAME_DENOMINATOR_SPACE_CHECK")
    inputs = [script, coordinates_path, DATA / "cm_frame_denominator_space_reduced.m",
              DATA / "cm_frame_doubling_normalized_128.m", DATA / "cm_frame_curve_candidate.m"]
    job["sources"] = [source(p) for p in inputs]
    report = {"status": job["status"], "milestone": "D74", "date": "2026-09-18", "space_check": job,
              "sources": [source(p) for p in (__file__, ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          DATA / "cm_frame_doubling_check.json", space_path,
                          DATA / "cm_frame_denominator_recognition.json", DATA / "cm_frame_projective_denominator.json",
                          DATA / "cm_frame_denominator_space_nullspace_probe.json")]
                         +job_records}
    write_json(report_path, report)
    print("space certificate", job["status"], round(job["wall_seconds"], 3), flush=True)
    if job["status"] != "pass":
        print(Path(job["log"]["path"]).read_text()[-3500:])
        raise RuntimeError("independent space check failed")
    control = DATA / "cm_frame_denominator_space_negative_control.m"
    needle = 'load "dembele/data/computed/cm_frame_denominator_space_coordinates.m";'
    content = script.read_text().replace(needle, needle
              +"\nspace_denominator_coordinates[1] +:= normalized_modulus div 31;")
    assert content != script.read_text()
    control.write_text(content)
    negative = jobs.run_job(jobs.magma_command(control), control.with_suffix(".out"), 180,
                            "PASS|136_CM_FRAME_DENOMINATOR_SPACE_CHECK",
                            expected_failure="assert &and[Numerator(c) mod normalized_modulus eq 0")
    negative["sources"] = [source(control)]+[source(p) for p in inputs]
    negative["mutation"] = "add 31^127 to the first denominator basis coordinate"
    negative["lower_precision_preserved"] = True
    report["negative_control"] = negative
    if negative["status"] != "pass":
        report["status"] = "failed"
        write_json(report_path, report)
        raise RuntimeError("coordinate corruption was not rejected")
    report.update({"status": "pass", "precision_digits": 128, "denominator_space_dimension": 17,
                   "reduced_section_height_digits": space["section_height_decimal_digits"],
                   "number_field_cover_obtained": False, "Shimura_identification_certified": False,
                   "target_field_polynomial_obtained": False})
    write_json(report_path, report)
    checks.verify_records(report)
    print("PASS: exact reduced denominator space, unchanged 128-digit denominator, corruption rejected.")


if __name__ == "__main__":
    main()

"""D75: certify the B3 normalization and reject a wrong quadratic twist.

Default collects the exact numerator and finite-field transfer, then runs
an independent Magma verifier and a sign-corruption control. --rebuild
repeats the numerator search and transfer. --collect-only checks provenance.
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


jobs = module("B3_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = module("B3_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
source = checks.source


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2)+"\n")


def field(output, label):
    match = re.search(r"^"+re.escape(label)+r"\|(.*?)(?=^[A-Z][A-Z_0-9]*\||^Loading |\Z)",
                      output, re.M | re.S)
    assert match is not None, label
    return ast.literal_eval(match.group(1).strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--rebuild", action="store_true")
    mode.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    report_path = DATA / "cm_frame_B3_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        checks.verify_records(report)
        assert report["status"] == report["independent_check"]["status"] == report["negative_control"]["status"] == "pass"
        print("PASS: D75 height-583 numerator, B3 square transfer at 31 and wrong-twist rejection.")
        return
    definitions = [
        ("pari/142_cm_frame_B3_numerator.py", "cm_frame_B3_numerator", 240, "PASS|142_CM_FRAME_B3_NUMERATOR"),
        ("magma/143_cm_frame_B3_transfer.m", "cm_frame_B3_transfer", 180, "PASS|143_CM_FRAME_B3_TRANSFER")]
    if args.rebuild:
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d75-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        for relative, name, timeout, marker in definitions:
            script = ROOT / "dembele" / relative
            command = jobs.magma_command(script) if script.suffix == ".m" else [jobs.SAGE, "-python", str(script)]
            job = jobs.run_job(command, DATA / (name+".out"), timeout, marker,
                               env=env if script.suffix == ".py" else None)
            job["sources"] = [source(script), source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
            if script.suffix == ".m":
                job["sources"] += [source(DATA / p) for p in (
                    "cm_frame_curve_candidate.m", "cm_frame_marks.m", "cm_frame_resolvent.m", "cm_frame_B3_numerator.m")]
            else:
                job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
            write_json(DATA / (name+"_job.json"), job)
            print(name, job["status"], round(job["wall_seconds"], 3), flush=True)
            if job["status"] != "pass":
                raise RuntimeError(f"{name}: {job['status']}")
    for relative, name, timeout, marker in definitions:
        checks.read_job(DATA / (name+"_job.json"), marker)
    lattice_path = DATA / "cm_frame_B3_numerator.json"
    lattice = json.loads(lattice_path.read_text())
    checks.verify_records(lattice)
    assert lattice["status"] == "pass"
    output = (DATA / "cm_frame_B3_transfer.out").read_text()
    selected = field(output, "SELECTED_CANDIDATE")-1
    numerator = field(output, "NEW_NUMERATOR")
    candidate = lattice["candidates"][selected]
    assert numerator == candidate["coefficients"] and max(abs(x) for x in numerator) == int(candidate["height"])
    fields = {
        "B3_new_numerator": numerator,
        "B3_new_denominator": field(output, "NEW_DENOMINATOR_MOD31"),
        "B3_square_numerator": field(output, "SQUARE_FACTOR_NUMERATOR_MOD31"),
        "B3_square_denominator": field(output, "SQUARE_FACTOR_DENOMINATOR_MOD31"),
        "B3_new_E_quadrics": field(output, "NEW_E_QUADRICS_MOD31"),
        "B3_moving_section_basis": field(output, "MOVING_SECTION_BASIS_MOD31")}
    assert all(len(fields[k]) == 136 for k in (
        "B3_new_numerator", "B3_new_denominator", "B3_square_numerator", "B3_square_denominator"))
    assert len(fields["B3_moving_section_basis"]) == 3
    pair_path = DATA / "cm_frame_B3_normalization.json"
    pair = {"status": "pass", "milestone": "D75", "date": "2026-09-18",
            "sources": [source(p) for p in (__file__, lattice_path, DATA / "cm_frame_B3_numerator_job.json",
                        DATA / "cm_frame_B3_transfer_job.json", DATA / "cm_frame_resolvent_check.json")],
            "selected_candidate_one_based": selected+1, "numerator_height": candidate["height"],
            "numerator_height_digits": candidate["height_decimal_digits"],
            "numerator_exact_over_Q": True, "transfer_precision_digits": 1, "transfer_prime": 31,
            "divisor_identity": "D17+P32+2*B3-2*E_new", "new_E_degree": 18,
            "common_residual_degree": 24, "moving_section_space_dimension": 3,
            "coordinate_change": "w_new = w_old*g/q; n_new/d_new = (n_old/d_old)*(g/q)^2",
            "rational_residual_certificate": "integral-at-31 vanishing and reduced disjoint residual at good reduction",
            "number_field_denominator_obtained": False, "higher_precision_transfer_performed": False,
            "data": fields}
    write_json(pair_path, pair)
    data_path = DATA / "cm_frame_B3_transfer.m"
    data_path.write_text("// D75: exact Q numerator; denominator and square factor only modulo 31.\n"
                        +"\n".join(f"{key} := {value};" for key, value in fields.items())+"\n")
    script = ROOT / "dembele/magma/145_cm_frame_B3_check.m"
    inputs = [script, data_path, DATA / "cm_frame_curve_candidate.m", DATA / "cm_frame_marks.m",
              DATA / "cm_frame_resolvent.m"]
    job = jobs.run_job(jobs.magma_command(script), DATA / "cm_frame_B3_check.out", 180, "PASS|145_CM_FRAME_B3_CHECK")
    job["sources"] = [source(p) for p in inputs]
    report = {"status": job["status"], "milestone": "D75", "date": "2026-09-18", "independent_check": job,
              "sources": [source(p) for p in (__file__, pair_path, DATA / "cm_frame_joint_field_check.json",
                          DATA / "cm_frame_B3_rational_ideal_probe.json",
                          ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")],
              "numerator_height": candidate["height"], "transfer_precision_digits": 1,
              "old_128_digit_lift_preserved": True, "number_field_cover_obtained": False}
    write_json(report_path, report)
    print("B3 certificate", job["status"], round(job["wall_seconds"], 3), flush=True)
    if job["status"] != "pass":
        print(Path(job["log"]["path"]).read_text()[-4000:])
        raise RuntimeError("independent B3 check failed")
    negative_path = DATA / "cm_frame_B3_negative_control.m"
    needle = 'load "dembele/data/computed/cm_frame_B3_transfer.m";'
    content = script.read_text().replace(needle, needle
              +"\nB3_new_denominator := [(-c) mod 31:c in B3_new_denominator];")
    assert content != script.read_text()
    negative_path.write_text(content)
    negative = jobs.run_job(jobs.magma_command(negative_path), negative_path.with_suffix(".out"), 180,
                            "PASS|145_CM_FRAME_B3_CHECK", expected_failure="assert left eq right")
    negative["sources"] = [source(negative_path)]+[source(p) for p in inputs]
    negative["mutation"] = "negate the denominator: divisor unchanged, nonsquare twist by -1 in F31"
    report["negative_control"] = negative
    report["status"] = negative["status"]
    write_json(report_path, report)
    if negative["status"] != "pass":
        raise RuntimeError("wrong twist was not rejected")
    checks.verify_records(report)
    print("PASS: exact height-583 numerator, same square class at 31, wrong twist rejected.")


if __name__ == "__main__":
    main()

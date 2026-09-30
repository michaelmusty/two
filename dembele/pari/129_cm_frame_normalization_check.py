"""Reproduce, certify, or collect the D73 numerator normalization experiment.

The exact rational numerator is paired with a denominator modulo 31^8.
The global cross-product identity preserves the D72 radicand at that
precision. This does not reconstruct the denominator over a number field.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
MAGMA = "/Applications/Magma/magma"
SAGE = "/usr/local/bin/sage"
ERRORS = ("Runtime error", "User error", "Assertion failed", "Error:", "Traceback (most recent call last)")


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def verify_records(obj, visited=None):
    """Verify every linked source, transitively through JSON certificates."""
    if visited is None:
        visited = set()
    if isinstance(obj, dict):
        if "path" in obj and "sha256" in obj:
            p = Path(obj["path"])
            assert source(p)["sha256"] == obj["sha256"], f"changed source: {p}"
            if p.suffix == ".json" and str(p) not in visited:
                visited.add(str(p))
                verify_records(json.loads(p.read_text()), visited)
        else:
            for v in obj.values():
                verify_records(v, visited)
    elif isinstance(obj, list):
        for v in obj:
            verify_records(v, visited)
    return visited


def read_job(path, marker):
    job = json.loads(path.read_text())
    verify_records(job)
    assert job["status"] == "pass"
    output = Path(job["log"]["path"]).read_text()
    assert marker in output and not any(e in output for e in ERRORS)
    return job


def field(output, label):
    match = re.search(r"^" + re.escape(label) + r"\|(.*?)(?=^[A-Z_]+\||^Loading |\Z)", output, re.M | re.S)
    assert match is not None, label
    return ast.literal_eval(match.group(1).strip())


def collect_transfer():
    lattice = json.loads((DATA / "cm_frame_numerator_lattice.json").read_text())
    verify_records(lattice)
    assert lattice["status"] == "pass"
    read_job(DATA / "cm_frame_numerator_lattice_job.json", "PASS|127_CM_FRAME_NUMERATOR_LATTICE")
    job = read_job(DATA / "cm_frame_normalization_transfer_job.json", "PASS|128_CM_FRAME_NORMALIZATION_TRANSFER")
    output = Path(job["log"]["path"]).read_text()
    selected = field(output, "SELECTED_CANDIDATE") - 1
    candidate = lattice["candidates"][selected]
    num, den = field(output, "NORMALIZED_NUMERATOR"), field(output, "NORMALIZED_DENOMINATOR")
    assert num == candidate["coefficients"] and len(num) == len(den) == 136
    modulus = field(output, "MODULUS")
    assert modulus == 31**8 and all(0 <= c < modulus for c in den)
    h, coords = field(output, "RESIDUAL_MODULUS"), field(output, "RESIDUAL_COORDINATES")
    factors = field(output, "RESIDUAL_FACTOR_DEGREES")
    assert len(h) == 29 and len(coords) == 16 and sum(factors) == 28
    report = {
        "status": "pass", "milestone": "D73", "date": "2026-09-18",
        "sources": [source(p) for p in (__file__, DATA / "cm_frame_numerator_lattice.json",
                    DATA / "cm_frame_numerator_lattice.m", DATA / "cm_frame_numerator_lattice_job.json",
                    DATA / "cm_frame_normalization_transfer_job.json", DATA / "cm_frame_resolvent_lift.json",
                    DATA / "cm_frame_resolvent_lift_check.json")],
        "precision_digits": 8, "modulus": modulus,
        "selected_candidate_one_based": selected + 1,
        "numerator_coefficients": num, "denominator_coefficients": den,
        "numerator_is_exact_over_Q": True,
        "numerator_primitive_height": candidate["height"],
        "numerator_primitive_height_decimal_digits": candidate["height_decimal_digits"],
        "numerator_primitive_height_bits": candidate["height_bits"],
        "section_chart_indices_zero_based": lattice["section_chart_indices_zero_based"],
        "residual_modulus_mod31": h, "residual_coordinates_mod31": coords,
        "residual_factor_degrees": factors,
        "multiplication_rank": field(output, "MULTIPLICATION_RANK"),
        "quartic_coordinate_count": field(output, "QUARTIC_COORDINATES"),
        "identity": "q_num*q_den_new = q_num_new*q_den in the coordinate ring modulo 31^8",
        "number_field_denominator_obtained": False, "denominator_height_bound_obtained": False,
    }
    (DATA / "cm_frame_normalized_resolvent.json").write_text(json.dumps(report, indent=2)+"\n")
    bindings = (("normalized_modulus", modulus), ("normalized_numerator", num),
                ("normalized_denominator", den), ("normalized_residual_modulus", h),
                ("normalized_residual_coordinates", coords))
    (DATA / "cm_frame_normalized_resolvent.m").write_text(
        "// D73: exact rational numerator; denominator only modulo the displayed modulus.\n"
        + "\n".join(f"{name} := {value};" for name, value in bindings)+"\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--rebuild", action="store_true")
    modes.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    helper_path = ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"
    spec = importlib.util.spec_from_file_location("job_helpers", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    report_path = DATA / "cm_frame_normalization_check.json"
    script = ROOT / "dembele/magma/129_cm_frame_normalization_check.m"
    if args.rebuild:
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d73-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        solver = ROOT / "dembele/pari/127_cm_frame_numerator_lattice.py"
        job = helper.run_job([SAGE, "-python", str(solver)], DATA / "cm_frame_numerator_lattice.out",
                             240, "PASS|127_CM_FRAME_NUMERATOR_LATTICE", env=env)
        job["sources"] = [source(solver)]
        job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
        (DATA / "cm_frame_numerator_lattice_job.json").write_text(json.dumps(job, indent=2)+"\n")
        if job["status"] != "pass":
            raise RuntimeError(f"lattice job {job['status']}")
        transfer = ROOT / "dembele/magma/128_cm_frame_normalization_transfer.m"
        job = helper.run_job(helper.magma_command(transfer), DATA / "cm_frame_normalization_transfer.out",
                             180, "PASS|128_CM_FRAME_NORMALIZATION_TRANSFER")
        job["sources"] = [source(p) for p in (transfer, DATA / "cm_frame_curve_candidate.m",
                          DATA / "cm_frame_marks.m", DATA / "cm_frame_resolvent.m",
                          DATA / "cm_frame_resolvent_lift.m", DATA / "cm_frame_numerator_lattice.m")]
        (DATA / "cm_frame_normalization_transfer_job.json").write_text(json.dumps(job, indent=2)+"\n")
        if job["status"] != "pass":
            raise RuntimeError(f"transfer job {job['status']}")
    if args.collect_only:
        report = json.loads(report_path.read_text())
        verify_records(report)
        pair = json.loads((DATA / "cm_frame_normalized_resolvent.json").read_text())
        assert report["status"] == report["job"]["status"] == report["negative_control"]["status"] == "pass"
    else:
        pair = collect_transfer()
        job = helper.run_job(helper.magma_command(script), DATA / "cm_frame_normalization_check.out",
                             180, "PASS|129_CM_FRAME_NORMALIZATION_CHECK")
        report = {"status": job["status"], "milestone": "D73", "date": "2026-09-18", "job": job,
                  "sources": [source(p) for p in (__file__, helper_path, script,
                              DATA / "cm_frame_normalized_resolvent.json", DATA / "cm_frame_normalized_resolvent.m",
                              DATA / "cm_frame_curve_candidate.m", DATA / "cm_frame_marks.m",
                              DATA / "cm_frame_resolvent_lift.m", DATA / "cm_frame_resolvent.m")]}
        report_path.write_text(json.dumps(report, indent=2)+"\n")
        print("certificate", job["status"], f"{job['wall_seconds']:.3f}s", flush=True)
        if job["status"] != "pass":
            print(Path(job["log"]["path"]).read_text()[-4000:])
            raise SystemExit(1)
        needle = 'load "dembele/data/computed/cm_frame_normalized_resolvent.m";'
        control = DATA / "cm_frame_normalization_negative_control.m"
        control.write_text(script.read_text().replace(
            needle, needle + "\nnormalized_denominator[1] +:= normalized_modulus div 31;"))
        negative = helper.run_job(helper.magma_command(control), control.with_suffix(".out"), 180,
                                  "PASS|129_CM_FRAME_NORMALIZATION_CHECK",
                                  expected_failure="assert &and[Numerator(c) mod normalized_modulus eq 0")
        negative["mutation"] = "add 31^7 to the denominator's X1^2 coefficient"
        negative["lower_precision_preserved"] = True
        report["negative_control"] = negative
        report["sources"].append(source(control))
        if negative["status"] != "pass":
            report["status"] = "failed"
            report_path.write_text(json.dumps(report, indent=2)+"\n")
            raise RuntimeError("highest-digit corruption was not rejected as expected")
        report.update({"status": "pass", "modulus": pair["modulus"], "same_radicand_verified": True,
                       "exact_rational_numerator_verified": True,
                       "numerator_height_decimal_digits": pair["numerator_primitive_height_decimal_digits"],
                       "residual_factor_degrees": pair["residual_factor_degrees"],
                       "divisor_identity": "D17 + 15*P32 - 2*E",
                       "number_field_cover_obtained": False, "Shimura_identification_certified": False,
                       "genus64_cover_constructed": False, "target_field_polynomial_obtained": False})
        report_path.write_text(json.dumps(report, indent=2)+"\n")
        verify_records(report)
    print(f"PASS: {pair['numerator_primitive_height_decimal_digits']}-digit exact numerator; "
          "same radicand modulo 31^8; highest-digit corruption rejected.")


if __name__ == "__main__":
    main()

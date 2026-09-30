"""D74: certify each doubling stage and transfer to D73's short numerator.

Generate copies of the independent D72/D73 Magma verifiers with only the
data paths changed. Keep both the templates and generated sources hashed.
Default checks saved doubling output; --lift reproduces it first.
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
checks = module("hash_helpers", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
source, verify = checks.source, checks.verify_records


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2)+"\n")


def magma_data(lift, path):
    lines = ["// D74: precision doubling, preserving the D72 scale convention."]
    for name, key in (("lift_modulus", "modulus"), ("lift_numerator", "numerator_coefficients"),
                      ("lift_denominator", "denominator_coefficients"), ("lift_point_jets", "point_jets")):
        lines.append(f"{name} := {lift[key]};")
    lines.append("lift_components := [*")
    for i, c in enumerate(lift["components"]):
        fields = [json.dumps(c["label"]), str(c["degree"]), str(c["etale_modulus"]),
                  str(c["coordinates"]), str(c["tangent"]), str(c.get("second_jet_mod31", []))]
        lines.append("<"+",".join(fields)+">"+("," if i+1 < len(lift["components"]) else ""))
    lines.append("*];")
    path.write_text("\n".join(lines)+"\n")


def generated_script(template, output, replacements):
    content = template.read_text()
    for old, new in replacements:
        assert content.count(old) == 1, old
        content = content.replace(old, new)
    output.write_text("// D74 generated verifier/transfer; only the displayed data paths differ.\n"+content)


def run_magma(script, marker, sources, expected_failure=None):
    job = jobs.run_job(jobs.magma_command(script), script.with_suffix(".out"), 240,
                       marker, expected_failure=expected_failure)
    job["sources"] = [source(p) for p in [script]+sources]
    print(script.stem, job["status"], f"{job['wall_seconds']:.3f}s", flush=True)
    if job["status"] != "pass":
        write_json(script.with_suffix(".job.json"), job)
        print(script.with_suffix(".out").read_text()[-3500:])
        raise RuntimeError(f"{script.name}: {job['status']}")
    return job


def check_compatibility(lift, previous):
    modulus = previous["modulus"]
    for key in ("numerator_coefficients", "denominator_coefficients"):
        assert [v % modulus for v in lift[key]] == previous[key]
    assert [[v % modulus for v in row] for row in lift["point_jets"]] == previous["point_jets"]
    pc = {(c["label"], tuple(c["etale_modulus"])): c for c in previous["components"]}
    for c in lift["components"]:
        old = pc[c["label"], tuple(c["etale_modulus"])]
        for key in ("coordinates", "tangent"):
            assert [[v % modulus for v in row] for row in c[key]] == old[key]
    assert lift["precision_digits"] == 2*previous["precision_digits"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--lift", action="store_true")
    modes.add_argument("--collect-only", action="store_true")
    parser.add_argument("--digits", type=int, choices=(16, 32, 64, 128, 256), default=128)
    args = parser.parse_args()
    report_path = DATA / "cm_frame_doubling_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        verify(report)
        assert report["status"] == report["negative_control"]["status"] == "pass"
        assert all(stage[k]["status"] == "pass" for stage in report["stages"]
                   for k in ("divisor_check", "transfer", "normalization_check"))
        print("PASS: saved doubling, transfer, independent checks and corruption control through 31^"
              +str(report["final_precision_digits"]))
        return
    if args.lift:
        solver = ROOT / "dembele/pari/130_cm_frame_precision_doubling.py"
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d74-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        job = jobs.run_job([jobs.SAGE, "-python", str(solver), "--digits", str(args.digits)],
                           DATA / "cm_frame_doubling.out", 900,
                           f"PASS|130_CM_FRAME_DOUBLING_COMPLETE {args.digits} ", env=env)
        job["sources"] = [source(solver)]
        job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
        write_json(DATA / "cm_frame_doubling_job.json", job)
        if job["status"] != "pass":
            raise RuntimeError(f"doubling solver: {job['status']}")
    solver_report = json.loads((DATA / "cm_frame_doubling.json").read_text())
    verify(solver_report)
    checks.read_job(DATA / "cm_frame_doubling_job.json", "PASS|130_CM_FRAME_DOUBLING_COMPLETE")
    assert solver_report["status"] == "pass" and solver_report["control_4_to_8_exact_agreement"]
    previous = json.loads((DATA / "cm_frame_resolvent_lift_8.json").read_text())
    short = json.loads((DATA / "cm_frame_normalized_resolvent.json").read_text())
    previous_short = short
    templates = [ROOT / f"dembele/magma/{name}" for name in (
        "125_cm_frame_resolvent_lift_check.m", "128_cm_frame_normalization_transfer.m",
        "129_cm_frame_normalization_check.m")]
    original_load = 'load "dembele/data/computed/cm_frame_resolvent_lift.m";'
    short_load = 'load "dembele/data/computed/cm_frame_normalized_resolvent.m";'
    common = [DATA / name for name in ("cm_frame_curve_candidate.m", "cm_frame_marks.m", "cm_frame_resolvent.m")]
    report = {"status": "running", "milestone": "D74", "date": "2026-09-18", "stages": [],
              "sources": [source(p) for p in (__file__, ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          DATA / "cm_frame_doubling.json", DATA / "cm_frame_doubling_job.json",
                          DATA / "cm_frame_normalization_check.json")]}
    for record in solver_report["stages"]:
        path = Path(record["path"])
        lift = json.loads(path.read_text())
        check_compatibility(lift, previous)
        digits = lift["precision_digits"]
        data_m = path.with_suffix(".m")
        magma_data(lift, data_m)
        replacement = (original_load, f'load "{data_m.relative_to(ROOT)}";')
        divisor = DATA / f"cm_frame_doubling_divisor_check_{digits}.m"
        generated_script(templates[0], divisor, [replacement])
        divisor_job = run_magma(divisor, "PASS|125_CM_FRAME_RESOLVENT_LIFT_CHECK",
                               [templates[0], path, data_m]+common)
        transfer = DATA / f"cm_frame_doubling_transfer_{digits}.m"
        generated_script(templates[1], transfer, [replacement])
        transfer_job = run_magma(transfer, "PASS|128_CM_FRAME_NORMALIZATION_TRANSFER",
                                [templates[1], path, data_m, DATA / "cm_frame_numerator_lattice.m"]+common)
        output = transfer.with_suffix(".out").read_text()
        numerator = checks.field(output, "NORMALIZED_NUMERATOR")
        denominator = checks.field(output, "NORMALIZED_DENOMINATOR")
        assert numerator == short["numerator_coefficients"]
        assert [v % previous_short["modulus"] for v in denominator] == previous_short["denominator_coefficients"]
        assert checks.field(output, "MODULUS") == lift["modulus"]
        assert checks.field(output, "RESIDUAL_MODULUS") == short["residual_modulus_mod31"]
        assert checks.field(output, "RESIDUAL_COORDINATES") == short["residual_coordinates_mod31"]
        pair = {"status": "pass", "milestone": "D74", "precision_digits": digits, "modulus": lift["modulus"],
                "sources": [source(path), source(transfer), source(transfer.with_suffix(".out")),
                            source(DATA / "cm_frame_normalized_resolvent.json")],
                "numerator_coefficients": numerator, "denominator_coefficients": denominator,
                "section_chart_indices_zero_based": lift["section_chart_indices_zero_based"],
                "residual_modulus_mod31": short["residual_modulus_mod31"],
                "residual_coordinates_mod31": short["residual_coordinates_mod31"],
                "numerator_is_exact_over_Q": True, "number_field_denominator_obtained": False}
        pair_path = DATA / f"cm_frame_doubling_normalized_{digits}.json"
        write_json(pair_path, pair)
        pair_m = pair_path.with_suffix(".m")
        pairs = (("normalized_modulus", "modulus"), ("normalized_numerator", "numerator_coefficients"),
                 ("normalized_denominator", "denominator_coefficients"),
                 ("normalized_residual_modulus", "residual_modulus_mod31"),
                 ("normalized_residual_coordinates", "residual_coordinates_mod31"))
        pair_m.write_text("// D74 short numerator transfer; finite-precision denominator.\n"
                          +"\n".join(f"{name} := {pair[key]};" for name, key in pairs)+"\n")
        normalized = DATA / f"cm_frame_doubling_normalization_check_{digits}.m"
        new_short_load = f'load "{pair_m.relative_to(ROOT)}";'
        generated_script(templates[2], normalized, [replacement, (short_load, new_short_load)])
        normalized_job = run_magma(normalized, "PASS|129_CM_FRAME_NORMALIZATION_CHECK",
                                  [templates[2], path, data_m, pair_path, pair_m]+common)
        report["stages"].append({"precision_digits": digits, "data": source(path),
                                 "normalized_data": source(pair_path), "divisor_check": divisor_job,
                                 "transfer": transfer_job, "normalization_check": normalized_job})
        write_json(report_path, report)
        previous, previous_short = lift, pair
    control = DATA / "cm_frame_doubling_negative_control.m"
    content = normalized.read_text().replace(new_short_load, new_short_load
                  +"\nnormalized_denominator[1] +:= normalized_modulus div 31;")
    assert content != normalized.read_text()
    control.write_text(content)
    negative = run_magma(control, "PASS|129_CM_FRAME_NORMALIZATION_CHECK",
                         [normalized, data_m, pair_m]+common,
                         expected_failure="assert &and[Numerator(c) mod normalized_modulus eq 0")
    negative["mutation"] = f"add 31^{digits-1} to denominator coefficient X1^2"
    negative["lower_precision_preserved"] = True
    report.update({"status": "pass", "final_precision_digits": digits, "negative_control": negative,
                   "control_4_to_8_exact_agreement": True, "compatible_at_all_saved_stages": True,
                   "same_radicand_at_each_stage": True, "number_field_cover_obtained": False,
                   "Shimura_identification_certified": False, "target_field_polynomial_obtained": False})
    write_json(report_path, report)
    verify(report)
    print(f"PASS: independent divisors and unchanged radicand through 31^{digits}; highest-digit error rejected.")


if __name__ == "__main__":
    main()

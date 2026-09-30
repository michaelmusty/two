"""D76: collect and independently check the B3 transfer at 64 and 128 digits.

--rebuild repeats the linear g-space lifts and multiplication-kernel
construction. Default checks the saved results and a highest-digit error.
--collect-only validates all saved provenance without arithmetic reruns.
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


jobs = module("B3_lift_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = module("B3_lift_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
parser_helpers = module("B3_lift_fields", ROOT / "dembele/pari/144_cm_frame_B3_check.py")
source = checks.source


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2)+"\n")


def generate(template, target, digits):
    text = template.read_text()
    for name in ("cm_frame_B3_moving", "cm_frame_B3_product_lift", "cm_frame_doubling"):
        text = text.replace(name+"_128.m", name+f"_{digits}.m")
    target.write_text("// D76 generated copy: only the input precision paths change.\n"+text)


def collect(digits):
    job_path = DATA / f"cm_frame_B3_product_space_{digits}_job.json"
    checks.read_job(job_path, "PASS|147_CM_FRAME_B3_PRODUCT_SPACE")
    moving_path = DATA / f"cm_frame_B3_moving_{digits}.json"
    moving = json.loads(moving_path.read_text())
    checks.verify_records(moving)
    output = (DATA / f"cm_frame_B3_product_space_{digits}.out").read_text()
    fields = {
        "product_h": "H_COEFFICIENTS", "product_q_basis": "Q_BASIS_COEFFICIENTS",
        "product_q_witnesses": "Q_WITNESS_COEFFICIENTS", "product_indices": "PRODUCT_INDICES",
        "product_denominators": "PRODUCT_DENOMINATOR_COEFFICIENTS",
        "product_space_rank": "PRODUCT_SPACE_RANK_MOD31", "product_selected_q": "SELECTED_Q_COEFFICIENTS",
        "product_selected_denominator": "SELECTED_DENOMINATOR_COEFFICIENTS"}
    data = {name: parser_helpers.field(output, label) for name, label in fields.items()}
    data["product_modulus"] = parser_helpers.field(output, "MODULUS")
    data["product_g"] = moving["g_coefficients"]
    h_index = parser_helpers.field(output, "H_BASIS_INDEX")-1
    assert data["product_h"] == moving["g_space_basis"][h_index]
    assert data["product_modulus"] == 31**digits
    assert len(data["product_q_basis"]) == len(data["product_q_witnesses"]) == 3
    assert len(data["product_denominators"]) == 6
    report = {"status": "pass", "milestone": "D76", "date": "2026-09-18",
              "sources": [source(p) for p in (__file__, job_path, moving_path,
                          DATA / "cm_frame_B3_moving_job.json", DATA / "cm_frame_B3_moving.json",
                          ROOT / "dembele/pari/144_cm_frame_B3_check.py")],
              "precision_digits": digits, "h_basis_index_one_based": h_index+1,
              "moving_kernel_rank": parser_helpers.field(output, "MOVING_KERNEL_RANK"),
              "degree_eight_coordinates": parser_helpers.field(output, "DEGREE_EIGHT_COORDINATES"),
              "section_chart_indices_zero_based": moving["section_chart_indices_zero_based"],
              "new_numerator_coefficients": moving["new_numerator_coefficients"],
              "data": data, "number_field_cover_obtained": False,
              "identity": "n_old*g^2*d_ij = n_new*d_old*q_i*q_j; selected q gives the square map"}
    path = DATA / f"cm_frame_B3_product_lift_{digits}.json"
    write_json(path, report)
    path.with_suffix(".m").write_text("// D76 finite-precision product sections and exact square map.\n"
        +"\n".join(f"{name} := {value};" for name, value in data.items())+"\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--rebuild", action="store_true")
    modes.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    report_path = DATA / "cm_frame_B3_lift_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        checks.verify_records(report)
        assert report["status"] == report["negative_control"]["status"] == "pass"
        assert all(v["status"] == "pass" for v in report["independent_checks"])
        print("PASS: B3 square transfer and six-product space at 31^64 and 31^128.")
        return
    if args.rebuild:
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d76-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        script = ROOT / "dembele/pari/146_cm_frame_B3_moving_sections.py"
        job = jobs.run_job([jobs.SAGE, "-python", str(script)], DATA / "cm_frame_B3_moving.out", 180,
                           "PASS|146_CM_FRAME_B3_MOVING_SECTIONS", env=env)
        job["sources"] = [source(script), source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
        job["environment"] = {k: env[k] for k in ("DOT_SAGE", "OPENBLAS_NUM_THREADS")}
        write_json(DATA / "cm_frame_B3_moving_job.json", job)
        if job["status"] != "pass":
            raise RuntimeError(f"moving section lift: {job['status']}")
        template = ROOT / "dembele/magma/147_cm_frame_B3_product_space.m"
        for digits in (64, 128):
            script = DATA / f"cm_frame_B3_product_space_{digits}.m"
            generate(template, script, digits)
            job = jobs.run_job(jobs.magma_command(script), script.with_suffix(".out"), 180,
                               "PASS|147_CM_FRAME_B3_PRODUCT_SPACE")
            job["sources"] = [source(p) for p in (template, script, DATA / f"cm_frame_B3_moving_{digits}.m",
                              DATA / "cm_frame_B3_transfer.m", DATA / "cm_frame_curve_candidate.m",
                              DATA / "cm_frame_marks.m", DATA / "cm_frame_resolvent.m",
                              ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
            write_json(DATA / f"cm_frame_B3_product_space_{digits}_job.json", job)
            print("product space", digits, job["status"], round(job["wall_seconds"], 3), flush=True)
            if job["status"] != "pass":
                raise RuntimeError(f"product space {digits}: {job['status']}")
    checks.read_job(DATA / "cm_frame_B3_moving_job.json", "PASS|146_CM_FRAME_B3_MOVING_SECTIONS")
    stages = [collect(digits) for digits in (64, 128)]
    lower, upper = [s["data"] for s in stages]
    m = lower["product_modulus"]
    for key in ("product_g", "product_h", "product_selected_q", "product_selected_denominator"):
        assert [x % m for x in upper[key]] == lower[key]
    for key in ("product_q_basis", "product_q_witnesses", "product_denominators"):
        assert [[x % m for x in row] for row in upper[key]] == lower[key]
    assert upper["product_space_rank"] == lower["product_space_rank"] == 6
    report = {"status": "incomplete", "milestone": "D76", "date": "2026-09-18",
              "sources": [source(p) for p in (__file__, ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          DATA / "cm_frame_B3_check.json", DATA / "cm_frame_arithmetic_check.json")]
                         +[source(DATA / f"cm_frame_B3_product_lift_{n}.json") for n in (64, 128)],
              "independent_checks": [], "compatible_reductions": True,
              "product_space_dimension": 6, "final_precision_digits": 128,
              "number_field_cover_obtained": False}
    template = ROOT / "dembele/magma/149_cm_frame_B3_lift_check.m"
    for digits in (64, 128):
        script = DATA / f"cm_frame_B3_lift_check_{digits}.m"
        generate(template, script, digits)
        inputs = [script, template, DATA / f"cm_frame_B3_product_lift_{digits}.m",
                  DATA / f"cm_frame_doubling_{digits}.m", DATA / "cm_frame_B3_transfer.m",
                  DATA / "cm_frame_curve_candidate.m", DATA / "cm_frame_marks.m", DATA / "cm_frame_resolvent.m"]
        job = jobs.run_job(jobs.magma_command(script), script.with_suffix(".out"), 180,
                           "PASS|149_CM_FRAME_B3_LIFT_CHECK")
        job["sources"] = [source(p) for p in inputs]
        report["independent_checks"].append(job)
        write_json(report_path, report)
        print("B3 lift certificate", digits, job["status"], round(job["wall_seconds"], 3), flush=True)
        if job["status"] != "pass":
            print(script.with_suffix(".out").read_text()[-4000:])
            raise RuntimeError("independent B3 lift check failed")
    script = DATA / "cm_frame_B3_lift_negative_control.m"
    needle = 'load "dembele/data/computed/cm_frame_B3_product_lift_128.m";'
    column = stages[1]["section_chart_indices_zero_based"][0]+1
    text = template.read_text().replace(needle, needle
        +f"\nproduct_selected_denominator[{column}] +:= product_modulus div 31;")
    assert text != template.read_text()
    script.write_text(text)
    negative = jobs.run_job(jobs.magma_command(script), script.with_suffix(".out"), 180,
                            "PASS|149_CM_FRAME_B3_LIFT_CHECK", expected_failure="assert selected_left eq selected_right")
    negative["sources"] = [source(script)]+[source(p) for p in inputs]
    negative["mutation"] = f"add 31^127 to denominator coefficient {column}; all lower digits unchanged"
    report["negative_control"] = negative
    report["status"] = negative["status"]
    write_json(report_path, report)
    if negative["status"] != "pass":
        raise RuntimeError("highest-digit corruption was not rejected")
    checks.verify_records(report)
    print("PASS: B3 normalization transferred through 31^128, six products checked, corruption rejected.")


if __name__ == "__main__":
    main()

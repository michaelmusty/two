# D85 precision adapter; original SHA256 09ac98359528457cd42873b54f217624c221c870a1ad346127fa2c0f5110460b
"""D85: independently check the 128-digit class in two bounded jobs."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("class_checks_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def main():
    names = ["cm_frame_cubic_precision_128_sections", "cm_frame_cubic_pointed_128_jets",
             "cm_frame_cubic_pointed_128_newton_average", "cm_frame_cubic_pointed_128_newton_divisor",
             "cm_frame_cubic_pointed_64", "cm_frame_cubic_pointed_64_check"]
    paths = [DATA / (name+".json") for name in names]
    records = [json.loads(p.read_text()) for p in paths]
    for record in records: checks.verify_records(record)
    assert records[3]["actual_interpolated_divisor_verified"]
    coordinates = records[2]["data"]["average_coordinates"]
    assert records[3]["data"]["divisor_coordinates"] == coordinates
    wrapper = "precision_digits := 128;\n" + "".join(prior.loadline(p.with_suffix(".m")) for p in paths[:3])
    wrapper += prior.binding("previous_cubic_", {"modulus": 31**64,
        "descended_divisor_coordinates": records[4]["data"]["descended_divisor_coordinates"]})
    jobs = []
    script = ROOT / "dembele/magma/264_cm_frame_cubic_class_checks.m"
    for mode in ("relation", "symmetries"):
        base = DATA / ("cm_frame_cubic_pointed_128_newton_"+mode+"_check")
        job, path = prior.run(script, base, "PASS|264_CM_FRAME_CUBIC_CLASS_CHECKS",
                             prior.CORE+[Path(__file__)]+paths,
                             wrapper+f'class_check_mode := "{mode}";\n', False)
        jobs.append(path)
        if mode == "relation":
            delta = prior.helpers.field(Path(job["log"]["path"]).read_text(), "NEWTON_DELTA_COORDINATES")
        print("CLASS_INDEPENDENT_CHECK_PASS", mode, round(job["wall_seconds"], 3), flush=True)
    data = {"coordinates": coordinates, "delta_coordinates": delta}
    base = DATA / "cm_frame_cubic_pointed_128_newton_third"
    artifact = base.with_suffix(".m"); artifact.write_text(prior.binding("precision_third_", data))
    report = {"status": "pass", "milestone": "D85", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), *jobs, *paths]],
              "magma_artifact": checks.source(artifact), "data": data,
              "precision_digits": 128, "modulus": 31**128,
              "actual_divisor_verified": True, "three_division_verified": True,
              "frobenius_fixed": True, "antiinvariant": True,
              "scalar_comparison_completed": False, "matches_existing_pointed_model": False,
              "class_number_assumed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|264_CM_FRAME_CUBIC_CLASS_CHECKS", flush=True)


if __name__ == "__main__":
    main()

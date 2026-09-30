"""Lift the actual saved divisor by an idempotent in its section zero algebra."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("formal_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, checks = prior.helpers, prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(); n = args.digits
    prev = prior.previous_cubic(n).with_suffix(".json")
    sections = prior.stem(n, "_sections").with_suffix(".json")
    for path in (prev, sections): checks.verify_records(json.loads(path.read_text()))
    data_prev = json.loads(prev.read_text())["data"]
    wrapper = f"precision_digits := {n};\n"+prior.loadline(sections.with_suffix(".m"))
    wrapper += prior.binding("previous_cubic_", {"descended_divisor_coordinates": data_prev["descended_divisor_coordinates"], "modulus": 31**(n//2)})
    script = ROOT / "dembele/magma/208_cm_frame_cubic_formal_divisor.m"
    base = prior.stem(n, "_formal_divisor")
    job, jpath = prior.run(script, base, "PASS|208_CM_FRAME_CUBIC_FORMAL_DIVISOR",
        prior.CORE+[Path(__file__), prev, sections, ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m"], wrapper, args.rebuild)
    output = Path(job["log"]["path"]).read_text()
    names = ("divisor_coordinates", "g_coefficients", "h_coefficients", "quotient_basis_indices", "idempotent_coefficients")
    data = {key: helpers.field(output, "FORMAL_"+key.upper()) for key in names}
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding("formal_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), jpath, prev, sections)],
              "magma_artifact": checks.source(mpath), "data": data,
              "precision_digits": n, "modulus": 31**n,
              "zero_algebra_rank": 240, "idempotent_summand_rank": 120,
              "actual_divisor_lift_verified": True, "previous_representative_reduction_verified": True,
              "three_division_corrected": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|209_CM_FRAME_CUBIC_FORMAL_DIVISOR", n, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()

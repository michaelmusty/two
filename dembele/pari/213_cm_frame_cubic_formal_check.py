"""Check a saved idempotent lift and compare the short and global scalar routes."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("formal_check_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(); n = args.digits
    bases = [prior.stem(n, "_sections"), prior.stem(n, "_formal_divisor"), prior.stem(n, "_formal_third")]
    prev = prior.previous_cubic(n)
    for p in [*bases, prev]: checks.verify_records(json.loads(p.with_suffix(".json").read_text()))
    old = json.loads(prev.with_suffix(".json").read_text())["data"]
    inputs = prior.CORE+[Path(__file__), prev.with_suffix(".json")]+[p.with_suffix(".json") for p in bases]
    wrapper = f"precision_digits := {n};\n"+"".join(prior.loadline(p.with_suffix(".m")) for p in bases)
    wrapper += prior.binding("previous_cubic_", {"descended_divisor_coordinates": old["descended_divisor_coordinates"], "modulus": 31**(n//2)})
    comparison = prior.stem(n, "_third").with_suffix(".json")
    available = comparison.exists()
    if available:
        other = json.loads(comparison.read_text()); checks.verify_records(other)
        inputs.append(comparison)
        wrapper += prior.binding("comparison_", {"third_coordinates": other["data"]["coordinates"]})
    else:
        wrapper += "comparison_third_coordinates := [];\n"
    wrapper += f"comparison_available := {'true' if available else 'false'};\n"
    script = ROOT / "dembele/magma/212_cm_frame_cubic_formal_check.m"
    suffix = "_formal_comparison" if available else "_formal_check"
    base = prior.stem(n, suffix)
    job, jpath = prior.run(script, base, "PASS|212_CM_FRAME_CUBIC_FORMAL_CHECK", inputs, wrapper, args.rebuild)
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), jpath)],
              "precision_digits": n, "modulus": 31**n,
              "independent_idempotent_verification": True, "three_division_verified": True,
              "global_scalar_comparison_completed": available}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|213_CM_FRAME_CUBIC_FORMAL_CHECK", n, "comparison", available, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()

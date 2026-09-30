"""Lift only the rational quartic-space constraints, without any class arithmetic."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("quartic_space_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(128, 256, 512, 1024, 2048), required=True)
    args = parser.parse_args(); n = args.digits
    previous = DATA / "cm_frame_cubic_pointed_32_jets.json"
    checks.verify_records(json.loads(previous.read_text()))
    base = DATA / f"cm_frame_cubic_quartic_space_{n}"
    script = ROOT / "dembele/magma/246_cm_frame_cubic_quartic_space_jets.m"
    wrapper = f"precision_digits := {n};\n"+prior.loadline(previous.with_suffix(".m"))
    job, jpath = prior.run(script, base, "PASS|246_CM_FRAME_CUBIC_QUARTIC_SPACE_JETS",
        [Path(__file__), previous], wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {"quartic_jets": prior.helpers.field(output, "QUARTIC_SPACE_JETS"),
            "curve_jets": prior.helpers.field(output, "QUARTIC_CURVE_JETS")}
    report = {"status": "pass", "sources": [checks.source(p) for p in (Path(__file__), jpath)],
              "data": data, "precision_digits": n, "modulus": 31**n,
              "space": "H0(4*K_C-80*P32)", "dimension": 25, "constraint_rank": 80,
              "parameter": "s=n/d=w^2", "cubic_class_lift_performed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|247_CM_FRAME_CUBIC_QUARTIC_SPACE_JETS", n, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()

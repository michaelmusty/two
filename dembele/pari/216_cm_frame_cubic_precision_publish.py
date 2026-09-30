"""Publish a verified formal-route lift as the canonical input for the next precision."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("precision_publish_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    args = parser.parse_args(); n = args.digits
    source = prior.stem(n, "_formal_cubic").with_suffix(".json")
    proof = prior.stem(n, "_formal_cubic_check").with_suffix(".json")
    data = json.loads(source.read_text()); certificate = json.loads(proof.read_text())
    checks.verify_records(data); checks.verify_records(certificate)
    assert certificate["independent_verification_completed"]
    target = prior.stem(n).with_suffix(".json")
    if target.exists():
        existing = json.loads(target.read_text()); checks.verify_records(existing)
        assert existing["data"] == data["data"]
        print("PASS|216_CM_FRAME_CUBIC_PRECISION_EXISTING_DATA_PRESERVED", n)
        return
    mpath = target.with_suffix(".m")
    mpath.write_text(prior.binding("precision_cubic_", data["data"]))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), source, proof)],
              "magma_artifact": checks.source(mpath), "data": data["data"],
              "precision_digits": n, "modulus": 31**n, "origin_route": "formal kernel correction",
              "independent_verification_completed": True, "persistent_gauge_verified": True,
              "coefficientwise_reduction_verified": True, "characteristic_zero_cubic_constructed": False}
    target.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|216_CM_FRAME_CUBIC_PRECISION_PUBLISH", n)


if __name__ == "__main__":
    main()

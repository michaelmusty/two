# D83 generated precision extension; original SHA256: 7f4cbc757f157c12730982b90e5500022414ec5106adf40895c456e022d44bbe
# Original: dembele/pari/244_cm_frame_cubic_pointed_publish.py; generator: 261_cm_frame_cubic_precision64.py
"""Publish verified Newton-route data under the standard precision filenames."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed_publish_build", ROOT / "dembele/pari/221_cm_frame_cubic_pointed_function.py")
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
prior, checks, stem = build.prior, build.checks, build.stem


def read(path):
    report = json.loads(path.read_text()); checks.verify_records(report)
    assert report["status"] == "pass"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(64,), required=True)
    parser.add_argument("--stage", choices=("third", "cubic"), required=True)
    args = parser.parse_args(); n = args.digits
    if args.stage == "third":
        source = stem(n, "_newton_third").with_suffix(".json"); original = read(source)
        assert original["actual_divisor_verified"] and original["three_division_verified"]
        base = stem(n, "_third"); prefix = "precision_third_"; roots = [source]
    else:
        source = stem(n, "_direct").with_suffix(".json"); original = read(source)
        verification = stem(n, "_direct_check").with_suffix(".json"); checked = read(verification)
        assert checked["independent_verification_completed"]
        base = stem(n); prefix = "pointed_cubic_"; roots = [source, verification]
    target = base.with_suffix(".json")
    if target.exists():
        previous = read(target); assert previous["data"] == original["data"]
        print("PASS|244_CM_FRAME_CUBIC_POINTED_ALREADY_PUBLISHED", n, args.stage); return
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding(prefix, original["data"]))
    report = {"status": "pass", "milestone": "D83", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__)]+roots],
              "magma_artifact": checks.source(mpath), "data": original["data"],
              "precision_digits": n, "modulus": 31**n,
              "route": "pointed linear Newton correction", "three_division_verified": True,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False}
    target.write_text(json.dumps(report, indent=2)+"\n")
    if args.stage == "cubic":
        checked = {**checked, "published_canonical_model": checks.source(target),
                   "publication_sources": [checks.source(Path(__file__)), checks.source(verification)]}
        stem(n, "_check").with_suffix(".json").write_text(json.dumps(checked, indent=2)+"\n")
        checks.verify_records(checked)
    print("PASS|244_CM_FRAME_CUBIC_POINTED_PUBLISH", n, args.stage)


if __name__ == "__main__":
    main()

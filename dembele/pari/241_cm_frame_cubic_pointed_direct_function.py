"""Recover functions directly from the certified pointed Newton divisor."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("direct_pointed_build", ROOT / "dembele/pari/221_cm_frame_cubic_pointed_function.py")
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
prior, helpers, checks, stem, jets = old.prior, old.helpers, old.checks, old.stem, old.jets


def inputs_and_wrapper(n):
    # All provenance needed by the earlier constructor remains available.
    # Substitute the proved pointed divisor, removing the redundant move search.
    paths, wrapper, previous = old.inputs_and_wrapper(n)
    path = stem(n, "_newton_third").with_suffix(".json")
    report = json.loads(path.read_text()); checks.verify_records(report)
    assert report["actual_divisor_verified"] and report["three_division_verified"]
    paths += [path, Path(old.__file__)]
    wrapper += prior.loadline(path.with_suffix(".m"))
    return paths, wrapper, previous


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(16, 32), required=True)
    args = parser.parse_args(); n = args.digits
    paths, wrapper, previous = inputs_and_wrapper(n)
    script = ROOT / "dembele/magma/240_cm_frame_cubic_pointed_direct_function.m"
    base = stem(n, "_direct")
    job, jpath = prior.run(script, base, "PASS|240_CM_FRAME_CUBIC_POINTED_DIRECT_FUNCTION",
        prior.CORE+[Path(__file__), Path(jets.__file__)]+paths, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {key: helpers.field(output, "POINTED_"+key.upper()) for key in old.CORE_NAMES}
    for key in old.CORE_NAMES: assert old.reduced(data[key], previous["modulus"]) == previous[key], key
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding("pointed_cubic_", data))
    paths = [Path(__file__), jpath]
    original = stem(n).with_suffix(".json"); compared = original.exists()
    if compared:
        record = json.loads(original.read_text()); checks.verify_records(record); paths.append(original)
        assert data == {key: record["data"][key] for key in old.CORE_NAMES}
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in paths], "magma_artifact": checks.source(mpath),
              "data": data, "precision_digits": n, "modulus": 31**n,
              "route": "functions recovered directly from certified pointed Newton divisor",
              "coefficientwise_reduction_verified": True, "comparison_with_earlier_constructor": compared,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|241_CM_FRAME_CUBIC_POINTED_DIRECT_FUNCTION", n, round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

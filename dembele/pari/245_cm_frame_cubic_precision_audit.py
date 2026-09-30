"""Audit completed D82 certificates, exact route comparisons and frozen provenance."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("precision_audit_build", ROOT / "dembele/pari/221_cm_frame_cubic_pointed_function.py")
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
checks, stem = build.checks, build.stem
FROZEN_D78 = "a81750ea1fe8abfbbf27ac338154ef863ecea72dc95ada066656f8d981429931"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(16, 32), required=True)
    args = parser.parse_args(); n = args.digits
    paths = [DATA / name for name in (
        "cm_frame_cubic_lift_check.json", "cm_frame_cubic_precision_4_check.json",
        "cm_frame_cubic_precision_4_formal_comparison.json", "cm_frame_cubic_precision_8_formal_comparison.json",
        "cm_frame_cubic_pointed_isomorphism.json", "cm_frame_cubic_pointed_16_formal_check.json")]
    levels = [1, 2, 4, 8, 16]+([32] if n == 32 else [])
    paths += [stem(k, "_check").with_suffix(".json") for k in levels]
    paths += [stem(k, suffix).with_suffix(".json") for k in levels if k >= 8
              for suffix in ("_newton_third", "_recognition", "_local_recognition")]
    comparisons = []
    for k in levels:
        if k < 8: continue
        original_path = stem(k).with_suffix(".json")
        newton_path = stem(k, "_newton_third").with_suffix(".json")
        original = json.loads(original_path.read_text())["data"]
        newton = json.loads(newton_path.read_text())["data"]
        assert original["descended_divisor_coordinates"] == newton["coordinates"]
        comparison = {"precision_digits": k, "pointed_divisor_entries_compared": 81*201,
                      "newton_and_canonical_divisors_identical": True}
        paths += [original_path, newton_path]
        if k >= 16:
            direct_path = stem(k, "_direct").with_suffix(".json"); paths.append(direct_path)
            direct = json.loads(direct_path.read_text())["data"]
            assert {key: original[key] for key in build.CORE_NAMES} == direct
            comparison["all_core_coefficient_arrays_identical"] = True
        comparisons.append(comparison)
    seen = {}; json_seen = set()
    def walk(obj):
        if isinstance(obj, dict):
            if "path" in obj and "sha256" in obj:
                path = Path(obj["path"]); digest = hashlib.sha256(path.read_bytes()).hexdigest()
                assert digest == obj["sha256"], f"changed source: {path}"
                assert str(path) not in seen or seen[str(path)] == digest
                seen[str(path)] = digest
                if path.suffix == ".json" and str(path) not in json_seen:
                    json_seen.add(str(path)); walk(json.loads(path.read_text()))
            else:
                for value in obj.values(): walk(value)
        elif isinstance(obj, list):
            for value in obj: walk(value)
    for path in paths: walk(checks.source(path))
    assert hashlib.sha256((DATA / "cm_frame_cover_check.json").read_bytes()).hexdigest() == FROZEN_D78
    parsed = []
    for path in sorted((ROOT / "dembele/pari").glob("*.py")):
        prefix = path.name.split("_", 1)[0]
        if prefix.isdigit() and 195 <= int(prefix) <= 245:
            ast.parse(path.read_text()); parsed.append(str(path.relative_to(ROOT)))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__)]+list(dict.fromkeys(paths))],
              "precision_digits": n, "distinct_files_verified": len(seen),
              "linked_json_records_verified": len(json_seen), "frozen_D78_sha256": FROZEN_D78,
              "route_comparisons": comparisons, "python_sources_parsed": parsed,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False}
    result = DATA / f"cm_frame_cubic_precision_audit_{n}.json"
    result.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|245_CM_FRAME_CUBIC_PRECISION_AUDIT", n, len(seen), "file hashes", len(json_seen), "JSON records")


if __name__ == "__main__":
    main()

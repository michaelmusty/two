"""D84: audit the alternative-cover census and independent recognition calibration."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output_path = DATA / "cm_frame_structural_checkpoint.json"
    roots = [DATA / name for name in ("cm_frame_cubic_adjoint_audit_64.json",
        "cm_frame_cubic_adjoint_package_64.json", "cm_frame_third_ambiguity_0.json",
        "cm_frame_third_ambiguity_0_2.json", "cm_frame_recognition_calibration_check.json",
        "cm_frame_rational_three_torsion_1_job.json", "local_s3_cover.out", "genus64_cosets.gp")]
    roots += [ROOT / "dembele/pari/66_local_s3_cover.gp", Path(__file__)]
    ambiguity = json.loads((DATA / "cm_frame_third_ambiguity_0_2.json").read_text())
    assert ambiguity["rank_lower_bound"] == 2 and ambiguity["third_count_lower_bound"] == 9
    assert ambiguity["wrong_torsion_rejected"] and not ambiguity["torsion_subgroup_complete"]
    covers = []
    for index in range(9):
        path = DATA / f"cm_frame_alternative_cover_0_2_{index}.json"
        roots.append(path)
        record = json.loads(path.read_text())
        assert record["status"] == "pass" and record["cover_independently_verified"]
        assert record["third_label"] == ambiguity["third_labels"][index]
        counts = record["counts"]
        assert [c["extension_degree"] for c in counts] == [1, 2]
        assert [c["Hecke_expected"] for c in counts] == [68, 2818]
        assert all(c["independently_verified"] for c in counts)
        measured = [c["point_count"] for c in counts]
        match = measured == [68, 2818]
        assert record["matches_both_Hecke_counts"] == match
        covers.append({"case": index, "label": record["third_label"], "counts": measured, "matches": match})
    assert [c["case"] for c in covers if c["matches"]] == [0]
    assert all(c["counts"][0] != 68 and c["counts"][1] != 2818 for c in covers[1:])
    calibration = json.loads((DATA / "cm_frame_recognition_calibration_check.json").read_text())
    assert calibration["status"] == "pass" and calibration["synthetic_cases"] == 67
    thresholds = []
    for digits, train, success, failure in ((64, 48, 7, 8), (64, 60, 9, 10), (128, 112, 18, 19)):
        for seed in range(3):
            cases = {c["height"]: c for c in calibration["cases"]
                     if (c["digits"], c["train"], c["seed"], c["root"]) == (digits, train, seed, 4)}
            assert cases[10**success]["recovered"] and not cases[10**failure]["recovered"]
        thresholds.append({"digits": digits, "training_digits": train, "validation_digits": digits-train,
                           "example_height_recovered": 10**success, "example_height_failed": 10**failure,
                           "independent_seeds": 3, "root_mod31": 4})
    diagnostic_path = DATA / "cm_frame_rational_three_torsion_1_job.json"
    diagnostic = json.loads(diagnostic_path.read_text())
    assert diagnostic["status"] == "failed"
    assert "assert #indices eq 120" in Path(diagnostic["log"]["path"]).read_text()
    assert not (DATA / "cm_frame_rational_three_torsion_1.json").exists()
    seen, json_seen = {}, set()

    def walk(value):
        if isinstance(value, dict):
            if "path" in value and "sha256" in value:
                path = Path(value["path"]).resolve()
                key = str(path)
                if key not in seen:
                    seen[key] = hashlib.sha256(path.read_bytes()).hexdigest()
                assert seen[key] == value["sha256"], f"Changed source: {path}"
                if path.suffix == ".json" and key not in json_seen:
                    json_seen.add(key)
                    walk(json.loads(path.read_text()))
            else:
                for child in value.values():
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for path in roots:
        walk(source(path))
    frozen = "a81750ea1fe8abfbbf27ac338154ef863ecea72dc95ada066656f8d981429931"
    assert source(DATA / "cm_frame_cover_check.json")["sha256"] == frozen
    for name in seen:
        if name.endswith(".py"):
            ast.parse(Path(name).read_text())
    result = {"status": "pass", "milestone": "D84", "date": "2026-09-22",
              "sources": [source(p) for p in roots], "distinct_files_verified": len(seen),
              "linked_json_records_verified": len(json_seen), "frozen_D78_sha256": frozen,
              "compatible_three_torsion_rank_lower_bound": 2, "compatible_thirds_tested": 9,
              "cover_comparisons": covers, "unique_matching_case_in_tested_subgroup": 0,
              "torsion_subgroup_complete": False, "direct_Fuchsian_monodromy_comparison_completed": False,
              "recognition_calibration": thresholds, "synthetic_calibration_cases": calibration["synthetic_cases"],
              "exact_synthetic_recoveries": calibration["exact_recoveries_independently_checked"],
              "empirical_thresholds_are_uniform_guarantees": False, "target_height_bound_claimed": False,
              "actual_curve_precision_digits": 64, "arithmetic_identification_certified": False,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False,
              "recommendation": "One bounded 128-digit reconstruction experiment; retain the separate identification obligations.",
              "unsuccessful_diagnostic": {"path": str(diagnostic_path), "reason": "Random support did not reach degree 120; no class accepted."}}
    if args.check:
        assert output_path.exists()
        existing = json.loads(output_path.read_text())
        assert existing == result, "Changed checkpoint report"
    else:
        assert not output_path.exists(), "Use --check to verify an existing checkpoint."
        output_path.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|281_STRUCTURAL_CHECKPOINT", len(seen), len(json_seen), "matching cover", 0,
          "synthetic cases", calibration["synthetic_cases"])


if __name__ == "__main__":
    main()

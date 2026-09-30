"""Audit the bounded, unsuccessful 128-digit lift and the completed descent review."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUTPUT = DATA / "cm_frame_cubic_128_attempt_review.json"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    roots = [DATA / name for name in (
        "cm_frame_structural_checkpoint.json",
        "cm_frame_cubic_precision128_sections_receipt.json",
        "cm_frame_cubic_precision128_jets_receipt.json",
        "cm_frame_precision_aware_inverse_check.json",
        "cm_frame_memory_arithmetic_check.json",
        "cm_frame_block_arithmetic_check_v2.json",
        "cm_frame_block_arithmetic_check_job.json",
        "cm_frame_descent_review.json")]
    roots += [ROOT / "dembele/certificates/cm-frame-cubic-128-review.md", Path(__file__)]
    # Include source revisions that were superseded before a production run,
    # as well as all executed sources reached through the job receipts.
    for folder, suffix in (("pari", ".py"), ("magma", ".m")):
        roots += sorted(p for p in (ROOT / "dembele" / folder).glob("*"+suffix)
                        if p.name.split("_")[0].isdigit()
                        and 282 <= int(p.name.split("_")[0]) <= 297)
    roots = sorted(set(roots), key=str)
    attempts = []
    for suffix in ("", "_memory2", "_block3"):
        path = DATA / ("cm_frame_cubic_pointed_128_formal_divisor"+suffix+"_job.json")
        record = json.loads(path.read_text()); roots.append(path)
        log = Path(record["log"]["path"]).read_text()
        assert record["timeout_seconds"] == 180
        assert record["memory_limit_bytes"] == 2000000000
        assert record["timeout_terminates_process_group"]
        assert "PASS|208_CM_FRAME_CUBIC_FORMAL_DIVISOR" not in log
        if suffix == "_block3":
            assert record["status"] == "timeout" and record["exit_code"] < 0
            reason = "180-second process-group timeout"
        else:
            assert record["status"] == "failed"
            assert "User memory limit has been reached" in log
            reason = "2 GB Magma memory limit"
        attempts.append({"job": path.name, "status": record["status"],
                         "wall_seconds": record["wall_seconds"], "reason": reason})
    for name in ("cm_frame_cubic_pointed_128_formal_divisor.json",
                 "cm_frame_cubic_pointed_128_newton_third.json",
                 "cm_frame_cubic_adjoint_128.json",
                 "cm_frame_cubic_adjoint_128_check.json"):
        assert not (DATA / name).exists(), "Review checkpoint must reflect new work if this exists"
    assert not list(DATA.glob("cm_frame_cubic_adjoint_joint_128_112_*.json"))
    positive = []
    for name in ("cm_frame_cubic_precision_128_sections", "cm_frame_cubic_pointed_128_jets"):
        path = DATA / (name+".json")
        record = json.loads(path.read_text())
        assert record["status"] == "pass" and record["precision_digits"] == 128
        positive.append(name)
    for name in ("cm_frame_precision_aware_inverse_check", "cm_frame_memory_arithmetic_check",
                 "cm_frame_block_arithmetic_check_v2"):
        record = json.loads((DATA / (name+".json")).read_text())
        assert record["status"] == "pass" and record["native_inverse_equality_verified"]
        assert record["highest_digit_inverse_corruption_rejected"]
    failed_control = json.loads((DATA / "cm_frame_block_arithmetic_check_job.json").read_text())
    assert failed_control["status"] == "failed"
    assert "No valid universe containing all elements" in Path(failed_control["log"]["path"]).read_text()
    review = json.loads((DATA / "cm_frame_descent_review.json").read_text())
    assert review["status"] == "pass"
    assert review["prym_dimension_from_genera"] == 24
    assert review["geometric_third_torsor_degree"] == 3**48
    assert review["reflection_normalizer_order"] == review["reflection_subgroup_order"] == 2
    control = review["local_rationality_counterexample"]
    assert control["precision_digits"] == 128 and not control["has_root_in_F"]
    assert control["root"] % 31 == 6 and (control["root"]**2-5) % 31**128 == 0
    seen, linked = {}, set()

    def walk(value):
        if isinstance(value, dict):
            if "path" in value and "sha256" in value:
                path = Path(value["path"]).resolve(); key = str(path)
                if key not in seen:
                    seen[key] = hashlib.sha256(path.read_bytes()).hexdigest()
                assert seen[key] == value["sha256"], f"Changed source: {path}"
                if path.suffix == ".json" and key not in linked:
                    linked.add(key); walk(json.loads(path.read_text()))
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
    result = {
        "status": "pass", "milestone": "D85", "date": "2026-09-22",
        "sources": [source(p) for p in roots],
        "distinct_files_verified": len(seen), "linked_json_records_verified": len(linked),
        "frozen_D78_sha256": frozen, "attempted_precision_digits": 128,
        "verified_cubic_precision_digits": 64, "successful_128_digit_preparations": positive,
        "divisor_attempts": attempts, "attempt_outcome": "resource_failure_before_cubic_construction",
        "precision128_cubic_constructed": False, "precision128_recognition_run": False,
        "negative_precision128_recognition_claimed": False,
        "coefficient_field_excluded": False, "review_completed": True,
        "geometric_third_torsor_degree": 3**48,
        "candidate_global_Galois_action_determined": False,
        "arithmetic_identification_certified": False, "target_field_constructed": False,
        "next_deliverable": "Marked arithmetic comparison and the global Galois action on the selected third; pause precision escalation.",
        "proof": "dembele/certificates/cm-frame-cubic-128-review.md"}
    if args.check:
        assert json.loads(OUTPUT.read_text()) == result, "Changed D85 checkpoint"
    else:
        assert not OUTPUT.exists(), "Use --check for the existing checkpoint"
        OUTPUT.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|297_CUBIC_128_REVIEW_AUDIT", len(seen), "file hashes", len(linked),
          "JSON records; cubic remains at 64 digits; review complete", flush=True)


if __name__ == "__main__":
    main()

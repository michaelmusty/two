"""D86: package the verified 128-digit cubic, recognition, and Chatelet provenance."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
STAGES = ("divisor", "charts", "newton_divisor", "class_check", "publish_third",
          "pointed_functions", "pointed_fit", "pointed_check", "publish_cubic",
          "adjoint_move", "adjoint_functions", "adjoint_check")


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def immutable_json(path, record):
    if path.exists():
        assert json.loads(path.read_text()) == record, "Changed artifact: "+str(path)
    else:
        path.write_text(json.dumps(record, indent=2)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    roots = [Path(__file__), DATA / "cm_frame_cubic_128_attempt_review.json",
        DATA / "cm_frame_cubic_pointed_128_check.json", DATA / "cm_frame_cubic_adjoint_128_check.json",
        DATA / "cm_frame_cubic_adjoint_128_recognition.json",
        DATA / "cm_frame_cubic_precision128_sections_receipt.json",
        DATA / "cm_frame_cubic_precision128_jets_receipt.json",
        DATA / "cm_frame_cubic128_upload_interruption_d86.json",
        DATA / "cm_frame_cubic128_transfer_resume_d86.json",
        DATA / "cm_frame_cubic128_remote_completion_d86.json",
        DATA / "cm_frame_cubic_pointed_128_formal_divisor_chatelet_d86_planned_transfer.json"]
    for stage in STAGES:
        path = DATA / ("cm_frame_cubic_precision128_chatelet_"+stage+"_receipt.json")
        record = json.loads(path.read_text()); roots.append(path)
        assert record["status"] == "pass" and record["precision_digits"] == 128
        assert record["stage"] == stage and record["execution_host"] == "chatelet.mit.edu"
    for family in ("pointed", "adjoint"):
        record = json.loads((DATA / f"cm_frame_cubic_{family}_128_check.json").read_text())
        assert record["status"] == "pass" and record["independent_verification_completed"]
        assert record["function_divisors_and_norm_verified"]
        assert record["highest_digit_norm_control"]["status"] == "pass"
        key = "highest_digit_septic_control" if family == "pointed" else "highest_digit_trace_control"
        assert record[key]["status"] == "pass"
    recognition = json.loads((DATA / "cm_frame_cubic_adjoint_128_recognition.json").read_text())
    assert recognition["status"] == "pass" and recognition["precision_digits"] == 128
    assert recognition["independent_final_precision_model_check"]
    assert recognition["known_rational_control_passed"] and recognition["known_field_control_passed"]
    assert recognition["first_unused_digit_corruptions_rejected"]
    joint, heights = [], []
    for index in range(8):
        path = DATA / f"cm_frame_cubic_adjoint_joint_128_112_{index}.json"
        record = json.loads(path.read_text()); roots.append(path)
        assert record["status"] == "pass" and record["known_control"]["survivors"]
        assert record["training_digits"] == 112 and record["validation_digits"] == 16
        assert record["unused_digit_error_rejected"] and record["result"]["determinant_verified"]
        joint.append({"root_mod31": record["root_mod31"], "training_digits": 112, "validation_digits": 16,
            "known_control_survivors": len(record["known_control"]["survivors"]),
            "target_survivors": len(record["result"]["survivors"]),
            "maximum_matching_digits": max(c["matching_digits"] for c in record["result"]["candidates"])})
        path = DATA / f"cm_frame_cubic_adjoint_dual_height_128_112_{index}.json"
        height = json.loads(path.read_text()); roots.append(path)
        assert height["status"] == "pass" and height["integer_matrix_identity_verified"]
        B, K = record["result"]["rows"], height["scaled_inverse_rows"]
        assert len(B) == len(K) == 200 and all(len(row) == 200 for row in B+K)
        D = 31**112; assert height["scale"] == D
        columns = list(zip(*K))
        for i, row in enumerate(B):
            for j, column in enumerate(columns):
                assert sum(x*y for x, y in zip(row, column)) == (D if i == j else 0)
        sums = [sum(abs(x) for x in column) for column in columns]
        S = max(sums); H = height["excluded_integral_coefficient_height_through"]
        assert sums == height["column_absolute_sums"] and S == height["maximum_column_absolute_sum"]
        assert H*S < D <= (H+1)*S and height["root_mod31"] == record["root_mod31"]
        heights.append({"root_mod31": record["root_mod31"], "excluded_height_through": H})
        print("INDEPENDENT_INTEGER_HEIGHT_IDENTITY_PASS", index, H, flush=True)
    old_path, current_path = DATA / "cm_frame_cubic_adjoint_package_64.json", DATA / "cm_frame_cubic_adjoint_128.json"
    old, current = [json.loads(p.read_text()) for p in (old_path, current_path)]
    data = current["data"]
    assert [x % 31**64 for x in data["a_quadratic_coefficients"]] == old["A2_coefficients"]
    assert [x % 31**64 for x in data["trace_quartic_coefficients"]] == old["R4_coefficients"]
    package = dict(old, precision_digits=128, modulus=31**128,
        A2_coefficients=data["a_quadratic_coefficients"], R4_coefficients=data["trace_quartic_coefficients"],
        sources=[source(p) for p in (Path(__file__), old_path, current_path, DATA / "cm_frame_cubic_adjoint_128_check.json")])
    package_path = DATA / "cm_frame_cubic_adjoint_package_128.json"
    if args.check:
        assert json.loads(package_path.read_text()) == package
    else:
        immutable_json(package_path, package)
    roots += [package_path, old_path, current_path]
    seen, linked, remote_jobs = {}, set(), {}

    def walk(value):
        if isinstance(value, dict):
            if "path" in value and "sha256" in value:
                path = Path(value["path"]).resolve(); key = str(path)
                if key not in seen:
                    seen[key] = hashlib.sha256(path.read_bytes()).hexdigest()
                assert seen[key] == value["sha256"], f"Changed source: {path}"
                if path.suffix == ".json" and key not in linked:
                    linked.add(key); record = json.loads(path.read_text())
                    if record.get("execution_host") == "chatelet.mit.edu" and "remote_directory" in record:
                        assert record["status"] == "pass"
                        assert record["memory_limit_bytes"] == 8000000000 and record["timeout_seconds"] == 1800
                        assert record["input_hashes_verified"] and record["timeout_terminates_process_group"]
                        assert record["wall_seconds"] < 1801
                        job_name = Path(record["remote_directory"]).name
                        spec_path = DATA / "chatelet_d86_128" / job_name / "spec.json"
                        assert any(item.get("path") == str(spec_path) for item in record["sources"])
                        spec = json.loads(spec_path.read_text())
                        log = Path(record["log"]["path"]).read_text()
                        expected = spec["expected_failure"]
                        if expected is None:
                            assert record["exit_code"] == 0 and spec["marker"] in log
                        else:
                            assert record["exit_code"] != 0 and expected in log and "Assertion failed" in log
                            assert spec["marker"] not in log
                        for name, digest in spec["inputs"].items():
                            assert source(ROOT / name)["sha256"] == digest
                        remote_jobs[key] = {"job": path.name, "wall_seconds": record["wall_seconds"],
                            "maximum_resident_bytes": record["maximum_resident_bytes"], "exit_code": record["exit_code"],
                            "expected_failure": expected}
                    walk(record)
            else:
                for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)

    for path in roots: walk(source(path))
    frozen = "a81750ea1fe8abfbbf27ac338154ef863ecea72dc95ada066656f8d981429931"
    assert source(DATA / "cm_frame_cover_check.json")["sha256"] == frozen
    for name in seen:
        if name.endswith(".py"): ast.parse(Path(name).read_text())
    remote_summary = [remote_jobs[k] for k in sorted(remote_jobs)]
    completed = json.loads((DATA / "cm_frame_cubic128_remote_completion_d86.json").read_text())
    assert completed["status"] == "pass" and completed["all_remote_jobs_completed"]
    assert completed["remote_statuses_equal_saved_local_records"]
    assert len(remote_summary) == completed["remote_job_count"] == 21
    result = {"status": "pass", "milestone": "D86", "date": "2026-09-23",
        "sources": [source(p) for p in roots], "distinct_files_verified": len(seen),
        "linked_json_records_verified": len(linked), "frozen_D78_sha256": frozen,
        "verified_precision_digits": 128, "coefficientwise_reduction_to_64_verified": True,
        "remote_jobs": remote_summary, "remote_job_count": len(remote_summary),
        "maximum_remote_wall_seconds": max(x["wall_seconds"] for x in remote_summary),
        "maximum_remote_resident_bytes": max(x["maximum_resident_bytes"] for x in remote_summary),
        "joint_F_recognition": joint, "independently_verified_height_exclusions": heights,
        "uniform_excluded_integral_height_through": min(x["excluded_height_through"] for x in heights),
        "characteristic_zero_cubic_constructed": False, "coefficient_field_excluded": False,
        "arithmetic_identification_certified": False, "target_field_constructed": False,
        "proof": "dembele/certificates/cm-frame-cubic-128-chatelet.md"}
    result_path = DATA / "cm_frame_cubic_adjoint_audit_128.json"
    if args.check:
        assert json.loads(result_path.read_text()) == result
    else:
        immutable_json(result_path, result)
    print("PASS|303_CUBIC_128_AUDIT", len(seen), "file hashes", len(linked), "JSON records;",
          len(remote_summary), "remote jobs; target survivors", sum(x["target_survivors"] for x in joint), flush=True)


if __name__ == "__main__":
    main()

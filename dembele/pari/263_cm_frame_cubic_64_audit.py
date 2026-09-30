"""Package the independently checked 64-digit cubic and audit its provenance."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("audit64_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", type=int, nargs="+", default=[48])
    parser.add_argument("--height-train", type=int)
    args = parser.parse_args()
    roots = [DATA / name for name in (
        "cm_frame_cubic_adjoint_audit_32.json", "cm_frame_cubic_pointed_64_check.json",
        "cm_frame_cubic_adjoint_64_check.json", "cm_frame_cubic_adjoint_64_recognition.json")]
    roots += sorted(DATA.glob("cm_frame_cubic_precision64_*_receipt.json"))
    roots += [DATA / "cm_frame_cubic_adjoint_height_late_archive.json",
              DATA / "cm_frame_bounded_sage_timeout_control.json",
              ROOT / "dembele/pari/274_cm_frame_bounded_recognition.py"]
    diagnostics = []
    for name in ("cm_frame_cubic_pointed_64_newton_check_job.json",
                 "cm_frame_cubic_pointed_64_function_checkpoint_job.json",
                 "cm_frame_cubic_adjoint_height_64_48_0_job.json"):
        path = DATA / name
        record = json.loads(path.read_text())
        assert record["status"] == "timeout" and record["timeout_seconds"] == 180
        roots.append(path)
        diagnostics.append({"record": name, "status": "timeout", "wall_seconds": record["wall_seconds"]})
    joint = []
    for train in args.train:
        for i in range(8):
            path = DATA / f"cm_frame_cubic_adjoint_joint_64_{train}_{i}.json"
            record = json.loads(path.read_text()); roots.append(path)
            assert record["status"] == "pass" and record["known_control"]["survivors"]
            assert record["unused_digit_error_rejected"]
            joint.append({"training_digits": train, "validation_digits": 64-train,
                "root_mod31": record["root_mod31"],
                "known_control_survivors": len(record["known_control"]["survivors"]),
                "target_survivors": len(record["result"]["survivors"]),
                "maximum_matching_digits": max(c["matching_digits"] for c in record["result"]["candidates"])})
    heights = []
    if args.height_train is not None:
        train = args.height_train
        for i in range(8):
            path = DATA / f"cm_frame_cubic_adjoint_dual_height_64_{train}_{i}.json"
            record = json.loads(path.read_text()); roots.append(path)
            assert record["status"] == "pass" and record["integer_matrix_identity_verified"]
            lattice = json.loads((DATA / f"cm_frame_cubic_adjoint_joint_64_{train}_{i}.json").read_text())
            B = lattice["result"]["rows"]; K = record["scaled_inverse_rows"]
            assert len(B) == len(K) == 200 and all(len(row) == 200 for row in B+K)
            D = 31**train; assert record["scale"] == D
            columns = list(zip(*K))
            # Independent integer verification from saved witnesses; no Sage,
            # inversion, orthogonalization or floating-point arithmetic.
            for a, row in enumerate(B):
                for b, column in enumerate(columns):
                    assert sum(x*y for x, y in zip(row, column)) == (D if a == b else 0)
            sums = [sum(abs(x) for x in column) for column in columns]
            S = max(sums); H = record["excluded_integral_coefficient_height_through"]
            assert sums == record["column_absolute_sums"] and S == record["maximum_column_absolute_sum"]
            assert H*S < D <= (H+1)*S
            assert record["root_mod31"] == lattice["root_mod31"]
            heights.append({"root_mod31": record["root_mod31"], "excluded_height_through": H})
            print("INDEPENDENT_INTEGER_HEIGHT_IDENTITY_PASS", i, H, flush=True)
    seen, json_seen = {}, set()
    def walk(obj):
        if isinstance(obj, dict):
            if "path" in obj and "sha256" in obj:
                path = Path(obj["path"]).resolve(); digest = hashlib.sha256(path.read_bytes()).hexdigest()
                assert digest == obj["sha256"], f"changed input: {path}"
                assert str(path) not in seen or seen[str(path)] == digest
                seen[str(path)] = digest
                if path.suffix == ".json" and str(path) not in json_seen:
                    json_seen.add(str(path)); walk(json.loads(path.read_text()))
            else:
                for value in obj.values(): walk(value)
        elif isinstance(obj, list):
            for value in obj: walk(value)
    for path in roots: walk(checks.source(path))
    frozen = "a81750ea1fe8abfbbf27ac338154ef863ecea72dc95ada066656f8d981429931"
    assert hashlib.sha256((DATA / "cm_frame_cover_check.json").read_bytes()).hexdigest() == frozen
    previous_path = DATA / "cm_frame_cubic_adjoint_package_32.json"
    current_path = DATA / "cm_frame_cubic_adjoint_64.json"
    old = json.loads(previous_path.read_text()); current = json.loads(current_path.read_text())
    for path in (previous_path, current_path): walk(checks.source(path))
    data = current["data"]
    assert [x % 31**32 for x in data["a_quadratic_coefficients"]] == old["A2_coefficients"]
    assert [x % 31**32 for x in data["trace_quartic_coefficients"]] == old["R4_coefficients"]
    package = dict(old, precision_digits=64, modulus=31**64,
        A2_coefficients=data["a_quadratic_coefficients"], R4_coefficients=data["trace_quartic_coefficients"],
        sources=[checks.source(p) for p in (Path(__file__), previous_path, current_path,
            DATA / "cm_frame_cubic_adjoint_64_check.json")])
    package_path = DATA / "cm_frame_cubic_adjoint_package_64.json"
    package_path.write_text(json.dumps(package, indent=2)+"\n")
    walk(checks.source(package_path))
    parsed = []
    for name in seen:
        path = Path(name)
        if path.suffix == ".py":
            ast.parse(path.read_text())
            parsed.append(str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path))
    report = {"status": "pass", "milestone": "D83", "date": "2026-09-22",
        "sources": [checks.source(p) for p in [Path(__file__), package_path]+roots],
        "distinct_files_verified": len(seen), "linked_json_records_verified": len(json_seen),
        "frozen_D78_sha256": frozen, "python_sources_parsed": sorted(parsed),
        "verified_precision_digits": 64, "coefficientwise_reduction_to_32_verified": True,
        "joint_F_recognition": joint, "characteristic_zero_cubic_constructed": False,
        "independently_verified_height_exclusions": heights,
        "uniform_excluded_integral_height_through": min(x["excluded_height_through"] for x in heights) if heights else None,
        "archived_unsuccessful_diagnostics": diagnostics,
        "arithmetic_identification_certified": False, "target_field_constructed": False,
        "proof": "dembele/certificates/cm-frame-cubic-64.md"}
    result = DATA / "cm_frame_cubic_adjoint_audit_64.json"
    result.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|263_CUBIC_64_AUDIT", len(seen), "file hashes", len(json_seen), "JSON records",
          "joint survivors", sum(x["target_survivors"] for x in joint), flush=True)


if __name__ == "__main__":
    main()

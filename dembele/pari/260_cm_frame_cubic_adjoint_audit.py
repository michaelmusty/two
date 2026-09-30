"""Package the verified low-degree cubic and audit all completed D82 inputs."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("adjoint_audit_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def main():
    roots = [DATA / name for name in (
        "cm_frame_cubic_precision_audit_32.json", "cm_frame_cubic_adjoint_1_check.json",
        "cm_frame_cubic_adjoint_32_check.json", "cm_frame_cubic_adjoint_isomorphism.json",
        "cm_frame_cubic_adjoint_quadratic_space.json", "cm_frame_cubic_quartic_lattice_128_256.json")]
    roots += [DATA / f"cm_frame_cubic_adjoint_{n}_recognition.json" for n in (8, 16, 32)]
    roots += [DATA / f"cm_frame_cubic_adjoint_joint_32_24_{i}.json" for i in range(8)]
    for n in (1, 2, 4, 8, 16, 32): roots.append(DATA / f"cm_frame_cubic_adjoint_{n}.json")
    seen, json_seen = {}, set()
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
                for v in obj.values(): walk(v)
        elif isinstance(obj, list):
            for v in obj: walk(v)
    for path in roots: walk(checks.source(path))
    frozen = "a81750ea1fe8abfbbf27ac338154ef863ecea72dc95ada066656f8d981429931"
    assert hashlib.sha256((DATA / "cm_frame_cover_check.json").read_bytes()).hexdigest() == frozen
    joint = []
    for i in range(8):
        record = json.loads((DATA / f"cm_frame_cubic_adjoint_joint_32_24_{i}.json").read_text())
        assert record["known_control"]["survivors"] and record["unused_digit_error_rejected"]
        joint.append({"root_mod31": record["root_mod31"],
                      "known_control_survivors": len(record["known_control"]["survivors"]),
                      "candidate_rows_tested": len(record["result"]["candidates"]),
                      "target_survivors": len(record["result"]["survivors"]),
                      "maximum_matching_digits": max(c["matching_digits"] for c in record["result"]["candidates"])})
    curve_path = DATA / "cm_frame_curve_candidate.json"
    sections_path = DATA / "cm_frame_cover_sections.json"
    old_cubic_path = DATA / "cm_frame_cubic.json"
    current_path = DATA / "cm_frame_cubic_adjoint_32.json"
    curve, sections, old, current = [json.loads(p.read_text()) for p in (curve_path, sections_path, old_cubic_path, current_path)]
    for path in (curve_path, sections_path, old_cubic_path, current_path): walk(checks.source(path))
    data = current["data"]
    package = {"status": "verified_finite_precision", "prime": 31, "precision_digits": 32, "modulus": 31**32,
               "sources": [checks.source(p) for p in [curve_path, sections_path, old_cubic_path, current_path,
                   DATA / "cm_frame_cubic_adjoint_32_check.json", DATA / "cm_frame_cubic_adjoint_isomorphism.json"]],
               "base_curve": {"variables": curve["variables"], "monomial_pair_index_base": 0,
                              "quadratic_monomial_pairs": curve["monomial_pairs"], "quadrics": curve["quadrics"]},
               "equation": "ell*T^3 - 3*A2*ell*T - R4 = 0", "weight_T": 1,
               "ell_coefficients": [-24,28,-8,15,-10,22,40,-2,12,-5,16,38,-8,32,12,1],
               "A2_monomial_exponents": sections["data"]["even_monomial_exponents"],
               "A2_coefficients": data["a_quadratic_coefficients"],
               "R4_monomial_exponents": old["data"]["cubic_quartic_monomials"],
               "R4_coefficients": data["trace_quartic_coefficients"],
               "interpretation": "Finite-precision equations for the compatible cover. On the special fibre take the smooth projective normalization of the component dominating C on ell != 0; clearing ell may add vertical components.",
               "normalization_genus": 64, "special_fibre_point_counts": {"F31": 68, "F961": 2818},
               "characteristic_zero_reconstruction_certified": False, "arithmetic_identification_certified": False, "target_field_constructed": False}
    package_path = DATA / "cm_frame_cubic_adjoint_package_32.json"
    package_path.write_text(json.dumps(package, indent=2)+"\n")
    walk(checks.source(package_path)); walk(checks.source(Path(__file__)))
    parsed = []
    for path in sorted((ROOT / "dembele/pari").glob("*.py")):
        prefix = path.name.split("_", 1)[0]
        if prefix.isdigit() and 195 <= int(prefix) <= 260:
            ast.parse(path.read_text()); parsed.append(str(path.relative_to(ROOT)))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), package_path]+roots],
              "distinct_files_verified": len(seen), "linked_json_records_verified": len(json_seen),
              "frozen_D78_sha256": frozen, "python_sources_parsed": parsed,
              "verified_precision_digits": 32, "final_equation_weight_T": 1,
              "joint_F_recognition": joint, "exact_rational_A2_space_dimension": 25,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False,
              "proof": "dembele/certificates/cm-frame-cubic-precision.md"}
    result = DATA / "cm_frame_cubic_adjoint_audit_32.json"
    result.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|260_CM_FRAME_CUBIC_ADJOINT_AUDIT", len(seen), "file hashes", len(json_seen), "JSON records",
          "joint survivors", sum(r["target_survivors"] for r in joint))


if __name__ == "__main__":
    main()

"""D75: joint projective recognition over F in the exact denominator space.

Fit seventeen degree-at-most-seven polynomials with a common F-valued
scale. Only 64 digits enter the lattice; the other 64 validate candidates.
The search is bounded to LLL basis rows and is not a height exclusion.
"""
import importlib.util
import json
from pathlib import Path
import random
import time

from sage.all import GF, QQ, ZZ, NumberField, PolynomialRing, Zmod, identity_matrix, matrix

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
TRAIN, VALID = 64, 128
POLYNOMIAL = [2, 0, -16, 0, 20, 0, -8, 0, 1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("joint_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
rec = module("joint_recognition", ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py")
source = checks.source


def evaluate(row, root, modulus):
    powers = [pow(root, j, modulus) for j in range(8)]
    return [sum(int(row[8*i+j])*powers[j] for j in range(8)) % modulus for i in range(17)]


def candidate_record(row, target, root, anchor, index):
    modulus = 31**VALID
    values = evaluate(row, root, modulus)
    if values[anchor] % 31 == 0:
        return None
    defects = [(values[i]*target[anchor]-values[anchor]*target[i]) % modulus
               for i in range(17) if i != anchor]
    matching = min(rec.valuation(x, VALID) for x in defects)
    assert matching >= TRAIN
    height = max(abs(int(x)) for x in row)
    return {"row_index_zero_based": index, "height": str(height),
            "height_decimal_digits": len(str(height)), "matching_digits": matching,
            "validates_unused_digits": matching == VALID}


def experiment(label, target, root, F, exact_control=None):
    started = time.monotonic()
    m = 31**TRAIN
    Z = Zmod(m)
    anchor = next(i for i, value in enumerate(target) if value % 31)
    others = [i for i in range(17) if i != anchor]
    ratios = [Z(value)/Z(target[anchor]) for value in target]
    powers = [Z(root)**j for j in range(8)]
    H = matrix(Z, 16, 136)
    for k, i in enumerate(others):
        for j in range(8):
            H[k, 8*i+j] = powers[j]
            H[k, 8*anchor+j] = -ratios[i]*powers[j]
    active = [8*i for i in others]
    assert H.matrix_from_columns(active) == identity_matrix(Z, 16)
    # Identity columns make this a basis of the full congruence kernel.
    # Reordering active coordinates gives determinant m^16.
    B = identity_matrix(ZZ, 136)
    for j in range(136):
        if j in active:
            B[j, j] = m
        else:
            for k, col in enumerate(active):
                B[j, col] = -ZZ(H[k, j])
    assert B.change_ring(Z)*H.transpose() == 0
    print("JOINT_LATTICE_READY", label, "ROOT", root % 31, flush=True)
    reduced = B.LLL()
    assert reduced.change_ring(Z)*H.transpose() == 0
    assert abs(reduced.det()) == m**16
    rows = [[int(x) for x in row] for row in reduced]
    candidates = [c for i, row in enumerate(rows)
                  if (c := candidate_record(row, target, root, anchor, i)) is not None]
    survivors = [c for c in candidates if c["validates_unused_digits"]]
    if exact_control is not None:
        expected = [F(row) for row in exact_control]
        assert survivors
        for candidate in survivors:
            row = rows[candidate["row_index_zero_based"]]
            exact = [F(row[8*i:8*i+8]) for i in range(17)]
            assert exact[anchor] != 0
            assert all(exact[i]*expected[anchor] == exact[anchor]*expected[i] for i in range(17))
            candidate["exact_control_projective_identity"] = True
    candidates.sort(key=lambda c: int(c["height"]))
    print("JOINT_FIELD", label, "ROOT", root % 31, "SURVIVORS", len(survivors),
          "TESTED", len(candidates), "MIN_DIGITS", min(c["height_decimal_digits"] for c in candidates),
          "SECONDS", round(time.monotonic()-started, 3), flush=True)
    return {"label": label, "root_mod31": root % 31, "root_mod_validation": root,
            "projective_anchor_index_zero_based": anchor,
            "lattice_rank": 136, "congruence_equations": 16,
            "lattice_index": str(m**16), "index_verified_by_exact_determinant": True,
            "reduced_rows": rows, "candidates": candidates,
            "candidate_count": len(candidates), "nonunit_anchor_rows_skipped": 136-len(candidates),
            "survivor_row_indices": [c["row_index_zero_based"] for c in survivors],
            "minimum_candidate_height_digits": min(c["height_decimal_digits"] for c in candidates),
            "maximum_matching_digits": max(c["matching_digits"] for c in candidates),
            "wall_seconds": time.monotonic()-started}


def main():
    started = time.monotonic()
    old_check = DATA / "cm_frame_arithmetic_check.json"
    space_path = DATA / "cm_frame_denominator_space_reduced.json"
    old = json.loads(old_check.read_text())
    checks.verify_records(old)
    assert old["status"] == "pass"
    space = json.loads(space_path.read_text())
    target = space["denominator_basis_coefficients"][str(VALID)]
    assert len(target) == 17
    assert [x % (31**TRAIN) for x in target] == space["denominator_basis_coefficients"][str(TRAIN)]
    T = PolynomialRing(ZZ, "t")
    f = T(POLYNOMIAL)
    F = NumberField(f.change_ring(QQ), "theta")
    roots31 = sorted(int(r) for r, multiplicity in f.change_ring(GF(31)).roots() if multiplicity == 1)
    assert len(roots31) == 8
    roots = [rec.hensel_root(f, r, VALID) for r in roots31]
    rng = random.Random(75)
    known = [[rng.randint(-10**6, 10**6) for _ in range(8)] for _ in range(17)]
    values = evaluate(sum(known, []), roots[0], 31**VALID)
    anchor = next(i for i, value in enumerate(values) if value % 31)
    values = [value*pow(values[anchor], -1, 31**VALID) % (31**VALID) for value in values]
    control = experiment("known_F_projective_point", values, roots[0], F, exact_control=known)
    assert control["projective_anchor_index_zero_based"] == anchor
    changed = next(i for i in range(17) if i != anchor)
    bad = list(values)
    bad[changed] = (bad[changed]+31**TRAIN) % (31**VALID)
    rejected = [candidate_record(row, bad, roots[0], anchor, i)
                for i, row in enumerate(control["reduced_rows"])]
    assert not any(c and c["validates_unused_digits"] for c in rejected)
    old_survivors = 0
    for i, value in enumerate(values):
        if i != anchor:
            old_survivors += bool([c for c in rec.field_candidates(value, roots[0], TRAIN, VALID)
                                  if c["validates_unused_digits"]])
    control.update({"exact_control_coefficients": known, "target_residues": values,
                    "separate_ratio_recognition_survivors": old_survivors,
                    "negative_control_coordinate": changed,
                    "first_unused_digit_error_rejected": True})
    print("PASS|JOINT_F_CONTROL_AND_UNUSED_DIGIT_CORRUPTION", "SEPARATE_RATIO_SURVIVORS", old_survivors, flush=True)
    report = {"status": "incomplete", "milestone": "D75", "date": "2026-09-18",
              "sources": [source(p) for p in (__file__, old_check, space_path,
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py")],
              "field_polynomial_ascending": POLYNOMIAL, "all_roots_mod31": roots31,
              "training_digits": TRAIN, "validation_digits": VALID,
              "control": control, "denominator_target_residues": target, "denominator_trials": [],
              "number_field_cover_obtained": False, "scalar_recovery_performed": False,
              "height_exclusion_or_nonmembership_proved": False,
              "search_scope": "unit-anchor rows of the LLL basis; no exhaustive enumeration"}
    path = DATA / "cm_frame_joint_field_recognition.json"
    for root in roots:
        report["denominator_trials"].append(experiment("denominator", target, root, F))
        path.write_text(json.dumps(report, indent=2)+"\n")
    report.update({"status": "pass", "wall_seconds": time.monotonic()-started,
                   "provisional_survivor_count": sum(len(t["survivor_row_indices"]) for t in report["denominator_trials"])})
    path.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|138_CM_FRAME_JOINT_FIELD_RECOGNITION", "SURVIVORS", report["provisional_survivor_count"],
          "SECONDS", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

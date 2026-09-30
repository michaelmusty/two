"""D77: certify that the oriented branch difference is not principal.

The evaluation rank at B3 gives h0_C(B3)=1. D70 excludes L~B3,
where L is the rational branch half. The double-cover pushforward
then gives h0_X(pi^*B3)=1, excluding a function with divisor D+-D-.
Only a small determinant modulo 31 is new arithmetic in this audit.
"""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("branch_class_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")


def mod31(value):
    c = Fraction(value)
    return c.numerator*pow(c.denominator, -1, 31) % 31


def determinant_mod31(rows):
    a = [list(row) for row in rows]
    det = 1
    for j in range(len(a)):
        pivot = next(i for i in range(j, len(a)) if a[i][j])
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            det = -det
        value = a[j][j]
        det = det*value % 31
        a[j] = [x*pow(value, -1, 31) % 31 for x in a[j]]
        for i in range(j+1, len(a)):
            coefficient = a[i][j]
            a[i] = [(x-coefficient*y) % 31 for x, y in zip(a[i], a[j])]
    return det % 31


def main():
    fiber_path = DATA / "cm_frame_B3_fiber.json"
    certificate_path = DATA / "cm_frame_B3_fiber_check.json"
    marks_path = DATA / "cm_frame_marks_check.json"
    model_path = DATA / "cm_frame_B3_rational_model.json"
    fiber, certificate, marks, model = [json.loads(p.read_text())
                                      for p in (fiber_path, certificate_path, marks_path, model_path)]
    for record in (fiber, certificate, marks, model):
        checks.verify_records(record)
    assert certificate["status"] == "pass" and certificate["oriented_branch_degrees"] == [9, 9]
    coords = [[mod31(x) for x in row] for row in fiber["data"]["point_coordinates"]]
    echelon = {}
    selected = []
    for index, row in enumerate(coords):
        row = list(row)
        for j in sorted(echelon):
            multiplier = row[j]
            row = [(x-multiplier*y) % 31 for x, y in zip(row, echelon[j])]
        if not any(row):
            continue
        pivot = next(i for i, x in enumerate(row) if x)
        inverse = pow(row[pivot], -1, 31)
        echelon[pivot] = [x*inverse % 31 for x in row]
        selected.append(index)
        if len(selected) == 9:
            break
    assert len(selected) == 9
    minor = [coords[i] for i in selected]
    det = determinant_mod31(minor)
    assert det != 0
    assert model["branch_degree"] == 18 and model["genus"] == 40
    assert marks["simple_branch_relation"]["h0_2B3_minus_B2_over_Q"] == 0
    gC, degree = 16, 9
    h0_K_minus_B3 = gC-len(selected)
    h0_B3 = degree+1-gC+h0_K_minus_B3
    assert h0_B3 == 1
    report = {"status": "pass", "milestone": "D77", "date": "2026-09-19",
              "sources": [checks.source(p) for p in (__file__, fiber_path, certificate_path, marks_path, model_path,
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")],
              "linear_evaluation_rank": 9, "minor_rows_one_based": [i+1 for i in selected],
              "minor_mod31": minor, "minor_determinant_mod31": det,
              "h0_C_K_minus_B3": h0_K_minus_B3, "h0_C_B3": h0_B3,
              "h0_C_B3_minus_L": 0,
              "reason_for_odd_summand_vanishing": "degree zero, and L~B3 would contradict h0(2B3-B2)=0",
              "double_cover_pushforward": "pi_* O_X = O_C + L^(-1)",
              "h0_X_pullback_B3": 1,
              "oriented_difference_principal": False,
              "proof": "D+ and D- are disjoint and pi^*B3=D++D-; a function with their difference as divisor contradicts h0=1",
              "next_divisor_equation": "div(h)=D+ - D- + 3*A, with A a degree-zero divisor",
              "three_division_class_computed": False, "cyclic_cubic_constructed": False}
    path = DATA / "cm_frame_B3_branch_class.json"
    path.write_text(json.dumps(report, indent=2)+"\n")
    print("B3_LINEAR_EVALUATION_RANK 9 MINOR_DETERMINANT_MOD31", det)
    print("H0_PULLBACK_B3 1 ORIENTED_DIFFERENCE_PRINCIPAL false")
    print("PASS|163_CM_FRAME_B3_BRANCH_CLASS")


if __name__ == "__main__":
    main()

"""Recover the fixed numerator over Q and calibrate the lift's coefficient height.

The numerator is cut out by rational D17 and order-15 jets at rational P32.
Solving those linear conditions over Q is independent of the 31-adic solves.
This recovers only the numerator, not the square class or double cover over Q.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import time

from sage.all import QQ, ZZ, GF, NumberField, PolynomialRing, matrix, vector, lcm, gcd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path":str(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    started = time.monotonic()
    helper_path = ROOT/"dembele/pari/124_cm_frame_resolvent_lift.py"
    spec = importlib.util.spec_from_file_location("lift_helpers",helper_path)
    helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    helper.BASE = QQ
    curve = json.loads((DATA/"cm_frame_curve_candidate.json").read_text())
    original = json.loads((DATA/"cm_frame_resolvent.json").read_text())
    lift = json.loads((DATA/"cm_frame_resolvent_lift.json").read_text())
    marks = json.loads((DATA/"cm_frame_marks.json").read_text())
    pairs = [tuple(p) for p in curve["monomial_pairs"]]
    T = PolynomialRing(QQ,"t")
    field = NumberField(T(curve["CM_field_polynomial_ascending"]),"a")
    xs = [field([QQ(c) for c in row]) for row in curve["CM_projective_coordinates_power_basis"]]
    products = [xs[i]*xs[j] for i,j in pairs]
    evaluation = matrix(QQ,[[x[i] for x in products] for i in range(17)])
    assert evaluation*matrix(QQ,curve["quadrics"]).transpose() == 0
    print("EXACT_D17_EVALUATION",round(time.monotonic()-started,3),flush=True)
    jets = helper.point_jets(marks["rational_point"]["primitive_coordinates"],curve["quadrics"],pairs)
    products = [jets[i]*jets[j] for i,j in pairs]
    jetmatrix = matrix(QQ,[[x[n] for x in products] for n in range(15)])
    assert jetmatrix*matrix(QQ,curve["quadrics"]).transpose() == 0
    constraints = evaluation.stack(jetmatrix)
    chart = lift["section_chart_indices_zero_based"]
    active = [chart[j] for j in lift["numerator_linear_system"]["correction_pivot_columns"]]
    square = constraints.matrix_from_columns(active)
    assert square.nrows() == square.ncols() == 32
    print("EXACT_CONSTRAINTS",round(time.monotonic()-started,3),flush=True)
    row = vector(QQ,original["numerator_coefficients"])
    correction = square.solve_right(-constraints*row)
    for j,c in zip(active,correction):
        row[j] += c
    assert constraints*row == 0
    assert len(jets) == 16
    # Verify the entire 8-digit computation against the independent Q result.
    modulus = lift["modulus"]
    residues = []
    for c in row:
        n,d = int(c.numerator()),int(c.denominator())
        assert d%31 != 0
        residues.append(n*pow(d,-1,modulus)%modulus)
    assert residues == lift["numerator_coefficients"]
    primitive = list(row*lcm([c.denominator() for c in row]))
    content = gcd([ZZ(c) for c in primitive])
    primitive = [ZZ(c)/content for c in primitive]
    height = max(abs(c) for c in primitive)
    numerator_bound = max(abs(c.numerator()) for c in row)
    denominator_bound = max(c.denominator() for c in row)
    uniqueness_bound = 2*numerator_bound*denominator_bound
    digits = 0; power = ZZ(1)
    while power <= uniqueness_bound:
        power *= 31; digits += 1
    report = {
        "status":"pass", "milestone":"D72", "base_field":"Q",
        "sources":[source(p) for p in (__file__,helper_path,
                   DATA/"cm_frame_curve_candidate.json",DATA/"cm_frame_resolvent.json",
                   DATA/"cm_frame_resolvent_lift.json",DATA/"cm_frame_marks.json")],
        "monomial_pairs_zero_based":pairs,
        "numerator_coefficients_rational":[str(c) for c in row],
        "primitive_integer_coefficients":[str(c) for c in primitive],
        "primitive_height":str(height), "primitive_height_decimal_digits":len(str(height)),
        "primitive_height_bits":int(ZZ(height).nbits()),
        "maximum_affine_numerator":str(numerator_bound),
        "maximum_affine_denominator":str(denominator_bound),
        "sufficient_digits_for_uniform_bounded_rational_reconstruction":digits,
        "bound_meaning":"31^digits > 2*max(abs(numerators))*max(denominators); sufficient, not a minimal threshold",
        "exact_divisor_containment":"D17 + 15*P32 <= div(q_num)",
        "agrees_with_lift_modulus":modulus,
        "denominator_or_cover_reconstructed_over_number_field":False,
        "wall_seconds":time.monotonic()-started,
    }
    (DATA/"cm_frame_lift_numerator.json").write_text(json.dumps(report,indent=2)+"\n")
    print("NUMERATOR_HEIGHT_DIGITS",report["primitive_height_decimal_digits"],flush=True)
    print("SUFFICIENT_RECONSTRUCTION_DIGITS",digits,flush=True)
    print("PASS|126_CM_FRAME_LIFT_NUMERATOR",round(report["wall_seconds"],3),flush=True)


if __name__ == "__main__":
    main()

"""D75: test the geometric normalization B2+2*B3 instead of B2+14*P32.

Construct short exact sections of 2K-B2-2B3, allowing curve relations.
The rational numerator alone does not transfer or identify a cover.
"""
import importlib.util
import json
from pathlib import Path
import time

from sage.all import GF, QQ, ZZ, NumberField, PolynomialRing, matrix, vector

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


norm = module("B3_normalization", ROOT / "dembele/pari/127_cm_frame_numerator_lattice.py")
proj = module("B3_projection", ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")
checks = module("B3_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")


def main():
    started = time.monotonic()
    curve_path = DATA / "cm_frame_curve_candidate.json"
    marks_path = DATA / "cm_frame_marks.json"
    curve, marks = [json.loads(p.read_text()) for p in (curve_path, marks_path)]
    pairs = [tuple(p) for p in curve["monomial_pairs"]]
    lines = [v["coefficients"] for v in marks["order_three_divisor"]["relations"]]
    assert len(lines) == 7
    products = [[a[i]*b[j]+(a[j]*b[i] if i != j else 0) for i, j in pairs]
                for k, a in enumerate(lines) for b in lines[k:]]
    A = matrix(QQ, curve["quadrics"])
    doubled = A.stack(matrix(QQ, products))
    assert doubled.rank() == 118
    double_constraints = doubled.right_kernel_matrix()
    assert double_constraints.nrows() == 18
    T = PolynomialRing(QQ, "t")
    K = NumberField(T(curve["CM_field_polynomial_ascending"]), "a")
    xs = [K([QQ(c) for c in row]) for row in curve["CM_projective_coordinates_power_basis"]]
    mon = [xs[i]*xs[j] for i, j in pairs]
    evaluation = matrix(QQ, [[q[j] for q in mon] for j in range(17)])
    pt = marks["rational_point"]["primitive_coordinates"]
    point_row = matrix(QQ, [[pt[i]*pt[j] for i, j in pairs]])
    constraints = double_constraints.stack(evaluation).stack(point_row)
    assert constraints.nrows() == constraints.rank() == 36
    assert constraints*A.transpose() == 0
    integral = matrix(ZZ, [norm.primitive(row) for row in constraints])
    print("B3_EXACT_CONSTRAINTS", 36, round(time.monotonic()-started, 3), flush=True)
    lattice = integral.right_kernel_matrix(algorithm="pari", basis="LLL")
    assert lattice.nrows() == 100 and constraints*lattice.transpose() == 0
    smith = lattice.elementary_divisors()
    assert smith == [1]*100
    pair_path = DATA / "cm_frame_doubling_normalized_128.json"
    chart = json.loads(pair_path.read_text())["section_chart_indices_zero_based"]
    projection = proj.section_projection(curve, chart)
    images = lattice.change_ring(QQ)*projection
    nonzero = [row for row, image in zip(lattice, images) if image]
    # Short section directions can be interspersed with curve relations;
    # LLL need not put all 91 pure relations in separate rows.
    nonzero_images = matrix(QQ, nonzero)*projection
    pivots = list(nonzero_images.change_ring(GF(31)).transpose().pivots())
    assert len(pivots) == 9
    sections = [nonzero[i] for i in pivots]
    assert (matrix(QQ, sections)*projection).change_ring(GF(31)).rank() == 9
    candidates = []
    seen = set()
    trials = list(nonzero)+[sections[i]+sign*sections[j]
                            for i in range(9) for j in range(i+1, 9) for sign in (-1, 1)]
    for row in trials:
        row = norm.primitive(row)
        if tuple(row) in seen:
            continue
        seen.add(tuple(row))
        height = max(abs(x) for x in row)
        candidates.append({"coefficients": [int(x) for x in row], "height": str(height),
                           "height_decimal_digits": len(str(height))})
    candidates.sort(key=lambda c: int(c["height"]))
    report = {"status": "pass", "milestone": "D75", "date": "2026-09-18",
              "sources": [checks.source(p) for p in (__file__, curve_path, marks_path, pair_path,
                          DATA / "cm_frame_marks_check.json", DATA / "cm_frame_joint_field_check.json",
                          ROOT / "dembele/pari/127_cm_frame_numerator_lattice.py",
                          ROOT / "dembele/pari/133_cm_frame_projective_denominator.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")],
              "vanishing_divisor": "D17+P32+2*B3", "vanishing_degree": 36,
              "constraint_rank": 36, "section_dimension": 9, "full_integer_lattice_rank": 100,
              "smith_invariants": [int(x) for x in smith],
              "full_lattice_basis": [[int(x) for x in row] for row in lattice],
              "section_rows": [[int(x) for x in row] for row in sections],
              "nonzero_section_rows_in_full_LLL_basis": len(nonzero),
              "section_height_digits": [len(str(max(abs(x) for x in row))) for row in sections],
              "candidates": candidates, "best": candidates[0],
              "cover_transfer_performed": False, "shortest_vector_proved": False,
              "wall_seconds": time.monotonic()-started}
    path = DATA / "cm_frame_B3_numerator.json"
    path.write_text(json.dumps(report, indent=2)+"\n")
    path.with_suffix(".m").write_text("// D75 exact numerator candidates for B2+2*B3.\n"
            +"B3_numerator_candidates := "+str([c["coefficients"] for c in candidates])+";\n")
    print("PASS|142_CM_FRAME_B3_NUMERATOR", "HEIGHT_DIGITS", candidates[0]["height_decimal_digits"],
          "SECTION_HEIGHTS", report["section_height_digits"], round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

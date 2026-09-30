"""D73: short exact numerators, with and without the known curve relations.

Compute saturated integer kernels of the D17 and order-15 P32 conditions.
The 45-column chart has rank 13; the full 136-column kernel has rank 104,
including the 91-dimensional space of equations of C. LLL on the latter
also permits shortening representatives by adding known curve equations.
This is a local adaptation of the quotient-by-known-relations principle
in the M23 paper, not an implementation of its unpublished reduction code.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

from sage.all import QQ, ZZ, GF, NumberField, PolynomialRing, matrix, vector, lcm, gcd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def primitive(row):
    row = vector(ZZ, row * lcm([c.denominator() for c in row]))
    content = gcd(list(row))
    row = vector(ZZ, [c // content for c in row])
    if next(c for c in row if c) < 0:
        row = -row
    return row


def integers(rows):
    return [[int(c) for c in row] for row in rows]


def exact_constraints(helper, curve, marks):
    pairs = [tuple(p) for p in curve["monomial_pairs"]]
    T = PolynomialRing(QQ, "t")
    field = NumberField(T(curve["CM_field_polynomial_ascending"]), "a")
    xs = [field([QQ(c) for c in row]) for row in curve["CM_projective_coordinates_power_basis"]]
    products = [xs[i] * xs[j] for i, j in pairs]
    evaluation = matrix(QQ, [[x[i] for x in products] for i in range(17)])
    helper.BASE = QQ
    jets = helper.point_jets(marks["rational_point"]["primitive_coordinates"], curve["quadrics"], pairs)
    products = [jets[i] * jets[j] for i, j in pairs]
    jetmatrix = matrix(QQ, [[x[n] for x in products] for n in range(15)])
    constraints = evaluation.stack(jetmatrix)
    assert constraints * matrix(QQ, curve["quadrics"]).transpose() == 0
    assert constraints.rank() == 32
    return constraints, pairs


def saturated_kernel(M):
    integral = matrix(ZZ, [primitive(row) for row in M.rows()])
    K = integral.right_kernel_matrix(algorithm="pari", basis="LLL")
    assert K.nrows() == M.ncols() - 32 and M * K.transpose() == 0
    # Unit Smith invariants certify saturation in the ambient integer lattice.
    invariants = K.elementary_divisors()
    assert invariants == [1] * K.nrows()
    return K, [int(x) for x in invariants]


def local_filter(helper, lift, pairs):
    k = GF(31)
    jets = matrix(k, lift["point_jets"])
    coefficient15 = vector(k, [sum(jets[n, i] * jets[15-n, j] for n in range(16))
                               for i, j in pairs])
    checks = []
    T = PolynomialRing(k, "s")
    for c in lift["components"]:
        if c["label"] not in ("D17", "E"):
            continue
        h = T(c["etale_modulus"])
        A = k if c["degree"] == 1 else GF(31**c["degree"], name="a", modulus=h)
        a = -h[0] if c["degree"] == 1 else A.gen()
        xs = [sum(A(v)*a**i for i, v in enumerate(row)) for row in c["coordinates"]]
        vs = [sum(A(v)*a**i for i, v in enumerate(row)) for row in c["tangent"]]
        checks.append((c["label"], xs, vs))

    def acceptable(row):
        if coefficient15.dot_product(vector(k, row)) == 0:
            return False
        for label, xs, vs in checks:
            if label == "D17":
                assert helper.evaluate(row, xs, pairs) == 0
                if helper.dot(helper.gradient(row, xs, pairs), vs) == 0:
                    return False
            elif helper.evaluate(row, xs, pairs) == 0:
                return False
        return True

    return acceptable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DATA / "cm_frame_numerator_lattice.json")
    args = parser.parse_args()
    started = time.monotonic()
    helper_path = ROOT / "dembele/pari/124_cm_frame_resolvent_lift.py"
    spec = importlib.util.spec_from_file_location("lift_helpers", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    curve = json.loads((DATA / "cm_frame_curve_candidate.json").read_text())
    marks = json.loads((DATA / "cm_frame_marks.json").read_text())
    lift = json.loads((DATA / "cm_frame_resolvent_lift.json").read_text())
    old = json.loads((DATA / "cm_frame_lift_numerator.json").read_text())
    M, pairs = exact_constraints(helper, curve, marks)
    print("EXACT_CONSTRAINTS", round(time.monotonic()-started, 3), flush=True)
    chart = lift["section_chart_indices_zero_based"]
    Kchart, schart = saturated_kernel(M.matrix_from_columns(chart))
    chart_rows = []
    for row in Kchart:
        ambient = vector(ZZ, 136)
        for j, c in zip(chart, row):
            ambient[j] = c
        chart_rows.append(primitive(ambient))
    print("CHART_LATTICE", Kchart.nrows(), "MIN_HEIGHT_DIGITS",
          min(len(str(max(abs(c) for c in row))) for row in chart_rows),
          round(time.monotonic()-started, 3), flush=True)
    Kfull, sfull = saturated_kernel(M)
    print("FULL_LATTICE", Kfull.nrows(), round(time.monotonic()-started, 3), flush=True)
    equations = matrix(QQ, curve["quadrics"]).row_space()
    full_rows = [primitive(row) for row in Kfull if vector(QQ, row) not in equations]
    relation_rows = [row for row in Kfull if vector(QQ, row) in equations]
    assert matrix(QQ, curve["quadrics"] + integers(full_rows)).rank() == 104
    acceptable = local_filter(helper, lift, pairs)
    candidates = []
    seen = set()
    for label, rows in (("chart", chart_rows), ("relations_allowed", full_rows)):
        # Include deterministic short two-vector combinations, retaining provenance.
        trials = [(row, [i, 1]) for i, row in enumerate(rows)]
        trials += [(rows[i] + sign*rows[j], [i, 1, j, sign])
                   for i in range(len(rows)) for j in range(i+1, len(rows)) for sign in (-1, 1)]
        accepted = []
        for row, combination in trials:
            row = primitive(row)
            key = tuple(row)
            if key in seen or not acceptable(row):
                continue
            seen.add(key)
            height = max(abs(c) for c in row)
            entry = {"method": label, "basis_combination": combination,
                     "coefficients": [int(c) for c in row], "height": str(height),
                     "height_decimal_digits": len(str(height)), "height_bits": int(height.nbits()),
                     "squared_norm": str(row.dot_product(row))}
            candidates.append(entry)
            accepted.append(entry)
        assert accepted
        best = min(accepted, key=lambda x: (int(x["height"]), int(x["squared_norm"])))
        print("BEST", label, best["height_decimal_digits"], best["height_bits"], flush=True)
    candidates.sort(key=lambda x: (int(x["height"]), int(x["squared_norm"])))
    best = candidates[0]
    assert M * vector(ZZ, best["coefficients"]) == 0
    assert int(best["height"]) < int(old["primitive_height"])
    report = {
        "status": "pass", "milestone": "D73", "date": "2026-09-18",
        "sources": [source(p) for p in (__file__, helper_path,
                    DATA / "cm_frame_curve_candidate.json", DATA / "cm_frame_marks.json",
                    DATA / "cm_frame_resolvent_lift.json", DATA / "cm_frame_lift_numerator.json")],
        "constraint_rank": 32, "section_dimension": 13,
        "section_chart_indices_zero_based": chart,
        "chart_lattice_basis": integers(Kchart), "chart_smith_invariants": schart,
        "full_lattice_basis": integers(Kfull), "full_smith_invariants": sfull,
        "full_basis_curve_relation_rows": len(relation_rows),
        "full_basis_nonzero_sections": integers(full_rows),
        "old_primitive_height_decimal_digits": old["primitive_height_decimal_digits"],
        "best": best, "candidate_count": len(candidates), "candidates": candidates[:20],
        "best_by_method": {label: next(x for x in candidates if x["method"] == label)
                           for label in ("chart", "relations_allowed")},
        "local_filter": "exact order 15 at P32; simple at D17; nonvanishing at E, all mod 31",
        "shortest_vector_proved": False, "denominator_transferred": False,
        "wall_seconds": time.monotonic()-started,
    }
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    data_m = args.output.with_suffix(".m")
    data_m.write_text("// D73 exact integer numerator candidates, in increasing coefficient height.\n"
                      + "normalized_numerator_candidates := "
                      + str([x["coefficients"] for x in candidates[:20]]) + ";\n"
                      + "normalization_chart := " + str([j+1 for j in chart]) + ";\n")
    print("PASS|127_CM_FRAME_NUMERATOR_LATTICE", best["height_decimal_digits"],
          round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

"""D76: recognize the six-product denominator space over Q.

Fit whole quadratic representatives modulo curve equations at 31^64,
then test their section classes for membership in the saved space at
31^128. An exact six-dimensional rational space is a positive control.
Any recovered denominator space remains provisional until exact geometry.
"""
import importlib.util
import json
from pathlib import Path
import time

from sage.all import GF, QQ, ZZ, Zmod, identity_matrix, matrix, vector

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("space_recognition_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
proj = module("space_recognition_projection", ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")
rec = module("space_recognition_rational", ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py")


def experiment(label, target, P, chart, curve, exact=None):
    started = time.monotonic()
    m, M = 31**64, 31**128
    Z, Zhigh = Zmod(m), Zmod(M)
    pivots = list(target.change_ring(GF(31)).pivots())
    dimension = len(pivots)
    assert dimension == 6
    normal = target.matrix_from_columns(pivots).inverse()*target
    assert normal.matrix_from_columns(pivots) == identity_matrix(Zhigh, dimension)
    others = [j for j in range(45) if j not in pivots]
    P0 = P.change_ring(Z)
    H = (P0.matrix_from_columns(others)
         -P0.matrix_from_columns(pivots)*normal.change_ring(Z).matrix_from_columns(others)).transpose()
    active = [chart[j] for j in others]
    assert H.matrix_from_columns(active) == identity_matrix(Z, 39)
    B = identity_matrix(ZZ, 136)
    for j in range(136):
        if j in active:
            B[j, j] = m
        else:
            for i, col in enumerate(active):
                B[j, col] = -ZZ(H[i, j])
    equations = matrix(ZZ, curve["quadrics"])
    assert B.change_ring(Z)*H.transpose() == 0
    assert equations.change_ring(Z)*H.transpose() == 0
    print("SPACE_LATTICE_READY", label, 136, 39, flush=True)
    reduced = matrix(ZZ, [row for row in equations.stack(B).LLL() if row])
    assert reduced.nrows() == 136 and abs(reduced.det()) == m**39
    assert reduced.change_ring(Z)*H.transpose() == 0
    images = reduced.change_ring(QQ)*P
    high = images.change_ring(Zhigh)
    defects = high.matrix_from_columns(others)-high.matrix_from_columns(pivots)*normal.matrix_from_columns(others)
    records, survivors = [], []
    for i, (row, image, defect) in enumerate(zip(reduced, images, defects)):
        if not image:
            continue
        matching = min(rec.valuation(int(x), 128) for x in defect)
        assert matching >= 64
        height = max(abs(x) for x in row)
        record = {"row_index_zero_based": i, "coefficients": [int(x) for x in row],
                  "height": str(height), "height_decimal_digits": len(str(height)),
                  "matching_digits": matching, "validates_unused_digits": matching == 128}
        if matching == 128:
            if exact is not None:
                assert image in exact.row_space()
                record["exact_control_space_membership"] = True
            survivors.append(record)
        records.append(record)
    survivors.sort(key=lambda r: int(r["height"]))
    surviving_images = matrix(QQ, [vector(QQ, r["coefficients"])*P for r in survivors]) if survivors else matrix(QQ, 0, 45)
    rank = int(surviving_images.change_ring(GF(31)).rank())
    selected = list(surviving_images.change_ring(GF(31)).transpose().pivots()) if rank else []
    selected_rows = [survivors[i]["coefficients"] for i in selected]
    control_rejected = None
    if exact is not None:
        assert rank == 6
        assert (matrix(QQ, selected_rows)*P).row_space() == exact.row_space()
        changed = matrix(Zhigh, normal)
        changed[0, others[0]] += m
        control_images = (matrix(QQ, selected_rows)*P).change_ring(Zhigh)
        altered_defect = (control_images.matrix_from_columns(others)
                         -control_images.matrix_from_columns(pivots)*changed.matrix_from_columns(others))
        assert altered_defect != 0 and altered_defect.change_ring(Z) == 0
        control_rejected = True
    print("SPACE_RECOGNITION", label, "RANK", rank, "SURVIVORS", len(survivors),
          "HEIGHTS", [survivors[i]["height_decimal_digits"] for i in selected],
          "SECONDS", round(time.monotonic()-started, 3), flush=True)
    return {"label": label, "training_digits": 64, "validation_digits": 128,
            "dimension": dimension, "projective_pivot_chart_columns": pivots,
            "lattice_rank": 136, "congruence_equations": 39, "lattice_index": str(m**39),
            "candidate_count": len(records), "survivor_count": len(survivors),
            "surviving_rank_mod31": rank, "selected_quadric_rows": selected_rows,
            "selected_height_digits": [survivors[i]["height_decimal_digits"] for i in selected],
            "survivors": survivors, "candidate_matching_digits": [r["matching_digits"] for r in records],
            "control_unused_digit_mutation_rejected": control_rejected,
            "wall_seconds": time.monotonic()-started}


def main():
    started = time.monotonic()
    check_path = DATA / "cm_frame_B3_lift_check.json"
    check = json.loads(check_path.read_text())
    checks.verify_records(check)
    assert check["status"] == "pass"
    curve_path = DATA / "cm_frame_curve_candidate.json"
    low_path = DATA / "cm_frame_B3_product_lift_64.json"
    high_path = DATA / "cm_frame_B3_product_lift_128.json"
    control_path = DATA / "cm_frame_B3_numerator.json"
    curve, lower, upper, control = [json.loads(p.read_text()) for p in (curve_path, low_path, high_path, control_path)]
    chart = upper["section_chart_indices_zero_based"]
    P = proj.section_projection(curve, chart)
    Z = Zmod(31**128)
    known = matrix(QQ, control["section_rows"][:6])*P
    assert known.change_ring(GF(31)).rank() == 6
    test = experiment("known_rational_six_space", known.change_ring(Z), P, chart, curve, exact=known)
    target = matrix(Z, [[row[j] for j in chart] for row in upper["data"]["product_denominators"]])
    assert [[int(x) % (31**64) for x in row] for row in target] == [
        [row[j] for j in chart] for row in lower["data"]["product_denominators"]]
    result = experiment("B3_denominator_six_space", target, P, chart, curve)
    selected = [upper["data"]["product_selected_denominator"][j] for j in chart]
    anchor = next(i for i, x in enumerate(selected) if x % 31)
    inverse = pow(selected[anchor], -1, 31**128)
    ratios = [rec.rational_candidate(x*inverse % (31**128), 64, 128)
              for i, x in enumerate(selected) if i != anchor]
    report = {"status": "pass", "milestone": "D76", "date": "2026-09-18",
              "sources": [checks.source(p) for p in (__file__, check_path, curve_path, low_path, high_path,
                          control_path, ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py",
                          ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")],
              "control": test, "denominator_space": result,
              "selected_denominator_rational_ratios": ratios,
              "selected_ratio_survivors": sum(bool(c and c["validates_unused_digits"]) for c in ratios),
              "arithmetic_space_provisional": True, "number_field_cover_obtained": False,
              "wall_seconds": time.monotonic()-started}
    path = DATA / "cm_frame_B3_space_recognition.json"
    path.write_text(json.dumps(report, indent=2)+"\n")
    path.with_suffix(".m").write_text("// D76 provisional rational product-space representatives.\n"
        +"recognized_product_rows := "+str(result["selected_quadric_rows"])+";\n")
    print("PASS|150_CM_FRAME_B3_SPACE_RECOGNITION", "RANK", result["surviving_rank_mod31"],
          "SELECTED_RATIO_SURVIVORS", report["selected_ratio_survivors"], round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

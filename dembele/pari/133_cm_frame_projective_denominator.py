"""D74: reconstruct a whole rational quadric modulo known curve equations.

The congruence lattice contains every integer quadric whose class is in
the given projective line modulo 31^64. Training uses 64 digits; validation
uses 128. A known 39-digit section supplies an exact positive control.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import time

from sage.all import QQ, ZZ, GF, Zmod, matrix, vector, identity_matrix

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def section_projection(curve, chart):
    A = matrix(QQ, curve["quadrics"])
    pivots = [j for j in range(136) if j not in chart]
    reduced = A.matrix_from_columns(pivots).inverse()*A
    P = matrix(QQ, 136, 45)
    for i, j in enumerate(chart):
        P[j, i] = 1
    for i, j in enumerate(pivots):
        for k, col in enumerate(chart):
            P[j, k] = -reduced[i, col]
    assert A*P == 0 and P.matrix_from_rows(chart) == identity_matrix(QQ, 45)
    assert all(c.denominator() % 31 for c in P.list())
    return P


def experiment(label, target, P, chart, curve, exact_target=None):
    started = time.monotonic()
    train, valid = 64, 128
    modulus = 31**train
    Z = Zmod(modulus)
    anchor = next(i for i, c in enumerate(target) if ZZ(c) % 31)
    others = [i for i in range(45) if i != anchor]
    ratios = [Z(c)/Z(target[anchor]) for c in target]
    P0 = P.change_ring(Z)
    H = matrix(Z, [[P0[j, i]-ratios[i]*P0[j, anchor] for j in range(136)] for i in others])
    active = [chart[i] for i in others]
    assert H.matrix_from_columns(active) == identity_matrix(Z, 44)
    # With these 44 identity columns, the displayed triangular basis is
    # the full integral congruence kernel, of index (31^64)^44.
    B = identity_matrix(ZZ, 136)
    for j in range(136):
        if j in active:
            B[j, j] = modulus
        else:
            for i, col in enumerate(active):
                B[j, col] = -ZZ(H[i, j])
    assert B.change_ring(Z)*H.transpose() == 0
    equations = matrix(ZZ, curve["quadrics"])
    assert equations.change_ring(Z)*H.transpose() == 0
    # Adding known rows does not change the lattice; it exposes its short
    # relation directions before reduction of the large modular basis.
    seeded = equations.stack(B)
    print("LATTICE_READY", label, seeded.nrows(), seeded.ncols(), flush=True)
    reduced = seeded.LLL()
    assert reduced.change_ring(Z)*H.transpose() == 0
    print("LATTICE_REDUCED", label, round(time.monotonic()-started, 3), flush=True)
    reduced = matrix(ZZ, [row for row in reduced if row])
    section_rows = reduced.change_ring(QQ)*P
    Zvalid = Zmod(31**valid)
    target_valid = vector(Zvalid, target)
    target_Q = None if exact_target is None else vector(QQ, exact_target)*P
    candidates = []
    curve_count = 0
    for row, image in zip(reduced, section_rows):
        if not image:
            curve_count += 1
            continue
        im = vector(Zvalid, image)
        if ZZ(im[anchor]) % 31 == 0:
            continue
        residuals = [int(im[i]*target_valid[anchor]-im[anchor]*target_valid[i]) for i in others]
        assert all(c % modulus == 0 for c in residuals)
        survives = all(c == 0 for c in residuals)
        height = max(abs(c) for c in row)
        exact = (False if target_Q is None else
                 all(image[i]*target_Q[anchor] == image[anchor]*target_Q[i] for i in others))
        candidates.append({"coefficients": [str(c) for c in row], "height_decimal_digits": len(str(height)),
                           "height": str(height), "validates_unused_digits": survives,
                           "exact_projective_control_identity": bool(exact)})
    candidates.sort(key=lambda x: int(x["height"]))
    assert curve_count == 91
    if exact_target is not None:
        assert any(c["validates_unused_digits"] and c["exact_projective_control_identity"] for c in candidates)
    survivors = [c for c in candidates if c["validates_unused_digits"]]
    print("WHOLE_QUADRIC", label, "SURVIVORS", len(survivors), "TESTED", len(candidates),
          "MIN_HEIGHT_DIGITS", min(c["height_decimal_digits"] for c in candidates), flush=True)
    return {"label": label, "training_digits": train, "validation_digits": valid,
            "congruence_equations": 44, "lattice_rank": 136, "known_curve_directions": curve_count,
            "projective_anchor_chart_index": anchor, "candidate_count": len(candidates),
            "smallest_candidate": candidates[0], "survivors": survivors,
            "minimum_candidate_height_digits": min(c["height_decimal_digits"] for c in candidates),
            "wall_seconds": time.monotonic()-started}


def main():
    started = time.monotonic()
    curve = json.loads((DATA / "cm_frame_curve_candidate.json").read_text())
    path = DATA / "cm_frame_doubling_normalized_128.json"
    data = json.loads(path.read_text())
    chart = data["section_chart_indices_zero_based"]
    P = section_projection(curve, chart)
    full_num = data["numerator_coefficients"]
    target_num = vector(QQ, full_num)*P
    # Convert rational chart coordinates to p-adic residues only for fitting.
    target_num_mod = [int(Zmod(31**128)(x)) for x in target_num]
    control = experiment("known_numerator", target_num_mod, P, chart, curve, exact_target=full_num)
    denominator = [data["denominator_coefficients"][j] for j in chart]
    result = experiment("denominator", denominator, P, chart, curve)
    report = {"status": "pass", "milestone": "D74", "date": "2026-09-18",
              "sources": [source(p) for p in (__file__, path, DATA / "cm_frame_curve_candidate.json",
                          DATA / "cm_frame_doubling_check.json", DATA / "cm_frame_denominator_recognition.json")],
              "control": control, "denominator": result,
              "search_field": "Q", "field_F_whole_section_search_performed": False,
              "nonmembership_or_height_exclusion_proved": False,
              "number_field_cover_obtained": False, "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_projective_denominator.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|133_CM_FRAME_PROJECTIVE_DENOMINATOR", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

"""D74: bounded Q/F coefficient recognition with unused-digit validation.

Search both the scale-preserving coefficients and projective coefficient
ratios. Projective scaling is diagnostic only: it does not alter the saved
radicand. Finite-precision agreement is not an exact algebraic certificate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

from sage.all import QQ, ZZ, GF, CyclotomicField, PolynomialRing, matrix, vector, gcd, lcm, rational_reconstruction

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def hensel_root(f, initial, digits):
    root, precision = int(initial), 1
    while precision < digits:
        precision = min(2*precision, digits)
        modulus = 31**precision
        root = (root-int(f(root))*pow(int(f.derivative()(root)), -1, modulus)) % modulus
        assert int(f(root)) % modulus == 0
    return root


def valuation(n, limit):
    if n == 0:
        return limit
    v = 0
    while v < limit and n % 31 == 0:
        n //= 31
        v += 1
    return v


def rational_candidate(value, train, valid):
    try:
        candidate = rational_reconstruction(ZZ(value % (31**train)), ZZ(31**train))
    except (ArithmeticError, ZeroDivisionError):
        return None
    a, b = int(candidate.numerator()), int(candidate.denominator())
    v = valuation(a-b*value, valid)
    assert v >= train
    return {"numerator": str(a), "denominator": str(b), "matching_digits": v,
            "validates_unused_digits": v == valid}


def field_candidates(value, root, train, valid):
    modulus = 31**train
    residues = [pow(root, j, modulus) for j in range(8)]+[-value % modulus]
    K = matrix(ZZ, 9, 9)
    K[0, 0] = modulus
    for i in range(1, 9):
        K[i, i] = 1
        K[i, 0] = -residues[i] % modulus
    K = K.LLL()
    assert all(int(x) % modulus == 0 for x in K*vector(ZZ, residues))
    rows = []
    for row in K:
        if row[8] == 0 or row[8] % 31 == 0:
            continue
        content = gcd(list(row))
        row = [int(x // content) for x in row]
        if row[8] < 0:
            row = [-x for x in row]
        defect = sum(row[j]*pow(root, j, 31**valid) for j in range(8))-row[8]*value
        v = valuation(defect, valid)
        assert v >= train
        height = max(abs(x) for x in row)
        rows.append({"coefficients_and_denominator": [str(x) for x in row],
                     "height_decimal_digits": len(str(height)), "matching_digits": v,
                     "validates_unused_digits": v == valid})
    rows.sort(key=lambda r: max(abs(int(x)) for x in r["coefficients_and_denominator"]))
    return rows


def numerator_chart_calibration():
    curve = json.loads((DATA / "cm_frame_curve_candidate.json").read_text())
    short = json.loads((DATA / "cm_frame_normalized_resolvent.json").read_text())
    A = matrix(QQ, curve["quadrics"])
    chart = short["section_chart_indices_zero_based"]
    pivots = [j for j in range(136) if j not in chart]
    row = vector(QQ, short["numerator_coefficients"])
    correction = A.matrix_from_columns(pivots).transpose().solve_right(vector(QQ, [row[j] for j in pivots]))
    reduced = row-correction*A
    assert all(reduced[j] == 0 for j in pivots)
    denominator = lcm([x.denominator() for x in reduced])
    integral = [ZZ(denominator*x) for x in reduced]
    content = gcd(integral)
    height = max(abs(x // content) for x in integral)
    return {"full_monomial_primitive_height_digits": 39,
            "chart_primitive_height_digits": len(str(height)),
            "chart_max_numerator_digits": max(len(str(abs(x.numerator()))) for x in reduced),
            "chart_max_denominator_digits": max(len(str(x.denominator())) for x in reduced)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final-digits", type=int, choices=(32, 64, 128, 256), default=128)
    args = parser.parse_args()
    started = time.monotonic()
    check_path = DATA / "cm_frame_doubling_check.json"
    check = json.loads(check_path.read_text())
    assert check["status"] == "pass" and check["final_precision_digits"] >= args.final_digits
    T = PolynomialRing(ZZ, "t")
    f = T([2, 0, -16, 0, 20, 0, -8, 0, 1])
    zeta = CyclotomicField(32).gen()
    assert T((zeta+1/zeta).minpoly()) == f
    roots31 = sorted(int(r) for r, e in f.change_ring(GF(31)).roots() if e == 1)
    assert len(roots31) == 8
    roots = [hensel_root(f, r, args.final_digits) for r in roots31]
    # Positive and negative controls with known Q and F elements.
    train, valid = args.final_digits//2, args.final_digits
    short = json.loads((DATA / "cm_frame_normalized_resolvent.json").read_text())
    known_integer = short["numerator_coefficients"][0]
    control_train = max(64, train)
    control_valid = 2*control_train
    qc = rational_candidate(known_integer % (31**control_valid), control_train, control_valid)
    assert qc and qc["validates_unused_digits"] and QQ(qc["numerator"])/QQ(qc["denominator"]) == known_integer
    bad = rational_candidate((known_integer+31**control_train) % (31**control_valid), control_train, control_valid)
    assert bad and not bad["validates_unused_digits"]
    control_root = hensel_root(f, roots31[0], control_valid)
    ac = [(-1)**i*((i+1)*10**7+2*i+3) for i in range(8)]
    bc = 999983
    control_value = (sum(ac[i]*pow(control_root, i, 31**control_valid) for i in range(8))
                     *pow(bc, -1, 31**control_valid)) % (31**control_valid)
    fc = field_candidates(control_value, control_root, control_train, control_valid)
    expected = [str(x) for x in ac+[bc]]
    assert any(c["validates_unused_digits"] and c["coefficients_and_denominator"] == expected for c in fc)
    fc_bad = field_candidates((control_value+31**control_train) % (31**control_valid),
                              control_root, control_train, control_valid)
    assert not any(c["validates_unused_digits"] for c in fc_bad)
    print("PASS|RECOGNITION_Q_F_POSITIVE_AND_UNUSED_DIGIT_NEGATIVE_CONTROLS", flush=True)
    results, inputs = [], []
    valid = 32
    while valid <= args.final_digits:
        train = valid//2
        lower_path = DATA / f"cm_frame_doubling_normalized_{train}.json"
        upper_path = DATA / f"cm_frame_doubling_normalized_{valid}.json"
        lower, upper = [json.loads(p.read_text()) for p in (lower_path, upper_path)]
        inputs.extend([source(lower_path), source(upper_path)])
        chart = upper["section_chart_indices_zero_based"]
        unit = next(j for j in chart if upper["denominator_coefficients"][j] % 31)
        for mode in ("affine", "projective"):
            inv_upper = pow(upper["denominator_coefficients"][unit], -1, 31**valid) if mode == "projective" else 1
            inv_lower = pow(lower["denominator_coefficients"][unit], -1, 31**train) if mode == "projective" else 1
            records = []
            for j in chart:
                if mode == "projective" and j == unit:
                    continue
                value = upper["denominator_coefficients"][j]*inv_upper % (31**valid)
                assert value % (31**train) == lower["denominator_coefficients"][j]*inv_lower % (31**train)
                qr = rational_candidate(value, train, valid)
                fr = []
                for residue, root in zip(roots31, roots):
                    candidates = field_candidates(value, root, train, valid)
                    fr.append({"root_mod31": residue, "tested_rows": len(candidates),
                               "best_candidate": candidates[0] if candidates else None,
                               "survivors": [c for c in candidates if c["validates_unused_digits"]],
                               "maximum_matching_digits": max((c["matching_digits"] for c in candidates), default=0)})
                records.append({"monomial_index_zero_based": j, "rational_candidate": qr, "field_trials": fr})
            qr_count = sum(r["rational_candidate"] is not None for r in records)
            qr_survive = sum(bool(r["rational_candidate"] and r["rational_candidate"]["validates_unused_digits"]) for r in records)
            fr_survive = sum(any(trial["survivors"] for trial in r["field_trials"]) for r in records)
            result = {"training_digits": train, "validation_digits": valid, "mode": mode,
                      "projective_unit_index_zero_based": unit if mode == "projective" else None,
                      "coefficients_tested": len(records), "rational_training_fits": qr_count,
                      "rational_survivors": qr_survive, "field_survivors": fr_survive,
                      "records": records}
            results.append(result)
            print("RECOGNITION", train, valid, mode, "Q", qr_survive, "F", fr_survive,
                  "OF", len(records), flush=True)
        valid *= 2
    calibration = numerator_chart_calibration()
    report = {"status": "pass", "milestone": "D74", "date": "2026-09-18",
              "sources": [source(p) for p in (__file__, check_path, DATA / "cm_frame_curve_candidate.json",
                          DATA / "cm_frame_normalized_resolvent.json")]+inputs,
              "field_polynomial_ascending": [int(x) for x in f.list()], "all_roots_mod31": roots31,
              "positive_and_negative_controls_pass": True, "control_precision_digits": control_valid,
              "numerator_chart_calibration": calibration, "results": results,
              "provisional_candidates_only": True, "nonmembership_in_Q_or_F_proved": False,
              "height_exclusion_bound_proved": False, "number_field_cover_obtained": False,
              "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_denominator_recognition.json").write_text(json.dumps(report, indent=2)+"\n")
    print("NUMERATOR_CHART_CALIBRATION", calibration, flush=True)
    print("PASS|132_CM_FRAME_DENOMINATOR_RECOGNITION", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

"""D76: export the exact Q cover and recover its recorded 31-adic twist.

The primitive rational denominator is a square section in the split
Veronese space. Its rank-one product coordinates give the explicit
square factor to the old lift. A scalar 1 or 3 fixes the residue twist;
this does not identify a global arithmetic/Shimura quadratic twist.
"""
import importlib.util
import json
from pathlib import Path
import time

from sage.all import GF, QQ, ZZ, Zmod, matrix, vector, gcd, lcm

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("rational_model_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
proj = module("rational_model_projection", ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")
veronese = module("rational_model_fields", ROOT / "dembele/pari/152_cm_frame_B3_veronese.py")


def unit_square_root(value, digits):
    root = next(x for x in range(1, 31) if (x*x-value) % 31 == 0)
    precision = 1
    while precision < digits:
        precision = min(2*precision, digits)
        m = 31**precision
        root = (root+value*pow(root, -1, m))*pow(2, -1, m) % m
    assert (root*root-value) % (31**digits) == 0
    return root


def main():
    started = time.monotonic()
    job_path = DATA / "cm_frame_B3_rational_cover_job.json"
    checks.read_job(job_path, "PASS|153_CM_FRAME_B3_RATIONAL_COVER")
    output = (DATA / "cm_frame_B3_rational_cover.out").read_text()
    ver_path = DATA / "cm_frame_B3_veronese.json"
    prod_path = DATA / "cm_frame_B3_product_lift_128.json"
    curve_path = DATA / "cm_frame_curve_candidate.json"
    ver, prod, curve = [json.loads(p.read_text()) for p in (ver_path, prod_path, curve_path)]
    for record in (ver, prod):
        checks.verify_records(record)
    row = vector(QQ, [QQ(x) for x in ver["veronese_section_rows"][0]])
    denominator = veronese.primitive(row)
    index = next(i for i, x in enumerate(row) if x)
    scale = denominator[index]/row[index]
    assert denominator == scale*row
    chart = prod["section_chart_indices_zero_based"]
    P = proj.section_projection(curve, chart)
    digits = 128
    modulus = 31**digits
    Z = Zmod(modulus)
    product_space = matrix(Z, [[r[j] for j in chart] for r in prod["data"]["product_denominators"]])
    target = (denominator*P).change_ring(Z)
    pivots = list(product_space.change_ring(GF(31)).pivots())
    coefficients = vector(Z, [target[j] for j in pivots])*product_space.matrix_from_columns(pivots).inverse()
    assert coefficients*product_space == target
    S = matrix(Z, 3, 3)
    for c, (i, j) in zip(coefficients, prod["data"]["product_indices"]):
        S[i-1, j-1] = S[j-1, i-1] = c if i == j else c/Z(2)
    anchor = next(i for i in range(3) if int(S[i, i]) % 31)
    lam = S[anchor, anchor]
    v = vector(Z, [S[i, anchor]/lam for i in range(3)])
    assert S == lam*v.column()*v.row()
    twist = 1 if GF(31)(int(lam)).is_square() else 3
    assert GF(31)(3).is_square() is False
    root = unit_square_root(int(Z(twist)*lam), digits)
    newq = Z(root)*v*matrix(Z, prod["data"]["product_q_basis"])
    denominator *= twist
    scale *= twist
    n = prod["new_numerator_coefficients"]
    d = [int(x) for x in denominator]
    second = veronese.field(output, "SECOND_NUMERATOR")
    witnesses = [[QQ(x) for x in r] for r in veronese.field(output, "RATIONAL_T_MEMBERSHIP_WITNESSES")]
    e_rows = veronese.field(output, "RATIONAL_COVER_E_QUADRICS")
    bindings = {"rational_numerator": n, "rational_denominator": d,
                "rational_veronese_scale": scale, "rational_second_numerator": second,
                "rational_witness_rows": witnesses, "rational_E_quadrics_F31": e_rows,
                "rational_square_g": prod["data"]["product_g"],
                "rational_square_q": [int(x) for x in newq], "rational_modulus": modulus}
    (DATA / "cm_frame_B3_rational_model.m").write_text("// D76: exact rational equation w^2=n/d on C, and its 31^128 square map.\n"
        +"\n".join(f"{name} := {value};" for name, value in bindings.items())+"\n")
    report = {"status": "pass", "milestone": "D76", "date": "2026-09-18",
              "sources": [checks.source(p) for p in (__file__, job_path, ver_path, prod_path, curve_path,
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          ROOT / "dembele/pari/133_cm_frame_projective_denominator.py",
                          ROOT / "dembele/pari/152_cm_frame_B3_veronese.py")],
              "base_field": "Q", "equation": "w^2 = n/d on the certified candidate C",
              "monomial_pairs_zero_based": curve["monomial_pairs"],
              "numerator_coefficients": n, "denominator_coefficients": d,
              "numerator_height": max(abs(x) for x in n), "denominator_height": max(abs(x) for x in d),
              "scale_relative_to_veronese_F": str(scale), "residue_twist_multiplier": twist,
              "square_map_precision_digits": digits, "square_map_modulus": modulus,
              "rank_one_product_coordinates": [int(x) for x in coefficients],
              "rank_one_anchor_zero_based": anchor, "rank_one_scalar_before_twist": int(lam),
              "rank_one_vector": [int(x) for x in v], "twisted_scalar_square_root": root,
              "square_numerator_coefficients": bindings["rational_square_g"],
              "square_denominator_coefficients": bindings["rational_square_q"],
              "second_numerator_coefficients": second,
              "T_membership_witness_rows": [[str(x) for x in r] for r in witnesses],
              "E_quadrics_mod31": e_rows, "branch_degree": 18, "genus": 40,
              "divisor_n": "B2 + 2*B3 + T", "divisor_d": "2*E_Q + T",
              "arithmetic_identification_obtained": False, "global_twist_identified": False,
              "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_B3_rational_model.json").write_text(json.dumps(report, indent=2)+"\n")
    print("RATIONAL_COVER_HEIGHTS", report["numerator_height"], report["denominator_height"],
          "TWIST_MULTIPLIER", twist, flush=True)
    print("PASS|154_CM_FRAME_B3_RATIONAL_MODEL", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

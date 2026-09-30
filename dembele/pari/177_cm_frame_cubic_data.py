"""Collect D79's descended Kummer function and explicit cubic over F31."""
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


helpers = module("cubic_data_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
checks = helpers.checks


def main():
    job_path = DATA / "cm_frame_kummer_function_job.json"
    job = checks.read_job(job_path, "PASS|176_CM_FRAME_KUMMER_FUNCTION")
    output = re.sub(r'^Loading .*\n', '', Path(job["log"]["path"]).read_text(), flags=re.M)
    names = ("kummer_evaluation_indices", "kummer_product4_pairs",
             "kummer_third_coordinates", "kummer_descended_divisor_coordinates",
             "kummer_moving_coefficients", "kummer_q_coefficients",
             "kummer_u_coefficients", "kummer_f_coefficients", "kummer_norm_scalar",
             "cubic_quartic_monomials", "cubic_decic_monomials", "cubic_a_coefficients",
             "cubic_denominator_coefficients", "cubic_trace_numerator_coefficients")
    data = {name: helpers.field(output, name.upper()) for name in names}
    assert len(set(data["kummer_evaluation_indices"])) == 1024
    assert len(data["kummer_product4_pairs"]) == 441
    for key in ("kummer_third_coordinates", "kummer_descended_divisor_coordinates"):
        assert len(data[key]) == 81 and all(len(row) == 201 for row in data[key])
    assert all(0 <= c < 31 for row in data["kummer_descended_divisor_coordinates"] for c in row)
    for key, length in (("moving", 441), ("q", 81), ("u", 441), ("f", 201)):
        row = data[f"kummer_{key}_coefficients"]
        assert len(row) == length and all(0 <= c < 31 for c in row)
    assert 0 < data["kummer_norm_scalar"] < 31
    for key, degree, count in (("quartic", 4, 105), ("decic", 10, 285)):
        mons = data[f"cubic_{key}_monomials"]
        assert len(mons) == count and len(set(map(tuple, mons))) == count
        assert all(len(row) == 16 and min(row) >= 0 and sum(row) == degree for row in mons)
    for key, length in (("a", 105), ("denominator", 105), ("trace_numerator", 285)):
        row = data[f"cubic_{key}_coefficients"]
        assert len(row) == length and all(0 <= c < 31 for c in row)
    mpath = DATA / "cm_frame_cubic.m"
    mpath.write_text("// D79: cubic data over F31, with exact Kummer/divisor witnesses.\n"+
                     "// On C: Q4*T^3 - 3*A4*Q4*T - P10 = 0; T has weight 2.\n"+
                     "\n".join(f"{key} := {helpers.magma(value)};" for key, value in data.items())+"\n")
    report = {
        "status": "pass", "milestone": "D79", "date": "2026-09-21", "characteristic": 31,
        "sources": [checks.source(p) for p in (__file__, job_path,
                    ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")],
        "magma_artifact": checks.source(mpath), "data": data,
        "field_modulus": [3, 29, 1], "extension_entry_encoding": "c0+31*c1",
        "evaluation_count": 1024, "base_divisor_degree": 120,
        "section_dimensions": [81, 201, 321, 441],
        "descended_representative": "W_R=L(2D0-E_R), E_R effective of degree 120 over F31",
        "third_class": "[E_R-D0]=A, 3A=-[D+-D-]",
        "kummer_function": "h=c*u/q", "norm_root": "a=c*f",
        "function_divisor": "div(h)=D+-D-+3E_R-3D0",
        "norm_identity": "h*tau(h)=a^3, tau(a)=a",
        "cyclic_cubic": "v^3=h", "involution_lift": "tau(v)=a/v",
        "reflection_quotient": "y=v+a/v; y^3-3*a*y-(h+tau(h))=0",
        "weighted_equation": "Q4*T^3-3*A4*Q4*T-P10=0",
        "coordinate_weights": {"X1_through_X16": 1, "T": 2},
        "coefficient_interpretation": "a=A4/X16^4; h+tau(h)=P10/(Q4*X16^6); T=X16^2*y",
        "curve_interpretation": "smooth projective normalization of the cubic function field over the saved candidate C",
        "base_genus": 16, "quadratic_resolvent_genus": 40,
        "cyclic_cover_genus": 136, "reflection_quotient_genus": 64,
        "cyclic_cubic_constructed": True, "genus64_curve_constructed_modulo31": True,
        "independent_verification_completed": False,
        "characteristic_zero_cubic_constructed": False,
        "arithmetic_identification_certified": False,
        "target_field_constructed": False,
    }
    (DATA / "cm_frame_cubic.json").write_text(json.dumps(report, indent=2)+"\n")
    print("NORM_SCALAR", data["kummer_norm_scalar"], "CUBIC_COEFFICIENT_LENGTHS", [105, 105, 285])
    print("PASS|177_CM_FRAME_CUBIC_DATA")


if __name__ == "__main__":
    main()

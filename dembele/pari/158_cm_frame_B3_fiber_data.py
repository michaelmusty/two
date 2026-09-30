"""D77: collect exact B3 residue-field coordinates and normalized fibre jets.

The fibre is K[z]/(z^2-alpha), with K the nonic residue field and
alpha the order-two leading coefficient of n/d. It has Q-dimension
18 and involution z -> -z. Splitting is recorded separately.
"""
import ast
from fractions import Fraction
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


checks = module("fiber_hashes", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")


def field(output, label):
    raw = re.search(r"^"+re.escape(label)+r"\|(.*?)(?=^[A-Z][A-Z_0-9]*\||\Z)",
                    output, re.M | re.S).group(1).strip()
    return ast.literal_eval(re.sub(r"(-?\d+/\d+)", r"'\1'", raw))


def rational_strings(value):
    if isinstance(value, list):
        return [rational_strings(x) for x in value]
    return str(Fraction(value))


def magma(value):
    if isinstance(value, list):
        return "["+", ".join(magma(x) for x in value)+"]"
    return str(value)


def main():
    job_path = DATA / "cm_frame_B3_fiber_job.json"
    job = checks.read_job(job_path, "PASS|157_CM_FRAME_B3_FIBER")
    output = Path(job["log"]["path"]).read_text()
    names = {"nonic_coefficients": "FIBER_NONIC_COEFFICIENTS",
             "point_coordinates": "FIBER_POINT_COORDINATES", "tangent": "FIBER_TANGENT",
             "second_jet": "FIBER_SECOND_JET", "numerator_leading": "FIBER_NUMERATOR_LEADING",
             "denominator_value": "FIBER_DENOMINATOR_VALUE", "unit": "FIBER_UNIT",
             "unit_norm": "FIBER_UNIT_NORM"}
    data = {key: rational_strings(field(output, label)) for key, label in names.items()}
    data["jacobian_rows_one_based"] = field(output, "FIBER_JACOBIAN_ROWS")
    mark_path = DATA / "cm_frame_marks_check.json"
    marks = json.loads(mark_path.read_text())
    assert data["nonic_coefficients"] == marks["nonic_residue_field"]["polynomial_coefficients_ascending"]
    assert all(len(data[key]) == 16 and all(len(row) == 9 for row in data[key])
               for key in ("point_coordinates", "tangent", "second_jet"))
    assert len(data["unit"]) == 9 and any(Fraction(x) for x in data["unit"])
    assert Fraction(data["unit_norm"]) != 0
    report = {"status": "pass", "milestone": "D77", "date": "2026-09-19",
              "sources": [checks.source(p) for p in (__file__, job_path, mark_path,
                          DATA / "cm_frame_B3_rational_check.json",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")],
              "data": data, "base_residue_field_degree": 9, "fiber_dimension_over_Q": 18,
              "fiber_algebra": "K[z]/(z^2-alpha)", "involution": "a -> a, z -> -z",
              "local_parameter": "X15/X16-a", "numerator_order": 2, "denominator_order": 0,
              "splitting_determined": False, "arithmetic_identification_obtained": False,
              "genus64_cover_constructed": False}
    path = DATA / "cm_frame_B3_fiber.json"
    path.write_text(json.dumps(report, indent=2)+"\n")
    path.with_suffix(".m").write_text("// D77 normalized B3 fibre and exact order-two jets.\n"
        +"\n".join("fiber_"+name+" := "+magma(value)+";" for name, value in data.items())+"\n")
    norm = Fraction(data["unit_norm"])
    print("NORMALIZED_FIBER_DIMENSION", 18, "UNIT_NORM_SIGN", 1 if norm > 0 else -1,
          "NORM_HEIGHT_DIGITS", max(len(str(abs(norm.numerator))), len(str(norm.denominator))))
    print("PASS|158_CM_FRAME_B3_FIBER_DATA")


if __name__ == "__main__":
    main()

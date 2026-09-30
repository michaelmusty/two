"""D77: explicit cyclotomic structure and oriented branches over B3.

From alpha=-3*s^2, the normalized fibre is K(b), b^2=-3. Re-express
the local generator using a rational linear form ell vanishing on B3,
so that W=w/(ell/X16) has values +/- b*s/ell_1. These are the two
degree-nine divisors after base extension to Q(b).
"""
import importlib.util
import json
from pathlib import Path
import time

from sage.all import GF, QQ, NumberField, PolynomialRing, matrix, vector

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


collect = module("fiber_structure_data", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
checks = collect.checks


def main():
    started = time.monotonic()
    job_path = DATA / "cm_frame_B3_fiber_squareclass_job.json"
    job = checks.read_job(job_path, "PASS|159_CM_FRAME_B3_FIBER_SQUARECLASS")
    output = Path(job["log"]["path"]).read_text()
    assert "SMALL_RATIONAL_SQUARECLASS_FOUND|true" in output
    assert collect.field(output, "SMALL_RATIONAL_SQUARECLASS") == -3
    witness = [QQ(x) for x in collect.field(output, "SQUARECLASS_WITNESS")]
    data_path = DATA / "cm_frame_B3_fiber.json"
    data = json.loads(data_path.read_text())["data"]
    marks_path = DATA / "cm_frame_marks.json"
    marks = json.loads(marks_path.read_text())
    T = PolynomialRing(QQ, "t")
    f = T([QQ(x) for x in data["nonic_coefficients"]])
    K = NumberField(f, "a")
    alpha = K([QQ(x) for x in data["unit"]])
    s = K(witness)
    assert s != 0 and -3*s*s == alpha
    assert alpha.norm() < 0
    pts, tangent, second = [vector(K, [K([QQ(c) for c in row]) for row in data[key]])
                           for key in ("point_coordinates", "tangent", "second_jet")]
    lines = [vector(QQ, rec["coefficients"]) for rec in marks["order_three_divisor"]["relations"]]
    # Prefer a parameter also nonzero in the conormal fibre at every point mod 31.
    selected = None
    for i, line in enumerate(lines):
        assert line*pts == 0
        slope = line*tangent
        if slope and slope.norm().valuation(31) == 0:
            selected = i
            break
    assert selected is not None
    line = lines[selected]
    slope = line*tangent
    curvature = line*second
    ratio = s/slope
    beta = alpha/(slope*slope)
    assert beta == -3*ratio*ratio
    changed_first = tangent/slope
    changed_second = second/(slope*slope)-tangent*curvature/(slope**3)
    assert line*changed_first == 1 and line*changed_second == 0
    def coefficients(x):
        return [str(x[j]) for j in range(9)]
    new_data = {"squareclass": -3, "squareclass_witness": [str(x) for x in witness],
                "parameter_linear_form": [int(x) for x in line],
                "parameter_linear_form_index_one_based": selected+1,
                "parameter_slope": coefficients(slope), "parameter_second_coefficient": coefficients(curvature),
                "rational_parameter_unit": coefficients(beta), "branch_ratio": coefficients(ratio),
                "changed_tangent": [coefficients(x) for x in changed_first],
                "changed_second_jet": [coefficients(x) for x in changed_second]}
    report = {"status": "pass", "milestone": "D77", "date": "2026-09-19",
              "sources": [checks.source(p) for p in (__file__, job_path, data_path, marks_path,
                          ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")],
              "data": new_data, "fiber_is_a_field": True, "fiber_degree_over_Q": 18,
              "fiber_presentation": "K(b), b^2=-3; normalized z=s*b",
              "involution": "a -> a, b -> -b", "invariant_subalgebra_degree": 9,
              "contains_primitive_cube_root": "zeta3=(-1+b)/2",
              "constant_extension": "Q(b), b^2=-3",
              "oriented_branch_degrees": [9, 9],
              "oriented_branches": "B3 and W=+/- b*branch_ratio(a), W=w/(ell/X16)",
              "cover_involution_exchanges_branches": True,
              "constant_conjugation_exchanges_branches": True,
              "arithmetic_cover_identified": False, "cyclic_cubic_constructed": False,
              "wall_seconds": time.monotonic()-started}
    path = DATA / "cm_frame_B3_fiber_structure.json"
    path.write_text(json.dumps(report, indent=2)+"\n")
    path.with_suffix(".m").write_text("// D77 cyclotomic fibre and rational local parameter.\n"
        +"\n".join("branch_"+key+" := "+collect.magma(value)+";" for key, value in new_data.items())+"\n")
    print("FIBER_PRESENTATION K(sqrt(-3)) DEGREE 18 ORIENTED_DEGREES 9 9")
    print("RATIONAL_PARAMETER_LINEAR_FORM", selected+1)
    print("PASS|160_CM_FRAME_B3_FIBER_STRUCTURE", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

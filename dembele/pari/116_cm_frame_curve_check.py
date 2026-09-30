"""Export and check D68's integer canonical-curve candidate.

This certifies the recorded algebraic properties of a candidate over Q.
Its identification with the intended Shimura curve remains a separate task.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import time

import mpmath as mp
from sage.all import PolynomialRing, QQ, ZZ, matrix, vector


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data/computed"
spec = importlib.util.spec_from_file_location("curve_frame", HERE/"114_cm_projective_frame.py")
frame = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frame)


def nonsplit_control():
    ring = PolynomialRing(QQ, "x")
    x = ring.gen()
    h = x**3-x-1
    f = x**5-x**2-x
    assert h.is_irreducible() and f.gcd(f.derivative()) == 1
    assert f == 1+(x*x+1)*h
    # On y^2=f(x), D=(h(x),y-1) has degree three. (y+1)/h has
    # simple poles exactly at D, with principal parts 2/h'(root).
    field = h.splitting_field("a")
    roots = h.roots(field, multiplicities=False)
    e = matrix(field, [[1, root] for root in roots])
    values = matrix(field, [[root, root**2-QQ(2)/3] for root in roots])
    parts = vector(field, [2/h.derivative()(root) for root in roots])
    assert parts*e == 0 and sum(values.rows()) == 0
    change, weights = frame.exact_frame_change(e, values)
    assert weights/weights[0] == parts/parts[0]
    scale = next(c for c in change.list() if c)
    normalized = change/scale
    assert all(c in QQ for c in normalized.list())
    return {"curve": "y^2=x^5-x^2-x", "divisor": "(x^3-x-1,y-1)",
            "residue_field_degree": 3, "exact_residue_identity": True,
            "projective_change_defined_over_Q": True,
            "projective_change": [[str(QQ(c)) for c in row] for row in normalized.rows()]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", type=Path, default=DATA/"cm_frame_curve_check.json")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("positive timeout required")
    started = time.monotonic()
    mp.mp.dps = 80
    search_path = DATA/"cm_frame_quadric_search.json"
    search = json.loads(search_path.read_text())
    rows = [row["coefficients"] for row in search["accepted_candidates"]]
    quadrics = matrix(ZZ, rows)
    assert quadrics.dimensions() == (91, 136) and quadrics.rank() == 91
    assert all(d == 1 for d in quadrics.elementary_divisors())
    _, field_report, evaluation = frame.field_frame()
    assert evaluation*quadrics.transpose() == 0
    pairs = [[i, j] for i in range(16) for j in range(i, 16)]
    point_report = json.loads((DATA/"cm_projective_frame.json").read_text())
    jets, _ = frame.precise.read_source(Path(point_report["banks"]["current"]["source"]["path"]), 1, 50)
    change = frame.precise.decode(point_report["banks"]["current"]["frame"]["change_matrix"])
    coordinates = list(jets*change)
    point_search = frame.recognition.projective_search(coordinates, [mp.mpf("1e-14")]*16,
        point_report["banks"]["current"]["frame"]["common_scale_anchor_column"],
        height_cap=10**12, scales=(10**14, 10**16, 10**18, 10**20))
    points = []
    for candidate in point_search["accepted_directions"]:
        point = candidate["primitive_vector"]
        if quadrics*vector(ZZ, [point[i]*point[j] for i, j in pairs]) == 0:
            points.append(point)
    assert len(points) <= 1
    candidate_path = DATA/"cm_frame_curve_candidate.json"
    candidate = {"status": "integer curve candidate; Shimura identification not proved",
                 "base_field": "Q", "projective_space_dimension": 15,
                 "variables": [f"X{i}" for i in range(16)], "monomial_pairs": pairs,
                 "quadrics": rows, "independent_quadric_count": 91,
                 "saturated_integer_quadric_lattice": True,
                 "maximum_absolute_coefficient": int(max(abs(c) for c in quadrics.list())),
                 "rational_points": points,
                 "CM_field_polynomial_ascending": frame.recognition.arithmetic.HARBATER_COEFFICIENTS,
                 "CM_projective_coordinates_power_basis": json.loads(
                     (DATA/"cm_field_recognition.json").read_text())["field_basis"]["trace_centered_basis_power_coordinates"][1:],
                 "search_source": frame.source(search_path), "field_sources": field_report}
    candidate_path.write_text(json.dumps(candidate, indent=2)+"\n")
    model_path = DATA/"cm_frame_curve_candidate.m"
    model_path.write_text("\n".join([
        "// D68: exact integer candidate. Identification with the Shimura curve is unproved.",
        "// Load from the repository root. X1,...,X16 correspond to JSON X0,...,X15.",
        "if not assigned k then k := Rationals(); end if;",
        "P := ProjectiveSpace(k,15); R := CoordinateRing(P);",
        "pairs := "+str([[i+1,j+1] for i,j in pairs])+";",
        "rows := "+str(rows)+";",
        "polys := [&+[R!row[i]*R.(pairs[i][1])*R.(pairs[i][2]) : i in [1..#pairs]] : row in rows];",
        "C_candidate := Curve(P,polys);", ""]))
    job_path = DATA/"cm_frame_curve_basic.m"
    job_path.write_text("\n".join([
        "SetColumns(0); SetSeed(68);",
        'load "dembele/data/computed/cm_frame_curve_candidate.m";',
        "I := Ideal(C_candidate); G := GroebnerBasis(I);",
        "hp := HilbertPolynomial(I);",
        "assert Dimension(I) eq 2; assert hp eq 30*Parent(hp).1-15;",
        'print "PASS|Q_DIMENSION_DEGREE_ARITHMETIC_GENUS|1|30|16";',
        'print "GROEBNER_SIZE|", #G;',
        "den := LCM(&cat[[Denominator(c) : c in Coefficients(f)] : f in G]);",
        "assert GCD(den,31) eq 1;",
        "assert &and[LeadingCoefficient(f) eq 1 : f in G];",
        'print "PASS|MONIC_GROEBNER_OVER_Z_LOCALIZED_AT_31";',
        "ReducePolynomial := function(f,S)",
        "    kk := BaseRing(S); cs,ms := CoefficientsAndMonomials(f); ans := S!0;",
        "    for i in [1..#cs] do",
        "        ee := Exponents(ms[i]); cc := (kk!Numerator(cs[i]))/(kk!Denominator(cs[i]));",
        "        ans +:= cc*&*[S.j^ee[j] : j in [1..Rank(S)]];",
        "    end for; return ans;",
        "end function;",
        "P31 := ProjectiveSpace(GF(31),15); R31 := CoordinateRing(P31);",
        "I31 := ideal<R31 | [ReducePolynomial(f,R31) : f in polys]>;",
        "G31 := [ReducePolynomial(f,R31) : f in G];",
        "assert I31 eq ideal<R31|G31>;",
        "assert [Exponents(LeadingMonomial(f)) : f in G] eq [Exponents(LeadingMonomial(f)) : f in G31];",
        'print "PASS|FLAT_GROEBNER_MODEL_AT_31";',
        "C31 := Curve(P31,I31);",
        "assert Degree(C31) eq 30 and ArithmeticGenus(C31) eq 16;",
        "assert IsIrreducible(C31); assert IsReduced(C31);",
        'print "PASS|MOD31_INTEGRAL_CURVE";',
        "T<t> := PolynomialRing(Rationals());",
        "h := T!"+str(candidate["CM_field_polynomial_ascending"])+";",
        "assert IsIrreducible(h); L<theta> := NumberField(h);",
        "etas := [L!Evaluate(T!cs,theta) : cs in "+str(
            [[str(c) for c in cs] for cs in candidate["CM_projective_coordinates_power_basis"]]).replace("'", "")+"];",
        "assert &and[Evaluate(f,etas) eq 0 : f in polys];",
        "assert Degree(MinimalPolynomial(etas[2]/etas[1])) eq 17;",
        'print "PASS|EXACT_CM_CLOSED_POINT_DEGREE_17";',
        'print "PASS|116_CM_FRAME_CURVE_BASIC";', "quit;", ""]))
    log_path = DATA/"cm_frame_curve_basic.out"
    status = "failed"
    command = ["/Applications/Magma/magma", "-bn", "-l", "2000000000", str(job_path)]
    with log_path.open("w") as log:
        try:
            run = subprocess.run(command, cwd=HERE.parents[1], stdout=log,
                                 stderr=subprocess.STDOUT, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            status = "timeout"
        else:
            output = log_path.read_text()
            if run.returncode == 0 and "PASS|116_CM_FRAME_CURVE_BASIC" in output and not any(
                text in output for text in ("Runtime error", "User error", "Assertion failed")):
                status = "pass"
    report = {"status": status, "script_source": frame.source(__file__),
              "helper_source": frame.source(frame.__file__),
              "nonsplit_exact_control": nonsplit_control(),
              "candidate": frame.source(candidate_path), "magma_model": frame.source(model_path),
              "magma_job": frame.source(job_path), "magma_log": frame.source(log_path),
              "command": command, "timeout_seconds": args.timeout,
              "quadric_rank": 91, "maximum_absolute_coefficient": candidate["maximum_absolute_coefficient"],
              "rational_point_search": point_search, "exact_rational_points_found": points,
              "smoothness_certified_by_this_script": False,
              "Shimura_identification_certified": False,
              "wall_seconds": time.monotonic()-started}
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print("Basic curve checks:", status, "rational points:", points,
          "seconds:", report["wall_seconds"], flush=True)
    print(log_path.read_text()[-3000:], flush=True)
    if status != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

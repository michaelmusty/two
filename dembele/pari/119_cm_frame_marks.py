"""D70: recover marked-point candidates on the verified genus-16 curve.

The point and divisor equations are checked exactly on that curve. Their
identification with the analytic CM markings remains numerical. This does
not prove that the curve is the intended Shimura curve.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from sage.all import GF, QQ, ZZ, PowerSeriesRing, gcd, matrix, vector


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data/computed"
spec = importlib.util.spec_from_file_location("marks_frame", HERE/"114_cm_projective_frame.py")
frame = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frame)


def ratios_at_center(bank_record):
    jets, _ = frame.precise.read_source(Path(bank_record["source"]["path"]), 1, 50)
    values = list(jets*frame.precise.decode(bank_record["frame"]["change_matrix"]))
    pivot = bank_record["frame"]["common_scale_anchor_column"]
    return [z/values[pivot] for z in values], pivot


def recover_point(saved, candidate):
    values, pivot = ratios_at_center(saved["banks"]["current"])
    # One bounded LLL run. D68's height cap of 10^12 excluded this point.
    search = frame.recognition.projective_search(values, [mp.mpf("1e-18")]*16,
        pivot, height_cap=10**20, scales=(10**20,))
    Q = matrix(ZZ, candidate["quadrics"]); pairs = candidate["monomial_pairs"]
    points = []
    for found in search["accepted_directions"]:
        p = found["primitive_vector"]
        if Q*vector(ZZ, [p[i]*p[j] for i,j in pairs]) == 0:
            points.append(p)
    assert len(points) == 1
    p = points[0]
    assert gcd(p) == 1 and p[pivot] > 0
    errors = {}
    for name in ("current", "previous"):
        other, other_pivot = ratios_at_center(saved["banks"][name])
        errors[name] = mp.nstr(max(abs(other[j]-mp.mpf(p[j])/p[other_pivot])
                                  for j in range(16)), 30)
    return p, {"primitive_coordinates": p, "height": max(map(abs,p)),
               "exact_all_quadric_values_zero": True, "projective_anchor": pivot,
               "maximum_absolute_ratio_errors": errors, "search": search,
               "CM_marking_identification": "numerical agreement only"}


def order_three_evaluations(saved, points, label):
    rec = saved["banks"][label]; path = Path(rec["source"]["path"])
    meta = json.loads(path.with_suffix(".json").read_text())
    backend = frame.cm.native.Backend(50)
    bank = backend.read(path, meta["n"], meta["columns"])
    radius = mp.mpf(str(meta["radius"]))
    change = frame.precise.decode(rec["frame"]["change_matrix"])
    nodes, circles = [], []; count = 24
    for point in points:
        u = (point["w"]/radius)**32
        assert abs(u) < 1
        delta = min(mp.mpf(".001"), (1-abs(u))/32)
        for factor in (mp.mpf(1), mp.mpf(".5")):
            start = len(nodes); d = delta*factor
            nodes.extend(u+d*mp.exp(2j*mp.pi*k/count) for k in range(count))
            circles.append((start,d))
    values = frame.cm.native.evaluate(bank, backend.vector(nodes)).to_mpmath()
    coefficients = [mp.matrix(9,16), mp.matrix(9,16)]
    for index,(start,d) in enumerate(circles):
        for j in range(16):
            coefficients[index % 2][index // 2,j] = mp.fsum(
                values[start+k,j]*mp.exp(-4j*mp.pi*k/count) for k in range(count))/(count*d*d)
    output = {}
    for which in (0,1):
        E = coefficients[which]*change; pivots = []
        for i in range(9):
            pivot = max(range(16), key=lambda j: abs(E[i,j]))
            value = E[i,pivot]; pivots.append(pivot)
            for j in range(16): E[i,j] /= value
        output[f"{label}_radius{which}"] = (E, pivots)
    return output


def ordinary_point_mod31(point, candidate):
    """Exact implicit jets through degree 15; full rank proves ordinarity."""
    k = GF(31); S = PowerSeriesRing(k, "t", default_prec=16); t = S.gen()
    p = vector(k,point); anchor = next(i for i in range(16) if p[i])
    p /= p[anchor]; variables = [i for i in range(16) if i != anchor]
    Q = matrix(k,candidate["quadrics"]); pairs = candidate["monomial_pairs"]
    J = matrix(k,91,15)
    for row in range(91):
        for c,(i,j) in zip(Q[row],pairs):
            if i != anchor: J[row,variables.index(i)] += c*p[j]
            if j != anchor: J[row,variables.index(j)] += c*p[i]
    assert J.rank() == 14
    equations = list(J.transpose().pivots()); dependent = list(J.pivots())
    free = next(i for i in range(15) if i not in dependent)
    inverse = J.matrix_from_rows_and_columns(equations,dependent).inverse()
    series = [S(a) for a in p]; series[variables[free]] += t
    for degree in range(1,16):
        monomials = [series[i]*series[j] for i,j in pairs]
        rhs = vector(k, [sum(c*m for c,m in zip(Q[row],monomials))[degree]
                         for row in equations])
        correction = -inverse*rhs
        for j,c in zip(dependent,correction):
            series[variables[j]] += c*t**degree
    monomials = [series[i]*series[j] for i,j in pairs]
    assert all(sum(c*m for c,m in zip(row,monomials)).add_bigoh(16) == 0 for row in Q)
    coefficients = matrix(k, [[s[j] for s in series] for j in range(16)])
    assert coefficients.rank() == 16
    return {"prime": 31, "anchor_zero_based": anchor,
            "parameter_coordinate_zero_based": variables[free],
            "equation_rows_zero_based": equations,
            "dependent_affine_columns_zero_based": dependent,
            "canonical_jet_coefficients": [[int(c) for c in row] for row in coefficients],
            "canonical_jet_rank": 16, "canonical_jet_determinant_mod31": int(coefficients.det()),
            "all_quadrics_vanish_mod_t16": True,
            "conclusion_on_candidate": "ordinary modulo 31 and over Q"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DATA/"cm_frame_marks.json")
    args = parser.parse_args(); started = time.monotonic(); mp.mp.dps = 80
    frame_path = DATA/"cm_projective_frame.json"
    candidate_path = DATA/"cm_frame_curve_candidate.json"
    saved = json.loads(frame_path.read_text()); candidate = json.loads(candidate_path.read_text())
    point, point_report = recover_point(saved,candidate)
    print("Exact rational point height:", point_report["height"], flush=True)
    points, geometry = frame.cm.elliptic_points(orders=(3,))
    assert len(points) == 9
    evaluations = {}
    for label in ("current", "previous"):
        evaluations.update(order_three_evaluations(saved,points,label))
    E = evaluations["current_radius1"][0]; scale = mp.mpf(10)**12
    tail = matrix(ZZ, [[int(mp.nint(scale*component(E[j,i])))
                       for component in (mp.re,mp.im) for j in range(9)] for i in range(16)])
    reduced = matrix.identity(ZZ,16).augment(tail).LLL()
    relations = []
    for row in reduced.rows():
        v = list(map(int,row[:16])); vv = mp.matrix(v)
        residuals = {name: mp.norm(a*vv)/(mp.norm(a)*mp.norm(vv))
                     for name,(a,_) in evaluations.items()}
        if max(map(abs,v)) <= 1000 and all(
            e < (mp.mpf("1e-17") if name.startswith("current") else mp.mpf("1e-11"))
            for name,e in residuals.items()):
            relations.append({"coefficients": v, "height": max(map(abs,v)),
                              "normalized_residuals": {name: mp.nstr(e,30) for name,e in residuals.items()}})
    rows = [r["coefficients"] for r in relations]
    assert len(rows) == 7 and matrix(QQ,rows).rank() == 7
    assert all(d == 1 for d in matrix(ZZ,rows).elementary_divisors())
    # The degree-17 closed point already used in D68, cut out by all its quadrics.
    _, field_sources, evaluation = frame.field_frame()
    kernel = evaluation.right_kernel_matrix()
    quadrics = matrix(QQ,candidate["quadrics"])
    assert evaluation*quadrics.transpose() == 0
    combined = quadrics.stack(kernel)
    independent = list(combined.transpose().pivots())
    assert independent[:91] == list(range(91)) and len(independent) == 119
    extra = []
    for i in independent[91:]:
        row = combined[i]; integer = list(map(ZZ,row*row.denominator()))
        divisor = gcd(integer); extra.append([int(c/divisor) for c in integer])
    assert len(extra) == 28
    ordinary = ordinary_point_mod31(point,candidate)
    marks_path = DATA/"cm_frame_marks.m"
    marks_path.write_text("\n".join([
        "// D70: exact markings on the D68 candidate; analytic CM labels are unproved.",
        "// Load cm_frame_curve_candidate.m first; k can be Q or a suitable finite field.",
        "P32_coordinates := "+str(point)+";",
        "P32_candidate := C_candidate![k!a : a in P32_coordinates];",
        "B3_linear_rows := "+str(rows)+";",
        "B3_linear_forms := [&+[R!row[i]*R.i : i in [1..16]] : row in B3_linear_rows];",
        "B3_ideal := Ideal(C_candidate)+ideal<R|B3_linear_forms>;",
        "B3_candidate := Scheme(P,B3_ideal);",
        "D17_extra_rows := "+str(extra)+";",
        "D17_extra_quadrics := [&+[R!row[i]*R.(pairs[i][1])*R.(pairs[i][2]) : i in [1..#pairs]] : row in D17_extra_rows];",
        "D17_ideal := Ideal(C_candidate)+ideal<R|D17_extra_quadrics>;",
        "D17_candidate := Scheme(P,D17_ideal);", ""]))
    result = {
        "status": "exact marked-point and divisor candidates; CM identifications numerical",
        "script_source": frame.source(__file__), "helper_source": frame.source(frame.__file__),
        "frame_source": frame.source(frame_path), "curve_source": frame.source(candidate_path),
        "geometry_source": geometry, "field_sources": field_sources,
        "banks": {name: {"source": rec["source"], "metadata": frame.source(Path(rec["source"]["path"]).with_suffix(".json"))}
                  for name,rec in saved["banks"].items() if name in ("current","previous")},
        "rational_point": point_report, "ordinary_point_certificate": ordinary,
        "order_three_divisor": {
            "analytic_point_indices": [p["index"] for p in points],
            "Cauchy_coefficient_order": 2, "samples_per_circle": 24,
            "lattice_scale": 10**12, "lattice_shape": [16,34],
            "coefficient_height_cap": 1000, "relations": relations,
            "integer_row_lattice_saturated": True,
            "evaluations": {name: {"normalized_values": frame.encode(a), "row_pivots": pivots,
                                    "singular_values": np.linalg.svd(frame.numeric(a),compute_uv=False).tolist()}
                            for name,(a,pivots) in evaluations.items()},
            "exact_divisor_properties": "checked separately by Magma script 120"},
        "magma_marks_source": frame.source(marks_path),
        "limitations": ["No certified analytic error bounds or arithmetic Shimura-side jets.",
                        "Exact membership on the candidate does not certify the CM label.",
                        "The genus-64 cover and Shimura identification remain unconstructed."],
        "wall_seconds": time.monotonic()-started}
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print("Seven order-three divisor linear forms, height", max(r["height"] for r in relations), flush=True)
    print("Ordinary-point jet rank:",ordinary["canonical_jet_rank"],"seconds:",result["wall_seconds"],flush=True)


if __name__ == "__main__":
    main()

"""D68: choose canonical coordinates using the degree-(g+1) CM divisor.

The projective frame argument is exact under its geometric hypotheses.
The target evaluations, rank tests and equations below are numerical.
Only saved differential banks are read; no new Cauchy system is solved.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from scipy.linalg import qr, svdvals
from sage.all import (ComplexBallField, NumberField, PolynomialRing, QQ,
                      QuadraticField, diagonal_matrix, matrix, vector)


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


cm = module("frame_cm_fibers", "92_cm_fibers.py")
recognition = module("frame_field_recognition", "97_cm_field_recognition.py")
precise = cm.pointed.precise


def source(path):
    path = Path(path)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def pair(z):
    return [mp.nstr(mp.re(z), 55), mp.nstr(mp.im(z), 55)]


def encode(a):
    return [[pair(a[i, j]) for j in range(a.cols)] for i in range(a.rows)]


def numeric(a):
    return np.array(a.tolist(), dtype=complex)


def exact_frame_change(e, values):
    """Send g+1 projective points to the rows of a trace-zero value matrix."""
    g = e.ncols()
    if e.nrows() != g + 1 or values.dimensions() != e.dimensions():
        raise ValueError("expected two (g+1)-by-g matrices")
    if e.rank() != g or values.rank() != g:
        raise ValueError("the point matrices must have full column rank")
    if sum(values.rows()) != vector(values.base_ring(), [0] * g):
        raise ValueError("target rows must sum to zero")
    weights = e.left_kernel().basis()[0]
    if any(x == 0 for x in weights):
        raise ValueError("the source points are not a projective frame")
    weighted = diagonal_matrix(weights) * e
    change = weighted[:g, :].inverse() * values[:g, :]
    assert weighted * change == values
    return change, weights


def exact_control():
    """Fermat quartic, four rational points, and an explicit pole function.

    On x^4+y^4=1 take omega=(1,x,y) dx/(4y^3) and
    h=(x^2+y^2+1)/(xy).  Its four simple poles are (+/-1,0),(0,+/-1).
    The local parameters used below are y,y,x,x, respectively.
    """
    e = matrix(QQ, [[-1, -1, 0], [1, -1, 0],
                    [1, 0, 1], [-1, 0, 1]]) / 4
    principal_parts = vector(QQ, [2, -2, 2, -2])
    assert principal_parts * e == vector(QQ, [0, 0, 0])
    values = matrix(QQ, [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]])
    change, weights = exact_frame_change(e, values)
    assert weights / weights[0] == principal_parts / principal_parts[0]
    field = QuadraticField(2, "sqrt_two")
    a = field.gen()
    mixing = matrix(field, [[a, 1, 0], [0, 3, a], [1, 0, 2]])
    scales = diagonal_matrix(field, [2, 3+a, 5-a, 7])
    moved, _ = exact_frame_change(scales * e * mixing, values.change_ring(field))
    recovered = mixing * moved
    scalar = next(recovered[i, j] / change[i, j]
                  for i in range(3) for j in range(3) if change[i, j])
    assert recovered == scalar * change
    order = [2, 0, 3, 1]
    permuted, _ = exact_frame_change(e.matrix_from_rows(order), values.matrix_from_rows(order))
    ratio = next(permuted[i, j] / change[i, j]
                 for i in range(3) for j in range(3) if change[i, j])
    assert permuted == ratio * change
    ring = PolynomialRing(QQ, names=("A", "B", "C"))
    inverse = change.inverse()
    old = [sum(ring.gen(i) * inverse[i, j] for i in range(3)) for j in range(3)]
    equation = old[1]**4 + old[2]**4 - old[0]**4
    for row in values.rows():
        assert equation(*row) == 0
    rejected = 0
    for bad in [matrix(QQ, [[1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1]]),
                matrix(QQ, [[1, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0]])]:
        try:
            exact_frame_change(bad, values)
        except ValueError:
            rejected += 1
    assert rejected == 2
    return {"curve": "x^4+y^4=1", "pole_function": "(x^2+y^2+1)/(x*y)",
            "residue_identity": True, "nonrational_basis_change_invariance": True,
            "independent_row_rescaling_invariance": True,
            "simultaneous_point_permutation_invariance": True,
            "invalid_frames_rejected": rejected,
            "reconstructed_rational_quartic": str(equation)}


def field_frame():
    orbit_path = DATA / "cm_orbit.json"
    basis_path = DATA / "cm_field_recognition.json"
    orbit = json.loads(orbit_path.read_text())
    saved = json.loads(basis_path.read_text())["field_basis"]
    ring = PolynomialRing(QQ, "t")
    field = NumberField(ring(recognition.arithmetic.HARBATER_COEFFICIENTS), "theta")
    basis = [field([QQ(x) for x in row])
             for row in saved["trace_centered_basis_power_coordinates"]]
    assert basis[0] == 1 and all(z.trace() == 0 for z in basis[1:])
    assert matrix(QQ, [z.vector() for z in basis]).rank() == 17
    roots = [mp.mpc(*z) for z in orbit["field_root_action"]["complex_roots"]]
    lookup = orbit["matching"]["point_to_root_index_zero_based"]
    assert sorted(lookup) == list(range(17))
    values = mp.matrix([[recognition.evaluate(z, roots[j]) for z in basis[1:]]
                        for j in lookup])
    assert max(abs(sum(values[:, j])) for j in range(16)) < mp.mpf("1e-60")
    # Exact independent filter for any future proposed canonical quadric.
    pairs = list(itertools.combinations_with_replacement(range(16), 2))
    products = matrix(QQ, [(basis[i+1]*basis[j+1]).vector() for i, j in pairs]).transpose()
    assert products.rank() == 17
    return values, {"orbit": source(orbit_path), "basis": source(basis_path),
                    "trace_zero_basis_dimension": 16,
                    "quadric_evaluation_rank_at_D": 17,
                    "quadrics_vanishing_at_D_dimension": 119}, products


def sampled_derivatives(bank, points, radius, count=16):
    """Cauchy first coefficients at both circle radii, not finite differences.

    The original differentials have a common simple zero above each order-two
    elliptic point. Their first derivatives therefore give coarse canonical
    coordinates, up to an irrelevant nonzero scalar for each point.
    """
    nodes, circles = [], []
    centers = [(point["w"] / radius)**32 for point in points]
    for u in centers:
        if abs(u) >= 1:
            raise ValueError("CM point outside saved expansion disk")
        delta = min(mp.mpf(".001"), (1-abs(u))/32)
        for scale in [mp.mpf(1), mp.mpf(".5")]:
            start = len(nodes)
            nodes.extend(u+delta*scale*mp.exp(2j*mp.pi*k/count) for k in range(count))
            circles.append((start, delta*scale))
    evaluated = cm.native.evaluate(bank, bank.backend.vector(nodes)).to_mpmath()
    matrices = [mp.matrix(17, 16), mp.matrix(17, 16)]
    for index, (start, delta) in enumerate(circles):
        for j in range(16):
            matrices[index % 2][index // 2, j] = mp.fsum(
                evaluated[start+k, j]*mp.exp(-2j*mp.pi*k/count)
                for k in range(count))/(count*delta)
    return matrices, {"samples_per_circle": count,
                      "maximum_radius_over_boundary_distance": "1/32",
                      "relative_radius_comparison": mp.nstr(mp.norm(matrices[0]-matrices[1])/mp.norm(matrices[1]), 25)}


def numeric_frame_change(e, values, jets, drop=None, anchor=None):
    norms = [mp.sqrt(mp.fsum(abs(z)**2 for z in e[i, :])) for i in range(17)]
    scaled = mp.diag([1/z for z in norms])*e
    uu, singular, _ = np.linalg.svd(numeric(scaled), full_matrices=True)
    if singular[-1] < singular[0]*1e-8:
        raise ValueError("numerical CM points do not span the canonical space")
    if drop is None:
        drop = int(np.argmax(abs(uu[:, -1])))
    keep = [i for i in range(17) if i != drop]
    square = mp.matrix([list(scaled[i, :]) for i in keep])
    other = -(square.T**-1)*scaled[drop, :].T
    weights = [mp.mpc(1) if i == drop else other[keep.index(i)] for i in range(17)]
    if min(map(abs, weights)) < mp.mpf("1e-8"):
        raise ValueError("numerical frame has a vanishing dependence coefficient")
    weighted = mp.diag(weights)*scaled
    square = mp.matrix([list(weighted[i, :]) for i in keep])
    change = square**-1*mp.matrix([list(values[i, :]) for i in keep])
    frame_residual = mp.norm(weighted*change-values)/mp.norm(values)
    series = jets*change
    if anchor is None:
        anchor = max(range(16), key=lambda j: abs(series[0, j]))
    common = series[0, anchor]
    if abs(common) < mp.mpf("1e-30"):
        raise ValueError("zero common normalization at the marked point")
    change /= common
    series /= common
    return change, series, {
        "drop_row": drop, "common_scale_anchor_column": anchor,
        "row_scaled_evaluation_condition_2": float(singular[0]/singular[-1]),
        "smallest_relative_singular_value": float(singular[-1]/singular[0]),
        "minimum_absolute_normalized_dependence_weight": mp.nstr(min(map(abs, weights)), 25),
        "basis_change_condition_2": float(np.linalg.cond(numeric(change))),
        "frame_fit_relative_residual": mp.nstr(frame_residual, 25),
        "change_matrix": encode(change)}


def quadratic_relations(series, fixed=None):
    field = ComplexBallField(220)
    def ball(z):
        return field(mp.nstr(z.real, 60), mp.nstr(z.imag, 60))
    ring = PolynomialRing(field, "u")
    length = series.rows
    forms = [ring([ball(z) for z in series[:, i]]) for i in range(16)]
    pairs = list(itertools.combinations_with_replacement(range(16), 2))
    products = [(forms[i]*forms[j]).truncate(length) for i, j in pairs]
    full = matrix(field, [[p[n] for p in products] for n in range(length)])
    training = length//2
    numeric_products = precise.float_matrix(full[:training, :])
    scaled = numeric_products/np.linalg.norm(numeric_products, axis=0)
    singular = svdvals(scaled)
    if sum(singular > singular[0]*1e-9) != 45:
        raise ValueError("quadratic product rank differs from 45")
    if fixed is None:
        _, _, order = qr(scaled, mode="economic", pivoting=True)
        pivots = list(map(int, order[:45]))
        free = [j for j in range(136) if j not in pivots]
        rows = None
    else:
        pivots, free, rows = fixed["pivots"], fixed["free"], fixed["solve"]["interpolation_rows"]
    coefficients, solve = precise.solve_relations(full, pivots, free, training, rows)
    values = precise.decode([[precise.midpoint(z) for z in row] for row in coefficients.rows()])
    return values, {"pivots": pivots, "free": free, "solve": solve,
                    "pivot_coefficients": encode(values),
                    "imaginary_relative_norm": mp.nstr(mp.norm(mp.matrix([[z.imag for z in row] for row in values.tolist()]))/mp.norm(values), 25),
                    "maximum_absolute_pivot_coefficient": mp.nstr(max(map(abs, values)), 25),
                    "relative_singular_values_45_46": [float(singular[j]/singular[0]) for j in (44, 45)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-only", action="store_true")
    parser.add_argument("--output", type=Path, default=DATA/"cm_projective_frame.json")
    args = parser.parse_args()
    start = time.monotonic()
    mp.mp.dps = 80
    report = {"status": "exact control and numerical target-frame pilot; no exact target equation",
              "script_source": source(__file__), "exact_control": exact_control()}
    print("Exact Fermat-quartic frame control passes", flush=True)
    if not args.control_only:
        values, field_report, _ = field_frame()
        points, geometry = cm.elliptic_points()
        assert [p["index"] for p in points] == list(range(17))
        report.update(field_frame=field_report, geometry=geometry, banks={})
        current = previous = None
        normalized = {}
        for n in [16384, 12288]:
            path = DATA/f"acb_refinement_{n}.acb"
            meta = json.loads(path.with_suffix(".json").read_text())
            backend = cm.native.Backend(50)
            bank = backend.read(path, meta["n"], meta["columns"])
            jets = bank.to_mpmath(rows=256)
            evaluations, sampling = sampled_derivatives(bank, points, mp.mpf(str(meta["radius"])))
            for which in ([1, 0] if n == 16384 else [1]):
                label = "current" if n == 16384 and which == 1 else "other_radius" if n == 16384 else "previous"
                change, series, frame = numeric_frame_change(evaluations[which], values, jets,
                    current["frame"]["drop_row"] if current else None,
                    current["frame"]["common_scale_anchor_column"] if current else None)
                coefficients, equations = quadratic_relations(series, current["equations"] if current else None)
                result = {"source": source(path), "sampling": sampling, "frame": frame, "equations": equations}
                normalized[label] = series
                if current is None:
                    current = result
                    main_coefficients = coefficients
                else:
                    result["comparison_with_current"] = {
                        "canonical_series_relative_difference": mp.nstr(mp.norm(series-normalized["current"])/mp.norm(normalized["current"]), 25),
                        "quadric_coefficients_relative_difference": mp.nstr(mp.norm(coefficients-main_coefficients)/mp.norm(main_coefficients), 25),
                        "quadric_coefficients_maximum_absolute_difference": mp.nstr(max(map(abs, coefficients-main_coefficients)), 25)}
                report["banks"][label] = result
                print(label, "condition", frame["basis_change_condition_2"],
                      "quadric imaginary part", equations["imaginary_relative_norm"],
                      result.get("comparison_with_current", {}), flush=True)
        report["limitations"] = [
            "Arithmetic claims require the stated canonical curve and Galois-equivariant CM labelling.",
            "Numerical rank and circle/bank comparisons are not analytic error enclosures.",
            "The exact projective frame supplies coordinates, not equations of the target curve.",
            "No target quadric coefficient, curve, torsion point or field polynomial is certified.",
            "The genus-64 cover still has to be constructed after the genus-16 base."]
    report["wall_seconds"] = time.monotonic()-start
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print("Saved", args.output, "in", report["wall_seconds"], "seconds", flush=True)


if __name__ == "__main__":
    main()

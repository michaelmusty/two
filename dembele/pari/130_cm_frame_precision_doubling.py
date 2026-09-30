"""D74: exact Newton steps from 31^e to 31^(2e), preserving D72's scale.

The old numerator is known exactly over Q, so only the support points and
denominator need lifting. D73's short numerator is used by a subsequent
cross-product transfer. Earlier data and scripts remain unchanged.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

from sage.all import QQ, GF, Zmod, PolynomialRing, matrix, vector

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
HELPER = ROOT / "dembele/pari/124_cm_frame_resolvent_lift.py"
spec = importlib.util.spec_from_file_location("digit_helpers", HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
source = helper.source
evaluate, gradient, dot = helper.evaluate, helper.gradient, helper.dot


class Component(helper.Component):
    def inverse_unit(self, a):
        a = self.A(a)
        y = self.lift(self.reduce(a)**-1)
        precision = 1
        while precision < helper.DIGITS:
            y *= 2-a*y
            precision *= 2
        assert a*y == 1
        return y

    def solve_A(self, M, b):
        """Unit-pivot elimination; scalar inverses use precision doubling.

        Sage's polynomial xgcd is unavailable over this composite base ring.
        Every selected pivot is a unit, so this needs no nonunit division.
        """
        n = M.nrows()
        assert M.ncols() == n and len(b) == n
        rows = [list(M.row(i))+[self.A(b[i])] for i in range(n)]
        for j in range(n):
            pivot = next(i for i in range(j, n) if self.reduce(rows[i][j]) != 0)
            rows[j], rows[pivot] = rows[pivot], rows[j]
            inv = self.inverse_unit(rows[j][j])
            for k in range(j+1, n+1):
                rows[j][k] *= inv
            rows[j][j] = self.A(1)
            for i in range(n):
                if i == j:
                    continue
                a = rows[i][j]
                for k in range(j+1, n+1):
                    rows[i][k] -= a*rows[j][k]
                rows[i][j] = self.A(0)
        sol = [row[-1] for row in rows]
        assert M*vector(self.A, sol) == vector(self.A, b)
        return sol

    def lift_cutout_block(self, equations, pairs):
        J0 = matrix(self.K, [gradient(q, self.x0, pairs)[:15] for q in equations])
        inds = list(J0.transpose().pivots())
        assert len(inds) == 15
        M = matrix(self.A, [gradient(equations[i], self.x, pairs)[:15] for i in inds])
        b = [-evaluate(equations[i], self.x, pairs) for i in inds]
        assert all(v % helper.STEP == 0 for x in b for v in self.coefficients(x))
        delta = self.solve_A(M, b)
        self.x[:15] = [x+d for x, d in zip(self.x[:15], delta)]
        assert all(evaluate(q, self.x, pairs) == 0 for q in equations)

    def lift_on_curve_block(self, curve, pairs):
        inds = self.curve_indices
        M = matrix(self.A, [gradient(curve[i], self.x, pairs)[:14] for i in inds])
        b = [-evaluate(curve[i], self.x, pairs) for i in inds]
        assert all(v % helper.STEP == 0 for x in b for v in self.coefficients(x))
        delta = self.solve_A(M, b)
        self.x[:14] = [x+d for x, d in zip(self.x[:14], delta)]
        assert all(evaluate(q, self.x, pairs) == 0 for q in curve)

    def correct_double_zero(self, denominator, curve, pairs):
        v = self.tangent(curve, pairs)
        M = matrix(self.A, [gradient(curve[i], self.x, pairs)[:14] for i in self.curve_indices])
        w = self.solve_A(M, [-evaluate(curve[i], v, pairs) for i in self.curve_indices])
        w += [self.A(0), self.A(0)]
        assert all(dot(gradient(q, self.x, pairs), w)+evaluate(q, v, pairs) == 0 for q in curve)
        second = dot(gradient(denominator, self.x, pairs), w)+evaluate(denominator, v, pairs)
        assert self.reduce(second) != 0
        slope = dot(gradient(denominator, self.x, pairs), v)
        assert all(x % helper.STEP == 0 for x in self.coefficients(slope))
        delta = -slope*self.inverse_unit(2*second)
        self.x = [x+delta*t for x, t in zip(self.x, v)]
        assert all(evaluate(q, self.x, pairs) == 0 for q in curve)
        assert evaluate(denominator, self.x, pairs) == 0
        v = self.tangent(curve, pairs)
        assert dot(gradient(denominator, self.x, pairs), v) == 0
        return self.coefficients(delta), v


def compare_data(new, old):
    modulus = old["modulus"]
    for key in ("numerator_coefficients", "denominator_coefficients"):
        assert [v % modulus for v in new[key]] == old[key]
    assert [[v % modulus for v in row] for row in new["point_jets"]] == old["point_jets"]
    oldc = {(c["label"], tuple(c["etale_modulus"])): c for c in old["components"]}
    for c in new["components"]:
        prev = oldc[c["label"], tuple(c["etale_modulus"])]
        for key in ("coordinates", "tangent"):
            assert [[v % modulus for v in row] for row in c[key]] == prev[key]
        if c["label"] == "E":
            assert c["second_jet_mod31"] == prev["second_jet_mod31"]


def step(previous, previous_path, curve_data, marks, supports, exact_numerator):
    started = time.monotonic()
    old_digits = previous["precision_digits"]
    helper.DIGITS = 2*old_digits
    helper.STEP = 31**old_digits
    helper.MODULUS = helper.STEP**2
    helper.BASE = Zmod(helper.MODULUS)
    curve, pairs = curve_data["quadrics"], [tuple(p) for p in curve_data["monomial_pairs"]]
    oldc = {(c["label"], tuple(c["etale_modulus"])): c for c in previous["components"]}
    groups = {}
    T = PolynomialRing(GF(31), "s")
    for label in ("D17", "E", "F"):
        data = supports[label]
        groups[label] = []
        for f, exponent in T(data["modulus"]).factor():
            assert exponent == 1
            key = label, tuple(int(c) for c in f.list())
            groups[label].append(Component(label, f, data["coordinates"], curve, pairs, oldc[key]))
    qn = [int(helper.BASE(QQ(c))) for c in exact_numerator]
    assert [c % helper.STEP for c in qn] == previous["numerator_coefficients"]
    print("DOUBLING", old_digits, helper.DIGITS, flush=True)
    for c in groups["D17"]:
        c.lift_cutout_block(curve+supports["D17_extra_rows"], pairs)
        assert evaluate(qn, c.x, pairs) == 0
    for c in groups["F"]:
        c.lift_cutout_block(curve+[qn], pairs)
    for c in groups["E"]:
        c.lift_on_curve_block(curve, pairs)
    print("SUPPORTS_LIFTED", helper.DIGITS, round(time.monotonic()-started, 3), flush=True)

    # The previous 44 pivot coordinates and the remaining fixed scale are
    # retained. E motion affects values only to second order in 31^old_digits.
    chart = previous["section_chart_indices_zero_based"]
    pivots = previous["denominator_linear_system"]["correction_pivot_columns"]
    active = [chart[j] for j in pivots]
    values, columns = [], [[] for j in active]
    qd = list(previous["denominator_coefficients"])
    for c in groups["F"]+groups["E"]:
        values += c.coefficients(evaluate(qd, c.x, pairs))
        for column, j in zip(columns, active):
            a, b = pairs[j]
            column += c.coefficients(c.x[a]*c.x[b])
    assert len(values) == len(active) == 44
    assert all(v % helper.STEP == 0 for v in values)
    M = matrix(helper.BASE, columns).transpose()
    assert M.change_ring(GF(31)).rank() == 44
    delta = M.solve_right(-vector(helper.BASE, values))
    assert all(int(v) % helper.STEP == 0 for v in delta)
    for j, v in zip(active, delta):
        qd[j] = int(helper.BASE(qd[j])+v)
    assert all(evaluate(qd, c.x, pairs) == 0 for c in groups["F"]+groups["E"])
    fixed = [j for j in range(136) if j not in active]
    assert all(qd[j] == previous["denominator_coefficients"][j] for j in fixed)
    print("DENOMINATOR_LIFTED", helper.DIGITS, round(time.monotonic()-started, 3), flush=True)
    corrections, components = [], []
    for label, group in groups.items():
        for c in group:
            if label == "E":
                correction, v = c.correct_double_zero(qd, curve, pairs)
                corrections.append(correction)
                assert c.reduce(evaluate(qn, c.x, pairs)) != 0
            else:
                v = c.tangent(curve, pairs)
                assert evaluate(qn, c.x, pairs) == 0
                assert c.reduce(dot(gradient(qn, c.x, pairs), v)) != 0
                if label == "F":
                    assert evaluate(qd, c.x, pairs) == 0
                    assert c.reduce(dot(gradient(qd, c.x, pairs), v)) != 0
                else:
                    assert c.reduce(evaluate(qd, c.x, pairs)) != 0
            components.append(c.export(curve, pairs, second=label == "E", tangent=v))
    jets = helper.point_jets(marks["rational_point"]["primitive_coordinates"], curve, pairs)
    assert all(evaluate(qn, jets, pairs)[i] == 0 for i in range(15))
    assert int(evaluate(qn, jets, pairs)[15]) % 31 != 0
    assert int(evaluate(qd, jets, pairs)[0]) % 31 != 0
    result = {
        "status": "pass", "milestone": "D74", "date": "2026-09-18",
        "precision_digits": helper.DIGITS, "previous_precision_digits": old_digits,
        "modulus": helper.MODULUS,
        "sources": [source(p) for p in (__file__, HELPER, previous_path,
                    DATA / "cm_frame_curve_candidate.json", DATA / "cm_frame_marks.json",
                    DATA / "cm_frame_lift_supports.out", DATA / "cm_frame_lift_numerator.json")],
        "section_chart_indices_zero_based": chart,
        "numerator_coefficients": qn, "denominator_coefficients": qd,
        "numerator_method": "reduce the independently recovered exact rational numerator",
        "denominator_linear_system": {"rank": 44, "correction_pivot_columns": pivots,
                                      "fixed_coefficients_preserved": True},
        "components": components, "E_parameter_corrections": corrections,
        "point_jets": [[int(x[n]) for x in jets] for n in range(16)],
        "divisor_identity": "D17 + 15*P32 - 2*E", "scale_convention": "unchanged from D72",
        "number_field_cover_obtained": False, "wall_seconds": time.monotonic()-started,
    }
    compare_data(result, previous)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(16, 32, 64, 128, 256), default=128)
    args = parser.parse_args()
    started = time.monotonic()
    curve = json.loads((DATA / "cm_frame_curve_candidate.json").read_text())
    marks = json.loads((DATA / "cm_frame_marks.json").read_text())
    supports = helper.parse_supports((DATA / "cm_frame_lift_supports.out").read_text())
    exact = json.loads((DATA / "cm_frame_lift_numerator.json").read_text())["numerator_coefficients_rational"]
    reference_path = DATA / "cm_frame_resolvent_lift_8.json"
    reference = json.loads(reference_path.read_text())
    control_path = DATA / "cm_frame_resolvent_lift_4.json"
    control = step(json.loads(control_path.read_text()), control_path, curve, marks, supports, exact)
    compare_data(control, reference)
    print("PASS|DOUBLING_4_TO_8_MATCHES_SUCCESSIVE_DIGITS", flush=True)
    stages = []
    previous, previous_path = reference, reference_path
    while previous["precision_digits"] < args.digits:
        result = step(previous, previous_path, curve, marks, supports, exact)
        path = DATA / f"cm_frame_doubling_{result['precision_digits']}.json"
        path.write_text(json.dumps(result, indent=2)+"\n")
        stages.append(source(path))
        previous, previous_path = result, path
        print("PASS|130_CM_FRAME_PRECISION_DOUBLING", result["precision_digits"],
              round(result["wall_seconds"], 3), flush=True)
    report = {"status": "pass", "milestone": "D74", "sources": [source(__file__), source(HELPER)],
              "stages": stages, "control_4_to_8_exact_agreement": True,
              "control_sources": [source(control_path), source(reference_path)],
              "control_wall_seconds": control["wall_seconds"],
              "final_precision_digits": args.digits, "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_doubling.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|130_CM_FRAME_DOUBLING_COMPLETE", args.digits, round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

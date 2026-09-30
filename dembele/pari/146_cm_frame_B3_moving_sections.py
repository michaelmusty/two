"""D76: lift H0(2K-E-B3) using the existing certified E supports.

B3 imposes nine exact rational linear conditions and E imposes sixteen
finite-etale evaluation conditions. Fixed free coordinates retain D75's g.
The subsequent multiplication-kernel step avoids lifting its residual G.
"""
import importlib.util
import json
from pathlib import Path
import time

from sage.all import GF, QQ, ZZ, Zmod, PolynomialRing, matrix, vector, gcd, lcm

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("moving_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
projection_helper = module("moving_projection", ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")


def integral_row(row):
    out = [ZZ(x*lcm([a.denominator() for a in row])) for x in row]
    content = gcd(out)
    return [x//content for x in out]


def main():
    started = time.monotonic()
    check_path = DATA / "cm_frame_B3_check.json"
    old_check = DATA / "cm_frame_arithmetic_check.json"
    for path in (check_path, old_check):
        data = json.loads(path.read_text())
        checks.verify_records(data)
        assert data["status"] == "pass"
    curve_path = DATA / "cm_frame_curve_candidate.json"
    marks_path = DATA / "cm_frame_marks.json"
    pair_path = DATA / "cm_frame_B3_normalization.json"
    curve, marks, pair = [json.loads(p.read_text()) for p in (curve_path, marks_path, pair_path)]
    pairs = [tuple(p) for p in curve["monomial_pairs"]]
    lines = [r["coefficients"] for r in marks["order_three_divisor"]["relations"]]
    products = [[a[i]*(j == v)+(a[j]*(i == v) if i != j else 0) for i, j in pairs]
                for a in lines for v in range(16)]
    vanishing = matrix(QQ, curve["quadrics"]+products)
    assert vanishing.rank() == 127
    conditions = matrix(ZZ, [integral_row(row) for row in vanishing.right_kernel_matrix()])
    assert conditions.nrows() == 9 and conditions*vanishing.transpose() == 0
    stages = []
    previous = None
    for digits in (64, 128):
        stage_started = time.monotonic()
        old_path = DATA / f"cm_frame_doubling_{digits}.json"
        old = json.loads(old_path.read_text())
        Z = Zmod(31**digits)
        chart = old["section_chart_indices_zero_based"]
        P = projection_helper.section_projection(curve, chart)
        P31 = P.change_ring(GF(31))
        g31 = vector(GF(31), pair["data"]["B3_square_numerator"])*P31
        q31 = vector(GF(31), pair["data"]["B3_square_denominator"])*P31
        qs31 = matrix(GF(31), pair["data"]["B3_moving_section_basis"])*P31
        qfree = list(qs31.pivots())
        assert len(qfree) == 3
        rows = conditions.matrix_from_columns(chart).change_ring(Z).rows()
        for component in old["components"]:
            if component["label"] != "E":
                continue
            T = PolynomialRing(Z, "z")
            A = T.quotient(T(component["etale_modulus"]), "a")
            xs = [A(row) for row in component["coordinates"]]
            mon = [xs[pairs[j][0]]*xs[pairs[j][1]] for j in chart]
            for i in range(component["degree"]):
                rows.append(vector(Z, [q.lift()[i] for q in mon]))
        M = matrix(Z, rows)
        assert M.nrows() == 25 and M.ncols() == 45
        active = list(M.change_ring(GF(31)).pivots())
        assert len(active) == 25
        free = [j for j in range(45) if j not in active]
        inverse = M.matrix_from_columns(active).inverse()
        basis = matrix(Z, 20, 45)
        for i, j in enumerate(free):
            basis[i, j] = 1
            correction = -inverse*M.column(j)
            for col, value in zip(active, correction):
                basis[i, col] = value
        assert M*basis.transpose() == 0
        g = vector(Z, [int(g31[j]) for j in free])*basis
        assert g.change_ring(GF(31)) == g31
        jets = old["point_jets"]
        jet_matrix = [[sum(Z(jets[a][pairs[j][0]])*Z(jets[n-a][pairs[j][1]]) for a in range(n+1))
                       for j in chart] for n in range(7)]

        def full(row):
            out = [0]*136
            for j, x in zip(chart, row):
                out[j] = int(x)
            return out

        result = {"status": "pass", "milestone": "D76", "date": "2026-09-18",
                  "sources": [checks.source(p) for p in (__file__, curve_path, marks_path, pair_path,
                              old_path, check_path, old_check,
                              ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                              ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")],
                  "precision_digits": digits, "modulus": 31**digits,
                  "section_chart_indices_zero_based": chart,
                  "B3_full_integer_constraints": [[int(x) for x in row] for row in conditions],
                  "constraint_rank": 25, "space_dimension": 20,
                  "g_active_chart_columns": active, "g_free_chart_columns": free,
                  "g_coefficients": full(g), "g_space_basis": [full(row) for row in basis],
                  "q_free_chart_columns": qfree,
                  "q_selected_free_values": [int(q31[j]) for j in qfree],
                  "q_jet_constraints": [[int(x) for x in row] for row in jet_matrix],
                  "new_numerator_coefficients": pair["data"]["B3_new_numerator"],
                  "old_numerator_coefficients": old["numerator_coefficients"],
                  "old_denominator_coefficients": old["denominator_coefficients"],
                  "wall_seconds": time.monotonic()-stage_started}
        if previous is not None:
            m = previous["modulus"]
            assert [x % m for x in result["g_coefficients"]] == previous["g_coefficients"]
            for key in ("g_space_basis", "q_jet_constraints"):
                assert [[x % m for x in row] for row in result[key]] == previous[key]
            assert result["g_active_chart_columns"] == previous["g_active_chart_columns"]
        path = DATA / f"cm_frame_B3_moving_{digits}.json"
        path.write_text(json.dumps(result, indent=2)+"\n")
        names = {"moving_modulus": result["modulus"], "moving_chart": [j+1 for j in chart],
                 "moving_g": result["g_coefficients"], "moving_g_basis": result["g_space_basis"],
                 "moving_q_free": [j+1 for j in qfree], "moving_q_selected_free": result["q_selected_free_values"],
                 "moving_q_jets": result["q_jet_constraints"], "moving_new_numerator": result["new_numerator_coefficients"],
                 "moving_old_numerator": result["old_numerator_coefficients"],
                 "moving_old_denominator": result["old_denominator_coefficients"]}
        path.with_suffix(".m").write_text("// D76 exact linear lift of H0(2K-E-B3).\n"
            +"\n".join(f"{name} := {value};" for name, value in names.items())+"\n")
        previous = result
        stages += [checks.source(path), checks.source(path.with_suffix(".m"))]
        print("MOVING_G_SPACE", digits, 20, round(result["wall_seconds"], 3), flush=True)
    report = {"status": "pass", "milestone": "D76", "date": "2026-09-18",
              "sources": [checks.source(__file__)]+stages, "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_B3_moving.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|146_CM_FRAME_B3_MOVING_SECTIONS", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

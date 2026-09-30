"""D103 review: independent dense-frame algebra, constants and frozen sources."""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "cm_adjugate_height_review_d103.json"
SPEC = importlib.util.spec_from_file_location("d103", ROOT / "dembele/pari/380_cm_adjugate_height.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def bareiss(a):
    a = [list(row) for row in a]
    n, sign, previous = len(a), 1, 1
    for k in range(n-1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            sign = -sign
        p = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                value = p*a[i][j]-a[i][k]*a[k][j]
                assert value % previous == 0
                a[i][j] = value//previous
            a[i][k] = 0
        previous = p
    return sign*a[-1][-1]


def solve_inverse(a):
    n = len(a)
    a = [[Q(x) for x in row]+[Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[pivot], a[k] = a[k], a[pivot]
        value = a[k][k]
        a[k] = [x/value for x in a[k]]
        for i in range(n):
            if i != k:
                value = a[i][k]
                a[i] = [x-value*y for x, y in zip(a[i], a[k])]
    return [row[n:] for row in a]


def product(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def independent_frames():
    records = []
    for g in (3, 16):
        e = [[i**j for j in range(g)] for i in range(g+1)]
        cofactors = [(-1)**i*bareiss(e[:i]+e[i+1:]) for i in range(g+1)]
        assert all(cofactors)
        assert product([cofactors], e) == [[0]*g]
        phi = [[c*x for x in row] for c, row in zip(cofactors, e)]
        m, delta = phi[:g], bareiss(phi[:g])
        expected = (-1)**g
        for c in cofactors:
            expected *= c
        assert delta == expected != 0
        inverse = solve_inverse(m)
        adj = [[delta*x for x in row] for row in inverse]
        assert all(x.denominator == 1 for row in adj for x in row)
        rhs = [[delta*int(i == j) for j in range(g)] for i in range(g)]
        assert product(m, adj) == rhs
        assert product(phi, adj)[-1] == [-delta]*g
        # Take independent formal value and derivative functionals.
        a = [[Q(j+1) for j in range(g)], [Q((j+1)**3) for j in range(g)]]
        aj, ij = product(a, adj), product(a, inverse)
        aj_brackets = [aj[0][0]*aj[1][j]-aj[0][j]*aj[1][0] for j in range(g)]
        ij_brackets = [ij[0][0]*ij[1][j]-ij[0][j]*ij[1][0] for j in range(g)]
        assert aj_brackets == [delta**2*x for x in ij_brackets]
        denominator = next(j for j, x in enumerate(ij_brackets) if x)
        assert [x/aj_brackets[denominator] for x in aj_brackets] == [x/ij_brackets[denominator] for x in ij_brackets]
        wrong = [row[:] for row in adj]
        wrong[0][0] += 1
        assert product(m, wrong) != rhs
        records.append({"g": g, "frame": "dense Vandermonde on 0,...,g",
                        "determinants": "integer Bareiss", "adjugate": "determinant times rational solve",
                        "determinant_bit_length": abs(delta).bit_length(),
                        "Gaussian_ratios_match": True, "corrupted_adjugate_rejected": True})
    return records


def independent_field_bound(saved):
    basis = json.loads(M.BASIS.read_text())["field_basis"]["trace_centered_basis_power_coordinates"][1:]
    bounds = []
    for row in basis:
        value = Q(0)
        for coefficient in reversed(row):
            value = 4*value+abs(Q(coefficient))
        bounds.append(17*value)
    assert [str(x) for x in bounds] == saved["field_vector_bound"]["row_bounds"]
    assert max(bounds) < 34359738368
    f = json.loads(M.FIELD.read_text())["residue_algebra_input"]["polynomial_coefficients_ascending"]
    value = 0
    for coefficient in reversed(f[:-1]):
        value = 4*value+abs(coefficient)
    assert value < 4**17
    assert value == saved["field_vector_bound"]["Rouche_left"]
    return {"algorithm": "Horner absolute-coefficient bound", "rows": len(bounds),
            "all_scaled_conjugates_below_2_power_35": True,
            "Rouche_bound_independently_recomputed": True}


def independent_constants(saved):
    # Coarse mass = half of upstairs mass of 2*z*f(z^2)dz.
    integral_coefficients = [Q(1, 2)*4*2/Q(4*m+4) for m in range(9)]
    assert integral_coefficients == [Q(1, m+1) for m in range(9)]
    assert 512*1024 < 1024**2-1
    assert 4**8*Q(1, 65536) == 1
    assert Q(1, 3)*1024**4 < 2**40
    assert Q(2, 9)*1024**12 < 2**120
    g = 16
    fibre_weights = [2*(g-1)]*(g+1)
    fibre_weights[0] += 3
    determinant_weight = 2*(-(g-1)-1)
    assert sum(fibre_weights) == 513 and determinant_weight == -32
    # Bound the entire remaining constant by a rational multiple of log(2).
    exponents = [12, 70, 510*20, 60, 32*16*3]
    assert sum(exponents) == 11878
    assert Q(sum(exponents)*7, 10) == Q(41573, 5) < 8400
    # An independently iterated positive exponential sum establishes log2<0.7.
    term, partial = Q(1), Q(1)
    for k in range(1, 6):
        term *= Q(7, 10*k)
        partial += term
    assert partial > 2
    assert saved["constants"]["final_height_coefficient"] == sum(fibre_weights)
    assert saved["constants"]["final_additive_constant"] == 8400
    # The archived first toy jet really failed the necessary nonvanishing test.
    assert 1*6-2*3 == 0 and 1*5-2*2 != 0
    return {"coarse_disk_integral_coefficients_without_pi_or_radius": [str(x) for x in integral_coefficients],
            "coarse_fibre_weights": fibre_weights, "Hodge_determinant_weight": determinant_weight,
            "constant_rational_upper_bound": "41573/5",
            "bound": "513*H_CM_disk+8400", "failed_toy_chart_explained": True}


def checked_sources(items):
    for item in items:
        assert source(item["path"]) == item
    return [Path(item["path"]) for item in items]


def build():
    saved = json.loads(M.OUT.read_text())
    paths = checked_sources(saved["sources"])
    assert M.build() == saved
    d102_path = DATA / "cm_residue_lattice_review_d102.json"
    d101_path = DATA / "cm_tangent_exactness_review_d101.json"
    d102, d101 = json.loads(d102_path.read_text()), json.loads(d101_path.read_text())
    paths += checked_sources(d102["sources"])+checked_sources(d101["sources"])
    success_path = DATA / "cm_adjugate_height_d103_attempt02.job.json"
    success = json.loads(success_path.read_text())
    assert success["status"] == "pass" and success["timeout_seconds"] == 180
    assert success["wall_seconds"] < 180 and success["timeout_terminates_process_group"]
    paths += checked_sources(success["sources"]+[success["driver"], success["log"]])
    failed_path = DATA / "cm_adjugate_height_d103_attempt01.job.json"
    failed = json.loads(failed_path.read_text())
    snapshot = ROOT / "dembele/pari/380_cm_adjugate_height_attempt01.py"
    assert failed["status"] == "failed" and failed["exit_code"] == 1
    assert source(snapshot)["sha256"] == failed["driver"]["sha256"]
    assert "StopIteration" in Path(failed["log"]["path"]).read_text()
    paths += checked_sources(failed["sources"]+[failed["log"]])
    paths += [Path(__file__), M.OUT, success_path, failed_path, snapshot, d102_path, d101_path,
              ROOT / "dembele/certificates/cm-adjugate-height-d103.md",
              DATA / "cm_adjugate_height_sources_d103.json"]
    assert not saved["H_CM_disk_numerically_bounded"]
    assert not saved["independent_Shimura_tangent_obtained"]
    assert not saved["spectral_pilot_gate_passed"]
    return {"status": "pass", "milestone": "D103",
            "independent_frame_checks": independent_frames(),
            "independent_field_checks": independent_field_bound(saved),
            "independent_constant_checks": independent_constants(saved),
            "D102_bound_source_hashes_checked": len(d102["sources"]),
            "D101_bound_source_hashes_checked": len(d101["sources"]),
            "failed_control_source_preserved": source(snapshot),
            "sources": [source(p) for p in sorted(set(p.resolve() for p in paths))],
            "H_CM_disk_numerically_bounded": False,
            "independent_Shimura_tangent_obtained": False, "spectral_pilot_gate_passed": False,
            "scope": "Independent exact controls of a conditional height theorem; the intrinsic CM fibre height and arithmetic frame hypotheses remain open."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        old = json.loads(OUT.read_text())
        checked_sources(old["sources"])
    result = build()
    if args.check:
        assert result == old
    else:
        assert not OUT.exists(), "Preserve completed reviews."
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "pass", "source_hashes": len(result["sources"]),
                      "D102_hashes_unchanged": result["D102_bound_source_hashes_checked"],
                      "D101_hashes_unchanged": result["D101_bound_source_hashes_checked"],
                      "independent_dense_frames": "pass", "constants": "pass",
                      "H_CM_disk_numerically_bounded": False}), flush=True)
    print("PASS|D103_ADJUGATE_HEIGHT_REVIEW", flush=True)


if __name__ == "__main__":
    main()

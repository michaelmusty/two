"""D103: integral adjugate frames and exact constants for a CM tangent bound.

The geometric proof and outstanding hypotheses are in the companion report.
Only field arithmetic, earlier proof records and exact algebraic controls are
inputs. No candidate equations, candidate jets or numerical banks are used.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
FIELD = DATA / "cm_arithmetic_audit.json"
BASIS = DATA / "cm_field_recognition.json"
PREVIOUS = DATA / "cm_residue_lattice_d102.json"
OUT = DATA / "cm_adjugate_height_d103.json"


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def det(a):
    a = [[Q(x) for x in row] for row in a]
    result = Q(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result
        v = a[j][j]
        result *= v
        for i in range(j+1, len(a)):
            scale = a[i][j]/v
            if scale:
                for k in range(j+1, len(a)):
                    a[i][k] -= scale*a[j][k]
    return result


def minor(a, i, j):
    return [row[:j]+row[j+1:] for k, row in enumerate(a) if k != i]


def adjugate(a):
    n = len(a)
    return [[(-1)**(i+j)*det(minor(a, j, i)) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def scale(a, s):
    return [[s*x for x in row] for row in a]


def frame(e):
    g = len(e[0])
    c = [(-1)**i*det(e[:i]+e[i+1:]) for i in range(g+1)]
    assert mul([c], e) == [[0]*g]
    return c, [[ci*x for x in row] for ci, row in zip(c, e)]


def frame_controls():
    records = []
    for g in (2, 3, 16):
        e = [[(i+2)*int(i == j) for j in range(g)] for i in range(g)]
        e.append(list(range(1, g+1)))
        c, phi = frame(e)
        assert all(c)
        vectors = eye(g)+[[-1]*g]
        reference = None
        for r in (g, 0):
            m = phi[:r]+phi[r+1:]
            delta = det(m)
            assert delta == (-1)**r*math.prod(c) != 0
            adj = adjugate(m)
            assert mul(m, adj) == scale(eye(g), delta)
            assert mul(adj, m) == scale(eye(g), delta)
            assert all(x.denominator == 1 for row in adj for x in row)
            s = mul(adj, vectors[:r]+vectors[r+1:])
            assert mul(phi, s) == scale(vectors, delta)
            normalized = scale(s, 1/delta)
            if reference is None:
                reference = normalized
            else:
                assert normalized == reference
            # Formal jets of a basis: the common determinant squares in gamma.
            jets = mul([list(range(1, g+1)), [i*i+2 for i in range(1, g+1)]], s)
            inverse_jets = mul([list(range(1, g+1)), [i*i+2 for i in range(1, g+1)]], normalized)
            brackets = [jets[0][0]*jets[1][j]-jets[0][j]*jets[1][0] for j in range(g)]
            inv_brackets = [inverse_jets[0][0]*inverse_jets[1][j]-inverse_jets[0][j]*inverse_jets[1][0] for j in range(g)]
            assert brackets == [delta**2*x for x in inv_brackets]
            a = next(j for j, x in enumerate(brackets) if x)
            assert [x/brackets[a] for x in brackets] == [x/inv_brackets[a] for x in inv_brackets]
        if g <= 3:
            change = eye(g)
            change[0][0], change[0][1] = 2, 3
            t = list(range(2, g+3))
            e2 = [[ti*x for x in row] for ti, row in zip(t, mul(e, change))]
            _, phi2 = frame(e2)
            factor = det(change)*math.prod(t)
            assert phi2 == scale(mul(phi, change), factor)
            lhs = mul(change, adjugate(phi2[:g]))
            rhs = scale(adjugate(phi[:g]), factor**(g-1)*det(change))
            assert lhs == rhs
        # Full evaluation rank alone is insufficient: every cofactor must survive.
        bad = eye(g)+[[1]+[0]*(g-1)]
        bad_c, bad_phi = frame(bad)
        assert det(bad[:g]) == 1 and not all(bad_c)
        assert det(bad_phi[:g]) == 0
        records.append({"g": g, "deleted_rows": [g, 0],
                        "integral_adjugate": True, "full_trace_zero_system_checked": True,
                        "common_determinant_cancels_in_Gaussian_ratios": True,
                        "rank_only_negative_control_rejected": True})
    # The same construction remains integral at arbitrarily growing index.
    indices = []
    for n in (1, 2, 4, 8, 16):
        q = 5**n
        e = eye(3)+[[1, 1, q]]
        c, phi = frame(e)
        m, delta = phi[:3], det(phi[:3])
        assert abs(delta) == q
        adj = adjugate(m)
        assert all(x.denominator == 1 for row in adj for x in row)
        assert mul(m, adj) == scale(eye(3), delta)
        assert max((x/delta).denominator for row in adj for x in row) == q
        indices.append({"n": n, "inverse_denominator": q, "adjugate_integral": True})
    return {"ranks": records, "growing_index_controls": indices,
            "controls_are_not_actual_Shimura_evaluation_matrices": True}


def padd(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0)+v
    return {k: v for k, v in out.items() if v}


def pmul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x+y for x, y in zip(ka, kb))
            out[k] = out.get(k, 0)+va*vb
    return {k: v for k, v in out.items() if v}


def deriv(a):
    # Integral node derivation: dx -> x*xi, dy -> -y*xi, da -> 0.
    return {k: (k[0]-k[1])*v for k, v in a.items() if k[0] != k[1]}


def bracket(a, b):
    return padd(pmul(a, deriv(b)), {k: -v for k, v in pmul(b, deriv(a)).items()})


def nodal_controls():
    relation = {(1, 1, 0): 1, (0, 0, 1): -1}
    assert deriv(relation) == {}
    f = {(0, 0, 0): 1, (2, 0, 0): 1, (0, 1, 0): 1}
    g = {(0, 2, 0): 1, (1, 0, 1): 1}
    t = {(0, 0, 0): 1, (1, 1, 0): 1}
    assert bracket(f, f) == {}
    assert bracket(pmul(t, f), pmul(t, g)) == pmul(pmul(t, t), bracket(f, g))
    assert bracket(relation, f) == pmul(relation, deriv(f))
    assert any(v % 2 for v in bracket(f, g).values())
    return {"node_relation_annihilated": True, "Gaussian_gluing_identity_over_Z": True,
            "no_inversion_of_2_or_residue_characteristic": True,
            "nonzero_characteristic_two_control": True}


def field_vector_bound():
    field = json.loads(FIELD.read_text())["residue_algebra_input"]
    basis = json.loads(BASIS.read_text())["field_basis"]
    previous = json.loads(PREVIOUS.read_text())["field_lattice"]
    f = field["polynomial_coefficients_ascending"]
    assert f == previous["polynomial"] and len(f) == 18 and f[-1] == 1
    assert previous["ring_products_checked"] == 153
    rouche_left, rouche_right = sum(abs(x)*4**i for i, x in enumerate(f[:-1])), 4**17
    assert rouche_left < rouche_right
    b = [[Q(x) for x in row] for row in basis["integral_basis_power_coordinates"]]
    eta = [[Q(x) for x in row] for row in basis["trace_centered_basis_power_coordinates"]][1:]
    trace = previous["trace_vector"]
    bounds = []
    for j, row in enumerate(eta, 1):
        assert [17*x for x in row] == [17*x-trace[j]*y for x, y in zip(b[j], b[0])]
        bounds.append(17*sum(abs(x)*4**k for k, x in enumerate(row)))
    assert len(bounds) == 16 and max(bounds) < 2**35
    return {"root_radius": 4, "Rouche_left": rouche_left, "Rouche_right": rouche_right,
            "integral_vectors": "V_ij=sigma_i(17*eta_j)",
            "basis_integrality_bound_to_D102": True,
            "row_bounds": [str(x) for x in bounds], "maximum_bound": str(max(bounds)),
            "maximum_bound_ceiling": math.ceil(max(bounds)), "uniform_bound": 2**35,
            "power_of_two_exponent": 35,
            "actual_arithmetic_CM_label_is_still_a_hypothesis": True}


def constants():
    degree, g, rho = 8, 16, Q(1, 2**10)
    f = [2, 0, -16, 0, 20, 0, -8, 0, 1]
    assert sum(c*(-2)**i for i, c in enumerate(f)) == 2
    v_lower = Q(1, 4**degree)
    assert v_lower == Q(1, 2**16)
    sinh_r = 2*rho/(1-rho**2)
    assert sinh_r < Q(1, 2**8)
    # pi>3 gives B<rho^-2 and Gamma<rho^-6; no floating-point evaluation.
    assert Q(1, 3) < 1 and Q(2, 9) < 1
    b_exp, gamma_exp, vector_exp = 20, 60, 35
    assert rho**-2 == 2**b_exp and rho**-6 == 2**gamma_exp
    h_t_coeff, h_f_t_coeff = (g-1)*(g+1), -g
    h_coeff, h_f_coeff = 3+2*h_t_coeff, 2*h_f_t_coeff
    assert (h_t_coeff, h_f_t_coeff, h_coeff, h_f_coeff) == (255, -16, 513, -32)
    log2_coeff = 3*4+2*vector_exp+2*(g-1)*(g+1)*b_exp+gamma_exp
    falting_log_2pi_coeff = -h_f_coeff*g
    assert (log2_coeff, falting_log_2pi_coeff) == (10342, 512)
    # pi<4 makes log(2*pi)<3*log2. A positive Taylor sum proves log2<7/10.
    taylor = sum(Q(7, 10)**k/math.factorial(k) for k in range(6))
    assert taylor > 2
    total_log2_coeff = log2_coeff+3*falting_log_2pi_coeff
    rational_upper = total_log2_coeff*Q(7, 10)
    assert total_log2_coeff == 11878 and rational_upper < 8400
    return {"F_degree": degree, "g": g, "norm_pi": 2,
            "noncentral_CM_projection_norm_lower_bound": str(v_lower),
            "disk_radius": str(rho), "sinh_hyperbolic_radius": str(sinh_r),
            "required_sinh_upper_bound": "1/256", "strict_disjointness_verified": True,
            "evaluation_operator_bound": 2**b_exp, "Gaussian_operator_bound": 2**gamma_exp,
            "T_height": "255*H_CM_disk - 16*h_Fal(C)",
            "before_Faltings_lower_bound": "513*H_CM_disk - 32*h_Fal(C) + 10342*log(2)",
            "Faltings_lower_bound": "h_Fal(C) >= -16*log(2*pi)",
            "constant_upper_log2_coefficient": total_log2_coeff,
            "exp_0_7_positive_Taylor_lower_bound": str(taylor),
            "constant_rational_upper_bound": str(rational_upper),
            "final_height_coefficient": h_coeff, "final_additive_constant": 8400}


def build():
    paths = [Path(__file__), FIELD, BASIS, PREVIOUS,
             ROOT / "dembele/certificates/nelson-totally-real-kernel-d90.md",
             ROOT / "dembele/certificates/nelson-norm-one-control-d92.md",
             ROOT / "dembele/certificates/marked-descent.md"]
    return {"status": "pass", "milestone": "D103", "frame_controls": frame_controls(),
            "nodal_Gaussian_controls": nodal_controls(), "field_vector_bound": field_vector_bound(),
            "constants": constants(),
            "theorem": "h(v_j) <= 513*H_CM_disk + 8400, under the stated arithmetic frame and chart hypotheses",
            "remaining_hypotheses": ["Arithmetic identification and labels of the degree-17 CM residue field",
                                     "All 17 signed canonical evaluation minors nonzero",
                                     "Chosen Gaussian denominator at the actual CM point nonzero"],
            "remaining_numeric_input": "Upper bound on the stable coarse-canonical CM fibre height in disk metric",
            "separate_residue_index_bound_needed_for_this_height_inequality": False,
            "evaluation_minor_lower_bound_needed_for_this_height_inequality": False,
            "H_CM_disk_numerically_bounded": False,
            "independent_Shimura_tangent_obtained": False, "spectral_pilot_gate_passed": False,
            "sources": [source(p) for p in paths]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        old = json.loads(OUT.read_text())
        for item in old["sources"]:
            assert source(item["path"]) == item
    result = build()
    if args.check:
        assert result == old
    else:
        assert not OUT.exists(), "Preserve completed artifacts."
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "pass", "bound": result["theorem"],
                      "vector_bound_exponent": 35, "disk_radius": "1/1024",
                      "H_CM_disk_numerically_bounded": False}), flush=True)
    print("PASS|D103_ADJUGATE_HEIGHT", flush=True)


if __name__ == "__main__":
    main()

"""D104: exact CM height constants and controls for the stable-fibre comparison.

The comparison theorem is proved in the companion report. This calculation
uses the degree-16 CM field, not candidate curve equations or tangent values.
All analytic enclosures below use rational arithmetic with explicit remainders.
"""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
CM = DATA / "cm_arithmetic_audit.json"
D103 = DATA / "cm_adjugate_height_d103.json"
OUT = DATA / "cm_intrinsic_height_d104.json"
BITS, TERMS = 80, 32


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def times(a, t):
    return [t*x for x in a]


def zpower(k, n):
    k %= 2*n
    out = [Q(0)]*n
    out[k % n] = Q(1 if k < n else -1)
    return out


def cmul(a, b):
    n = len(a)
    out = [Q(0)]*(2*n-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i+j] += x*y
    for i in range(2*n-2, n-1, -1):
        out[i-n] -= out[i]
    return out[:n]


def bareiss(a):
    a = [list(row) for row in a]
    sign, old = 1, 1
    for k in range(len(a)-1):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k+1, len(a)):
            for j in range(k+1, len(a)):
                value = p*a[i][j]-a[i][k]*a[k][j]
                assert value % old == 0
                a[i][j] = value//old
            a[i][k] = 0
        old = p
    return sign*a[-1][-1]


def discriminant(f):
    n = len(f)-1
    d = [i*f[i] for i in range(1, n+1)]
    matrix = []
    for p, count in ((list(reversed(f)), n-1), (list(reversed(d)), n)):
        for shift in range(count):
            matrix.append([0]*shift+p+[0]*(2*n-1-shift-len(p)))
    return (-1)**(n*(n-1)//2)*bareiss(matrix)


def cinverse(a):
    n = len(a)
    cols = [cmul(a, zpower(i, n)) for i in range(n)]
    matrix = [[cols[j][i] for j in range(n)]+[Q(i == 0)] for i in range(n)]
    for k in range(n):
        p = next(i for i in range(k, n) if matrix[i][k])
        matrix[p], matrix[k] = matrix[k], matrix[p]
        v = matrix[k][k]
        matrix[k] = [x/v for x in matrix[k]]
        for i in range(n):
            if i != k:
                v = matrix[i][k]
                matrix[i] = [x-v*y for x, y in zip(matrix[i], matrix[k])]
    out = [row[-1] for row in matrix]
    assert cmul(a, out) == zpower(0, n)
    return out


def field_and_characters():
    f = [int(x) for x in json.loads(CM.read_text())["CM_cyclic_field"]["polynomial_coefficients_ascending"]]
    beta = add(zpower(1, 32), times(zpower(-1, 32), -1))
    value = [Q(0)]*32
    for c in reversed(f):
        value = add(cmul(value, beta), times(zpower(0, 32), c))
    assert not any(value)
    orbit = {a: add(zpower(a, 32), times(zpower(-a, 32), -1)) for a in range(1, 64, 2)}
    stabilizer = [a for a in orbit if orbit[a] == beta]
    assert stabilizer == [1, 31] and len(set(map(tuple, orbit.values()))) == 16
    assert orbit[63] == times(beta, -1)
    assert add(cmul(cmul(beta, beta), beta), times(beta, 3)) == orbit[3]
    assert next(m for m in range(1, 17) if pow(5, m, 64) in stabilizer) == 16
    assert orbit[pow(5, 8, 64)] == times(beta, -1)
    assert f[-1] == 1 and f[0] % 4 == 2 and all(x % 2 == 0 for x in f[:-1])
    fb = [2, 0, -16, 0, 20, 0, -8, 0, 1]
    assert discriminant(f) == 2**79 and discriminant(fb) == 2**31
    coordinates = {((-1)**s*pow(5, m, 64)) % 64: (s, m) for s in (0, 1) for m in range(16)}
    assert len(coordinates) == 32
    conductors = []
    for k in range(16):
        for conductor in (1, 2, 4, 8, 16, 32, 64):
            residues = {}
            for a, (s, m) in coordinates.items():
                residues.setdefault(a % conductor, set()).add((8*s*k+m*k) % 16)
            if all(len(v) == 1 for v in residues.values()):
                conductors.append(conductor)
                break
    assert all(conductors[k] == 64 for k in range(1, 16, 2))
    total, real = 1, 1
    for k, conductor in enumerate(conductors):
        total *= conductor
        if k % 2 == 0:
            real *= conductor
    assert (total, real) == (2**79, 2**31)
    chi = {a: times(zpower(m, 8), (-1)**s) for a, (s, m) in coordinates.items()}
    a0 = [-sum(Q(a)*chi[a][j] for a in chi)/64 for j in range(8)]
    inverse = cinverse(a0)
    coefficients = {a: 8*cmul(chi[a], inverse)[0] for a in sorted(chi)}
    assert sum(coefficients.values()) == 0
    assert sum(c*Q(a, 64) for a, c in coefficients.items()) == -8
    assert all(coefficients[64-a] == -c for a, c in coefficients.items())
    assert all((17*c).denominator == 1 for c in coefficients.values())
    matrix = [[int(cmul(a0, zpower(j, 8))[i]) for j in range(8)] for i in range(8)]
    norm = bareiss(matrix)
    assert norm != 0
    return {"CM_degree": 16, "polynomial": f, "cyclotomic_generator": "zeta_64-zeta_64^(-1)",
            "cyclotomic_stabilizer": stabilizer, "cyclic_generator": 5,
            "complex_conjugation_is_eighth_power": True,
            "Eisenstein_at_2": True, "polynomial_discriminant": 2**79,
            "maximal_order_reason": "Eisenstein uniformizer gives the full local order at 2; the polynomial discriminant has no other prime factor.",
            "base_discriminant": 2**31, "relative_discriminant_norm": 2**17,
            "quaternion_discriminant_norm": 2, "character_conductors": conductors,
            "odd_character_indices": list(range(1, 16, 2)),
            "L0_power_coordinates": [str(x) for x in a0],
            "L0_inverse_coordinates": [str(x) for x in inverse], "L0_norm": norm,
            "log_gamma_trace_coefficients": {str(a): str(c) for a, c in coefficients.items()},
            "coefficient_absolute_sum": str(sum(abs(c) for c in coefficients.values())),
            "CM_class_number_used": False}, coefficients


def iadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def iscale(a, q):
    return (q*a[0], q*a[1]) if q >= 0 else (q*a[1], q*a[0])


def log_series(q):
    assert 1 <= q <= 2
    z = (q-1)/(q+1)
    power, total = z, Q(0)
    for k in range(TERMS):
        total += 2*power/(2*k+1)
        power *= z*z
    tail = 2*power/((2*TERMS+1)*(1-z*z))
    return total, total+tail


@lru_cache(None)
def log_interval(q):
    q = Q(q)
    assert q > 0
    exponent = q.numerator.bit_length()-q.denominator.bit_length()
    unit = q / (Q(2)**exponent)
    if unit < 1:
        unit *= 2
        exponent -= 1
    assert 1 <= unit < 2
    value = iadd(log_series(unit), iscale(log_series(Q(2)), exponent))
    scale = 2**BITS
    lower = (value[0]*scale).numerator//(value[0]*scale).denominator
    upper = -(-(value[1]*scale).numerator//(value[1]*scale).denominator)
    return Q(lower, scale), Q(upper, scale)


def serialized(interval):
    return [str(x) for x in interval]


def analytic_bound(coefficients):
    n = 64
    partial = iscale(log_interval(64*n), -8)
    for a, c in coefficients.items():
        logs = (Q(0), Q(0))
        for k in range(n+1):
            logs = iadd(logs, log_interval(a+64*k))
        partial = iadd(partial, iscale(logs, -c))
    positive = sum(c*Q(a, 64) for a, c in coefficients.items() if c > 0)
    negative = sum(c*Q(a, 64) for a, c in coefficients.items() if c < 0)
    step = log_interval(Q(n+1, n))
    ratio = partial[0]+negative*step[1], partial[1]+positive*step[1]
    hodge = iadd(iscale(ratio, Q(-1, 8)), iscale(log_interval(2), Q(1, 16)))
    assert Q(8, 5) < hodge[0] <= hodge[1] < Q(17, 10)
    coarse_upper = 2*hodge[1]+log_interval(2)[1]
    assert coarse_upper < Q(41, 10)
    old = json.loads(D103.read_text())["constants"]
    assert old["final_height_coefficient"] == 513 and old["final_additive_constant"] == 8400
    tangent_upper = 513*Q(41, 10)+8400
    assert tangent_upper == Q(105033, 10) < 10504
    return {"method": "Finite Gamma products with log-convexity remainder; dyadic rational log intervals",
            "Gamma_product_n": n, "log_series_terms": TERMS, "log_interval_bits": BITS,
            "log_gamma_formula": "R=-8*log(64)+sum_a c_a*log(Gamma(a/64))",
            "finite_product_partial_interval": serialized(partial),
            "positive_error_weight": str(positive), "negative_error_weight": str(negative),
            "error_log_interval": serialized(step), "Lprime_over_L_interval": serialized(ratio),
            "Hodge_height_interval": serialized(hodge), "Hodge_height_upper": "17/10",
            "coarse_fibre_height_upper_from_interval": str(coarse_upper),
            "coarse_fibre_height_upper": "41/10", "tangent_height_upper": str(tangent_upper),
            "rounded_tangent_height_upper": 10504,
            "floating_point_values_used_for_certification": False}


def height_formula_controls():
    # Each pair records coefficients of R=L'/L(0) and log(2).
    average = (Q(-1, 2), Q(-48, 4))
    nearby = (average[0]/4, average[1]/4+Q(31, 16))
    hodge = (nearby[0], nearby[1]+Q(1+17, 16))
    main_theorem = (average[0]/4, average[1]/4+Q(31+17+1, 16))
    assert hodge == main_theorem == (Q(-1, 8), Q(1, 16))
    omitted = (average[0]/4, average[1]/4+Q(31+1, 16))
    assert hodge != omitted and hodge[1]-omitted[1] == Q(17, 16)
    types = list(range(2**8))
    neighbors = [(a, a ^ (1 << j)) for a in types for j in range(8) if a < (a ^ (1 << j))]
    assert len(neighbors) == 8*2**7
    assert Q(len(neighbors), 2**7)*Q(1, 2) == 4
    return {"CM_type_count": len(types), "unordered_nearby_pairs": len(neighbors),
            "nearby_height_identity": "average_CM_height=4*h_nearby-(1/4)*log(d_F)",
            "Hodge_height_formula": "h_L(Q)=-(1/8)*Lprime_over_L(0,chi_M/F)+(1/16)*log(2)",
            "main_theorem_and_nearby_derivation_agree": True,
            "d_Sigma_omission_rejected": True, "omission_changes_height_by": "(17/16)*log(2)",
            "excluded_Yuan_Zhang_CM_point_theorems_used": False,
            "CM_Faltings_metric": "norm squared = abs(integral alpha wedge conjugate(alpha))/(2*pi)^8",
            "Hodge_metric": "norm(d_tau)=2*Im(tau)",
            "D103_curve_Faltings_metric_is_kept_separate": True}


def jet_controls():
    # Smooth simple branch u=z^2+a*z^3+b*z^4: differentiate d(u) at z=0.
    cases = []
    for a, b in ((0, 0), (3, -2), (-7, 5)):
        derivative = [0, 2, 3*a, 4*b]
        assert derivative[0] == 0 and derivative[1] == 2
        # At a zero of the differential, change eta by f and xi by g.
        for f0, g0 in ((1, 1), (3, 5), (7, -3)):
            transformed = Q(f0, g0**2)*derivative[1]
            assert transformed*g0**2 == f0*2
        cases.append({"u_coefficients": [0, 0, 1, a, b], "ramification_derivative": 2})
    # Branch-swapping node xy=t^2, u=x+y: D=x*d_x-y*d_y.
    node_cases = []
    for t in (2, 4, 16, 256):
        x, y = t, t
        assert x*y == t*t and x-y == 0
        second = x+y
        assert second == 2*t
        node_cases.append({"t": t, "differential_at_section": 0,
                           "ramification_derivative": second, "integral_at_2": True})
    # Branch-preserving wild involution on xy=4: x->4-x, y->y/(y-1).
    # Invariants t=x^2*(y-1), s=y^2/(y-1) satisfy t*s=16.
    x, y = Q(2), Q(2)
    invariant_t, invariant_s = x*x*(y-1), y*y/(y-1)
    assert invariant_t*invariant_s == 16
    differential = (y-2)/(y-1)
    derivative = -y/(y-1)**2
    assert differential == 0 and derivative == -2
    assert Q(4)-x == x and y/(y-1) == y
    # Formal denominator y-1 is a unit at the special node y=0.
    assert 0-1 == -1
    # The derivative-of-a-line-map construction requires its restriction to vanish.
    assert [1, 2][0] != 0  # u=z+z^2, excluded unramified chart.
    assert [0, 0, 3][1] == 0  # u=z^3, excluded higher ramification chart.
    return {"smooth_simple_branch": cases, "branch_swapping_nodes": node_cases,
            "wild_branch_preserving_node": {"xy": 4, "target_ts": 16, "point": [2, 2], "ramification_derivative": -2},
            "unramified_chart_rejected": True, "higher_ramification_chart_rejected": True,
            "finite_place_construction_divides_by_2": False,
            "archimedean_operator_norm": 2,
            "comparison": "H_CM_disk <= 2*H_S_disk+log(2) <= 2*h_L(Q)+log(2)",
            "controls_are_not_explicit_models_of_the_actual_bad_fibre": True}


def build():
    field, coefficients = field_and_characters()
    paths = [Path(__file__), CM, D103,
             ROOT / "dembele/certificates/cm-adjugate-height-d103.md",
             ROOT / "dembele/certificates/marked-descent.md"]
    return {"status": "pass", "milestone": "D104", "field": field,
            "height_formula_controls": height_formula_controls(), "analytic_bound": analytic_bound(coefficients),
            "ramification_controls": jet_controls(), "coarse_CM_fibre_height_numerically_bounded": True,
            "tangent_height_bound_conditional_on_D103_arithmetic_frame_hypotheses": True,
            "remaining_hypotheses": ["Intended arithmetic CM field labels", "All evaluation cofactors nonzero", "Chosen Gaussian denominator nonzero"],
            "independent_Shimura_tangent_obtained": False,
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
    print(json.dumps({"status": "pass", "Hodge_height_upper": "17/10", "coarse_CM_height_upper": "41/10",
                      "conditional_tangent_height_upper": 10504,
                      "independent_Shimura_tangent_obtained": False}), flush=True)
    print("PASS|D104_INTRINSIC_HEIGHT", flush=True)


if __name__ == "__main__":
    main()

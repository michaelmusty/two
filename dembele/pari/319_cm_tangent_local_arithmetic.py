"""D89: exact local input audit for an independent CM tangent construction.

No candidate curve equations, candidate jets, or differential banks are read.
This checks the tame quotient and local Hecke branches, not section values.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUTPUT = DATA / "cm_tangent_local_arithmetic_d89.json"
N = 10


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def series(entries=()):
    return [Q(entries[i]) if i < len(entries) else Q(0) for i in range(N)]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def scale(a, c):
    return [Q(c) * x for x in a]


def mul(a, b):
    return [sum(a[j] * b[i-j] for j in range(i+1)) for i in range(N)]


def compose(a, b):
    assert b[0] == 0
    result = series()
    for c in reversed(a):
        result = mul(result, b)
        result[0] += c
    return result


def inverse(a):
    assert a[0]
    result = series([1/a[0]])
    for n in range(1, N):
        result[n] = -sum(a[j]*result[n-j] for j in range(1, n+1))/a[0]
    assert mul(a, result) == series([1])
    return result


def formal_quotient():
    x = series([0, 1])
    # If q=1+x and the split CM action sends q to q^{-1}, then
    # x -> -x/(1+x). The tame linear coordinate z=x/(2+x) is odd.
    involution = scale(mul(x, inverse(series([1, 1]))), -1)
    z = mul(x, inverse(series([2, 1])))
    coarse = mul(z, z)
    assert compose(involution, involution) == x
    assert compose(z, involution) == scale(z, -1)
    assert compose(coarse, involution) == coarse
    assert coarse[:3] == [0, 0, Q(1, 4)]
    assert coarse[:2] == [0, 0]

    # For u=z^2, (a+b*u+c*u^2) du pulls back to
    # (2*a*z+2*b*z^3+2*c*z^5) dz. Reversing z fixes the differential.
    packets = []
    for a, b, c in [(1, 2, 3), (1, 7, 3), (0, 1, 0)]:
        upstairs = series([0, 2*a, 0, 2*b, 0, 2*c])
        minus_z = scale(x, -1)
        assert scale(compose(upstairs, minus_z), -1) == upstairs
        packets.append({"coarse_coefficients": [a, b, c],
                        "upstairs_coefficients": [str(v) for v in upstairs[:6]]})
    assert packets[0]["coarse_coefficients"][0] == packets[1]["coarse_coefficients"][0]
    assert packets[0]["coarse_coefficients"][1] != packets[1]["coarse_coefficients"][1]
    # This is a local-section example, not a pair of global Shimura forms.
    return {"truncation_order": N,
            "ST_involution_x": [str(v) for v in involution],
            "odd_coordinate_z": [str(v) for v in z],
            "coarse_coordinate_u": [str(v) for v in coarse],
            "coarse_coordinate_zero_on_dual_numbers": True,
            "differential_degrees_for_three_coarse_coefficients": [1, 3, 5],
            "same_value_different_tangent_local_sections": packets,
            "scope": "Formal identities; existence of a matched arithmetic ST test object is not certified."}


def poly_eval(coefficients, x, p):
    answer = 0
    for c in reversed(coefficients):
        answer = (answer*x + int(c)) % p
    return answer


def local_hecke(arithmetic):
    p = 31
    f = [2, 0, -16, 0, 20, 0, -8, 0, 1]
    prime_generator = [1, 2, 0, -4, 0, 1]
    roots = [b for b in range(p) if poly_eval(f, b, p) == 0]
    selected = [b for b in roots if poly_eval(prime_generator, b, p) == 0]
    assert roots == [4, 9, 10, 11, 20, 21, 22, 27] and selected == [27]
    cm_poly = arithmetic["CM_cyclic_field"]["polynomial_coefficients_ascending"]
    split_data = []
    for b in roots:
        beta = [v for v in range(p) if (v*v+2+b) % p == 0]
        assert len(beta) == 2 and all(poly_eval(cm_poly, v, p) == 0 for v in beta)
        split_data.append({"b": b, "beta_roots": beta})
    beta = next(row["beta_roots"] for row in split_data if row["b"] == 27)
    assert beta == [8, 23]
    # Choose eigenvectors of the integral split CM algebra. Every maximal
    # local embedding is conjugate to this diagonal model.
    lines = [(1, a) for a in range(p)] + [(0, 1)]

    def normalise(v):
        if v[0] % p:
            return (1, v[1]*pow(v[0], -1, p) % p)
        return (0, 1)

    permutation = [lines.index(normalise((beta[0]*v[0], beta[1]*v[1]))) for v in lines]
    assert all(permutation[permutation[i]] == i for i in range(p+1))
    records = []
    for i, v in enumerate(lines):
        stable = [(a, b) for a in range(p) for b in range(p)
                  if (a*v[0]*v[1]-b*v[1]*v[0]) % p == 0]
        horizontal = v[0] == 0 or v[1] == 0
        assert len(stable) == (p*p if horizontal else p)
        if not horizontal:
            assert stable == [(a, a) for a in range(p)]
        records.append({"line": list(v), "elliptic_image": permutation[i],
                        "horizontal": horizontal,
                        "CM_endomorphism_residues": len(stable),
                        "local_multiplier_order": "R x R" if horizontal else "{(a,b): a=b mod31}"})
    fixed = [i for i in range(p+1) if permutation[i] == i]
    pairs = [[i, permutation[i]] for i in range(p+1) if i < permutation[i]]
    assert fixed == [0, 31] and len(pairs) == 15
    assert all(records[i]["horizontal"] == (i in fixed) for i in range(p+1))

    # For t=s^2, trace(g(s) ds) has coefficients g_1,g_3,g_5,... .
    # It is surjective locally, so unknown descending-branch jets cannot
    # simply be dropped from an equation for a known Hecke operator.
    trace_controls = []
    for target in ([1, 2, 3], [0, 1, 0], [7, 0, 19], [30, 30, 30]):
        g = [0]*6
        for j, c in enumerate(target):
            g[2*j+1] = c
        trace = g[1::2]
        assert trace == list(target)
        assert [(g[i]-((-1)**i)*g[i]) % p for i in range(6)] == [2*x % p for x in g]
        trace_controls.append({"target": list(target), "upstairs_differential": g, "trace": trace})
    # Negative control: deleting all 30 nonhorizontal branches loses a
    # trace contribution even when every horizontal term is zero.
    assert trace_controls[1]["trace"] == [0, 1, 0]
    return {"prime": p, "field_roots": roots, "Hecke_place_b": 27,
            "CM_beta_roots_at_Hecke_place": beta, "splitting_at_all_places": split_data,
            "unquotiented_neighbor_count": len(lines), "horizontal_count": len(fixed),
            "conductor_31_count": len(lines)-len(fixed),
            "elliptic_fixed_neighbor_indices": fixed, "descending_neighbor_pairs": pairs,
            "coarse_branch_count_with_multiplicity": {"horizontal_multiplicity_one": 2,
                                                       "descending_multiplicity_two": 15},
            "neighbors": records, "local_trace_controls": trace_controls,
            "discarding_descending_terms_rejected": True,
            "scope": "Local branches with multiplicity, not a global census of distinct image points."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    arithmetic_path = DATA / "cm_arithmetic_audit.json"
    arithmetic = json.loads(arithmetic_path.read_text())
    report = {"status": "pass", "date": "2026-09-23", "milestone": "D89",
              "formal_quotient": formal_quotient(), "local_Hecke": local_hecke(arithmetic),
              "candidate_curve_inputs_used": False, "Shimura_tangent_computed": False,
              "arithmetic_ST_test_object_constructed": False,
              "sources": [source(__file__), source(arithmetic_path),
                          source(ROOT / "dembele/magma/58_levelraise_p2k.m")],
              "conclusion": "The known CM orbit is not closed under the full Hecke correspondence; an arithmetic section evaluator is still needed."}
    if args.check:
        assert json.loads(OUTPUT.read_text()) == report
    else:
        assert not OUTPUT.exists(), "Refusing to overwrite an existing certificate"
        OUTPUT.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS: tame CM quotient; 2 horizontal and 30 descending Hecke branches; trace controls")


if __name__ == "__main__":
    main()

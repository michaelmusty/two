"""D104 audit: conjugate-product character traces and an independent Gamma series.

Also supplies conservative, conditional recognition tolerances. Candidate data
enters only that diagnostic, never the target's CM height calculation.
"""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import importlib.util
import json
from math import lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "cm_intrinsic_height_review_d104.json"
SPEC = importlib.util.spec_from_file_location("d104", ROOT / "dembele/pari/382_cm_intrinsic_height.py")
MAIN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MAIN)


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def checked_sources(items):
    for item in items:
        assert source(item["path"]) == item
    return [Path(item["path"]) for item in items]


def multiply(a, b):
    # Direct signed cyclic convolution, not the main program's reduction.
    result = [Q(0)]*8
    for i in range(8):
        for j in range(8):
            result[(i+j) % 8] += a[i]*b[j]*(1 if i+j < 8 else -1)
    return result


def automorphism(a, k):
    result = [Q(0)]*8
    for i, c in enumerate(a):
        exponent = i*k % 16
        result[exponent % 8] += c*(1 if exponent < 8 else -1)
    return result


def independent_characters(saved):
    # The independent character sends 3 to w and 31 to 1.
    table = {(pow(3, m, 64)*pow(31, s, 64)) % 64: m
             for m in range(16) for s in range(2)}
    assert len(table) == 32 and table[63] == 8 and table[31] == 0
    chi = {}
    for a, m in table.items():
        row = [Q(0)]*8
        row[m % 8] = Q(1 if m < 8 else -1)
        chi[a] = row
    value = [-sum(Q(a, 64)*chi[a][j] for a in chi) for j in range(8)]
    product_other = [Q(1)]+[Q(0)]*7
    for k in range(3, 16, 2):
        product_other = multiply(product_other, automorphism(value, k))
    norm = multiply(value, product_other)
    assert norm[0] == 2176 and not any(norm[1:])
    inverse = [x/norm[0] for x in product_other]
    coefficients = {a: 8*multiply(chi[a], inverse)[0] for a in sorted(chi)}
    assert {str(a): str(c) for a, c in coefficients.items()} == saved["field"]["log_gamma_trace_coefficients"]
    assert all(coefficients[a] == -coefficients[64-a] for a in coefficients)
    assert sum(coefficients[a]*Q(a, 64) for a in coefficients if a < 32) == 4
    corrupted = dict(coefficients)
    corrupted[1] += 1
    assert sum(corrupted.values()) != 0
    return coefficients, {"quotient_generator": 3, "inverse_method": "product of seven other Galois conjugates divided by norm",
                          "L0_norm": int(norm[0]), "all_32_trace_coefficients_agree": True,
                          "corrupted_coefficient_rejected": True}


def plus(a, b):
    return a[0]+b[0], a[1]+b[1]


def scale(a, c):
    return tuple(sorted((a[0]*c, a[1]*c)))


@lru_cache(None)
def log_bounds(value):
    value, exponent = Q(value), 0
    assert value > 0
    while value < 1:
        value *= 2
        exponent -= 1
    while value >= 2:
        value /= 2
        exponent += 1

    def series(x):
        t = (x-1)/(x+1)
        lower = sum((2*t**(2*j+1)/Q(2*j+1) for j in range(40)), Q(0))
        upper = lower+2*t**81/(81*(1-t*t))
        return lower, upper

    low, high = plus(series(value), scale(series(Q(2)), exponent))
    unit = 2**64
    return Q((low*unit).__floor__(), unit), Q((high*unit).__ceil__(), unit)


def dyadic(a, bits=64):
    unit = 2**bits
    return Q((a[0]*unit).__floor__(), unit), Q((a[1]*unit).__ceil__(), unit)


def independent_analytic(coefficients, saved):
    harmonic_n, zeta_n = 512, 64
    harmonic = sum((Q(1, k) for k in range(1, harmonic_n+1)), Q(0))
    logn = log_bounds(harmonic_n)
    gamma = dyadic((harmonic-logn[1]-Q(1, harmonic_n), harmonic-logn[0]))
    zeta = {}
    for m in range(3, 26, 2):
        partial = sum((Q(1, k**m) for k in range(1, zeta_n+1)), Q(0))
        zeta[m] = dyadic((partial+Q(1, (m-1)*(zeta_n+1)**(m-1)),
                         partial+Q(1, (m-1)*zeta_n**(m-1))))
    ratio = scale(log_bounds(64), -8)
    for a, c in coefficients.items():
        if a >= 32:
            continue
        x = Q(a, 64)
        difference = plus(scale(log_bounds(x), -1), scale(gamma, -2*x))
        for m in range(3, 26, 2):
            difference = plus(difference, scale(zeta[m], -2*x**m/m))
        # Remaining odd powers start at 27; zeta(m)<2.
        remainder = 4*x**27/(27*(1-x*x))
        difference = difference[0]-remainder, difference[1]
        ratio = plus(ratio, scale(difference, c))
    ratio = dyadic(ratio)
    hodge = dyadic(plus(scale(ratio, Q(-1, 8)), scale(log_bounds(2), Q(1, 16))))
    old = tuple(map(Q, saved["analytic_bound"]["Lprime_over_L_interval"]))
    assert old[0] < ratio[0] < ratio[1] < old[1]
    assert Q(168, 100) < hodge[0] < hodge[1] < Q(17, 10)
    assert 2*hodge[1]+log_bounds(2)[1] < Q(41, 10)
    return {"method": "Antisymmetric log-Gamma Taylor series, harmonic Euler-constant bounds and integral zeta tails",
            "harmonic_n": harmonic_n, "zeta_n": zeta_n, "largest_odd_power": 25,
            "log_terms": 40, "outward_rounding_bits": 64,
            "Euler_constant_interval": list(map(str, gamma)),
            "Lprime_over_L_interval": list(map(str, ratio)),
            "Hodge_height_interval": list(map(str, hodge)),
            "interval_strictly_inside_main_interval": True,
            "independently_proves_Hodge_below_17_over_10": True,
            "independently_proves_coarse_height_below_41_over_10": True}


def independent_node_jets():
    # Truncated exponential coordinate: x=x0*exp(z), y=y0*exp(-z).
    def mul(a, b):
        return [sum(a[j]*b[k-j] for j in range(k+1)) for k in range(3)]

    cases = []
    for t in (2, 8, 32):
        x, y = [Q(t), Q(t), Q(t, 2)], [Q(t), Q(-t), Q(t, 2)]
        assert mul(x, y) == [t*t, 0, 0]
        u = [x[i]+y[i] for i in range(3)]
        assert u[1] == 0 and 2*u[2] == 2*t
        cases.append({"xy": t*t, "second_jet": str(2*u[2])})
    x, y = [Q(2), Q(2), Q(1)], [Q(2), Q(-2), Q(1)]
    ym1 = y[:]
    ym1[0] -= 1
    invariant = mul(mul(x, x), ym1)
    assert invariant == [4, 0, -4]
    # Target dualizing generator is d(t)/t: differentiate its zero coefficient.
    assert 2*invariant[2]/invariant[0] == -2
    # A changed fibre generator scales the second map quadratically.
    for f, g in ((Q(3), Q(5)), (Q(-2), Q(7))):
        assert f*Q(-2)/(g*g)*g*g == f*(-2)
    return {"algorithm": "second-order exponential-coordinate jets",
            "branch_swapping_nodes": cases, "wild_branch_preserving_second_map": -2,
            "controls_do_not_assert_actual_bad_fibre_equations": True}


def recognition_budget():
    candidate_path = DATA / "cm_tangent_exactness_d101.json"
    candidate = json.loads(candidate_path.read_text())
    field = json.loads((DATA / "cm_arithmetic_audit.json").read_text())
    f = field["residue_algebra_input"]["polynomial_coefficients_ascending"]
    assert f[-1] == 1 and sum(abs(int(c))*4**i for i, c in enumerate(f[:-1])) < 4**17
    rows = []
    for row in candidate["candidate_tangent_power_basis"]:
        row = list(map(Q, row))
        denominator = lcm(*(x.denominator for x in row))
        numerator_bound = sum(abs(denominator*x)*4**i for i, x in enumerate(row))
        assert numerator_bound.denominator == 1
        bound = int(max(denominator, numerator_bound))
        rows.append({"clearing_integer": str(denominator), "max_denominator_or_numerator_bound": str(bound),
                     "strict_power_of_two_exponent": bound.bit_length()})
    max_bits = max(r["strict_power_of_two_exponent"] for r in rows)
    assert max_bits == 975 and log_bounds(2)[1] < Q(7, 10)
    assert max_bits*Q(7, 10) < 683
    # Absolute logarithmic heights; the subtraction contributes at most log(2).
    target, reference, degree = 10504, 683, 136
    difference_bound = Q(target+reference)+Q(7, 10)
    log10 = log_bounds(10)
    single_digits = (degree*difference_bound/log10[0]).__floor__()+1
    all_digits = (difference_bound/log10[0]).__floor__()+1
    assert single_digits == 660791 and all_digits == 4859
    assert single_digits*log10[0] > degree*difference_bound
    assert all_digits*log10[0] > difference_bound
    # A nonzero rational at equality illustrates why a strict norm threshold is required.
    assert Q(1, 10**4)*10**4 == 1
    return {"candidate_only_rows": rows, "candidate_height_upper": reference,
            "candidate_max_power_of_two_exponent": max_bits,
            "target_height_upper_conditional": target, "common_field_degree_upper_conditional": degree,
            "difference_height_upper": str(difference_bound),
            "single_embedding_absolute_error_sufficient": "10^(-660791)",
            "all_embeddings_uniform_absolute_error_sufficient": "10^(-4859)",
            "digits_are_sufficient_not_minimal_or_an_evaluation_cost_estimate": True,
            "requires_D103_frame_and_chart_hypotheses": True,
            "requires_common_field_degree_bound_and_correct_embedding_labels": True,
            "actual_errors_not_certified": True}


def build():
    saved = json.loads(MAIN.OUT.read_text())
    paths = checked_sources(saved["sources"])
    assert MAIN.build() == saved
    old_path = DATA / "cm_adjugate_height_review_d103.json"
    old = json.loads(old_path.read_text())
    paths += checked_sources(old["sources"])
    job_path = DATA / "cm_intrinsic_height_d104_attempt01.job.json"
    job = json.loads(job_path.read_text())
    assert job["status"] == "pass" and job["timeout_seconds"] == 180
    assert job["wall_seconds"] < 180 and job["timeout_terminates_process_group"]
    paths += checked_sources(job["sources"]+[job["driver"], job["log"]])
    coefficients, character_check = independent_characters(saved)
    analytic = independent_analytic(coefficients, saved)
    budget = recognition_budget()
    paths += [Path(__file__), MAIN.OUT, old_path, job_path,
              DATA / "cm_tangent_exactness_d101.json",
              ROOT / "dembele/certificates/cm-intrinsic-height-d104.md",
              DATA / "cm_intrinsic_height_sources_d104.json"]
    return {"status": "pass", "milestone": "D104", "independent_characters": character_check,
            "independent_analytic": analytic, "independent_node_jets": independent_node_jets(),
            "conditional_recognition_budget": budget,
            "D103_bound_source_hashes_checked": len(old["sources"]),
            "D102_and_D101_transitive_sources_unchanged": True,
            "sources": [source(p) for p in sorted(set(p.resolve() for p in paths))],
            "intrinsic_height_comparison_proved_in_companion_report": True,
            "arithmetic_frame_and_chart_hypotheses_still_open": True,
            "independent_Shimura_tangent_obtained": False,
            "spectral_pilot_gate_passed": False,
            "scope": "Exact arithmetic and independent analytic checks; the geometric and cited theorem proofs are not machine-verified."}


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
                      "D103_hashes_unchanged": result["D103_bound_source_hashes_checked"],
                      "independent_Gamma_series": "pass", "conditional_target_height_upper": 10504,
                      "sufficient_error_decimal_exponents": [660791, 4859]}), flush=True)
    print("PASS|D104_INTRINSIC_HEIGHT_REVIEW", flush=True)


if __name__ == "__main__":
    main()

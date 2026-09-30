"""D98: rational replay and provenance for the spectral ideal bound.

Replays rectangle summation, algebraic powers, normalization controls,
the tail polynomial, Euler coefficients and directed error assembly.
The spectral proof and Arb transcendental evaluations are hash-bound.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
REPORT = ROOT/"dembele/certificates/nelson-spectral-ideal-d98.md"
OUTPUT = DATA/"nelson_spectral_ideal_d98.json"
spec = importlib.util.spec_from_file_location("prior_arithmetic", Path(__file__).with_name("367_nelson_signed_orbit_audit.py"))
ar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ar)
box, add, mul, divide, scale = ar.box, ar.add, ar.mul, ar.divide, ar.scale


def point(x):
    return Q(x), Q(x)


def power(x, exponent):
    assert x[0] > 0
    exponent = Q(exponent)
    if exponent < 0:
        return divide(point(1), power(x, -exponent))
    n, d = exponent.numerator, exponent.denominator
    if d == 1:
        return ar.rounded((x[0]**n, x[1]**n))
    return ar.radical(x[0]**n, d)[0], ar.radical(x[1]**n, d)[1]


def polyadd(p, q):
    r = dict(p)
    for m, c in q.items():
        r[m] = r.get(m, 0)+c
    return {m: c for m, c in r.items() if c}


def polymul(p, q):
    r = {}
    for m, c in p.items():
        for n, d in q.items():
            k = tuple(a+b for a, b in zip(m, n))
            r[k] = r.get(k, 0)+c*d
    return {m: c for m, c in r.items() if c}


def algebra_replay():
    # Polynomial identity after independently cancelling Gamma factors.
    lhs = polyadd(polymul({(1, 0): -1, (0, 0): -2}, {(1, 0): 1, (0, 0): -1}),
                  polymul({(1, 0): 1, (0, 0): 1, (0, 1): -1}, {(1, 0): 1, (0, 1): 1}))
    assert lhs == {(0, 0): 2, (0, 1): 1, (0, 2): -1}
    # Laurent-polynomial radial Casimir equation for both discrete series.
    for lam, phi in [(0, {(-1,): -2, (-2,): 3}), (-2, {(-2,): 1})]:
        d1 = {(j-1,): j*c for (j,), c in phi.items()}
        d2 = {(j-2,): j*(j-1)*c for (j,), c in phi.items()}
        equation = polyadd(polymul({(2,): 1, (1,): -1}, d2),
                           polymul({(1,): 2, (0,): -1}, d1))
        equation = polyadd(equation, polymul({(0,): lam, (-1,): 4}, phi))
        assert equation == {} and sum(phi.values()) == 1
    # Local all-content Hecke mass, rather than a primitive double coset.
    count = 64
    coefficients = [(e+1)**2 for e in range(count)]
    for e in range(count):
        value = sum((-1)**j*comb(3, j)*coefficients[e-j] for j in range(min(3, e)+1))
        assert value == (1 if e in (0, 1) else 0)
    kappa, cutoff = Q(32, 7), Q(64)
    packing = 1+3*kappa/(2*cutoff**2)
    assert packing == Q(1795, 1792)
    return {"Mellin_multiplier_identity": True, "discrete_series_radial_ODE_checks": 2,
            "local_Euler_coefficients_checked": count, "positive_pretrace_bound": str(packing)}


def replay(packet, prior, prime):
    assert packet["precision_bits"] == 320
    denominator, height = packet["mesh_denominator"], packet["height"]
    assert (denominator, height) == (128, 16)
    delta, packing = Q(packet["finite_Hecke_exponent"]), Q(packet["positive_pretrace_bound"])
    assert delta == Q(7, 64) and packing == Q(1795, 1792)
    polynomial = [Q(1)]
    for _ in range(28):
        polynomial = [2*polynomial[0]]+[2*b+a for a, b in zip(polynomial, polynomial[1:])]+[polynomial[-1]]
    polynomial = [3*polynomial[0]]+[3*b+2*a for a, b in zip(polynomial, polynomial[1:])]+[2*polynomial[-1]]
    integral = sum(a*sum(Q(comb(j, v)*height**(j-v)*factorial(v), 21**(v+1))
                         for v in range(j+1)) for j, a in enumerate(polynomial))
    assert len(polynomial) == 30
    rows, rectangle_count = [], 0
    for row in packet["rows"]:
        c, w = Q(row["contour"]), Q(row["norm_exponent"])
        assert 1+delta < c <= 2 and w == c-delta
        # Both real and principal-series Gamma comparisons have this margin.
        assert c*(c+1)-2 == (c+Q(1, 2))**2-Q(9, 4) == (c-1)*(c+2) > 0
        cells = list(map(Q, row["rectangle_upper_bounds"]))
        assert len(cells) == denominator*height
        assert all(v >= 0 and v.denominator & (v.denominator-1) == 0 for v in cells)
        rectangle_count += len(cells)
        finite = sum(cells, Q(0))/denominator
        assert finite == Q(row["finite_integral_upper"])
        assert list(map(Q, row["tail_polynomial"])) == polynomial
        assert Q(row["tail_integral_before_exponential"]) == integral
        vertical = box(row["vertical_tail"])
        assert 0 < vertical[0] < vertical[1] < Q(1, 10**103)
        value = mul(box(row["gamma_comparison_factor"]), box(row["zeta_2c"]))
        value = mul(value, box(row["cusp_factor"]))
        value = divide(mul(value, add(point(finite), vertical)), box(packet["pi"]))
        ar.overlap(value, box(row["B_c"]))
        zscale = power(box(packet["Z0"]), -c)
        ar.overlap(zscale, box(row["Z0_minus_c"]))
        prime_mass = scale(power(point(31), -w), 4)
        ar.overlap(prime_mass, box(row["removed_prime31_mass"]))
        omitted = add(add(box(row["odd_squared_divisor_mass"]), point(-1)), ar.neg(prime_mass))
        assert omitted[0] > 0
        ar.overlap(omitted, box(row["omitted_mass"]))
        bound = scale(mul(mul(value, zscale), omitted), packing)
        ar.overlap(bound, box(row["uncomputed_ideal_S11_bound"]))
        rows.append({"contour": str(c), "norm_exponent": str(w),
                     "omitted_bound": list(map(str, bound))})
    best = min(rows, key=lambda row: Q(row["omitted_bound"][1]))
    assert best["contour"] == packet["best_contour"] == "5/4"
    omitted_upper = Q(best["omitted_bound"][1])
    selected = prime["weighted_first_quartic_orbit"][prime["selected_root_index"]]["unit_plus_prime_families"]["1"]
    partial = box(selected["partial_sum"]["real"])
    two_error = box(selected["absolute_error_bound"])[1]
    full_error = omitted_upper+two_error
    enclosure = partial[0]-full_error, partial[1]+full_error
    improvement = Q(prior["certified_omitted_S11_error_upper"])/omitted_upper
    assert omitted_upper < 24784932714 and full_error < 24784942340
    assert improvement > Q(27248, 100)
    assert enclosure[0] < 0 < enclosure[1]
    assert Q(packet["certified_omitted_S11_error_upper"]) <= omitted_upper
    ar.overlap(partial, box(packet["selected_S11_partial_sum"]))
    for key in ["CM_anchor_derivative_nonzero", "signed_infinite_counting_estimate_assumed",
                "new_quaternion_enumeration", "new_Hecke_data", "enumeration_expansion_justified"]:
        assert packet[key] is False
    return {"rectangle_upper_endpoints_checked": rectangle_count,
            "dyadic_interval_records_checked": ar.interval_count(packet), "contours": rows,
            "best_contour": best["contour"], "certified_omitted_S11_error_upper": str(omitted_upper),
            "certified_two_saved_family_error_upper": str(two_error),
            "certified_full_S11_error_upper": str(full_error),
            "full_S11_rational_enclosure": list(map(str, enclosure)),
            "selected_S11_partial_sum": list(map(str, partial)),
            "improvement_over_D96_lower": str(improvement),
            "bound_to_partial_ratio_upper": str(omitted_upper/partial[0])}


def compute():
    sources = {}
    def bind(path, expected=None):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT/path
        name = str(path.relative_to(ROOT))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None:
            assert digest == expected, name
        if name in sources:
            assert sources[name]["sha256"] == digest
        sources[name] = {"path": name, "sha256": digest}
    def read(name):
        path = DATA/name
        bind(path)
        value = json.loads(path.read_text())
        for row in value.get("sources", []):
            bind(row["path"], row["sha256"])
        return value
    prior_root = read("nelson_signed_orbit_d97.json")
    prior = read("nelson_completed_majorant_d96.json")
    packet = read("nelson_spectral_ideal_bound_d98.json")
    prime = read("nelson_prime31_sum_d93_exact_d93.json")
    job = read("nelson_spectral_ideal_bound_d98_attempt01.job.json")
    bind(job["log"]["path"], job["log"]["sha256"])
    assert job["status"] == "pass" and job["exit_code"] == 0
    assert job["timeout_seconds"] == 180 and job["wall_seconds"] < 180
    assert job["timeout_terminates_process_group"]
    algebra = algebra_replay()
    arithmetic = replay(packet, prior, prime)
    for path in [Path(__file__), REPORT]:
        bind(path)
    return {"status": "pass: explicit spectral ideal bound; CM anchor remains uncertified",
            "prior_source_hashes_verified": len(prior_root["sources"]),
            "algebra_replay": algebra, "rational_replay": arithmetic,
            "analytic_proof": str(REPORT.relative_to(ROOT)),
            "spectral_ideal_bound_proved": True, "global_kernel_identified_up_to_positive_scalar": True,
            "signed_infinite_counting_estimate_assumed": False, "CM_anchor_derivative_nonzero": False,
            "arithmetic_CM_jet_computed": False, "enumeration_expansion_justified": False,
            "job": {"status": job["status"], "wall_seconds": job["wall_seconds"],
                    "path": "dembele/data/computed/nelson_spectral_ideal_bound_d98_attempt01.job.json"},
            "sources": sorted(sources.values(), key=lambda row: row["path"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = compute()
    if args.check:
        assert result == json.loads(OUTPUT.read_text())
    else:
        assert not OUTPUT.exists()
        OUTPUT.write_text(json.dumps(result, indent=2)+"\n")
    counts = result["rational_replay"]
    print("PASS|369_nelson_spectral_ideal_audit", len(result["sources"]), "hashes",
          counts["rectangle_upper_endpoints_checked"], "rectangle endpoints",
          counts["dyadic_interval_records_checked"], "intervals")


if __name__ == "__main__":
    main()

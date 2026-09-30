"""D96: rational sign-certificate replay, error assembly and provenance.

Arb transcendental evaluations are hash-bound to the successful bounded
runs. The Bernstein signs and final directed rational bounds are replayed
without Sage. This certificate does not assert a nonzero CM anchor.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb, factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
OUTPUT = DATA/"nelson_completed_majorant_d96.json"
REPORT = ROOT/"dembele/certificates/nelson-completed-majorant-d96.md"


def box(row):
    return Q(row["lower"]), Q(row["upper"])


def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def scale(x, c):
    values = x[0]*c, x[1]*c
    return min(values), max(values)


def dyadic_intervals(value):
    count = 0
    if isinstance(value, dict):
        if "lower" in value and "upper" in value:
            lo, hi = box(value)
            assert lo <= hi
            assert all(v.denominator & (v.denominator-1) == 0 for v in (lo, hi))
            count += 1
        for v in value.values():
            count += dyadic_intervals(v)
    elif isinstance(value, list):
        count += sum(dyadic_intervals(v) for v in value)
    return count


def bernstein(coefficients, radius):
    n = len(coefficients)-1
    powers = []
    # Direct binomial shift to t in [0,1], followed by the standard
    # triangular power-to-Bernstein transformation. All arithmetic exact.
    for l in range(n+1):
        value = (Q(0), Q(0))
        for m in range(l, n+1):
            value = add(value, scale(coefficients[m], comb(m, l)*(-radius)**(m-l)*(2*radius)**l))
        powers.append(value)
    result = []
    for k in range(n+1):
        value = (Q(0), Q(0))
        for l in range(k+1):
            value = add(value, scale(powers[l], Q(comb(k, l), comb(n, l))))
        result.append(value)
    return result


def sign_replay(blocks, packet):
    signs = packet["sign_certificates"]
    radius = Q(signs["polynomial_domain_radius"])
    assert radius == Q(3, 8) > box(blocks["log_half_width"])[1]
    assert signs["certified_block_count"] == len(signs["records"]) == 72
    assert signs["A_range"] == ["1", str(2**72)] and signs["first_uncertified_block"] is None
    conditions = 0
    for record in signs["records"]:
        j = record["block_index"]
        row = blocks["blocks"][j]
        assert row["A_lower"] == str(2**j) and row["A_upper"] == str(2**(j+1))
        hs = list(map(box, row["kernels"]["H"]["finite_Taylor_coefficients"]))
        qs = list(map(box, row["kernels"]["Q"]["finite_Taylor_coefficients"]))
        assert len(hs) == len(qs) == 32
        k3 = []
        for m in range(32):
            value = hs[m]
            for l in range(m+1):
                value = add(value, scale(qs[l], Q(1, factorial(m-l))))
            k3.append(value)
        polynomials = {"K3": k3, "K4_minus_K3": [scale(v, -1) for v in hs],
                       "minus_Qprime": [scale(qs[m+1], -(m+1)) for m in range(31)]}
        for name, coefficients in polynomials.items():
            values = bernstein(coefficients, radius)
            error = box(record["certificates"][name]["error_bound"])[1]
            # This independent interval expansion loses correlations;
            # positivity must survive it, not only Sage's calculation.
            assert min(v[0] for v in values) > error > 0, (j, name)
            assert box(record["certificates"][name]["positive_margin"])[0] > 0
            conditions += len(values)
    return {"blocks": 72, "positive_function_conditions": 216,
            "positive_Bernstein_coefficients": conditions, "range_upper": str(2**72)}


def multiply(p, q):
    result = [Q(0)]*(len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            result[i+j] += a*b
    return result


def tail_replay(packet):
    polynomial = [Q(1)]
    for _ in range(39):
        polynomial = multiply(polynomial, [3, 1])
    polynomial = multiply(polynomial, [4, 2])
    for j in range(4):
        polynomial = multiply(polynomial, [3+j, 1])
    completed = packet["completed_norm_sum"]
    assert polynomial == list(map(Q, completed["tail_polynomial"]))
    assert len(polynomial)-1 == 44 < 24*16
    integral = sum(coefficient*sum(Q(comb(j, r)*16**(j-r)*factorial(r), 24**(r+1))
                                  for r in range(j+1)) for j, coefficient in enumerate(polynomial))
    assert integral == Q(completed["tail_integral_before_exponential"])
    assert completed["contour"] == "5/2" and completed["strip_half_width"] == "1/2"
    assert completed["step_denominator"] == 64 and completed["height"] == 16
    for row in completed["values"].values():
        fine, coarse = box(row["value"]), box(row["coarse_value"])
        assert max(fine[0], coarse[0]) <= min(fine[1], coarse[1])
        assert row["coarse_grid_overlaps"]
        assert fine[1]-fine[0] < Q(1, 10**40)
    local_denominator = multiply(multiply([1, -1], [1, -1]), multiply([1, -2], [1, -2]))
    assert local_denominator == [1, -6, 13, -12, 4]
    return {"tail_polynomial_degree": 44, "tail_integral_replayed": True,
            "fine_coarse_overlaps": 3, "norm_two_Euler_denominator": list(map(str, local_denominator))}


def sqrt_box(value, bits=128):
    lo, hi = value
    assert 0 <= lo <= hi
    m = 2**bits
    low = isqrt((lo*m*m).numerator//(lo*m*m).denominator)
    high = isqrt((hi*m*m).numerator//(hi*m*m).denominator)+1
    assert Q(low, m)**2 <= lo <= hi <= Q(high, m)**2
    return Q(low, m), Q(high, m)


def complex_absolute(real, imag):
    def abs_box(v):
        lo, hi = v
        return (Q(0) if lo<=0<=hi else min(abs(lo), abs(hi)), max(abs(lo), abs(hi)))
    r, i = abs_box(real), abs_box(imag)
    return sqrt_box((r[0]**2+i[0]**2, r[1]**2+i[1]**2))


def family_diagnostic(packet):
    absolute, real, imag = (Q(0), Q(0)), (Q(0), Q(0)), (Q(0), Q(0))
    for row in packet["class_terms"]:
        value = row["values"]["1"]
        r, i = box(value["real"]), box(value["imag"])
        real, imag = add(real, r), add(imag, i)
        absolute = add(absolute, complex_absolute(r, i))
    signed = complex_absolute(real, imag)
    assert signed[0]>0
    return {"class_count": len(packet["class_terms"]),
            "sum_of_absolute_values": list(map(str, absolute)),
            "absolute_of_signed_sum": list(map(str, signed)),
            "cancellation_factor": [str(absolute[0]/signed[1]), str(absolute[1]/signed[0])],
            "scope": "saved finite family only; no inference about omitted norms or displacements"}


def compute():
    sources = {}
    def bind(path, expected=None):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT/path
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None:
            assert digest == expected, path
        name = str(path.relative_to(ROOT))
        sources[name] = {"path": name, "sha256": digest}
    def read(name):
        path = DATA/name
        bind(path)
        value = json.loads(path.read_text())
        for row in value.get("sources", []):
            bind(row["path"], row["sha256"])
        return value
    prior = read("nelson_global_identification_d95.json")
    blocks = read("nelson_completed_scalar_blocks_d96.json")
    packet = read("nelson_completed_ideal_majorant_d96.json")
    unit = read("nelson_norm_one_sum_d92_T25600_exact_d93.json")
    prime = read("nelson_prime31_sum_d93_exact_d93.json")
    jobs = []
    for stem in ("nelson_completed_scalar_blocks_d96", "nelson_completed_ideal_majorant_d96"):
        name = stem+"_attempt01.job.json"
        job = read(name)
        bind(job["log"]["path"], job["log"]["sha256"])
        assert job["status"] == "pass" and job["exit_code"] == 0
        assert job["timeout_seconds"] == 180 and job["timeout_terminates_process_group"]
        assert job["wall_seconds"]<180
        jobs.append({"path": "dembele/data/computed/"+name, "wall_seconds": job["wall_seconds"], "status": "pass"})
    interval_count = dyadic_intervals(blocks)+dyadic_intervals(packet)
    signs = sign_replay(blocks, packet)
    print("BERNSTEIN_RATIONAL_REPLAY", signs, flush=True)
    analytic = tail_replay(packet)
    splice = packet["splice"]
    assert splice["T"] == str(2**72) and splice["c"] == "4" and splice["u"] == "25/16"
    kappa = Q(packet["packing_count_coefficient"])
    assert kappa == Q(32, 7)
    completed_hi = box(packet["completed_norm_sum"]["omitted_ideal_sum"])[1]
    tail_hi = box(splice["all_A_above_T_error"])[1]
    splice_hi = box(splice["norm_sum_splice_error"])[1]
    assert 0 < tail_hi+splice_hi < Q(14, 10**7)
    omitted_hi = kappa*completed_hi+tail_hi+splice_hi
    assert 0 < omitted_hi < 6754*10**9
    assert box(packet["uncomputed_ideal_S11_bound"])[0] <= omitted_hi
    improvement = box(packet["D94_bound"])[0]/omitted_hi
    assert Q(3967, 1000) < improvement < Q(3968, 1000)
    full_error = omitted_hi+box(packet["two_family_tail"])[1]
    partial = box(packet["selected_partial_sum"])
    full = partial[0]-full_error, partial[1]+full_error
    assert full[0]<0<full[1]
    assert 883*10**6 < omitted_hi/partial[1] < 885*10**6
    diagnostics = {"unit": family_diagnostic(unit), "prime31": family_diagnostic(prime)}
    bind(REPORT)
    bind(Path(__file__))
    assert packet["global_kernel_identified_up_to_positive_scalar"]
    for name in ("new_quaternion_enumeration", "new_Hecke_data", "CM_anchor_derivative_nonzero", "arithmetic_CM_jet_computed"):
        assert packet[name] is False
    return {"status": "pass: completed positive majorant improves fourfold; numerical feasibility gate remains closed",
            "prior_root_hashes_verified": len(prior["sources"]), "dyadic_intervals_checked": interval_count,
            "sign_replay": signs, "analytic_replay": analytic,
            "certified_omitted_S11_error_upper": str(omitted_hi), "certified_full_S11_error_upper": str(full_error),
            "full_S11_rational_enclosure": list(map(str, full)), "certified_improvement_lower": str(improvement),
            "saved_family_cancellation_diagnostics": diagnostics,
            "global_kernel_identified_up_to_positive_scalar": True,
            "full_Mellin_series_numerically_evaluated": False, "CM_anchor_derivative_nonzero": False,
            "arithmetic_CM_jet_computed": False, "enumeration_expansion_justified": False,
            "jobs": jobs, "analytic_proof": str(REPORT.relative_to(ROOT)),
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
    print("PASS|362_nelson_completed_majorant_audit", len(result["sources"]), "hashes", result["dyadic_intervals_checked"], "intervals")


if __name__ == "__main__":
    main()

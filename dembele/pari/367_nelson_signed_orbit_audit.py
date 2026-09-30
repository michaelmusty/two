"""D97 independent rational replay, conditional-tail audit, and provenance.

Replays exact shell phases, conjugation, finite Abel bounds, fractional
power integrals, far-tail polynomials, and unchanged actual error bounds.
Arb evaluations and analytic quadrature errors are bound to their runs.
No signed-count estimate outside the enumerated range is asserted.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
OUTPUT = DATA/"nelson_signed_orbit_d97.json"
REPORT = ROOT/"dembele/certificates/nelson-signed-orbit-d97.md"
spec = importlib.util.spec_from_file_location("arithmetic", Path(__file__).with_name("334_nelson_unfolding_audit.py"))
ar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ar)
BITS = 192


def box(row):
    lo, hi = Q(row["lower"]), Q(row["upper"])
    assert lo <= hi
    return lo, hi


def dyadic(x, up=False):
    if not x:
        return Q(0)
    exponent = abs(x.numerator).bit_length()-x.denominator.bit_length()
    scale = Q(2)**(BITS-exponent)
    y = x*scale
    floor = y.numerator//y.denominator
    return Q(floor+int(up and y != floor))/scale


def rounded(x):
    return dyadic(x[0]), dyadic(x[1], True)


def add(x, y):
    return rounded((x[0]+y[0], x[1]+y[1]))


def neg(x):
    return -x[1], -x[0]


def mul(x, y):
    values = [a*b for a in x for b in y]
    return rounded((min(values), max(values)))


def scale(x, c):
    return mul(x, (Q(c), Q(c)))


def divide(x, y):
    assert y[0]*y[1] > 0
    return mul(x, (1/y[1], 1/y[0]))


def absolute(x):
    lo, hi = x
    return (Q(0) if lo <= 0 <= hi else min(abs(lo), abs(hi)), max(abs(lo), abs(hi)))


def overlap(x, y):
    assert max(x[0], y[0]) <= min(x[1], y[1]), (x, y)


def polynomial(coefficients, x):
    # Exact interval Horner before dyadic rounding avoids coefficient-height
    # cancellation losing precision at every intermediate operation.
    result = (Q(0), Q(0))
    for c in reversed(coefficients):
        values = [a*b for a in result for b in x]
        result = min(values)+Q(c), max(values)+Q(c)
    return rounded(result)


def integer_root(n, q):
    if q == 2:
        return isqrt(n)
    lo, hi = 0, 1 << ((n.bit_length()+q-1)//q)
    while hi-lo > 1:
        m = (lo+hi)//2
        if m**q <= n:
            lo = m
        else:
            hi = m
    return lo


def radical(value, q):
    assert value >= 0 and q >= 2
    if not value:
        return Q(0), Q(0)
    exponent = (value.numerator.bit_length()-value.denominator.bit_length())//q
    m = 2**max(0, BITS-exponent)
    scaled = value*m**q
    a = integer_root(scaled.numerator//scaled.denominator, q)
    lo, hi = Q(a, m), Q(a+1, m)
    assert lo**q <= value <= hi**q
    return lo, hi


def complex_absolute(r, i):
    r, i = absolute(r), absolute(i)
    return radical(r[0]**2+i[0]**2, 2)[0], radical(r[1]**2+i[1]**2, 2)[1]


def canonical(v):
    v = tuple(v)
    return v if next(x for x in v if x) > 0 else tuple(-x for x in v)


def field(row):
    assert len(row) <= 8
    return tuple(map(Q, row))+(Q(0),)*(8-len(row))


def encoded(x):
    return list(map(str, x))


def finite_summary(rows):
    total = phase = grouped = atomic = abel = abel_bound = (Q(0), Q(0))
    for i, row in enumerate(rows):
        total = add(total, row["term"])
        grouped = add(grouped, absolute(row["term"]))
        atomic = add(atomic, row["atomic"])
        phase = add(phase, row["phase"])
        difference = add(row["f"], neg(rows[i+1]["f"])) if i+1 < len(rows) else row["f"]
        abel = add(abel, mul(phase, difference))
        abel_bound = add(abel_bound, mul(absolute(phase), absolute(difference)))
    overlap(abel, total)
    best = min(grouped[1], abel_bound[1])
    return {"classes": sum(row["count"] for row in rows), "groups": len(rows),
            "signed_sum": encoded(total), "signed_phase_sum": encoded(phase),
            "atomic_absolute_sum": encoded(atomic), "grouped_absolute_sum": encoded(grouped),
            "Abel_reconstruction": encoded(abel), "Abel_absolute_bound": encoded(abel_bound),
            "best_finite_bound_upper": str(best), "finite_gain_lower": str(atomic[0]/best)}


def signed_replay(packet, enumerations, saved_sums):
    root = box(packet["split_field_root"])
    assert Q(0) < root[0] < root[1] < 1
    p = ar.POLY+[1]
    assert polynomial(p, (root[0], root[0]))[1] < 0 < polynomial(p, (root[1], root[1]))[0] or polynomial(p, (root[1], root[1]))[1] < 0 < polynomial(p, (root[0], root[0]))[0]
    results = []
    for family, enumeration, saved in zip(packet["families"], enumerations, saved_sums):
        N = family["norm"]
        n = field(family["norm_generator"])
        assert n == (ar.ONE if N == 1 else field(enumeration["norm_generator"]["totally_positive_generator_coefficients"]))
        assert ar.fnorm(n) == N
        classes = {row["index"]: row for row in enumeration["classes"]}
        quaternions = {canonical(map(Q, row["quaternion_power_coordinates"])): row["index"] for row in classes.values()}
        assert len(classes) == len(quaternions) == family["class_count"]
        partners = {}
        for q, index in quaternions.items():
            mate = quaternions[canonical(q[:8]+tuple(-x for x in q[8:]))]
            assert classes[mate]["A_field_coefficients"] == classes[index]["A_field_coefficients"]
            partners[index] = mate
        assert sorted(map(list, partners.items())) == family["conjugation_partners"]
        kernels = {field(row["A_field_coefficients"]): row for row in saved["kernels"]}
        terms = {row["class_index"]: row["values"]["1"] for row in saved["class_terms"]}
        seen, replay = set(), []
        prefix = (Q(0), Q(0))
        prefix_count = 0
        prefix_bounds = {theta: Q((box(row)[1]*1000).__ceil__(), 1000)
                         for theta, row in family["observed_finite_prefix_constants"].items()}
        for group in family["groups"]:
            A, phase = field(group["A_field_coefficients"]), field(group["phase_sum_field_coefficients"])
            ids = group["class_indices"]
            assert ids and not seen.intersection(ids)
            seen.update(ids)
            assert all(field(classes[i]["A_field_coefficients"]) == A and partners[i] in ids for i in ids)
            trace2 = trace4 = ar.ZERO
            atomic = old_real = old_imag = (Q(0), Q(0))
            for index in ids:
                trace = ar.fscale(field(classes[index]["quaternion_power_coordinates"][:8]), 2)
                square = ar.fmul(trace, trace)
                trace2 = ar.fadd(trace2, square)
                trace4 = ar.fadd(trace4, ar.fmul(square, square))
                real, imag = box(terms[index]["real"]), box(terms[index]["imag"])
                old_real, old_imag = add(old_real, real), add(old_imag, imag)
                atomic = add(atomic, complex_absolute(real, imag))
            nA = ar.fmul(n, A)
            lhs = ar.fscale(ar.fmul(ar.fmul(nA, nA), ar.fadd(phase, ar.fscale(ar.ONE, -len(ids)))), 2)
            rhs = ar.fadd(ar.fscale(ar.fmul(nA, trace2), -4*N), ar.fscale(trace4, N*N))
            assert lhs == rhs
            a, phase_box = polynomial(A, root), polynomial(phase, root)
            overlap(a, box(group["A"]))
            overlap(phase_box, box(group["phase_sum"]))
            if replay:
                assert replay[-1]["A"][1] < a[0]
            assert a[0] >= N and a[1] < 25600
            k = {v["k"]: box(v["value"]) for v in kernels[A]["values"]}
            rho = add((Q(1), Q(1)), neg(divide((Q(N), Q(N)), a)))
            f = divide(add(k[3], neg(mul(rho, k[4]))), a)
            term = mul(phase_box, f)
            overlap(f, box(group["radial_scalar"]))
            overlap(term, box(group["signed_term"]))
            overlap(term, old_real)
            assert old_imag[0] <= 0 <= old_imag[1]
            prefix, prefix_count = add(prefix, phase_box), prefix_count+len(ids)
            overlap(prefix, box(group["cumulative_signed_phase"]))
            assert prefix_count == group["cumulative_count"]
            for theta, constant in prefix_bounds.items():
                theta = Q(theta)
                assert (absolute(prefix)[1]/constant)**theta.denominator <= (a[0]/N)**theta.numerator
            replay.append({"A": a, "phase": phase_box, "f": f, "term": term, "count": len(ids), "atomic": atomic})
        assert seen == set(classes) and len(replay) == family["group_count"]
        summaries = {"cutoffs": [], "shells": []}
        for kind in summaries:
            for old in family[kind]:
                lower = old.get("lower_exclusive", 0)
                upper = old.get("upper_inclusive", old.get("cutoff"))
                rows = [row for row in replay if row["A"][0] > lower and row["A"][1] < upper]
                assert all(row["A"][1] <= lower or row["A"][0] > lower for row in replay)
                assert all(row["A"][1] < upper or row["A"][0] > upper for row in replay)
                summary = finite_summary(rows)
                assert summary["classes"] == old["classes"] and summary["groups"] == old["groups"]
                for name in ["signed_sum", "signed_phase_sum", "atomic_absolute_sum", "grouped_absolute_sum", "Abel_reconstruction", "Abel_absolute_bound"]:
                    overlap(tuple(map(Q, summary[name])), box(old[name]))
                summaries[kind].append({"lower_exclusive": lower, "upper_inclusive": upper, **summary})
        results.append({"label": family["label"], "norm": N, "classes": len(classes), "groups": len(replay),
                        "conjugation_verified": True, "exact_phase_identities": len(replay),
                        "finite_prefix_bounds_upper": {key: str(v) for key, v in prefix_bounds.items()}, **summaries})
    return results


def times(p, a, b):
    result = [Q(0)]*(len(p)+1)
    for i, x in enumerate(p):
        result[i] += a*x
        result[i+1] += b*x
    return result


def derivative_replay():
    initial = {(3, 1, 0): 1, (4, 1, 0): -1, (4, 2, 1): 1}
    derivative = defaultdict(int)
    for (k, p, n), coefficient in initial.items():
        derivative[k, p+1, n] += (k-p)*coefficient
        derivative[k+1, p+1, n] -= coefficient
    assert dict(derivative) == {(3, 2, 0): 2, (4, 2, 0): -4, (5, 2, 0): 1, (4, 3, 1): 2, (5, 3, 1): -1}
    return [{"kernel": k, "A_denominator_power": p, "norm_power": n, "coefficient": c}
            for (k, p, n), c in sorted(derivative.items())]


def transfer_replay(packet, blocks):
    assert packet["T"] == 25600 and packet["U"] == str(2**72)
    assert not packet["premise_proved"] and not packet["finite_observed_constants_extrapolated"]
    assert not packet["actual_error_bound_improved"]
    hlow = box(blocks["log_half_width"])[0]
    assert 0 < hlow < Q(3, 8)
    far = {}
    for label, shifts in [("H", [5, 6]), ("Q", [6, 7])]:
        p = [Q(1)]
        for _ in range(8):
            p = times(p, 1, 8)
        for end, power in [(3, 8), (4, 7), (6, 1)]:
            for j in range(1, end+1):
                for _ in range(power):
                    p = times(p, j, 1)
        p = times(p, 7, 2)
        for shift in shifts:
            p = times(p, shift, 1)
        integral = sum(c*Q(factorial(j), 24**(j+1)) for j, c in enumerate(p))
        constant = Q(8, 7)**8*Q(544, 31)*integral/3
        row = packet["far_constants"][label]
        assert p == list(map(Q, row["polynomial"])) and integral == Q(row["integral"])
        assert constant == Q(row["constant_upper"])
        far[label] = constant
    totals = defaultdict(lambda: (Q(0), Q(0)))
    previous = packet["T"]
    powers_checked = 0
    for row in packet["blocks"]:
        j, lower, upper = row["index"], row["lower"], row["upper"]
        assert lower == previous and 2**j <= lower < upper == 2**(j+1)
        previous = upper
        block = blocks["blocks"][j]
        bounds = {}
        for label in ["H", "Q"]:
            old = block["kernels"][label]
            coefficients = list(map(box, old["finite_Taylor_coefficients"]))
            polynomial = Q(0)
            for m, (lo, hi) in enumerate(coefficients):
                dl, dh = coefficients[m+1] if m+1 < len(coefficients) else (Q(0), Q(0))
                polynomial += max(abs((m+1)*dl-hi), abs((m+1)*dh-lo))*Q(3, 8)**m
            remainder = (32/hlow+1)*box(old["exponential_remainder_bound"])[1]
            record = row["bounds"][label]
            assert polynomial == Q(record["polynomial_absolute_bound"])
            assert remainder == Q(record["Taylor_derivative_and_value_remainder_upper"])
            total = polynomial+remainder+box(record["analytic_derivative_and_value_error"])[1]
            assert total == Q(record["total_upper"])
            bounds[label] = total
        for term in row["terms"]:
            N, theta = term["norm"], Q(term["theta"])
            p, q = theta.numerator, theta.denominator
            integral = scale(add(radical(Q(N)**(-p)*Q(lower)**(p-q), q),
                                 neg(radical(Q(N)**(-p)*Q(upper)**(p-q), q))), 1/(1-theta))
            overlap(integral, box(term["radial_integral"]))
            envelope = bounds["H"]+N/box(block["A_center"])[0]*bounds["Q"]
            assert envelope == Q(term["derivative_envelope_upper"])
            contribution = scale(integral, envelope)
            overlap(contribution, box(term["contribution"]))
            totals[N, theta] = add(totals[N, theta], contribution)
            powers_checked += 2
    assert previous == 2**72 and len(packet["blocks"]) == 58
    zlo, zhi = box(packet["Z0"])
    assert 0 < zlo <= zhi
    zinv = 1/zhi**4, 1/zlo**4
    results = []
    for family in packet["families"]:
        N = family["norm"]
        boundary = mul(absolute(box(family["signed_count_at_T"])), absolute(box(family["f_at_T"])))
        overlap(boundary, box(family["boundary_absolute"]))
        transfers = []
        for row in family["transfers"]:
            theta = Q(row["theta"])
            p, q = theta.numerator, theta.denominator
            H = scale(radical(Q(N)**(-p)*Q(2**72)**(p-5*q), q), far["H"]/(5-theta))
            K = scale(radical(Q(N)**(-p)*Q(2**72)**(p-6*q), q), N*far["Q"]/(6-theta))
            tail = mul(zinv, add(H, K))
            total = add(totals[N, theta], tail)
            overlap(tail, box(row["far_integral_upper_enclosure"]))
            overlap(total, box(row["J_upper_enclosure"]))
            transfers.append({"theta": str(theta), "J_upper": str(total[1]), "far_part_upper": str(tail[1])})
            powers_checked += 2
        results.append({"norm": N, "boundary_upper": str(boundary[1]), "transfers": transfers})
    return {"blocks": 58, "rational_radicals_checked": powers_checked, "derivative_identity": derivative_replay(),
            "far_polynomial_degrees": {key: len(row["polynomial"])-1 for key, row in packet["far_constants"].items()},
            "conditional_transfers": results, "premise_proved": False}


def interval_count(value):
    count = 0
    if isinstance(value, dict):
        if "lower" in value and "upper" in value:
            endpoints = box(value)
            assert all(x.denominator & (x.denominator-1) == 0 for x in endpoints)
            count += 1
        count += sum(interval_count(v) for v in value.values())
    elif isinstance(value, list):
        count += sum(interval_count(v) for v in value)
    return count


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
        result = json.loads(path.read_text())
        for row in result.get("sources", []):
            bind(row["path"], row["sha256"])
        return result
    prior = read("nelson_completed_majorant_d96.json")
    signed = read("nelson_signed_orbit_blocks_d97.json")
    transfer = read("nelson_signed_tail_transfer_d97.json")
    blocks = read("nelson_completed_scalar_blocks_d96.json")
    enumerations = [read(name) for name in ["nelson_norm_one_d92_T25600.json", "nelson_prime31_b27_d93_T25600.json"]]
    sums = [read(name) for name in ["nelson_norm_one_sum_d92_T25600_exact_d93.json", "nelson_prime31_sum_d93_exact_d93.json"]]
    jobs = []
    for stem, expected in [("nelson_signed_orbit_blocks_d97_attempt01", "pass"),
                           ("nelson_signed_tail_transfer_d97_attempt01", "failed"),
                           ("nelson_signed_tail_transfer_d97_attempt02", "failed"),
                           ("nelson_signed_tail_transfer_d97_attempt03", "pass")]:
        job = read(stem+".job.json")
        bind(job["log"]["path"], job["log"]["sha256"])
        assert job["status"] == expected and job["timeout_seconds"] == 180
        assert job["timeout_terminates_process_group"] and job["wall_seconds"] < 180
        assert job["exit_code"] == (0 if expected == "pass" else 1)
        jobs.append({"path": str((DATA/(stem+".job.json")).relative_to(ROOT)), "status": expected,
                     "wall_seconds": job["wall_seconds"]})
    finite = signed_replay(signed, enumerations, sums)
    analytic = transfer_replay(transfer, blocks)
    count = interval_count(signed)+interval_count(transfer)
    for key, old_key in [("unchanged_omitted_ideal_error_upper", "certified_omitted_S11_error_upper"),
                         ("unchanged_full_S11_error_upper", "certified_full_S11_error_upper"),
                         ("unchanged_full_S11_enclosure", "full_S11_rational_enclosure")]:
        assert signed[key] == prior[old_key]
    for key in ["signed_infinite_tail_bound_proved", "new_quaternion_enumeration", "new_Hecke_data",
                "enumeration_expansion_justified", "CM_anchor_derivative_nonzero"]:
        assert signed[key] is False
    eigenvalue = box(sums[1]["weighted_first_quartic_orbit"][0]["Hecke_eigenvalue"])
    partial = add(tuple(map(Q, finite[0]["cutoffs"][-1]["signed_sum"])),
                  mul(eigenvalue, tuple(map(Q, finite[1]["cutoffs"][-1]["signed_sum"]))))
    old_partial = box(sums[1]["weighted_first_quartic_orbit"][0]["unit_plus_prime_families"]["1"]["partial_sum"]["real"])
    overlap(partial, old_partial)
    error = Q(prior["certified_full_S11_error_upper"])
    enclosure = (partial[0]-error, partial[1]+error)
    assert enclosure[0] < 0 < enclosure[1]
    for path in [Path(__file__), Path(ar.__file__), REPORT]:
        bind(path)
    print("SIGNED_RATIONAL_REPLAY", [(v["label"], v["classes"], v["groups"]) for v in finite], flush=True)
    print("TRANSFER_RATIONAL_REPLAY", analytic["rational_radicals_checked"], "radicals", flush=True)
    return {"status": "pass: signed finite blocks and conditional transfer; actual global accuracy unchanged",
            "prior_source_hashes_verified": len(prior["sources"]), "dyadic_intervals_checked": count,
            "finite_signed_replay": finite, "tail_transfer_replay": analytic,
            "selected_S11_partial_sum": encoded(partial), "actual_full_S11_error_upper": str(error),
            "actual_full_S11_enclosure": encoded(enclosure), "global_kernel_identified_up_to_positive_scalar": True,
            "signed_infinite_tail_bound_proved": False, "CM_anchor_derivative_nonzero": False,
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
    print("PASS|367_nelson_signed_orbit_audit", len(result["sources"]), "hashes", result["dyadic_intervals_checked"], "intervals")


if __name__ == "__main__":
    main()

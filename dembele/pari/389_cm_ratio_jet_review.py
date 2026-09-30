"""D106 independent exact review of the rational-frame comparison packet.

--probe checks candidate arithmetic and prints budgets before the report is frozen.
The ordinary run binds the proof report, source ledger and all prior D105 sources.
--check reconstructs the saved review. No candidate jet is a Shimura evaluation.
"""
import argparse
import ast
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import lcm
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "cm_ratio_jet_review_d106.json"
N = 17


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def checked(items):
    paths = []
    for item in items:
        p = ROOT / item["path"]
        assert source(p)["sha256"] == item["sha256"], str(p)
        paths.append(p)
    return paths


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def mul(a, b, f):
    out = [0]*(2*N-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i+j] += x*y
    for k in range(2*N-2, N-1, -1):
        if out[k]:
            for i in range(N):
                out[k-N+i] -= out[k]*f[i]
    return out[:N]


def modq(c, p=31):
    c = Q(c)
    return c.numerator*pow(c.denominator, -1, p) % p


def rank(a, p=31):
    a = [[x % p for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        inv = pow(a[r][j], -1, p)
        a[r] = [x*inv % p for x in a[r]]
        for i in range(r+1, len(a)):
            c = a[i][j]
            if c:
                a[i] = [(x-c*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def field_checks(f):
    # Rabin's irreducibility criterion: degree 17 is prime.
    def power(a, n):
        out = [1]+[0]*16
        while n:
            if n & 1:
                out = [x % 31 for x in mul(out, a, f)]
            a = [x % 31 for x in mul(a, a, f)]
            n >>= 1
        return out
    def trim(a):
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        return a
    def rem(a, b, p=None):
        a, b = trim(a[:]), trim(b[:])
        while len(a) >= len(b) and any(a):
            c = a[-1]/b[-1] if p is None else a[-1]*pow(b[-1], -1, p) % p
            shift = len(a)-len(b)
            for j, x in enumerate(b):
                a[j+shift] -= c*x
                if p is not None:
                    a[j+shift] %= p
            trim(a)
        return a
    x = [0, 1]+[0]*15
    assert power(x, 31**17) == x
    a, b = [c % 31 for c in f], [(u-v) % 31 for u, v in zip(power(x, 31), x)]
    while any(b):
        a, b = b, rem(a, b, 31)
    assert len(trim(a)) == 1
    # Exact Sturm count, independent of the old floating root labels.
    chain = [list(map(Q, f)), [Q(i*f[i]) for i in range(1, len(f))]]
    while True:
        nxt = [-x for x in rem(chain[-2], chain[-1])]
        if not any(nxt):
            break
        chain.append(nxt)
    def changes(at_negative_infinity):
        signs = [(1 if a[-1] > 0 else -1)*(-1 if at_negative_infinity and (len(a)-1) % 2 else 1) for a in chain]
        return sum(x != y for x, y in zip(signs, signs[1:]))
    left, right = changes(True), changes(False)
    assert left-right == 1 and len(chain[-1]) == 1
    assert sum(abs(c)*4**i for i, c in enumerate(f[:-1])) < 4**17
    return {"mod31_irreducible_by_prime_degree_criterion": True,
            "prime31_inert_unramified_residue_degree": 17,
            "exact_Sturm_variations_at_negative_positive_infinity": [left, right],
            "signature": [1, 8], "strict_root_absolute_bound": 4}


def candidate_packet():
    receipt_path = DATA / "cm_candidate_ratio_jets_d106_attempt01.job.json"
    job = json.loads(receipt_path.read_text())
    assert job["status"] == "pass" and job["timeout_seconds"] == 180
    assert job["wall_seconds"] < 180 and job["timeout_terminates_process_group"]
    paths = checked(job["sources"]+[job["driver"], job["log"]]+job["inputs"])+[receipt_path]
    text = Path(job["log"]["path"]).read_text()
    assert "PASS|D106_CANDIDATE_RATIO_JETS" in text
    markers = list(re.finditer(r"^([A-Z0-9_]+)\|", text, re.M))
    blocks = {m.group(1): text[m.end():(markers[i+1].start() if i+1 < len(markers) else len(text))].strip()
              for i, m in enumerate(markers)}
    jets = []
    for n in range(4):
        numerators = ast.literal_eval(blocks[f"JET{n}_NUMERATORS"])
        denominators = ast.literal_eval(blocks[f"JET{n}_DENOMINATORS"])
        assert len(numerators) == len(denominators) == 16
        assert all(len(row) == 17 for row in numerators+denominators)
        jets.append([[Q(a, b) for a, b in zip(aa, bb)] for aa, bb in zip(numerators, denominators)])
    model_path = DATA / "cm_frame_curve_candidate.json"
    old_path = DATA / "cm_tangent_exactness_d101.json"
    d88_path = DATA / "d88_candidate_cm_jet_rank.json"
    model, old, d88 = [json.loads(p.read_text()) for p in [model_path, old_path, d88_path]]
    paths += [model_path, old_path, d88_path]
    f = list(map(int, model["CM_field_polynomial_ascending"]))
    assert len(f) == 18 and f[-1] == 1
    field = field_checks(f)
    raw = [list(map(Q, row)) for row in model["CM_projective_coordinates_power_basis"]]
    assert all(mul(row, raw[0], f) == target for row, target in zip(jets[0], raw))
    assert jets[1] == [list(map(Q, row)) for row in old["candidate_tangent_power_basis"]]
    zero, one = [Q(0)]*17, [Q(1)]+[Q(0)]*16
    assert jets[0][0] == one
    assert all(jets[n][0] == zero for n in (1, 2, 3))
    assert jets[1][1] == one and jets[2][1] == jets[3][1] == zero
    clearing = [lcm(*(c.denominator for row in a for c in row)) for a in jets]
    integers = [[[int(q*c) for c in row] for row in a] for q, a in zip(clearing, jets)]
    assert all(q % 31 for q in clearing)
    pairs, quadrics = model["monomial_pairs"], model["quadrics"]
    assert len(pairs) == 136 and len(quadrics) == 91
    exact_identities = 0
    for n in range(4):
        denominator = lcm(*(clearing[k]*clearing[n-k] for k in range(n+1)))
        products = []
        for i, j in pairs:
            row = [0]*17
            for k in range(n+1):
                weight = denominator//(clearing[k]*clearing[n-k])
                term = mul(integers[k][i], integers[n-k][j], f)
                row = [a+weight*b for a, b in zip(row, term)]
            products.append(row)
        for q in quadrics:
            assert all(sum(c*z[d] for c, z in zip(q, products)) == 0 for d in range(17))
            exact_identities += 1
    reduced = [[[modq(c) for c in row] for row in a] for a in jets]
    # D88 already normalizes X1=1. Its second jet compares DIRECTLY.
    assert reduced[:3] == d88["candidate_projective_jets_mod31"]
    matrix = []
    for n in range(4):
        products = []
        for i, j in pairs:
            row = [0]*17
            for k in range(n+1):
                term = mul(reduced[k][i], reduced[n-k][j], f)
                row = [(a+b) % 31 for a, b in zip(row, term)]
            products.append(row)
        matrix += [[row[d] for row in products] for d in range(17)]
    ranks = [rank(matrix[:17*n]) for n in range(1, 5)]
    assert ranks == [17, 34, 45, 45] and rank(quadrics) == 91
    # Perturbing the third coefficient of r3 by 1 changes a nonzero linearization.
    gradient = []
    for q in quadrics:
        row = [0]*17
        for c, (i, j) in zip(q, pairs):
            if i == 2:
                row = [(a+c*b) % 31 for a, b in zip(row, reduced[0][j])]
            if j == 2:
                row = [(a+c*b) % 31 for a, b in zip(row, reduced[0][i])]
        gradient.append(row)
    assert any(any(row) for row in gradient)
    # An erroneous extra raw-X1 factor at second order is detected.
    raw1mod = list(map(modq, raw[0]))
    wrong = [[x % 31 for x in mul(raw1mod, row, f)] for row in reduced[2]]
    assert wrong != reduced[2]
    prior = module("d105_logs", ROOT / "dembele/pari/386_cm_frame_arithmetic_review.py")
    log2, log10, log31 = (prior.log_bounds(p) for p in (2, 10, 31))
    heights, budgets = [], []
    for n, target in zip((1, 2, 3), (10504, 31518, 52533)):
        bound = max([clearing[n]]+[sum(abs(c)*4**i for i, c in enumerate(row)) for row in integers[n]])
        bits = bound.bit_length()
        reference = (bits*log2[1]).__floor__()+1
        difference = Q(target+reference)+Q(7, 10)
        real = (17*difference/log10[0]).__floor__()+1
        nonreal = (17*difference/(2*log10[0])).__floor__()+1
        all_embeddings = (difference/log10[0]).__floor__()+1
        padic = (difference/log31[0]).__floor__()+1
        assert real*log10[0] > 17*difference
        assert 2*nonreal*log10[0] > 17*difference
        assert all_embeddings*log10[0] > difference
        assert padic*log31[0] > difference
        heights.append({"order": n, "common_clearing_integer": str(clearing[n]),
                        "clearing_integer_decimal_digits": len(str(clearing[n])),
                        "strict_power_two_bound_exponent": bits,
                        "candidate_projective_Taylor_height_upper": reference})
        budgets.append({"order": n, "actual_height_upper": target,
                        "candidate_height_upper": reference, "difference_height_upper": str(difference),
                        "one_real_embedding_decimal_error_exponent": real,
                        "one_nonreal_embedding_with_conjugate_decimal_error_exponent": nonreal,
                        "all_17_embeddings_decimal_error_exponent": all_embeddings,
                        "inert_prime31_valuation_sufficient": padic})
    assert heights[0]["candidate_projective_Taylor_height_upper"] == 677
    assert budgets[0]["inert_prime31_valuation_sufficient"] == 3257
    packet = {"candidate_ratio_Taylor_coefficients_orders_0_through_3": [[[str(c) for c in row] for row in a] for a in jets],
              "parameter": "t=X2/X1-(X2/X1)(P); X1=1",
              "field": field, "exact_quadratic_coefficient_identities_checked": exact_identities,
              "D101_first_coefficient_matches_exactly": True, "D88_first_three_coefficients_match_directly_mod31": True,
              "incorrect_extra_raw_X1_factor_in_D88_comparison_rejected": True,
              "altered_third_coefficient_rejected": True, "jet_matrix_ranks_mod31": ranks,
              "candidate_only_height_bounds": heights, "sufficient_equality_budgets": budgets,
              "arithmetic_field_degree": 17, "common_31adic_precision_sufficient_for_J3": max(b["inert_prime31_valuation_sufficient"] for b in budgets[:2]),
              "common_31adic_precision_sufficient_for_J4": max(b["inert_prime31_valuation_sufficient"] for b in budgets),
              "bounds_are_sufficient_not_minimal": True, "actual_errors_certified": False,
              "actual_common_G12_chart_certified": False}
    return packet, paths


def build():
    packet, paths = candidate_packet()
    prior_path = DATA / "cm_frame_arithmetic_review_d105.json"
    prior = json.loads(prior_path.read_text())
    paths += checked(prior["sources"])+[prior_path]
    assert len(prior["sources"]) == 543
    main_path = ROOT / "dembele/pari/387_cm_rational_frame.py"
    main = module("rational_frame_main", main_path)
    main_result_path = DATA / "cm_rational_frame_d106.json"
    main_result = json.loads(main_result_path.read_text())
    assert main.build() == main_result
    paths += checked(main_result["sources"])+[main_path, main_result_path]
    main_receipt = DATA / "cm_rational_frame_d106_attempt02.job.json"
    job = json.loads(main_receipt.read_text())
    assert job["status"] == "pass" and job["timeout_seconds"] == 180
    assert job["wall_seconds"] < 180 and job["timeout_terminates_process_group"]
    paths += checked(job["sources"]+[job["driver"], job["log"]])+[main_receipt]
    failed_receipt = DATA / "cm_rational_frame_d106_attempt01.job.json"
    failed = json.loads(failed_receipt.read_text())
    snapshot = DATA / "cm_rational_frame_d106_attempt01_failed.py"
    assert failed["status"] == "failed"
    assert source(snapshot)["sha256"] == failed["driver"]["sha256"]
    paths += checked(failed["sources"]+[failed["log"]])+[failed_receipt, snapshot, DATA / "cm_rational_frame_d106_failure.json"]
    descent_path = DATA / "marked_descent.json"
    descent = json.loads(descent_path.read_text())
    paths += checked([descent["script_source"], descent["arithmetic_helper_source"]])+[descent_path]
    paths += [Path(__file__), ROOT / "dembele/certificates/marked-descent.md",
              ROOT / "dembele/certificates/cm-rational-frame-jets-d106.md",
              DATA / "cm_rational_frame_sources_d106.json",
              ROOT / "dembele/certificates/d88-cm-expansion-identification-review.md"]
    probe_receipt = DATA / "cm_ratio_jet_review_d106_probe_attempt01.job.json"
    if probe_receipt.exists():
        probe = json.loads(probe_receipt.read_text())
        assert probe["status"] == "pass"
        paths += checked(probe["sources"]+[probe["driver"], probe["log"]])+[probe_receipt]
    return {"status": "pass", "milestone": "D106", "finite_geometric_inputs": main_result,
            "candidate_comparison_packet": packet, "D105_source_hashes_checked_unchanged": 543,
            "sources": [source(p) for p in sorted(set(p.resolve() for p in paths))],
            "marked_geometric_automorphism_group_trivial_via_companion_proof": True,
            "compatible_Q_descent_of_given_F_marked_curve_via_companion_proof": True,
            "rational_CM_frame_unique_up_to_common_scalar_via_companion_proof": True,
            "D56_ordinary_point_and_moment_hypotheses_used": False,
            "saved_numeric_CM_point_root_matching_certified": False,
            "independent_Shimura_tangent_or_higher_jet_evaluated": False,
            "candidate_curve_identification_proved": False, "target_field_polynomial_constructed": False,
            "scope": "Exact finite arithmetic, candidate-only jets and preserved sources. The cited geometric/descent theorems and companion proof are not machine-verified."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--probe", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.probe:
        packet, _ = candidate_packet()
        print(json.dumps({"candidate_height_bounds": packet["candidate_only_height_bounds"],
                          "sufficient_budgets": packet["sufficient_equality_budgets"],
                          "ranks_mod31": packet["jet_matrix_ranks_mod31"]}, indent=2), flush=True)
        print("PASS|D106_CM_RATIO_JET_PROBE", flush=True)
        return
    if args.check:
        old = json.loads(OUT.read_text())
        checked(old["sources"])
    result = build()
    if args.check:
        assert result == old
    else:
        assert not OUT.exists(), "Preserve completed reviews."
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    packet = result["candidate_comparison_packet"]
    print(json.dumps({"status": "pass", "source_hashes": len(result["sources"]),
                      "previous_hashes_unchanged": 543, "quadric_coefficient_checks": 364,
                      "J3_sufficient_prime31_precision": packet["common_31adic_precision_sufficient_for_J3"],
                      "J4_sufficient_prime31_precision": packet["common_31adic_precision_sufficient_for_J4"]}), flush=True)
    print("PASS|D106_CM_RATIO_JET_REVIEW", flush=True)


if __name__ == "__main__":
    main()


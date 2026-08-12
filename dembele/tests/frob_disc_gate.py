#!/usr/bin/env python3
"""Discriminant / Hunter-volume gate for Frobenius reconstruction of the deg-257 field."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path


DEMBELE_ROOT = Path(__file__).resolve().parents[1]
CONSTITUENTS_PATH = DEMBELE_ROOT / "data" / "computed" / "constituents.json"
OUTPUT_PATH = DEMBELE_ROOT / "data" / "computed" / "frob_disc_gate.json"

Q = 256
P1_SIZE = Q + 1  # 257
KILL_VOLUME = 10**12
MODULI = {
    "q1": (1 << 8) | (1 << 4) | (1 << 3) | (1 << 1) | 1,
    "q2": (1 << 8) | (1 << 6) | (1 << 5) | (1 << 2) | 1,
}


def field_multiply(left: int, right: int, modulus: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & (1 << 8):
            left ^= modulus
    return result


def mobius_companion(
    trace: int, point: int | None, modulus: int
) -> int | None:
    """Apply the SL2 companion matrix [[0,1],[1,trace]] to a point of P^1.

    Points are affine elements of F_256, or None for infinity. In characteristic 2
    the companion used by the Magma residual encoding has determinant 1 and sends
    z |-> 1/(z+trace), with infinity <-> trace.
    """
    if point is None:
        return 0
    denominator = point ^ trace
    if denominator == 0:
        return None
    # a^{255}=1 for a≠0, so inverse is a^{254}
    inverse = 1
    base = denominator
    exponent = 254
    while exponent:
        if exponent & 1:
            inverse = field_multiply(inverse, base, modulus)
        base = field_multiply(base, base, modulus)
        exponent >>= 1
    return inverse


def cycle_type_on_p1(trace: int, modulus: int) -> dict[str, object]:
    remaining = {None, *range(Q)}
    lengths: list[int] = []
    while remaining:
        start = remaining.pop()
        length = 1
        point = mobius_companion(trace, start, modulus)
        while point != start:
            remaining.remove(point)
            point = mobius_companion(trace, point, modulus)
            length += 1
        lengths.append(length)
    lengths.sort()
    counts = Counter(lengths)
    partition = [[length, counts[length]] for length in sorted(counts)]
    return {
        "degree_partition": partition,
        "number_of_cycles": len(lengths),
        "fixed_points": counts.get(1, 0),
        "as_factorization_type": " * ".join(
            f"{length}^{counts[length]}" for length in sorted(counts)
        ),
    }


def classify_order(order: int) -> str:
    if order == P1_SIZE:
        return "nonsplit_singer"
    if order == Q - 1:
        return "split_maximal"
    if (Q - 1) % order == 0:
        return "split_torus"
    if P1_SIZE % order == 0:
        return "nonsplit_torus"
    return "unknown"


def expected_partition(order: int) -> list[list[int]]:
    """Group-theoretic cycle type on P^1(F_q) for an element of given order in SL2."""
    if order == 1:
        return [[1, P1_SIZE]]
    if order == P1_SIZE:
        return [[P1_SIZE, 1]]
    if (Q - 1) % order == 0:
        # split torus: 2 fixed points, (q-1)/ord cycles of length ord
        return [[1, 2], [order, (Q - 1) // order]]
    if P1_SIZE % order == 0:
        return [[order, P1_SIZE // order]]
    raise ValueError(f"order {order} does not divide q-1 or q+1")


def log10_binom(n: int, k: int) -> float:
    return (
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    ) / math.log(10)


def hunter_volume_log10(degree: int, conjugate_bound: float) -> dict[str, object]:
    """log10 of the axis-aligned Hunter coefficient box for a monic degree-n polynomial.

    If every conjugate satisfies |α| ≤ M, then |a_k| ≤ C(n,k) M^k, so each coefficient
    has at most 2*floor(bound)+1 integer choices.
    """
    log_volume = 0.0
    dominant_k = 0
    dominant_log_choices = 0.0
    coefficient_logs: list[float] = []
    for k in range(1, degree + 1):
        log_bound = log10_binom(degree, k) + k * math.log10(conjugate_bound)
        # number of integers in [-B,B] is ≤ 2*10^{log_bound} + 1
        # use log10(2) + log_bound as a tight upper estimate when B ≥ 1
        log_choices = math.log10(2) + log_bound
        coefficient_logs.append(log_choices)
        log_volume += log_choices
        if log_choices > dominant_log_choices:
            dominant_log_choices = log_choices
            dominant_k = k
    return {
        "degree": degree,
        "conjugate_bound_M": conjugate_bound,
        "log10_coefficient_box_volume": log_volume,
        "dominant_coefficient_index": dominant_k,
        "log10_dominant_coefficient_choices": dominant_log_choices,
        "middle_coefficient_index": degree // 2,
        "log10_middle_coefficient_choices": coefficient_logs[degree // 2 - 1],
    }


def chebotarev_filter_log10_savings(group_order: int) -> float:
    """Crude upper bound on search-space reduction from one Chebotarev condition."""
    return math.log10(group_order)


def build_report(constituents: dict) -> dict:
    normalization = constituents["normalization"]
    f_component = normalization["f_component"]
    modulus = MODULI[f_component]
    traces_out: dict[str, dict[str, dict]] = {}
    for prime, orbit in constituents["traces"].items():
        traces_out[prime] = {}
        for index, components in orbit.items():
            entry = components[f_component]
            trace = entry["polynomial_mask"]
            order = entry["frobenius_order"]
            computed = cycle_type_on_p1(trace, modulus)
            expected = expected_partition(order)
            traces_out[prime][index] = {
                "component": f_component,
                "field_modulus_mask": modulus,
                "trace_mask": trace,
                "frobenius_order": order,
                "sl2_class": classify_order(order),
                "p1_cycle_type": computed,
                "matches_group_theoretic_partition": computed["degree_partition"]
                == expected,
                "expected_degree_partition": expected,
            }

    # |PSL2(F_256)| = |SL2(F_256)| in char 2 = q(q-1)(q+1)
    psl2_order = Q * (Q - 1) * (Q + 1)

    # Optimistic absolute Hunter box for a degree-257 polynomial over Z
    # (even more optimistic than working over Z[sqrt(2)]).
    optimistic = hunter_volume_log10(P1_SIZE, conjugate_bound=2.0)
    # Still more optimistic: M=1 (all conjugates on the unit circle / integers 0,±1)
    extreme = hunter_volume_log10(P1_SIZE, conjugate_bound=1.0)

    # Two primes (31 and 97) each save at most log10(|G|) in a Chebotarev filter
    filter_savings = 2 * chebotarev_filter_log10_savings(psl2_order)
    filtered_log_volume = optimistic["log10_coefficient_box_volume"] - filter_savings

    # Relative formulation over Q(sqrt(2)): same degree, same binomial blow-up
    relative = hunter_volume_log10(P1_SIZE, conjugate_bound=2.0)

    disc_notes = {
        "base_of_target_field": "Q(sqrt(2))",
        "target_degree": P1_SIZE,
        "galois_closure_image": "PSL2(F_256) semidirect C_4 (abstract model)",
        "ramification": "only above 2",
        "artin_conductor_upper_bound": None,
        "artin_conductor_status": (
            "No small explicit conductor exponent for the projective residual "
            "representation is available from the present data; the Hunter gate "
            "is decided by coefficient-box volume under optimistic conjugate bounds, "
            "which already exceeds the kill threshold without needing a disc upper bound."
        ),
        "disc_Q_sqrt2_shape": "power of the unique prime above 2",
    }

    killed_by_volume = filtered_log_volume > math.log10(KILL_VOLUME)
    killed_by_missing_disc_bound = disc_notes["artin_conductor_upper_bound"] is None

    verdict = {
        "pure_frobenius_hunter_reconstruction_feasible": False,
        "kill_volume_threshold": KILL_VOLUME,
        "killed_by_hunter_volume": killed_by_volume,
        "killed_by_missing_2_power_disc_upper_bound": killed_by_missing_disc_bound,
        "filtered_log10_volume_optimistic_M2": filtered_log_volume,
        "summary": (
            "DEAD: even with conjugate bound M=2 and two maximal Chebotarev filters, "
            "the monic degree-257 Hunter box has log10(volume) "
            f"≈ {filtered_log_volume:.1f} ≫ 12."
        ),
    }

    return {
        "schema_version": 1,
        "source": {
            "constituents": "dembele/data/computed/constituents.json",
            "scorecard": "dembele/certificates/torsion-construction-scorecard.md",
            "script": "dembele/tests/frob_disc_gate.py",
        },
        "finite_field": {
            "q": Q,
            "p1_size": P1_SIZE,
            "psl2_order": psl2_order,
            "char_2_sl2_equals_psl2": True,
        },
        "frobenius_cycle_types": traces_out,
        "discriminant": disc_notes,
        "hunter_estimates": {
            "optimistic_absolute_M2": optimistic,
            "extreme_absolute_M1": extreme,
            "relative_over_Q_sqrt2_M2": relative,
            "chebotarev_log10_savings_two_primes_upper_bound": filter_savings,
            "filtered_optimistic_log10_volume": filtered_log_volume,
        },
        "verdict": verdict,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        type=Path,
        default=OUTPUT_PATH,
        help="output JSON path",
    )
    args = parser.parse_args()
    constituents = json.loads(CONSTITUENTS_PATH.read_text())
    report = build_report(constituents)

    # Sanity: every computed cycle type matches the group-theoretic partition
    for prime_data in report["frobenius_cycle_types"].values():
        for entry in prime_data.values():
            if not entry["matches_group_theoretic_partition"]:
                raise SystemExit(
                    f"cycle type mismatch at order {entry['frobenius_order']}"
                )

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(rendered)
    print(rendered, end="")
    print("PASS|dembele_frob_disc_gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

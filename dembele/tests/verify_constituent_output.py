#!/usr/bin/env python3
"""Aggregate parallel Magma lanes and match Dembélé's two trace tables."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEMBELE_ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_PATH = DEMBELE_ROOT / "data" / "published" / "dembele_2009.json"
TRACE_PATTERN = re.compile(
    r"^TRACE\|(31|97)\|([1-8])\|(q1|q2)\|([^|]+)\|(51|255|257)$"
)
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


def field_power(base: int, exponent: int, modulus: int) -> int:
    result = 1
    while exponent:
        if exponent & 1:
            result = field_multiply(result, base, modulus)
        base = field_multiply(base, base, modulus)
        exponent >>= 1
    return result


def evaluate_polynomial(polynomial: int, value: int, modulus: int) -> int:
    result = 0
    for exponent in range(polynomial.bit_length() - 1, -1, -1):
        result = field_multiply(result, value, modulus)
        if polynomial & (1 << exponent):
            result ^= 1
    return result


def parse_polynomial(text: str) -> int:
    text = text.strip()
    if text == "0":
        return 0
    result = 0
    for term in text.split(" + "):
        if term == "1":
            exponent = 0
        elif term == "t":
            exponent = 1
        elif term.startswith("t^"):
            exponent = int(term[2:])
        else:
            raise ValueError(f"unsupported GF(2) polynomial term: {term!r}")
        result |= 1 << exponent
    if result >= 1 << 8:
        raise ValueError(f"trace polynomial has degree at least 8: {text!r}")
    return result


def primitive_elements(modulus: int) -> list[int]:
    result = []
    for element in range(2, 1 << 8):
        if all(
            field_power(element, 255 // prime, modulus) != 1
            for prime in (3, 5, 17)
        ):
            result.append(element)
    return result


def parse_logs(paths: list[Path]) -> tuple[dict, set[int]]:
    traces: dict[tuple[str, int, str], dict[str, int]] = {}
    passed_lanes: set[int] = set()
    for path in paths:
        for line in path.read_text().splitlines():
            match = TRACE_PATTERN.fullmatch(line.strip())
            if match:
                prime, index, component, polynomial, order = match.groups()
                key = (prime, int(index), component)
                if key in traces:
                    raise ValueError(f"duplicate trace result: {key}")
                traces[key] = {
                    "polynomial_mask": parse_polynomial(polynomial),
                    "frobenius_order": int(order),
                }
            if line.startswith("PASS|constituent_orbit|"):
                passed_lanes.add(int(line.rsplit("|", 1)[1]))
    return traces, passed_lanes


def map_q1_to_q2(element: int, generator_image: int) -> int:
    return evaluate_polynomial(element, generator_image, MODULI["q2"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", type=Path, nargs="+")
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()

    published = json.loads(PUBLISHED_PATH.read_text())
    traces, passed_lanes = parse_logs(args.logs)
    expected_keys = {
        (prime, index, component)
        for prime in ("31", "97")
        for index in range(1, 9)
        for component in ("q1", "q2")
    }
    if set(traces) != expected_keys:
        missing = sorted(expected_keys - set(traces))
        extra = sorted(set(traces) - expected_keys)
        raise SystemExit(f"incomplete trace data; missing={missing}, extra={extra}")
    if passed_lanes != set(range(1, 9)):
        raise SystemExit(f"incomplete PASS markers: {sorted(passed_lanes)}")

    q1_roots_in_q2 = [
        element
        for element in range(1 << 8)
        if evaluate_polynomial(MODULI["q1"], element, MODULI["q2"]) == 0
    ]
    if len(q1_roots_in_q2) != 8:
        raise SystemExit("failed to enumerate the eight q1 roots in the q2 model")

    normalizations = []
    for generator_image in q1_roots_in_q2:
        common_values = {
            ("q1", prime, index): map_q1_to_q2(
                traces[(prime, index, "q1")]["polynomial_mask"],
                generator_image,
            )
            for prime in ("31", "97")
            for index in range(1, 9)
        }
        common_values.update(
            {
                ("q2", prime, index): traces[(prime, index, "q2")][
                    "polynomial_mask"
                ]
                for prime in ("31", "97")
                for index in range(1, 9)
            }
        )

        for f_component, f_prime_component in (("q1", "q2"), ("q2", "q1")):
            for alpha in primitive_elements(MODULI["q2"]):
                matches = True
                for prime in ("31", "97"):
                    table = published["table_1"][prime]
                    for index in range(1, 9):
                        if common_values[(f_component, prime, index)] != field_power(
                            alpha,
                            table["f_trace_exponents"][index - 1],
                            MODULI["q2"],
                        ):
                            matches = False
                            break
                        if common_values[
                            (f_prime_component, prime, index)
                        ] != field_power(
                            alpha,
                            table["f_prime_trace_exponents"][index - 1],
                            MODULI["q2"],
                        ):
                            matches = False
                            break
                    if not matches:
                        break
                if matches:
                    normalizations.append(
                        {
                            "q1_generator_image_in_q2": generator_image,
                            "paper_alpha_in_q2": alpha,
                            "f_component": f_component,
                            "f_prime_component": f_prime_component,
                        }
                    )

    if not normalizations:
        raise SystemExit("no common GF(256) normalization matches Dembélé's tables")

    chosen = normalizations[0]
    generator_image = chosen["q1_generator_image_in_q2"]
    common_values = {}
    for component in ("q1", "q2"):
        for prime in ("31", "97"):
            for index in range(1, 9):
                raw = traces[(prime, index, component)]["polynomial_mask"]
                common_values[(component, prime, index)] = (
                    map_q1_to_q2(raw, generator_image)
                    if component == "q1"
                    else raw
                )

    for component in ("q1", "q2"):
        for prime in ("31", "97"):
            values = [
                common_values[(component, prime, index)]
                for index in range(1, 9)
            ]
            for index, value in enumerate(values):
                if values[(index + 2) % 8] != field_power(
                    value, 4, MODULI["q2"]
                ):
                    raise SystemExit(
                        f"sigma^2/Frobenius relation failed for {component}, {prime}"
                    )

    f_component = chosen["f_component"]
    f_prime_component = chosen["f_prime_component"]
    sigma_shifts = []
    for shift in (-1, 1):
        if all(
            common_values[(f_component, prime, ((index + shift - 1) % 8) + 1)]
            == common_values[(f_prime_component, prime, index)]
            for prime in ("31", "97")
            for index in range(1, 9)
        ):
            sigma_shifts.append(shift)

    for prime in ("31", "97"):
        table = published["table_1"][prime]
        for index in range(1, 9):
            self_order = traces[(prime, index, f_component)]["frobenius_order"]
            prime_order = traces[
                (prime, index, f_prime_component)
            ]["frobenius_order"]
            if self_order != table["f_frobenius_orders"][index - 1]:
                raise SystemExit(f"f order mismatch at {prime}^{index}")
            if prime_order != table["f_prime_frobenius_orders"][index - 1]:
                raise SystemExit(f"f_prime order mismatch at {prime}^{index}")

    output = {
        "schema_version": 1,
        "source_script": "dembele/magma/12_constituent_orbit_job.m",
        "field_models": {
            "q1_polynomial_mask": MODULI["q1"],
            "q2_polynomial_mask": MODULI["q2"],
        },
        "normalization": chosen,
        "equivalent_normalization_count": len(normalizations),
        "sigma_squared_matches_fourth_power": True,
        "sigma_index_shifts_matching_f_to_f_prime": sigma_shifts,
        "traces": {
            prime: {
                str(index): {
                    component: traces[(prime, index, component)]
                    for component in ("q1", "q2")
                }
                for index in range(1, 9)
            }
            for prime in ("31", "97")
        },
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(rendered)
    print(rendered, end="")
    print("PASS|dembele_constituent_tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

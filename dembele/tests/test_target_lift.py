#!/usr/bin/env python3
"""Consistency checks for the characteristic-zero lift certificate."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "computed"
    / "target_lift_field.json"
)
STRUCTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "computed"
    / "lift_field_structure.json"
)


def multiply_mod_2(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, left_coefficient in enumerate(left):
        for j, right_coefficient in enumerate(right):
            result[i + j] ^= left_coefficient & right_coefficient
    return result


class TargetLiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(DATA_PATH.read_text())
        cls.structure = json.loads(STRUCTURE_PATH.read_text())

    def test_field_degree_and_order(self) -> None:
        self.assertEqual(self.data["target_component_dimension"], 16)
        self.assertEqual(self.data["hecke_field"]["degree"], 16)
        self.assertEqual(
            len(
                self.data["hecke_field"][
                    "defining_polynomial_coefficients_high_to_low"
                ]
            ),
            17,
        )
        self.assertEqual(
            self.data["order_at_2"][
                "equation_order_to_2_maximal_order_index"
            ],
            1,
        )

    def test_mod_2_factorization(self) -> None:
        q1_low_to_high = [1, 1, 0, 1, 1, 0, 0, 0, 1]
        q2_low_to_high = [1, 0, 1, 0, 0, 1, 1, 0, 1]
        product_high_to_low = list(
            reversed(multiply_mod_2(q1_low_to_high, q2_low_to_high))
        )
        self.assertEqual(
            product_high_to_low,
            self.data["defining_polynomial_mod_2"]["coefficients_high_to_low"],
        )

    def test_two_prime_decomposition(self) -> None:
        primes = self.data["primes_above_2"]
        self.assertEqual(len(primes), 2)
        self.assertEqual(
            sum(
                prime["ramification_index"] * prime["residue_degree"]
                for prime in primes
            ),
            16,
        )
        for prime in primes:
            self.assertEqual(prime["ramification_index"], 1)
            self.assertEqual(prime["residue_degree"], 8)
            self.assertEqual(prime["norm"], 256)

    def test_field_structure_and_dimension_obstruction(self) -> None:
        field = self.structure["field"]
        self.assertEqual(field["degree"], 16)
        self.assertEqual(field["signature"], [16, 0])
        self.assertEqual(field["automorphism_group"], "C8")
        self.assertFalse(field["is_galois_over_Q"])
        self.assertEqual(
            field["discriminant_factorization"],
            {"5": 14, "89": 7, "661": 4},
        )
        self.assertEqual(
            [item["degree"] for item in self.structure["unique_embedded_subfields"]],
            [2, 4, 8],
        )
        tests = self.structure["dimension_reduction_tests"]
        self.assertEqual(tests["quadratic_inner_twist"], "excluded")
        self.assertEqual(tests["proper_base_change"], "excluded")
        self.assertEqual(tests["expected_abelian_variety_dimension"], 16)


if __name__ == "__main__":
    unittest.main()

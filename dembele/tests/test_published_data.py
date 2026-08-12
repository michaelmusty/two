#!/usr/bin/env python3
"""Internal consistency checks for the transcription of Dembélé's Table 1."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


DEMBELE_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = DEMBELE_ROOT / "data" / "published" / "dembele_2009.json"
LOCK_PATH = DEMBELE_ROOT / "upstream.lock"


class PublishedDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(DATA_PATH.read_text())
        cls.lock = json.loads(LOCK_PATH.read_text())

    def test_base_field(self) -> None:
        field = self.data["base_field"]
        coefficients = field["minimal_polynomial_coefficients_high_to_low"]
        self.assertEqual(coefficients, [1, 0, -8, 0, 20, 0, -16, 0, 2])
        self.assertEqual(len(field["integral_basis"]), 8)
        self.assertEqual(field["galois_group_order"], 8)
        self.assertEqual(field["discriminant"], "2^31")

    def test_space_dimensions(self) -> None:
        space = self.data["space"]
        self.assertEqual(
            space["zero_primary_dimension"]
            + sum(space["nonzero_irreducible_constituent_dimensions"]),
            space["dimension_over_F2"],
        )
        self.assertEqual(space["dimension_over_F2"], 57)

    def test_prime_orbit_generators(self) -> None:
        for rational_prime in ("31", "97"):
            coordinates = self.data["prime_orbits"][rational_prime][
                "generator_power_basis_coordinates"
            ]
            self.assertEqual(len(coordinates), 8)

    def test_table_rows_are_complete(self) -> None:
        for rational_prime in ("31", "97"):
            table = self.data["table_1"][rational_prime]
            for key, row in table.items():
                self.assertEqual(len(row), 8, f"{rational_prime}: {key}")

    def test_f_prime_rows_are_right_shifts(self) -> None:
        for rational_prime in ("31", "97"):
            table = self.data["table_1"][rational_prime]
            for kind in ("trace_exponents", "frobenius_orders"):
                f_row = table[f"f_{kind}"]
                f_prime_row = table[f"f_prime_{kind}"]
                self.assertEqual(f_prime_row, [f_row[-1], *f_row[:-1]])

    def test_finite_field_exponents_and_orders(self) -> None:
        multiplicative_order = self.data["finite_field"][
            "multiplicative_group_order"
        ]
        allowed_matrix_orders = {51, 255, 257}
        for table in self.data["table_1"].values():
            for key, row in table.items():
                if key.endswith("trace_exponents"):
                    self.assertTrue(all(0 < exponent < multiplicative_order for exponent in row))
                elif key.endswith("frobenius_orders"):
                    self.assertTrue(set(row) <= allowed_matrix_orders)

    def test_target_group_degree(self) -> None:
        target = self.data["target_extension"]
        q = self.data["finite_field"]["size"]
        sl2_order = q * (q**2 - 1)
        self.assertEqual(sl2_order, target["sl2_order"])
        self.assertEqual(8 * sl2_order**2, target["degree_over_Q"])
        self.assertEqual(target["degree_over_Q"], 2251731094732800)

    def test_upstream_pin(self) -> None:
        package = self.lock["hilbertmodularforms"]
        self.assertEqual(
            package["commit"],
            "f5ce65826697ee1ba7ed6e77a3fda0ef779f633b",
        )
        self.assertEqual(self.lock["magma"]["version"], "V2.29-8")


if __name__ == "__main__":
    unittest.main()

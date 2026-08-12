#!/usr/bin/env python3
"""Tests for the small GF(256) verifier used on parallel Magma outputs."""

from __future__ import annotations

import unittest

from verify_constituent_output import (
    MODULI,
    evaluate_polynomial,
    field_multiply,
    field_power,
    primitive_elements,
)


class FiniteFieldTests(unittest.TestCase):
    def test_multiplicative_group(self) -> None:
        for modulus in MODULI.values():
            self.assertEqual(len(primitive_elements(modulus)), 128)
            for element in range(1, 1 << 8):
                self.assertEqual(field_power(element, 255, modulus), 1)
                self.assertEqual(field_multiply(element, 1, modulus), element)

    def test_q1_has_eight_roots_in_q2(self) -> None:
        roots = [
            element
            for element in range(1 << 8)
            if evaluate_polynomial(MODULI["q1"], element, MODULI["q2"]) == 0
        ]
        self.assertEqual(len(roots), 8)


if __name__ == "__main__":
    unittest.main()

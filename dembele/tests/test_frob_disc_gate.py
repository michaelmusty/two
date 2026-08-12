#!/usr/bin/env python3
"""Tests for the Frobenius discriminant / Hunter-volume gate."""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

from frob_disc_gate import (
    KILL_VOLUME,
    P1_SIZE,
    build_report,
    cycle_type_on_p1,
    expected_partition,
    hunter_volume_log10,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/computed/frob_disc_gate.json").read_text())
CONSTITUENTS = json.loads((ROOT / "data/computed/constituents.json").read_text())


class FrobDiscGateTests(unittest.TestCase):
    def test_cycle_types_match_group_theory(self) -> None:
        for prime_data in DATA["frobenius_cycle_types"].values():
            for entry in prime_data.values():
                self.assertTrue(entry["matches_group_theoretic_partition"])
                self.assertEqual(
                    entry["p1_cycle_type"]["degree_partition"],
                    expected_partition(entry["frobenius_order"]),
                )

    def test_observed_factorization_types(self) -> None:
        types = {
            entry["p1_cycle_type"]["as_factorization_type"]
            for prime_data in DATA["frobenius_cycle_types"].values()
            for entry in prime_data.values()
        }
        self.assertEqual(types, {"257^1", "1^2 * 255^1", "1^2 * 51^5"})

    def test_singer_cycle_direct(self) -> None:
        modulus = DATA["frobenius_cycle_types"]["31"]["1"]["field_modulus_mask"]
        trace = DATA["frobenius_cycle_types"]["31"]["1"]["trace_mask"]
        computed = cycle_type_on_p1(trace, modulus)
        self.assertEqual(computed["degree_partition"], [[P1_SIZE, 1]])

    def test_hunter_volume_kills(self) -> None:
        estimates = DATA["hunter_estimates"]
        self.assertGreater(
            estimates["filtered_optimistic_log10_volume"],
            math.log10(KILL_VOLUME),
        )
        self.assertGreater(
            estimates["optimistic_absolute_M2"]["log10_middle_coefficient_choices"],
            100,
        )
        self.assertFalse(
            DATA["verdict"]["pure_frobenius_hunter_reconstruction_feasible"]
        )
        self.assertTrue(DATA["verdict"]["killed_by_hunter_volume"])

    def test_rebuild_matches_artifact(self) -> None:
        rebuilt = build_report(CONSTITUENTS)
        self.assertEqual(
            rebuilt["verdict"]["pure_frobenius_hunter_reconstruction_feasible"],
            False,
        )
        self.assertGreater(
            rebuilt["hunter_estimates"]["filtered_optimistic_log10_volume"],
            math.log10(KILL_VOLUME),
        )
        # Extreme M=1 box is still absurd
        extreme = hunter_volume_log10(P1_SIZE, 1.0)
        self.assertGreater(extreme["log10_coefficient_box_volume"], 1000)


if __name__ == "__main__":
    unittest.main()

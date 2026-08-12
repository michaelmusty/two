#!/usr/bin/env python3
"""Tests for the constructive-idea exhaustion checklist."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/computed/idea_exhaustion.json").read_text())


class IdeaExhaustionTests(unittest.TestCase):
    def test_overall_verdict(self) -> None:
        self.assertFalse(
            DATA["verdict"]["explicit_polynomial_reachable_with_current_ideas"]
        )

    def test_core_routes_marked_dead(self) -> None:
        ideas = DATA["ideas"]
        for key in (
            "twisted_L_oda_periods",
            "greenberg_voight_shimura_periods",
            "dense_frobenius_hunter",
            "sparse_trinomial_x_n_ax_b",
            "csv_pipeline_without_new_frontend",
            "omega_plus_plus_RM_recovers_signs",
            "classical_mod2_level_2power",
        ):
            self.assertIn("dead", ideas[key]["verdict"])

    def test_sparse_local_obstruction_recorded(self) -> None:
        self.assertIn("0/930", DATA["ideas"]["sparse_trinomial_x_n_ax_b"]["evidence"])


if __name__ == "__main__":
    unittest.main()

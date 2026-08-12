import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads(
    (ROOT / "data/computed/period_feasibility.json").read_text()
)


class PeriodFeasibilityTests(unittest.TestCase):
    def test_base_discriminant(self):
        field = DATA["base_field"]
        self.assertEqual(field["degree"], 8)
        self.assertEqual(int(field["discriminant"]), 2**31)

    def test_required_single_negative_conductors(self):
        conductors = DATA["required_signs"][
            "minimum_quadratic_character_conductor_norms"
        ]
        self.assertEqual(conductors, [1] + [991] * 8)

    def test_coefficient_bounds_are_prohibitive(self):
        bounds = DATA["l_series_coefficient_bounds"]
        self.assertEqual(bounds["decimal_precisions"], [1, 2, 5, 10, 20, 40, 80])
        self.assertGreater(bounds["conductor_norm_991"][0], 10**10)
        self.assertGreater(bounds["conductor_norm_991"][-1], 10**17)
        self.assertFalse(
            DATA["verdict"]["naive_twisted_l_value_period_recovery_feasible"]
        )


if __name__ == "__main__":
    unittest.main()

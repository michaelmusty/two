import json
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads(
    (ROOT / "data/computed/eisenstein_genus4.json").read_text()
)


class EisensteinCertificateTests(unittest.TestCase):
    def test_control_field(self):
        field = DATA["rm_field"]
        self.assertEqual(field["degree"], 4)
        self.assertEqual(field["discriminant"], 725)
        self.assertEqual(field["narrow_class_number"], 1)

    def test_normalization(self):
        form = DATA["form"]
        self.assertEqual(form["parallel_weight"], 4)
        self.assertEqual(form["zeta_K_minus_3"], "541/15")
        self.assertEqual(form["nonconstant_coefficient_scale"], "240/541")

    def test_neighbor_separation_exceeds_error(self):
        result = DATA["results"]
        separation = Decimal(result["minimum_root_separation"])
        error = Decimal(result["coarse_fine_root_error"])
        self.assertEqual(result["neighbor_count"], 17)
        self.assertGreater(separation, 100 * error)
        self.assertTrue(result["separates_neighbors"])

    def test_coefficient_descent(self):
        result = DATA["results"]
        imaginary = Decimal(result["maximum_coefficient_imaginary_part"])
        self.assertLess(imaginary, Decimal("1e-15"))
        self.assertTrue(result["coefficient_descent_numerically_real"])
        self.assertFalse(result["exact_coefficients_recognized"])

    def test_fine_run_contains_coarse_run(self):
        truncations = DATA["truncations"]
        for coarse, fine in zip(
            truncations["coarse_term_counts_base_half_double"],
            truncations["fine_term_counts_base_half_double"],
        ):
            self.assertGreater(fine, coarse)


if __name__ == "__main__":
    unittest.main()

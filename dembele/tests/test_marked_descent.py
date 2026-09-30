"""Exact controls for D58 arithmetic and bounded rational intervals.

These test the computations, not the cited geometric descent theorem.
"""
from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest

from sage.all import CyclotomicField, NumberField, PolynomialRing, QQ


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "marked_descent", ROOT / "dembele/pari/95_marked_descent.py")
descent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(descent)


class MarkedDescentTests(unittest.TestCase):
    def test_field_identities_against_cyclotomic_action(self):
        report = descent.exact_descent_inputs()
        field = CyclotomicField(32)
        zeta = field.gen()
        b = zeta+zeta**-1
        sigma = field.hom([zeta**3], field)
        self.assertEqual(sigma(b), b**3-3*b)
        self.assertEqual(2+sigma(b), (2+b)*(b-1)**2)
        self.assertEqual(report["F_narrow_class_number_proved"], 1)
        self.assertEqual(report["distinguished_CM_field_class_number_proved"], 1)
        self.assertEqual(report["branch_degree_Riemann_Hurwitz"], 18)

    def test_normalization_removes_a_nonrational_semilinear_gauge(self):
        ring = PolynomialRing(QQ, "b")
        field = NumberField(ring(descent.arithmetic.FIELD_COEFFICIENTS), "b")
        b = field.gen()
        sigma = field.hom([b**3-3*b], field)
        polynomials = PolynomialRing(field, "t")
        algebra = polynomials.quotient(
            polynomials(descent.arithmetic.HARBATER_COEFFICIENTS), "a")
        a = algebra.gen()
        conjugate = lambda v: algebra([sigma(c) for c in v.lift().list()])
        average = lambda v: v.matrix().trace()/17
        x = (1+b)*a+b*b
        y = (2+b*b)*a*a+b*a-b**3
        expected = ((17*a-2)/30, (2*a-a*a)/9)
        self.assertNotEqual(conjugate(x), x)
        self.assertEqual(descent.arithmetic.normalize_pair(x, y, average), expected)
        self.assertEqual(descent.arithmetic.normalize_pair(
            conjugate(x), conjugate(y), average), expected)
        self.assertEqual(tuple(conjugate(v) for v in expected), expected)

    def test_interval_status_against_exhaustive_small_denominators(self):
        for bound in (1, 2, 3, 7, 13):
            for center in map(Fraction, ("-9/4", "-1/13", "0", "5/12", "17/7")):
                for radius in map(Fraction, ("0", "1/100", "1/12", "1/2")):
                    lower, upper = center-radius, center+radius
                    possible = set()
                    for q in range(1, bound+1):
                        for p in range((lower*q).__ceil__(), (upper*q).__floor__()+1):
                            possible.add(Fraction(p, q))
                    result = descent.bounded_interval(center, radius, bound)
                    expected = "none" if not possible else "unique" if len(possible) == 1 else "ambiguous"
                    self.assertEqual(result["status"], expected, (bound, center, radius))
                    if possible:
                        self.assertIn(Fraction(result["nearest"]), possible)

    def test_closed_endpoints_and_invalid_intervals(self):
        # Both endpoints are included; a strict comparison would miss ambiguity.
        self.assertEqual(descent.bounded_interval("5/12", "1/12", 3)["status"], "ambiguous")
        self.assertEqual(descent.bounded_interval("1/7", 0, 7)["status"], "unique")
        self.assertEqual(descent.bounded_interval("1/7", 0, 6)["status"], "none")
        for center, radius, bound in ((0, -1, 5), (0, 0, 0)):
            with self.assertRaises(ValueError):
                descent.bounded_interval(center, radius, bound)

    def test_interval_includes_fit_and_imaginary_discrepancies(self):
        banks = {}
        for name in ("current", "previous", "alternate_fit", "larger_probe"):
            values = [["0", "0"] for _ in range(18)]
            values[3], values[17] = ["0.125", "0"], ["1", "0"]
            banks[name] = {"x_cm_value_polynomial_ascending": values}
        banks["previous"]["x_cm_value_polynomial_ascending"][3] = ["0.1251", "0"]
        banks["alternate_fit"]["x_cm_value_polynomial_ascending"][3] = ["0.125", "0.0002"]
        rows, _ = descent.coefficient_intervals(banks)
        self.assertEqual(Fraction(rows[3]["empirical_radius"]), Fraction(1, 500))
        self.assertEqual(Fraction(rows[3]["center"]), Fraction(1, 8))

    def test_height_control_matches_independent_minimal_polynomial(self):
        report = descent.normalization_height_control()
        ring = PolynomialRing(QQ, "t")
        field = NumberField(ring(descent.arithmetic.HARBATER_COEFFICIENTS), "theta")
        actual = ((17*field.gen()-2)/30).minpoly()
        self.assertEqual(actual.list(), [QQ(c) for c in report["polynomial_coefficients_ascending"]])
        self.assertGreater(report["maximum_denominator"], 10**20)
        self.assertTrue(report["all_coefficients_recovered_from_80_place_truncations"])


if __name__ == "__main__":
    unittest.main()

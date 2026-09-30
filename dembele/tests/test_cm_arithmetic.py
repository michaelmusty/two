"""Independent trace and Frobenius controls for the D57 CM-input audit."""
import importlib.util
from pathlib import Path
import unittest

from sage.all import CyclotomicField, GF, QQ, PolynomialRing


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("cm_arithmetic", ROOT / "dembele/pari/94_cm_arithmetic.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class CMArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h, cls.field, cls.elements, cls.examples = audit.exact_examples()

    def test_two_distinct_normalized_elements_in_the_same_field(self):
        a = self.field.gen()
        x, y = self.elements[0]
        self.assertEqual(x, (17*a-2)/30)
        self.assertEqual(y, (2*a-a*a)/9)
        x2, y2 = self.elements[1]
        self.assertEqual(x2, (17*a*a-4)/213)
        self.assertEqual((x*x).trace()/17, QQ(16)/225)
        self.assertEqual((x2*x2).trace()/17, -QQ(32)/5041)
        self.assertNotEqual(x.minpoly(), x2.minpoly())
        # The algebra is the same even though the normalized spectra differ.
        self.assertEqual(x.minpoly().degree(), 17)
        self.assertEqual(x2.minpoly().degree(), 17)

    def test_cm_cyclic_field_matches_cyclotomic_construction(self):
        report = audit.cm_cyclic_field()
        field = CyclotomicField(64)
        zeta = field.gen()
        beta = zeta**16*(zeta+1/zeta)
        ring = PolynomialRing(QQ, "s")
        polynomial = ring([QQ(c) for c in report["polynomial_coefficients_ascending"]])
        self.assertEqual(polynomial(beta), 0)
        self.assertEqual(beta**3+3*beta, zeta**48*(zeta**3+zeta**-3))
        self.assertEqual(-beta, beta.conjugate())

    def test_triangular_changes_preserve_each_flag(self):
        a = self.field.gen()
        average = lambda v: v.trace()/17
        actual = audit.normalize_pair(7*a+5, -3*a*a+11*a-8, average)
        self.assertEqual(actual, self.elements[0])
        # Changing the flag does not preserve it; normalization is not a
        # canonical choice of elements of a number field alone.
        self.assertNotEqual(actual, self.elements[1])

    def test_irreducible_reduction_trace_equals_frobenius_sum(self):
        k = GF(31)
        hp = self.h.change_ring(k)
        self.assertTrue(hp.is_irreducible())
        extension = GF(31**17, name="u", modulus=hp)
        theta = extension.gen()
        def average(v):
            total = extension(0)
            conjugate = v
            for _ in range(17):
                total += conjugate
                conjugate = conjugate**31
            self.assertEqual(conjugate, v)
            return k(total)/k(17)
        values = audit.normalize_pair(theta, theta**2, average)
        expected = tuple(v.polynomial().change_ring(k)(theta) for v in self.elements[0])
        self.assertEqual(values, expected)
        self.assertFalse(any(audit.constraints(*values, average)))
        report = audit.reduction_report(self.h, self.elements, 31)
        self.assertEqual([r["E_X2"] for r in report["example_reductions"]], [2, 13])
        self.assertIsNone(report["target_X_Y_reductions"])

    def test_product_algebra_trace_equals_sum_of_factor_traces(self):
        k = GF(97)
        hp = self.h.change_ring(k)
        algebra = hp.parent().quotient(hp, "u")
        factors = list(hp.factor())
        self.assertEqual(sorted(f.degree() for f, _ in factors), [1]+[2]*8)
        for v in [self.elements[0][0]**2, self.elements[1][0]**2]:
            polynomial = v.polynomial().change_ring(k)
            total = k(0)
            for factor, multiplicity in factors:
                self.assertEqual(multiplicity, 1)
                if factor.degree() == 1:
                    total += polynomial(-factor[0])
                else:
                    extension = GF(97**2, name="z", modulus=factor)
                    value = polynomial(extension.gen())
                    total += k(value+value**97)
            self.assertEqual(total, algebra(polynomial).matrix().trace())
        report = audit.reduction_report(self.h, self.elements, 97)
        self.assertEqual([r["E_X2"] for r in report["example_reductions"]], [85, 43])

    def test_average_and_order_bad_primes_are_refused(self):
        with self.assertRaisesRegex(ValueError, "divides by 17"):
            audit.reduction_report(self.h, self.elements, 17)
        with self.assertRaisesRegex(ValueError, "not etale"):
            audit.reduction_report(self.h, self.elements, 2)


if __name__ == "__main__":
    unittest.main()

"""Independent algebraic controls for complex-ball relation recovery."""
import importlib.util
from itertools import combinations_with_replacement
from pathlib import Path
import unittest

from sage.all import ComplexBallField, matrix
from dembele.tests.test_arithmetic_quadrics import genus_four_forms

HERE = Path(__file__).resolve().parents[1]/'pari'
spec = importlib.util.spec_from_file_location('precise_quadrics', HERE/'86_precise_quadrics.py')
precise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(precise)


class PreciseQuadricsTests(unittest.TestCase):
    def test_known_curve_quadric_is_enclosed_and_validates_unused_jets(self):
        field = ComplexBallField(220)
        forms = genus_four_forms(45)
        pairs = list(combinations_with_replacement(range(4), 2))
        products = [forms[i]*forms[j] for i, j in pairs]
        full = matrix(field, [[p[n] for p in products] for n in range(45)])
        free = [pairs.index((1, 1))]
        pivots = [i for i in range(10) if i not in free]
        coefficients, report = precise.solve_relations(full, pivots, free, 25)
        for row, monomial in enumerate(pivots):
            expected = -1 if pairs[monomial] == (0, 2) else 0
            self.assertTrue((coefficients[row, 0]-expected).contains_zero())
        self.assertLess(report['held_out_absolute_residual_bound'], 1e-50)
        self.assertEqual(report['unused_training_rows'], 16)

    def test_information_below_double_precision_survives_solve(self):
        field = ComplexBallField(300)
        epsilon = field(10)**-35
        rows = [(field(1), field(1)), (field(1), 1+epsilon),
                (field(2), field(3)), (field(4), field(7))]
        full = matrix(field, [[a, b, 2*a-3*b] for a, b in rows])
        coefficients, report = precise.solve_relations(full, [0, 1], [2], 3, fit_rows=[0, 1])
        self.assertTrue((coefficients[0, 0]+2).contains_zero())
        self.assertTrue((coefficients[1, 0]-3).contains_zero())
        self.assertLess(report['held_out_absolute_residual_bound'], 1e-45)
        with self.assertRaises(ValueError):
            precise.solve_relations(full, [0, 1], [2], 3, fit_rows=[0, 0])


if __name__ == '__main__':
    unittest.main()

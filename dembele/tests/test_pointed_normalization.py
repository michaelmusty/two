"""Exact-curve and independent-substitution checks of the new gauge."""
import importlib.util
from pathlib import Path
import sys
import unittest

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from belyi.pointed_series import (control, intrinsic_forms, q8_ordinary_forms,
                                 weight_one_gauge, echelon)

spec = importlib.util.spec_from_file_location('pointed', ROOT/'dembele/pari/83_pointed_normalization.py')
pointed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pointed)


class PointedNormalizationTests(unittest.TestCase):
    def test_exact_thesis_curve_and_coordinate_change(self):
        result = control(length=12)
        self.assertEqual(result['scale'], '-78064/324675')
        self.assertEqual(result['infinity_weight_gcd'], 8)

    def test_lagrange_coefficients_against_exact_series_substitution(self):
        length = 18
        forms = q8_ordinary_forms(length+4)
        exact, _, witness = weight_one_gauge(intrinsic_forms(forms, [0, 1], length), [0, 1])
        with mp.workdps(80):
            data = [[mp.mpf(str(f[n].numerator()))/mp.mpf(str(f[n].denominator())) for f in forms]
                    for n in range(length+1)]
            numeric, error, psi = pointed.intrinsic(data, [0, 1], length)
            external, _, _ = pointed.intrinsic(data, [0, 1], length, coordinate_unit=psi)
            self.assertLess(mp.norm(numeric-external), mp.mpf('1e-60'))
            numeric, _ = pointed.rescale(numeric, [0, 1], witness)
            self.assertLess(error, mp.mpf('1e-60'))
            for n in range(length):
                for i in range(2):
                    expected = mp.mpf(str(exact[i][n].numerator()))/mp.mpf(str(exact[i][n].denominator()))
                    self.assertLess(abs(numeric[n, i]-expected)/max(1, abs(expected)), mp.mpf('1e-55'))

    def test_missing_coordinate_jets_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'insufficient'):
            intrinsic_forms(q8_ordinary_forms(12), [0, 1], 12)
        with self.assertRaisesRegex(ValueError, 'insufficient'):
            pointed.intrinsic([[1, 0], [0, 1]], [0, 1], 3)

    def test_three_forms_at_a_nonordinary_quartic_point(self):
        from sage.all import QQ, PowerSeriesRing
        ring = PowerSeriesRing(QQ, 'u', default_prec=32)
        u = ring.gen()
        # The smooth plane quartic x^3*y+y^3*z+z^3*x=0 at (0:0:1).
        # With y=u, solve x+u^3+x^3*u=0. The canonical orders are 0,1,3.
        x = -u**3
        for _ in range(5):
            x -= (x+u**3+x**3*u)/(1+3*x**2*u)
        self.assertEqual(x+u**3+x**3*u, 0)
        h = 1/(1+3*x**2*u)
        forms = [h, u*h, x*h]
        exact = intrinsic_forms(forms, [0, 1, 3], 20)
        with mp.workdps(80):
            data = [[mp.mpf(str(f[n].numerator()))/mp.mpf(str(f[n].denominator())) for f in forms]
                    for n in range(23)]
            numeric, error, _ = pointed.intrinsic(data, [0, 1, 3], 20)
            self.assertLess(error, mp.mpf('1e-65'))
            for n in range(20):
                for i in range(3):
                    value = exact[i][n]
                    expected = mp.mpf(str(value.numerator()))/mp.mpf(str(value.denominator()))
                    self.assertLess(abs(numeric[n, i]-expected), mp.mpf('1e-65'))

    def test_fixed_coefficient_functionals_need_not_be_vanishing_orders(self):
        forms = intrinsic_forms(q8_ordinary_forms(20), [0, 1], 16)
        # [1,4] is not the vanishing sequence [0,1]. It still defines an
        # arithmetic basis when the parameter is already arithmetic.
        exact = echelon(forms, [1, 4])
        with mp.workdps(80):
            data = mp.matrix([[mp.mpf(str(f[n].numerator()))/mp.mpf(str(f[n].denominator()))
                               for f in forms] for n in range(16)])
            change = mp.matrix([[2+1j, 1], [1-1j, 3+1j]])
            normalized, indices, _ = pointed.select_jets(data*change, [1, 4])
            self.assertEqual(indices, [1, 4])
            for n in range(16):
                for i in range(2):
                    value = exact[i][n]
                    expected = mp.mpf(str(value.numerator()))/mp.mpf(str(value.denominator()))
                    self.assertLess(abs(normalized[n, i]-expected), mp.mpf('1e-65'))


if __name__ == '__main__':
    unittest.main()

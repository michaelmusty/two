"""Controls independent of the target curve's numerical automorphy."""
import importlib.util
from pathlib import Path
import unittest

import mpmath as mp
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parents[1]/'pari'
spec = importlib.util.spec_from_file_location('relative_cubic', HERE/'84_relative_cubic.py')
cubic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cubic)


class RelativeCubicTests(unittest.TestCase):
    def test_exact_degree_three_belyi_control(self):
        # t=3*x^2-2*x^3, with critical values 0,1,infinity.
        # Compute the centered characteristic polynomial independently by
        # elimination, and its traces by the multiplication matrix of x.
        x, t, T = sp.symbols('x t T')
        expected = T**3-sp.Rational(3, 4)*T-(sp.Rational(1, 4)-t/2)
        eliminated = sp.Poly(sp.resultant(3*x*x-2*x**3-t, T-x+sp.Rational(1, 2), x), T).monic().as_expr()
        self.assertEqual(sp.expand(eliminated-expected), 0)
        matrix = sp.Matrix([[0, 0, -t/2], [1, 0, 0], [0, 1, sp.Rational(3, 2)]])-sp.eye(3)/2
        self.assertEqual(sp.trace(matrix), 0)
        self.assertEqual(sp.trace(matrix**2)/2, sp.Rational(3, 4))
        self.assertEqual(sp.expand(sp.trace(matrix**3)/3), sp.Rational(1, 4)-t/2)
        self.assertEqual(sp.expand(sp.discriminant(expected, T)-sp.Rational(27, 4)*t*(1-t)), 0)
        for value in [.31+.27j, .67-.14j]:
            roots = np.roots([1, 0, -.75, -(1/4-value/2)])
            a, b = -roots[0]/2, (roots[1]-roots[2])/2
            for u in [.43+.19j, .8-.3j]:
                for sign in [-1, 1]:
                    coefficients = cubic.cubic_coefficients(a, sign*b*np.sqrt(u), 1, u)/u
                    np.testing.assert_allclose(coefficients, [1, -.75, -(1/4-value/2)], rtol=1e-13, atol=1e-14)

    def test_sector_offsets_match_homogeneous_disk_polynomial(self):
        rng = np.random.default_rng(84530)
        differential = rng.normal(size=12)+1j*rng.normal(size=12)
        base = rng.normal(size=7)+1j*rng.normal(size=7)
        w = np.array([.73+.2j, -.77+.1j, .67-.5j])
        radius = .97
        coarse, _ = cubic.coarse_values((w/radius)**32, differential, base)
        disk, _ = cubic.disk_values(w, differential, base, radius)
        np.testing.assert_allclose(disk, (w/radius)[:, None]**61*coarse, rtol=2e-14, atol=1e-25)
        # An incorrect offset or forgotten differential multiplier changes
        # the degree 61 factor, so this is not just a root-sum identity.

    def test_complex_trace_invariance_does_not_imply_rational_descent(self):
        t = sp.Symbol('t')
        # Scaling a rational trace-zero generator by sqrt(2) keeps its
        # symmetric traces on the complex base, but changes its Q-structure.
        original = sp.Matrix([[0, 0, sp.Rational(1, 4)-t/2], [1, 0, sp.Rational(3, 4)], [0, 1, 0]])
        scaled = sp.sqrt(2)*original
        self.assertEqual(sp.trace(scaled**2)/2, sp.Rational(3, 2))
        self.assertEqual(sp.simplify(sp.trace(scaled**3)/3-sp.sqrt(2)*(sp.Rational(1, 2)-t)), 0)
        self.assertFalse(sp.trace(scaled**3).subs(t, 0).is_rational)

    def test_half_density_pullback_against_exact_substitution(self):
        # v=u/(1-u), hence u=v/(1+v). The transformed b coefficient is
        # b(v/(1+v))*(1+v)^(-3/2), computed independently by substitution.
        u, v = sp.symbols('u v')
        length = 10
        source = 1+2*u+3*u*u
        exact = sp.series(source.subs(u, v/(1+v))*(1+v)**(-sp.Rational(3, 2)), v, 0, length).removeO()
        spec = importlib.util.spec_from_file_location('test_pointed', HERE/'83_pointed_normalization.py')
        pointed = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pointed)
        with mp.workdps(50):
            psi = [mp.mpf(1), mp.mpf(-1)]+[mp.mpf(0)]*(length-2)
            rows = np.array([1, 2, 3]+[0]*(length-3), dtype=complex)[:, None]
            actual = cubic.weighted_pullback(rows, psi, mp.mpf(1), mp.mpf('.5'), pointed)[:, 0]
        np.testing.assert_allclose(actual, [float(exact.coeff(v, n)) for n in range(length)], rtol=1e-14)

    def test_zero_and_nonfinite_data_are_not_valid_checks(self):
        for bad in [np.zeros((5, 3)), np.full((5, 3), np.nan)]:
            with self.assertRaises(ValueError):
                cubic.compare(bad, bad)

    def test_arbitrary_local_series_fail_global_side_check(self):
        result = cubic.side_audit(np.array([1, 0, 1, 0], complex), np.array([1], complex),
                                 cubic.cover.Geometry(), .99991)
        self.assertGreater(result['homogeneous_cubic']['relative_l2'], .01)


if __name__ == '__main__':
    unittest.main()

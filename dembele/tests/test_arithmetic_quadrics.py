"""Exact curve controls for reconstruction after a short arithmetic gauge."""
import importlib.util
from pathlib import Path
import unittest

import mpmath as mp
import numpy as np
from sage.all import QQ, PowerSeriesRing

HERE = Path(__file__).resolve().parents[1]/'pari'
spec = importlib.util.spec_from_file_location('arithmetic_quadrics', HERE/'85_arithmetic_quadrics.py')
quadrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quadrics)


def genus_four_forms(length):
    # Smooth trigonal genus-four curve y^3=x^5-x+1 at the rational point
    # (0,1). Its canonical coordinates are [1,x,x^2,y], with the single
    # quadric X0*X2-X1^2. This equation is independent of reconstruction.
    ring = PowerSeriesRing(QQ, 'u', default_prec=length)
    u = ring.gen()
    y = (1-u+u**5)**(QQ(1)/3)
    return [1/y**2, u/y**2, u**2/y**2, 1/y]


def mp_rows(forms, length):
    return [[mp.mpf(str(f[n].numerator()))/mp.mpf(str(f[n].denominator())) for f in forms]
            for n in range(length)]


class ArithmeticQuadricsTests(unittest.TestCase):
    def test_short_change_preserves_known_exact_quadric(self):
        length = 42
        forms = genus_four_forms(length)
        with mp.workdps(70):
            source = mp_rows(forms, length)
            change, _, report = quadrics.arithmetic_change(source, list(range(4)), [(4, 2, -1), (4, 1, 1)])
            self.assertLess(mp.mpf(report['short_formal_consistency_error']), mp.mpf('1e-60'))
            transformed = np.array((mp.matrix(source)*change).tolist(), complex)
            # Reduce the evaluation radius to control the known Taylor
            # coefficient growth; this is not a change of canonical basis.
            transformed *= .2**np.arange(length)[:, None]
            full, pairs = quadrics.products(transformed)
            equations, fit = quadrics.fit_relations(full, 25, 9)
            self.assertEqual(fit['equation_count'], 1)
            self.assertLess(fit['held_out_relative_residual'], 1e-8)
            inverse = np.array((change**-1).tolist(), complex)
            # X=Y*change^-1 in row-vector notation. Substitute in the
            # independently known X0*X2-X1^2, then compare projectively.
            expected = []
            for i, j in pairs:
                value = inverse[i, 0]*inverse[j, 2]-inverse[i, 1]*inverse[j, 1]
                if i != j:
                    value += inverse[j, 0]*inverse[i, 2]-inverse[j, 1]*inverse[i, 1]
                expected.append(value)
            expected = np.array(expected)
            pivot = np.argmax(abs(expected))
            np.testing.assert_allclose(equations[:, 0]/equations[pivot, 0], expected/expected[pivot], atol=2e-7, rtol=2e-7)

    def test_short_change_matches_independent_exact_coordinate_method(self):
        from belyi.pointed_series import intrinsic_forms
        length = 18
        forms = genus_four_forms(length+3)
        exact = intrinsic_forms(forms, list(range(4)), length)
        scale = 12*exact[1][4]/exact[2][4]
        with mp.workdps(70):
            rows = mp_rows(forms, length+3)
            change, short, _ = quadrics.arithmetic_change(rows, list(range(4)), [(4, 2, -1), (4, 1, 1)])
            for n in range(short.rows):
                for i in range(4):
                    value = exact[i][n]*scale**(i-n)
                    target = mp.mpf(str(value.numerator()))/mp.mpf(str(value.denominator()))
                    self.assertLess(abs(short[n, i]-target)/max(1, abs(target)), mp.mpf('1e-60'))

    def test_wrong_rank_and_zero_data_are_rejected(self):
        with self.assertRaises(ValueError):
            quadrics.fit_relations(np.zeros((30, 10)), 20, 9)
        rng = np.random.default_rng(8516)
        with self.assertRaisesRegex(ValueError, 'product rank'):
            quadrics.fit_relations(rng.normal(size=(30, 10)), 20, 9)


if __name__ == '__main__':
    unittest.main()

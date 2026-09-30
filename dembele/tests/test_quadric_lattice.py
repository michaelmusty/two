"""Lattice discovery controls against a known canonical quadric and tiny units."""
import importlib.util
from pathlib import Path
import unittest

import mpmath as mp

HERE = Path(__file__).resolve().parents[1]/'pari'
spec = importlib.util.spec_from_file_location('quadric_lattice', HERE/'89_quadric_lattice.py')
lattice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lattice)


def known_quadric():
    # The genus-four control y^3=x^5-x+1 has canonical coordinates
    # [1,x,x^2,y] and relation X0 X2 - X1^2. In lexicographic monomial
    # order these are entries 2 and 4, independently of any lattice solve.
    pivots = [i for i in range(10) if i != 4]
    coefficients = [[['-1' if p == 2 else '0', '0']] for p in pivots]
    return {'pivots': pivots, 'free': [4], 'pivot_coefficients': coefficients}


class QuadricLatticeTests(unittest.TestCase):
    def test_lll_recovers_the_known_curve_equation(self):
        with mp.workdps(80):
            quotient = lattice.quotient_map(known_quadric())
            rows, details = lattice.reduce_tail(lattice.lattice_tail(quotient, [mp.mpf(1)], 20), 30)
            self.assertIsNotNone(rows)
            exact = [r for r in rows if lattice.relation_residual(quotient, r, [mp.mpf(1)]) < mp.mpf('1e-60')]
            self.assertTrue(exact)
            for row in exact:
                self.assertEqual(row[2], -row[4])
                self.assertEqual(sum(abs(z) for i, z in enumerate(row) if i not in [2, 4]), 0)

    def test_field_coefficients_use_the_declared_integral_basis(self):
        with mp.workdps(80):
            basis = lattice.fields.field_bases('cosine')[-1][1]
            quotient = lattice.quotient_map(known_quadric())
            quotient[2, 4] = 1/basis[1]
            row = [0]*80
            row[2*8] = -1
            row[4*8+1] = 1
            self.assertLess(lattice.relation_residual(quotient, row, basis), mp.mpf('1e-70'))

    def test_small_embedded_value_is_not_a_relation(self):
        with mp.workdps(100):
            quotient = mp.matrix([[1, 2]])
            basis = [mp.mpf(1), 1-mp.mpf('1e-60')]
            residual = lattice.relation_residual(quotient, [1, -1, 0, 0], basis)
            self.assertGreater(residual, mp.mpf('.4'))


if __name__ == '__main__':
    unittest.main()

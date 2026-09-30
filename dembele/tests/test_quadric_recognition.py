"""Controls for bounded recognition, including an honest failure case."""
import importlib.util
from pathlib import Path
import unittest

import mpmath as mp

HERE = Path(__file__).resolve().parents[1]/'pari'
spec = importlib.util.spec_from_file_location('quadric_recognition', HERE/'87_quadric_recognition.py')
recognition = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recognition)


class QuadricRecognitionTests(unittest.TestCase):
    def test_field_embedding_and_exact_candidate_control(self):
        with mp.workdps(80):
            fields = recognition.field_bases()
            self.assertLess(abs(fields[1][1][1]-mp.sqrt(2)), mp.mpf('1e-70'))
            basis = fields[-1][1]
            value = (3+2*basis[1]-basis[3])/5
            result = recognition.relation(value, basis, 8, mp.mpf('1e-50'))
            self.assertIsNotNone(result)
            self.assertTrue(result['same_relation_at_tighter_tolerance'])
            self.assertLess(mp.mpf(result['absolute_residual']), mp.mpf('1e-60'))

    def test_bounded_search_can_fail_and_rejects_imaginary_error(self):
        with mp.workdps(80):
            basis = recognition.field_bases()[-1][1]
            self.assertIsNone(recognition.relation(mp.pi, basis, 4, mp.mpf('1e-30')))
            self.assertIsNone(recognition.relation(1+mp.mpc(0, '1e-8'), basis, 4, mp.mpf('1e-20')))

    def test_cosine_basis_is_integral_and_trace_orthogonal(self):
        from sage.all import QQ, NumberField, PolynomialRing, matrix, diagonal_matrix
        ring = PolynomialRing(QQ, 'x')
        x = ring.gen()
        field = NumberField(x**8-8*x**6+20*x**4-16*x**2+2, 'b')
        b = field.gen()
        basis = [field(1), b]
        previous, current = field(2), b
        for _ in range(2, 8):
            previous, current = current, b*current-previous
            basis.append(current)
        change = matrix(QQ, [list(z) for z in basis])
        self.assertEqual(change.det(), 1)
        gram = matrix(QQ, [[(a*c).trace() for c in basis] for a in basis])
        self.assertEqual(gram, diagonal_matrix(QQ, [8]+[16]*7))
        self.assertEqual(gram.det(), field.discriminant())
        with mp.workdps(80):
            numeric = recognition.field_bases('cosine')[-1][1]
            for j in range(1, 8):
                self.assertLess(abs(numeric[j]-2*mp.cos(j*7*mp.pi/16)), mp.mpf('1e-70'))
            value = (2+numeric[2]-3*numeric[7])/5
            candidate = recognition.relation(value, numeric, 8, mp.mpf('1e-50'))
            self.assertIsNotNone(candidate)
            self.assertTrue(candidate['same_relation_at_tighter_tolerance'])

    def test_equal_weight_ratios_cancel_parameter_rescaling(self):
        with mp.workdps(80):
            rows = [[mp.mpc('.8'), mp.mpc('.6')], [mp.mpc('.7'), mp.mpc('1.1')]]
            old = [[mp.mpc('.800001'), mp.mpc('.60002')], [mp.mpc('.700001'), mp.mpc('1.100002')]]
            pairs, pivots, free = [(0, 0), (0, 1), (0, 2), (1, 1)], [0, 1], [2, 3]
            first = recognition.scale_invariant_ratios(rows, old, pivots, free, pairs)
            mu = mp.mpc('1.3', '.2')
            def scaled(values):
                return [[z*mu**(sum(pairs[free[j]])-sum(pairs[pivots[i]]))
                         for j, z in enumerate(row)] for i, row in enumerate(values)]
            second = recognition.scale_invariant_ratios(scaled(rows), scaled(old), pivots, free, pairs)
            self.assertEqual(first[2], second[2])
            for side in range(2):
                for i in range(2):
                    for j in range(2):
                        self.assertLess(abs(first[side][i][j]-second[side][i][j]), mp.mpf('1e-70'))


if __name__ == '__main__':
    unittest.main()

"""Independent precision/convention checks for the compiled residual backend.

Run using Sage Python, with local FLINT development files and pkg-config.
The mpmath direct DFT in script 78 is an independent reference.
"""
import importlib
from pathlib import Path
import sys
import tempfile
import unittest

import mpmath as mp
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'pari'))
from cm_acb import Backend, CauchyOperator, Vector, evaluate, weighted_difference

reference = importlib.import_module('78_mixed_precision_refinement')


class CompiledCauchyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = mp.workdps(80)
        cls.context.__enter__()
        cls.backend = Backend(50)

    @classmethod
    def tearDownClass(cls):
        cls.context.__exit__(None, None, None)

    def test_batched_actions_match_independent_direct_dft(self):
        n, count = 7, 17  # Includes a prime-size Bluestein transform.
        nodes = [mp.mpc(t, 2-t)/20 for t in range(count)]
        weights = [mp.exp(mp.mpc(0, t)/7) for t in range(count)]
        coefficients = [[mp.mpc(1, j)/(j+1), mp.mpc(j, -2)/(j+3)] for j in range(n)]
        expected = mp.matrix(n, 2)
        for c in range(2):
            expected[:, c] = reference.cauchy_apply(
                [row[c] for row in coefficients], nodes, weights, mp.mpf('.37'))
        native = self.backend.vector(coefficients)
        z, w = self.backend.vector(nodes), self.backend.vector(weights)
        for method in ('horner', 'rectangular'):
            op = CauchyOperator(self.backend, n, z, w, method=method)
            result = op.apply(native)
            self.assertLess(mp.norm(result.to_mpmath()-expected), mp.mpf('1e-55'))
            # Reuse the same FFT plan for a different input.
            zero = Vector(self.backend, n, 2)
            self.assertEqual(max(op.apply(zero).bounds()), 0)

    def test_nodes_beyond_double_precision_are_preserved(self):
        epsilon = mp.mpf('1e-40')
        nodes = self.backend.vector([1+epsilon]*4)
        weights = self.backend.vector([1]*4)
        coefficients = self.backend.vector([-1, 1])
        op = CauchyOperator(self.backend, 2, nodes, weights, offset='0')
        result = op.apply(coefficients).to_mpmath()
        self.assertLess(abs(result[0]-epsilon), mp.mpf('1e-60'))
        self.assertLess(abs(result[1]), mp.mpf('1e-60'))

    def test_fortran_assembly_avoids_a_second_dense_lu_array(self):
        from scipy.linalg import lu_factor, lu_solve
        pilot = importlib.import_module('68_cm_differentials')
        n, count = 17, 34
        nodes = np.exp(2j*np.pi*np.arange(count)/count)*.3
        weights = np.exp(1j*np.arange(count))*.01
        standard = pilot.operator_from_nodes(n, nodes, weights)
        inplace = pilot.operator_from_nodes(n, nodes, weights, order='F')
        np.testing.assert_array_equal(standard, inplace)
        self.assertTrue(inplace.flags.f_contiguous)
        inplace[np.diag_indices(n)] += 1
        expected = inplace.copy()
        factors = lu_factor(inplace, overwrite_a=True, check_finite=False)
        self.assertTrue(np.shares_memory(inplace, factors[0]))
        rhs = np.arange(n)+1j*np.arange(n)[::-1]
        answer = lu_solve(factors, rhs)
        np.testing.assert_allclose(expected@answer, rhs, atol=1e-13)

    def test_worker_plans_match_serial_and_can_be_reused(self):
        n, count = 64, 128
        coefficients = self.backend.vector([[mp.mpc(j, c)/(j+c+1) for c in range(5)] for j in range(n)])
        nodes = self.backend.vector([mp.exp(mp.mpc(0, t)/count)/2 for t in range(count)])
        weights = self.backend.vector([1]*count)
        serial = CauchyOperator(self.backend, n, nodes, weights)
        parallel = CauchyOperator(self.backend, n, nodes, weights, threads=4)
        expected = serial.apply(coefficients)
        for _ in range(2):
            result = parallel.apply(coefficients)
            self.assertEqual(mp.norm(result.to_mpmath()-expected.to_mpmath()), 0)
            self.assertEqual(result.bounds(1), expected.bounds(1))
        serial.close()
        parallel.close()
        with self.assertRaises(RuntimeError):
            parallel.apply(coefficients)

    def test_stabilized_residual_matches_explicit_formula(self):
        n, count, rank = 9, 24, 3
        nodes = [mp.exp(mp.mpc(0, t)/count)/2 for t in range(count)]
        weights = [mp.mpc(1, t)/count for t in range(count)]
        B = mp.matrix([[mp.mpc(i+1, j-1)/(i+j+2) for j in range(rank)] for i in range(n)])
        X = B[:, :2]*mp.mpc('.31', '.17')
        expected = mp.matrix(n, 2)
        for c in range(2):
            expected[:, c] = B[:, c]-X[:, c]+reference.cauchy_apply(X[:, c], nodes, weights, mp.mpf('.37'))
        expected -= B*(B.H*X)
        op = CauchyOperator(self.backend, n, self.backend.vector(nodes), self.backend.vector(weights))
        result = op.residual(self.backend.vector(X.tolist()), self.backend.vector(B.tolist()))
        self.assertLess(mp.norm(result.to_mpmath()-expected), mp.mpf('1e-53'))
        for i in range(n):
            for c in range(2):
                for part in (0, 1):
                    actual = mp.mpf(result.component(i, c, part))
                    radius = mp.mpf(result.component(i, c, part+2))
                    target = expected[i, c].real if part == 0 else expected[i, c].imag
                    self.assertLessEqual(abs(actual-target), radius+mp.mpf('1e-75'))

    def test_independent_side_evaluation(self):
        coefficients = self.backend.vector([[1, 2], [3, 4], [5, 6]])
        z = [mp.mpc('.1', '.2'), mp.mpc('-.2', '.3')]
        left = evaluate(coefficients, self.backend.vector(z))
        right = evaluate(coefficients, self.backend.vector([a/2 for a in z]), method='horner')
        weights = self.backend.vector([2, 3])
        result = weighted_difference(left, right, weights).to_mpmath()
        expected = mp.matrix(2, 2)
        for i in range(2):
            for j in range(2):
                a, b, c = j+1, j+3, j+5
                expected[i, j] = a+b*z[i]+c*z[i]**2-(i+2)*(a+b*z[i]/2+c*(z[i]/2)**2)
        self.assertLess(mp.norm(result-expected), mp.mpf('1e-55'))

    def test_column_scaling_survives_double_underflow_and_overflow(self):
        original = mp.matrix([[mp.mpc('1e-450', '2e-450'), mp.mpc('1e450', '-3e450')],
                              [mp.mpc('-3e-450', '1e-450'), mp.mpc('2e450', '1e450')]])
        v = self.backend.vector(original.tolist())
        normalized, exponents = v.scaled_doubles()
        self.assertTrue(np.all(np.isfinite(normalized)))
        self.assertGreater(np.min(np.abs(normalized)), .1)
        result = Vector(self.backend, 2, 2)
        result.add_correction(normalized, exponents)
        restored = result.to_mpmath()
        for i in range(2):
            for j in range(2):
                self.assertLess(abs(restored[i, j]/original[i, j]-1), mp.mpf('2e-16'))

    def test_exact_checkpoint_round_trip_and_no_overwrite(self):
        v = self.backend.vector([[mp.pi, mp.mpc(0, '1e-450')], [mp.sqrt(2), -3]])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'coefficients.acb'
            v.write(path)
            restored = self.backend.read(path, 2, 2)
            for i in range(2):
                for j in range(2):
                    for part in range(4):
                        self.assertEqual(v.component(i, j, part), restored.component(i, j, part))
            with self.assertRaises(ArithmeticError):
                v.write(path)
            with self.assertRaises(ValueError):
                self.backend.read(path, 4, 2)

    def test_invalid_inputs_fail_before_native_computation(self):
        with self.assertRaises(ArithmeticError):
            self.backend.vector([float('nan')], doubles=True)
        with self.assertRaises(ValueError):
            self.backend.vector([])
        v = self.backend.vector([1, 2])
        with self.assertRaises(ValueError):
            CauchyOperator(self.backend, 3, v, v)
        with self.assertRaises(ValueError):
            v.add_correction(np.zeros((3, 1)), [0])


if __name__ == '__main__':
    unittest.main()

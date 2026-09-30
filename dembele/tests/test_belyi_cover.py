"""Checks for the geometry adapter and reuse of the existing Belyi kernel."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest

import numpy as np

HERE = Path(__file__).resolve().parents[1]/'pari'
spec = importlib.util.spec_from_file_location('belyi_cover', HERE/'81_belyi_cover.py')
cover = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cover
spec.loader.exec_module(cover)


class CoverAdapterTests(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(8148)
        self.geometry = cover.Geometry()

    def test_old_new_decomposition_and_elliptic_sectors(self):
        n = 7
        full = self.rng.normal(size=(3*n, 2))+1j*self.rng.normal(size=(3*n, 2))
        new = cover.project_new(full)
        old = (full[:n]+2*full[n+1::2])/3
        np.testing.assert_allclose(cover.embed_new(new)+cover.embed_old(old), full, atol=1e-14)
        np.testing.assert_allclose(cover.project_new(cover.embed_new(new)), new, atol=1e-14)
        z = np.array([0.13+0.27j, -0.41+0.2j])
        def values(w):
            a = w[:, None]**31*np.polynomial.polynomial.polyval(w**32, new[:n]).T
            b = w[:, None]**15*np.polynomial.polynomial.polyval(w**32, new[n:]).T
            out = np.empty((len(w), 3, 2), complex)
            out[:, self.geometry.fixed] = -2*a
            out[:, self.geometry.moving] = a+b
            out[:, self.geometry.partner] = a-b
            return out
        lhs = self.geometry.zeta*values(self.geometry.zeta*z)
        rhs = values(z)[:, self.geometry.elliptic]
        np.testing.assert_allclose(lhs, rhs, rtol=1e-13, atol=1e-30)

    def test_zero_vector_is_not_a_valid_differential(self):
        audit = cover.side_audit(np.zeros((16, 1), complex), self.geometry, 0.99991)
        self.assertEqual(audit['nonzero_columns'], [False])
        self.assertEqual(audit['relative_l2_by_column'], [None])

    def test_dense_assembly_matches_direct_series_on_shifted_grid(self):
        problem = cover.make_problem(self.geometry, 13, oversample=3, offset=0.19)
        v = self.rng.normal(size=(26, 3))+1j*self.rng.normal(size=(26, 3))
        np.testing.assert_allclose(problem.dense_new()@v, problem.apply_new(v), rtol=1e-12, atol=1e-12)

    @unittest.skipUnless((Path(os.environ.get('BELYI_ROOT', '/Users/musty/Belyi'))/'Cext/powser_arnoldi.c').exists(),
                         'local Belyi source is required for the native integration check')
    def test_native_operator_with_wide_balls_and_threading(self):
        # At n=256 the upstream Horner balls are wide enough that directly
        # printing a ball with ARB_STR_NO_RADIUS would lose its midpoint.
        problem = cover.make_problem(self.geometry, 256)
        v = self.rng.normal(size=(512, 2))+1j*self.rng.normal(size=(512, 2))
        root = os.environ.get('BELYI_ROOT', '/Users/musty/Belyi')
        serial, _ = cover.native(problem, v, belyi_root=root, threads=1)
        threaded, _ = cover.native(problem, v, belyi_root=root, threads=4)
        self.assertGreater(np.linalg.norm(serial), 1)
        np.testing.assert_array_equal(serial, threaded)
        np.testing.assert_allclose(serial, problem.apply_new(v), rtol=2e-12, atol=2e-12)

    @unittest.skipUnless((Path(os.environ.get('BELYI_ROOT', '/Users/musty/Belyi'))/'Cext/powser_arnoldi.c').exists(),
                         'local Belyi source is required for the native integration check')
    def test_full_operator_old_component_against_scalar_geometry(self):
        n = 32
        problem = cover.make_problem(self.geometry, n)
        v = self.rng.normal(size=(n, 2))+1j*self.rng.normal(size=(n, 2))
        output, _ = cover.native(problem, cover.embed_old(v), mode='apply',
                                 belyi_root=os.environ.get('BELYI_ROOT', '/Users/musty/Belyi'))
        independent, _ = cover.scalar.sampled_operator(n, 0.99991, self.geometry.actions,
                                                       oversample=4, offset=0)
        np.testing.assert_allclose(output[:n], independent@v, rtol=1e-11, atol=1e-11)


if __name__ == '__main__':
    unittest.main()

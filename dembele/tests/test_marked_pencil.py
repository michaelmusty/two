"""Exact and numerical controls for five-point pencil normalization."""
import importlib.util
from itertools import permutations
from pathlib import Path
import runpy
import unittest

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('marked_pencil', ROOT/'dembele/pari/90_marked_pencil.py')
pencil = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pencil)


class MarkedPencilTests(unittest.TestCase):
    def test_reconstruct_known_diagonal_pencil_and_check_unused_rows(self):
        # Q0=sum X_i^2, Q1=sum i*X_i^2. Second differences annihilate
        # their coefficient vectors. This independently specifies the pencil.
        with mp.workdps(80):
            quotient = mp.matrix([[1, -2, 1, 0, 0], [0, 1, -2, 1, 0],
                                  [0, 0, 1, -2, 1], [1, -1, -1, 1, 0]])
            equations, gauge, details = pencil.reconstruct_pencil(quotient, 3, training=3)
            self.assertEqual(details['constraints_checked'], 4)
            self.assertLess(mp.mpf(details['all_constraint_relative_residual']), mp.mpf('1e-70'))
            known = mp.matrix([[1, i] for i in range(5)])
            rows = gauge['free']
            change = mp.matrix([[known[i, j] for j in range(2)] for i in rows])**-1
            self.assertLess(mp.norm(equations-known*change), mp.mpf('1e-70'))
            bad = quotient.copy()
            bad[3, 0] += 1
            with self.assertRaisesRegex(ValueError, 'product rank'):
                pencil.reconstruct_pencil(bad, 3)
            noisy = quotient.copy()
            noisy[3, 0] += mp.mpf('1e-10')
            with self.assertRaisesRegex(ValueError, 'product rank'):
                pencil.reconstruct_pencil(noisy, 3)
            _, _, noise_report = pencil.reconstruct_pencil(noisy, 3, allow_noisy=True)
            self.assertTrue(noise_report['noisy_reference_rank_truncated'])
            self.assertGreater(mp.mpf(noise_report['all_constraint_relative_residual']), mp.mpf('1e-15'))

    def test_all_sixty_markings_on_actual_thesis_branch_points_exactly(self):
        # Reuse the verified thesis Q8 curve. Only its five finite branch
        # points are the reference configuration; no Q8 quadric pencil is claimed.
        known = runpy.run_path(str(ROOT/'belyi/validate_q8.sage'))
        field, polynomial = known['K'], known['f']
        i = field.gen()
        roots = [field(0), field(1)/2, -field(1)/2, i/2, -i/2]
        self.assertTrue(all(polynomial(r) == 0 for r in roots))
        lines = [[field(1), -r] for r in roots]
        orbits = set()
        for triple in permutations(range(5), 3):
            remaining, values = pencil.marked_values(lines, triple)
            a, b, c = [roots[j] for j in triple]
            for target, value in zip(remaining, values):
                expected = (roots[target]-a)*(c-b)/((roots[target]-b)*(c-a))
                self.assertEqual(value, expected)
                key = pencil.orbit_key(triple, target)
                orbits.add(key)
                labels = sorted(key)
                a0, b0, c0, d0 = [roots[j] for j in labels]
                canonical = (d0-a0)*(c0-b0)/((d0-b0)*(c0-a0))
                self.assertEqual(pencil.canonical_cross_ratio(key, value), canonical)
                self.assertEqual(pencil.marked_cross_ratio(key, canonical), value)
        self.assertEqual(len(orbits), 30)

    def test_complex_basis_invariance_including_an_infinite_point(self):
        with mp.workdps(80):
            equations = mp.matrix([[1, 0], [0, 1], [1, -1], [1, -2-mp.j], [1, 1-mp.j]])
            change = mp.matrix([[2, mp.j], [1-mp.j, 3]])
            scales = mp.diag([1+mp.j, -2, 3-mp.j, mp.mpf(1)/7, 5*mp.j])
            for triple in permutations(range(5), 3):
                normalized, remaining, values = pencil.normalize_pencil(equations, list(range(5)), triple)
                altered, _, new_values = pencil.normalize_pencil(equations*change, list(range(5)), triple)
                self.assertLess(mp.norm(normalized-altered), mp.mpf('1e-65'))
                self.assertLess(max(abs(a-b) for a, b in zip(values, new_values)), mp.mpf('1e-65'))
                scaled = scales*equations*change
                lines = [[scaled[i, j] for j in range(2)] for i in range(5)]
                _, scaled_values = pencil.marked_values(lines, triple)
                self.assertLess(max(abs(a-b) for a, b in zip(values, scaled_values)), mp.mpf('1e-65'))
                a, b, c = triple
                self.assertLess(abs(normalized[a, 1]), mp.mpf('1e-65'))
                self.assertLess(abs(normalized[b, 0]), mp.mpf('1e-65'))
                self.assertLess(abs(normalized[c, 0]+normalized[c, 1]), mp.mpf('1e-65'))
                self.assertLess(abs(normalized[b, 1]-1), mp.mpf('1e-65'))

    def test_known_real_field_markings_are_recognized(self):
        with mp.workdps(80):
            basis = pencil.lattice.fields.field_bases('cosine')[-1][1]
            b, d = basis[1], (basis[1]**2+1)/3
            lines = [[mp.mpf(1), 0], [0, mp.mpf(1)], [mp.mpf(1), -1], [1, -b], [1, -d]]
            _, values = pencil.marked_values(lines, (0, 1, 2))
            self.assertLess(abs(values[0]-b)+abs(values[1]-d), mp.mpf('1e-70'))
            for value, minimum_degree in zip(values, [8, 4]):
                errors = pencil.accuracy(value, value, value, value)
                result = pencil.recognize(value, value, value, errors, [4])
                matches = [trial for trial in result['trials'] if trial['candidate'] is not None]
                self.assertEqual(min(match['field_degree'] for match in matches), minimum_degree)
                self.assertTrue(any(match['field_degree'] == 8 for match in matches))
                self.assertTrue(all(match['candidate']['same_relation_at_tighter_tolerance'] for match in matches))

    def test_accuracy_distinguishes_convergence_from_nonconvergence(self):
        with mp.workdps(80):
            exact = mp.mpf('.123')
            current = exact+mp.mpf('1e-18')
            data = pencil.accuracy(current, current+mp.mpf('2e-19'), exact+mp.mpf('1e-12'), exact+mp.mpf('1e-6'))
            self.assertLess(mp.mpf(data['successive_difference_ratio']), mp.mpf('2e-6'))
            self.assertGreater(mp.mpf(data['exploratory_absolute_tolerance']), abs(current-exact))
            bad = pencil.accuracy(mp.mpc(1), mp.mpc(1), mp.mpc(2), mp.mpc('2.01'))
            self.assertIsNone(bad['geometric_tail_estimate'])
            self.assertEqual(pencil.recognize(mp.mpc(1), mp.mpc(1), mp.mpc(2), bad, [4])['trials'], [])

    def test_coincident_markings_are_refused(self):
        with self.assertRaisesRegex(ValueError, 'coincide'):
            pencil.marked_values([[1, 0], [0, 1], [2, 0], [1, -1], [1, -2]], (0, 1, 3))

    def test_flag_preserving_coordinate_change_preserves_marked_configuration(self):
        from sage.all import QQ, PolynomialRing
        ring = PolynomialRing(QQ, [f'x{i}' for i in range(16)])
        x = ring.gens()
        pairs = [(i, j) for i in range(16) for j in range(i, 16) if i+j >= 22]
        marked = [(i, j) for i, j in pairs if i+j == 22]
        equations = []
        for column in range(2):
            polynomial = ring(0)
            for index, (i, j) in enumerate(pairs):
                coefficient = (1 if column == 0 else marked.index((i, j))) if (i, j) in marked \
                    else (index+1)**(column+1)
                polynomial += coefficient*x[i]*x[j]
            equations.append(polynomial)
        substitutions = [(i+1)*x[i]+(x[i+1] if i+1 < 16 else 0)
                         - (2*x[i+2] if i+2 < 16 else 0) for i in range(16)]
        changed = [q(*substitutions) for q in equations]
        for q in changed:
            self.assertTrue(all(sum(i*e for i, e in enumerate(exponent)) >= 22 for exponent in q.dict()))
        original_lines = [[q.monomial_coefficient(x[i]*x[j]) for q in equations] for i, j in marked]
        changed_lines = [[q.monomial_coefficient(x[i]*x[j]) for q in changed] for i, j in marked]
        for triple in permutations(range(5), 3):
            self.assertEqual(pencil.marked_values(original_lines, triple), pencil.marked_values(changed_lines, triple))


if __name__ == '__main__':
    unittest.main()

"""Exact orbit and independent reconstruction controls for D59."""
import importlib.util
import json
from pathlib import Path
import unittest

import mpmath as mp
from sage.all import QQ, ZZ, matrix, vector


ROOT = Path(__file__).resolve().parents[2]
def module(name, filename):
    spec = importlib.util.spec_from_file_location(name,ROOT/"dembele/pari"/filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
orbit = module("cm_orbit_test", "96_cm_orbit.py")
recognition = module("cm_field_test", "97_cm_field_recognition.py")


class CMOrbitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = json.loads((orbit.DATA/"cm_orbit.json").read_text())
        with mp.workdps(85):
            cls.roots = [mp.mpc(*z) for z in cls.saved["field_root_action"]["complex_roots"]]
            cls.lookup = cls.saved["matching"]["point_to_root_index_zero_based"]
            cls.field,cls.basis,cls.values,cls.inverse,cls.basis_report = recognition.evaluation_basis(cls.roots)

    def setUp(self):
        self.precision = mp.workdps(85)
        self.precision.__enter__()

    def tearDown(self):
        self.precision.__exit__(None,None,None)

    def test_saturated_preimage_against_direct_integrality(self):
        image = matrix(QQ,[[2,0],[0,3],[1,1]])
        basis = orbit.preimage_lattice(matrix.identity(QQ,3),image)
        inverse = basis.inverse()
        for a in range(-9,10):
            for b in range(-9,10):
                value = vector(QQ,[QQ(a)/6,QQ(b)/6])
                self.assertEqual(all(v in ZZ for v in image*value),
                                 all(v in ZZ for v in inverse*value))
        with self.assertRaises(ValueError):
            orbit.preimage_lattice(matrix.identity(QQ,2),matrix(QQ,[[1,0],[0,0]]))

    def test_saved_embeddings_give_all_exact_classes(self):
        report,cm,classes = orbit.cm_orbit(self.saved["quaternion_export"])
        labels = report["class_labels_in_point_order"]
        self.assertEqual(sorted(labels),list(range(17)))
        self.assertEqual(classes.order(),17)
        self.assertTrue(all(row["ideal_norm_times_intertwiner_norm"] == "1" for row in report["entries"]))
        for i,j in [(0,7),(1,6),(2,5),(3,4),(8,8),(9,16),(10,15),(11,14),(12,13)]:
            self.assertEqual((labels[i]+labels[j])%17,0)
        action = self.saved["field_root_action"]
        match = orbit.match_frobenius(report,cm,classes,action,orbit.DATA/"expansion_geometry.json")
        self.assertEqual(match["point_to_root_index_zero_based"],self.lookup)
        self.assertEqual(match["beta_mod31"],19)
        self.assertGreaterEqual(match["padic_generator_match_valuation"],60)

    def test_matching_intertwines_class_action_and_frobenius(self):
        labels = self.saved["CM_orbit"]["class_labels_in_point_order"]
        power = self.saved["matching"]["prime_ideal_class"]
        frobenius = self.saved["field_root_action"]["complex_frobenius_31"]
        for i,label in enumerate(labels):
            other = labels.index((label+power)%17)
            self.assertEqual(self.lookup[other],frobenius[self.lookup[i]]-1)
            conjugate = labels.index((-label)%17)
            self.assertLess(abs(self.roots[self.lookup[conjugate]]-mp.conj(self.roots[self.lookup[i]])),mp.mpf("1e-75"))

    def test_stable_basis_recovers_known_exact_coordinates(self):
        theta = self.field.gen()
        element = 3*theta**2-7*theta+2
        power_matrix = matrix(QQ,[v.vector() for v in self.basis]).transpose()
        exact = power_matrix.solve_right(element.vector())
        recovered = self.inverse*mp.matrix([recognition.evaluate(element,r) for r in self.roots])
        self.assertLess(max(abs(recovered[i]-mp.mpf(str(exact[i]))) for i in range(17)),mp.mpf("1e-60"))
        self.assertLess(mp.mpf(self.basis_report["evaluation_matrix_condition_inf"]),100)

    def test_joint_recovery_of_known_field_element_with_noise(self):
        result = recognition.known_field_control(self.field,self.basis,self.roots,self.lookup,self.inverse)
        self.assertTrue(result["exact_element_recovered"])

    def test_height_cap_rejects_large_denominator_fit(self):
        ratios = [mp.mpf(1),mp.mpf(137)/139]
        result = recognition.projective_search(ratios,[mp.mpf("1e-25")]*2,0,height_cap=100)
        self.assertFalse(result["accepted_directions"])
        result = recognition.projective_search(ratios,[mp.mpf("1e-25")]*2,0,height_cap=139)
        self.assertIn([139,137],[row["primitive_vector"] for row in result["accepted_directions"]])

    def test_independent_value_check_rejects_a_corrupted_bank(self):
        exact = recognition.normalized_line(self.field.gen())
        truth = [recognition.evaluate(exact,self.roots[j]) for j in self.lookup]
        corrupt = list(truth)
        corrupt[4] += mp.mpf("1e-3")
        result = recognition.value_validation(exact,self.roots,self.lookup,
            {"training":truth,"held_out":corrupt},[mp.mpf("1e-12")]*17)
        self.assertFalse(result["fits_all_empirical_value_intervals"])
        self.assertGreater(mp.mpf(result["bank_maximum_scaled_errors"]["held_out"]),10**8)


if __name__ == "__main__":
    unittest.main()

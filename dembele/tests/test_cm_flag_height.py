"""D60 controls for exact exclusions, exterior powers and empirical boxes."""
from copy import deepcopy
import importlib.util
import itertools
import json
from pathlib import Path
import unittest

from sage.all import QQ, ZZ, matrix


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("cm_flag_height_test",ROOT/"dembele/pari/98_cm_flag_height.py")
height = importlib.util.module_from_spec(spec)
spec.loader.exec_module(height)


class CMFlagHeightTests(unittest.TestCase):
    def test_chart_is_invariant_under_complex_generator_changes(self):
        exact = matrix(height.GAUSSIAN,[[1,0,QQ(2)/7,-3],[0,1,QQ(5)/11,4]])
        imaginary = height.GAUSSIAN.gen()
        change = matrix(height.GAUSSIAN,[[1+imaginary,2],[-1,3-imaginary]])
        box,charts = height.chart_box({"current":exact,"changed":change*exact})
        self.assertEqual(charts["current"],charts["changed"])
        self.assertTrue(all(QQ(v) == 0 for row in box["radii"] for v in row))

    def test_pluecker_height_uses_the_saturated_plane(self):
        basis = matrix(QQ,[[2,0,0,4],[0,3,6,0]])
        change = matrix(QQ,[[QQ(17)/3,-5],[11,QQ(2)/7]])
        self.assertEqual(height.primitive_pluecker(basis),height.primitive_pluecker(change*basis))
        self.assertEqual(height.primitive_pluecker(basis),[1,2,0,0,-2,-4])
        # The same plane can contain different distinguished lines.
        self.assertNotEqual(height.primitive_pluecker(basis.matrix_from_rows([0])),
                            height.primitive_pluecker((change*basis).matrix_from_rows([0])))

    def test_exterior_gram_schmidt_lengths_are_pairwise_products(self):
        basis = matrix(ZZ,[[7,2,0,1],[1,3,2,0],[0,1,5,2],[2,0,1,4]])
        pairs = list(itertools.combinations(range(4),2))
        exterior = matrix(ZZ,[[basis.matrix_from_rows_and_columns(rows,cols).det()
                              for cols in pairs] for rows in pairs])
        squared = height.gram_schmidt_squared(basis)
        self.assertEqual(height.gram_schmidt_squared(exterior),[squared[i]*squared[j] for i,j in pairs])

    def test_exclusion_agrees_with_exhaustive_small_plane_check(self):
        # In Q^3 a primitive normal vector parametrizes every rational plane.
        # This box contains the height-15 plane z=x/3+2*y/5.
        box = {"centers":[["1/3"],["2/5"]],"radii":[["1/10000"],["1/10000"]]}
        cert = height.make_certificate(box,10**5)
        excluded = cert["excluded_height_inclusive"]
        self.assertLess(excluded,15)
        for a,b,c in itertools.product(range(-6,7),repeat=3):
            if c == 0 or max(abs(a),abs(b),abs(c)) > excluded:
                continue
            inside = abs(-QQ(a)/c-QQ(1)/3) <= QQ(1)/10000 and abs(-QQ(b)/c-QQ(2)/5) <= QQ(1)/10000
            self.assertFalse(inside)
        self.assertTrue(height.verify_certificate(box,cert))

    def test_tampered_certificate_is_rejected(self):
        box = {"centers":[["314159/1000000","271828/1000000"]],
               "radii":[["1/100000000","1/100000000"]]}
        cert = height.make_certificate(box,10**7)
        for key in ("excluded_height_inclusive","unimodular_transformation","gram_schmidt_squared_lengths"):
            wrong = deepcopy(cert)
            if key == "excluded_height_inclusive":
                wrong[key] += 1
            elif key == "unimodular_transformation":
                wrong[key][0][0] = str(ZZ(wrong[key][0][0])+1)
            else:
                wrong[key][0] = str(QQ(wrong[key][0])+1)
            with self.assertRaises(AssertionError):
                height.verify_certificate(box,wrong)

    def test_exact_boundary_and_invalid_inputs(self):
        self.assertEqual(height.strict_integer_sqrt(9),2)
        self.assertEqual(height.strict_integer_sqrt(QQ(9001)/1000),3)
        self.assertEqual(height.strict_integer_sqrt(QQ(1)/4),0)
        with self.assertRaises(ValueError):
            height.strict_integer_sqrt(0)
        with self.assertRaises(ValueError):
            height.chart_box({"current":matrix(height.GAUSSIAN,[[1,2,3],[2,4,6]])})
        with self.assertRaises(ValueError):
            height.make_certificate({"centers":[["1/3"]],"radii":[["-1/100"]]},100)

    def test_known_field_plane_survives_exclusion_and_is_recovered(self):
        source = json.loads((height.DATA/"cm_field_recognition.json").read_text())
        result = height.known_plane_control(source)
        self.assertTrue(result["known_plane_inside_box"])
        self.assertTrue(result["exact_plane_recovered_with_known_height"])
        self.assertLess(result["excluded_height_inclusive"],result["exact_pluecker_height"])

    def test_saved_certificates_verify_without_lattice_reduction(self):
        saved = json.loads((height.DATA/"cm_flag_height.json").read_text())
        self.assertEqual([row["subspace"] for row in saved["subspaces"]],["X","Y","span(X,Y)"])
        for result in saved["subspaces"]:
            self.assertTrue(height.verify_certificate(result["box"],result["best_certificate"]))


if __name__ == "__main__":
    unittest.main()

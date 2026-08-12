import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads(
    (ROOT / "data/computed/brauer_local_data.json").read_text()
)
IDEALS = json.loads(
    (ROOT / "data/computed/lift_field_ideals.json").read_text()
)


class BrauerLocalDataTests(unittest.TestCase):
    def test_relative_discriminant(self):
        extension = DATA["extension"]
        expected = 5**6 * 89**7 * 661**4
        self.assertEqual(int(extension["relative_discriminant_norm"]), expected)

    def test_local_degrees_sum_to_eight(self):
        for decompositions in DATA["local_decomposition"].values():
            for item in decompositions:
                self.assertEqual(
                    item["prime_count"]
                    * item["ramification_index"]
                    * item["residue_degree"],
                    8,
                )

    def test_unique_split_relevant_prime(self):
        split = [
            (rational_prime, item)
            for rational_prime, decompositions
            in DATA["local_decomposition"].items()
            for item in decompositions
            if item["local_degree"] == 1
        ]
        self.assertEqual(len(split), 1)
        self.assertEqual(split[0][0], "661")
        self.assertEqual(split[0][1]["prime_count"], 8)

    def test_polarization_ideals_are_narrowly_principal(self):
        self.assertEqual(IDEALS["class_group"]["invariants"], [2])
        self.assertEqual(IDEALS["narrow_class_group"]["invariants"], [2, 2])
        self.assertTrue(IDEALS["codifferent"]["narrowly_principal"])
        self.assertTrue(
            all(
                item["narrowly_principal"]
                for item in IDEALS["primes_above_2"]
            )
        )


if __name__ == "__main__":
    unittest.main()

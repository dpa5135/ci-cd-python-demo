"""Run with: python -m unittest discover -s tests -v"""

import unittest

from risk import classify_transaction


class RiskTests(unittest.TestCase):
    def test_small_transaction(self):
        self.assertEqual(classify_transaction(500), "Low Risk")

    def test_large_transaction(self):
        self.assertEqual(classify_transaction(15000), "High Risk")

    def test_exact_threshold(self):
        self.assertEqual(classify_transaction(10000), "Low Risk")

    def test_negative_amount_rejected(self):
        with self.assertRaises(ValueError):
            classify_transaction(-5)


if __name__ == "__main__":
    unittest.main()

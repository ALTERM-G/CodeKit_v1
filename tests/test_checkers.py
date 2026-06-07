import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.core.checkers import (
    is_prime_check,
    is_divisible,
    find_divisors,
    is_perfect_square,
    is_armstrong,
    is_happy
)

class TestCheckers(unittest.TestCase):

    def test_is_prime_check(self):
        """Tests the prime number checker."""
        self.assertEqual(is_prime_check("7"), "True")
        self.assertEqual(is_prime_check("10"), "False")
        self.assertEqual(is_prime_check("1"), "False")
        self.assertEqual(is_prime_check("invalid"), "Error: Invalid input")

    def test_is_divisible(self):
        """Tests the divisibility checker."""
        self.assertEqual(is_divisible("10", "2"), "True")
        self.assertEqual(is_divisible("10", "3"), "False")
        self.assertEqual(is_divisible("10", "0"), "Error: Division by zero")

    def test_number_properties(self):
        """Tests various number property checkers."""
        self.assertTrue(is_armstrong(153))
        self.assertFalse(is_armstrong(154))
        self.assertTrue(is_happy(19))
        self.assertFalse(is_happy(20))
        self.assertEqual(is_perfect_square("16"), "True")
        self.assertEqual(is_perfect_square("17"), "False")

if __name__ == '__main__':
    unittest.main()
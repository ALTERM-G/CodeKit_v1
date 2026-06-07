import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.core.analyzers import (
    calculate_ic,
    calculate_entropy,
    character_stats,
    extract_numbers
)

class TestAnalyzers(unittest.TestCase):

    def test_calculate_ic(self):
        """Tests the Index of Coincidence calculation."""
        self.assertAlmostEqual(calculate_ic("AAAAAAAAAA"), 1.0)
        self.assertAlmostEqual(calculate_ic("ababababab"), 40/90)
        self.assertLess(calculate_ic("the quick brown fox"), 0.1)

    def test_character_stats(self):
        """Tests the character statistics function."""
        stats = character_stats("Hello 123!")
        self.assertEqual(stats["total_characters"], 10)
        self.assertEqual(stats["letter_count"], 5)
        self.assertEqual(stats["digit_count"], 3)
        self.assertEqual(stats["punctuation_count"], 1)

    def test_extract_numbers(self):
        """Tests the number extraction function."""
        self.assertEqual(extract_numbers("data 10, -3.14, and 42."), [10, -3.14, 42])

if __name__ == '__main__':
    unittest.main()
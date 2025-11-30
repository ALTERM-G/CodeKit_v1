import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.core.dispatcher import detect_conversion_type

class TestDispatcher(unittest.TestCase):

    def test_dispatch_to_converter(self):
        """Tests that the dispatcher correctly calls a converter function."""
        result = detect_conversion_type("10", "Decimal to Binary")
        self.assertEqual(result, "1010")

    def test_dispatch_to_analyzer(self):
        """Tests that the dispatcher correctly calls an analyzer function."""
        result = detect_conversion_type("test", "Characters")
        self.assertIn("Total characters: 4", result)

    def test_dispatch_to_checker(self):
        """Tests that the dispatcher correctly calls a checker function."""
        result = detect_conversion_type("7", "P. Checker")
        self.assertEqual(result, "True")

    def test_dispatch_to_generator(self):
        """Tests that the dispatcher correctly calls a generator function."""
        result = detect_conversion_type("12", "Random Password Generator")
        self.assertEqual(len(result), 12)

if __name__ == '__main__':
    unittest.main()
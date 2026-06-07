import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.core.converters import (
    decimal_to_binary, binary_to_decimal,
    decimal_to_hexadecimal, hexadecimal_to_decimal,
    text_to_morse, morse_to_text,
    integer_to_roman, roman_to_integer,
    rot_n_encrypt
)

class TestConverters(unittest.TestCase):

    def test_numerical_conversions(self):
        """Tests conversions between different numerical bases."""
        self.assertEqual(decimal_to_binary("10"), "1010")
        self.assertEqual(binary_to_decimal("1010"), "10")
        self.assertEqual(decimal_to_hexadecimal("255"), "FF")
        self.assertEqual(hexadecimal_to_decimal("FF"), "255")
        with self.assertRaises(ValueError):
            binary_to_decimal("102") # Invalid binary

    def test_text_conversions(self):
        """Tests conversions between text and other representations like Morse code."""
        self.assertEqual(text_to_morse("HELLO WORLD"), ".... . .-.. .-.. ---   .-- --- .-. .-.. -..")
        self.assertEqual(morse_to_text(".... . .-.. .-.. ---"), "HELLO")

    def test_roman_numerals(self):
        """Tests conversions between integers and Roman numerals."""
        self.assertEqual(integer_to_roman("1994"), "MCMXCIV")
        self.assertEqual(integer_to_roman("58"), "LVIII")
        self.assertEqual(roman_to_integer("MCMXCIV"), "1994")
        self.assertEqual(roman_to_integer("LVIII"), "58")
        with self.assertRaises(ValueError):
            integer_to_roman("4000") # Out of range

    def test_rot_n(self):
        """Tests the ROT-N cipher."""
        self.assertEqual(rot_n_encrypt("HELLO", 13), "URYYB")
        self.assertEqual(rot_n_encrypt("PYTHON", 3), "SBWKRQ")
        self.assertEqual(rot_n_encrypt("xyz", 3), "abc")

    # You can add more tests for other converters like:
    # - test_base_n_conversions()
    # - test_aes_encryption_decryption()
    # - test_hashing_functions()

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import os
import uuid
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.core.generators import (
    password_generator,
    letters_generator,
    number_generator,
    random_id_generator,
    random_ip_generator
)

class TestGenerators(unittest.TestCase):

    def test_password_generator(self):
        """Tests the random password generator for correct length and character types."""
        length = 16
        password = password_generator(str(length))
        self.assertEqual(len(password), length)

    def test_letters_generator(self):
        """Tests the random letters generator for correct length and content."""
        length = 20
        letters = letters_generator(str(length))
        self.assertEqual(len(letters), length)
        self.assertTrue(letters.isalpha())

    def test_number_generator(self):
        """Tests the random number generator for correct length and content."""
        length = 10
        numbers = number_generator(str(length))
        self.assertEqual(len(numbers), length)
        self.assertTrue(numbers.isdigit())

    def test_random_id_generator(self):
        """Tests that the UUID generator creates the correct number of valid UUIDs."""
        count = 5
        ids = random_id_generator(str(count))
        self.assertEqual(len(ids), count)
        # Check if the first ID is a valid UUID
        try:
            uuid.UUID(ids[0], version=4)
        except ValueError:
            self.fail("random_id_generator did not produce a valid UUID")

    def test_random_ip_generator(self):
        """Tests that the IP address generator creates valid IPv4 addresses."""
        count = 5
        ips = random_ip_generator(str(count))
        self.assertEqual(len(ips), count)
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        self.assertTrue(ip_pattern.match(ips[0]))

if __name__ == '__main__':
    unittest.main()
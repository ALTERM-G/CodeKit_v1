import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.core.equation_generator import (
    generate_random_equation,
    generate_multiple_equations
)

class TestEquationGenerator(unittest.TestCase):

    def test_generate_random_equation(self):
        """Tests that a single random equation is a non-empty string in LaTeX format."""
        equation = generate_random_equation()
        self.assertIsInstance(equation, str)
        self.assertTrue(equation.startswith("$") and equation.endswith("$"))

    def test_generate_multiple_equations(self):
        """Tests that multiple equations are generated correctly."""
        num_equations = 5
        equations_str = generate_multiple_equations(str(num_equations))
        self.assertEqual(equations_str.count("Equation "), num_equations)

if __name__ == '__main__':
    unittest.main()
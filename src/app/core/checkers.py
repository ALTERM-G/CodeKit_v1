from .data import (
    ERROR_MESSAGES, LANGUAGE_PATTERNS
)
import math
import re
import time
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


def is_prime_check(n):
    """Checks if a given number is prime."""
    try:
        n = int(n)
        if n < 2:
            return "False"
        if n == 2:
            return "True"
        if n % 2 == 0:
            return "False"
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return "False"
        return "True"
    except Exception:
        return "Error: Invalid input"


def is_divisible(n, divisor):
    """Checks if a number is divisible by another number."""
    try:
        n = int(n)
        divisor = int(divisor)
        if divisor == 0:
            return "Error: Division by zero"
        return "True" if n % divisor == 0 else "False"
    except Exception:
        return "Error: Invalid input"


def find_divisors(n):
    """Finds all divisors of a given integer."""
    try:
        n = int(n)
        if n == 0:
            return "All integers except 0"
        if n < 0:
            n = abs(n)
        divisors = []
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                divisors.append(i)
                if i*i != n:
                    divisors.append(n // i)
        return sorted(divisors)
    except Exception:
        return "Error: Invalid input"


def prime_factors(n):
    """Finds the prime factors of a given integer."""
    try:
        n = int(n)
        if n < 2:
            return "No prime factors for numbers less than 2."
        if n > 10**18:
            return "Error: Number is too large for prime factorization in a reasonable time."

        factors = []
        start_time = time.time()

        while n % 2 == 0:
            factors.append(2)
            n //= 2
        f = 3
        while f * f <= n:
            if time.time() - start_time > 5:  # Timeout after 5 seconds
                factors.append("... (timed out after 5s)")
                return factors
            if n % f == 0:
                factors.append(f)
                n //= f
            else:
                f += 2
        if n > 1:
            factors.append(n)

        return factors
    except Exception:
        return "Error: Invalid input"


def is_perfect_square(n):
    """Checks if a number is a perfect square."""
    try:
        n = int(n)
        if n < 0:
            return "False"
        root = math.isqrt(n)
        return "True" if root * root == n else "False"
    except Exception:
        return "Error: Invalid input"


def is_perfect_cube(n):
    """Checks if a number is a perfect cube."""
    try:
        n = int(n)
        root = round(n ** (1/3))
        return "True" if root * root * root == n else "False"
    except Exception:
        return "Error: Invalid input"


def get_proper_divisors(n):
    """Returns a sorted list of proper divisors for a given number (excluding the number itself)."""
    if n <= 1:
        return []
    divisors = {1}
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return sorted(list(divisors))


def is_palindrome(n):
    """Checks if a number is a palindrome (reads the same forwards and backwards)."""
    return str(n) == str(n)[::-1]


def is_perfect(n):
    """Checks if a number is a perfect number (sum of proper divisors equals the number)."""
    if n < 1:
        return False
    divisors_sum = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors_sum += i
            if i*i != n:
                divisors_sum += n // i
    return divisors_sum == n and n != 1


def is_armstrong(n):
    """Checks if a number is an Armstrong number (narcissistic number)."""
    if n < 0:
        return False
    s = str(n)
    order = len(s)
    sum_val = sum(int(digit)**order for digit in s)
    return n == sum_val


def is_happy(n):
    """Checks if a number is a 'happy number'."""
    if n <= 0: return False
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(digit)**2 for digit in str(n))
    return n == 1


def is_increasing(n):
    """Checks if the digits of a number are in non-decreasing order."""
    s = str(n)
    return all(s[i] <= s[i+1] for i in range(len(s) - 1))


def is_decreasing(n):
    """Checks if the digits of a number are in non-increasing order."""
    s = str(n)
    return all(s[i] >= s[i+1] for i in range(len(s) - 1))


def is_fibonacci(n):
    """Checks if a number is a Fibonacci number."""
    if n < 0: return False
    a, b = 0, 1
    while a < n:
        a, b = b, a + b
    return a == n


def is_binary(n):
    """Checks if the string representation of a number consists only of '0' and '1'."""
    return all(c in '01' for c in str(n))


class HTMLValidator(HTMLParser):
    """A simple HTML parser to catch basic syntax errors."""
    def __init__(self):
        super().__init__()
        self.errors = []
    def handle_starttag(self, tag, attrs): pass
    def handle_endtag(self, tag): pass
    def error(self, message): self.errors.append(message)


def _check_brackets_and_quotes(code: str, lang: str) -> str:
    """Performs a basic check for balanced brackets and quotes in a code string."""
    stack = []
    brackets = {"(": ")", "[": "]", "{": "}"}
    in_string = None
    for line_num, line in enumerate(code.splitlines(), 1):
        for char in line:
            if in_string:
                if char == in_string: in_string = None
            elif char in ('"', "'"): in_string = char
            elif char in brackets: stack.append((char, line_num))
            elif char in brackets.values():
                if not stack or brackets[stack.pop()[0]] != char:
                    return f"{lang} Syntax Error: Mismatched bracket '{char}' on line {line_num}."
    if stack:
        unclosed_char, line = stack[-1]
        return f"{lang} Syntax Error: Unclosed bracket '{unclosed_char}' from line {line}."
    return f"{lang} syntax appears valid (basic structural check)."


def _has_valid_structure(code: str, lang: str) -> bool:
    """Checks if the code contains any recognizable keywords or structures for a given language."""
    if lang not in LANGUAGE_PATTERNS: return False
    patterns = LANGUAGE_PATTERNS[lang]
    for pattern, weight in patterns:
        if pattern.search(code): return True
    return False

def syntax_analysis(code: str, language: str = "Python") -> str:
    """Analyzes the syntax of a code string for a given language."""
    if language == "Python":
        try:
            compile(code, '<string>', 'exec')
            return "Python syntax is valid."
        except SyntaxError as e:
            return f"Python Syntax Error: {e.msg} on line {e.lineno}"
    elif language == "JSON":
        try:
            json.loads(code)
            return "JSON syntax is valid."
        except json.JSONDecodeError as e:
            return f"JSON Syntax Error: {e.msg} on line {e.lineno} column {e.colno}"
    elif language == "XML":
        try:
            ET.fromstring(code)
            return "XML syntax is valid."
        except ET.ParseError as e:
            return f"XML Syntax Error: {e}"
    elif language == "HTML":
        parser = HTMLValidator()
        parser.feed(code)
        return "HTML syntax is valid (basic check)." if not parser.errors else f"HTML Error: {parser.errors[0]}"
    elif language in ["JavaScript", "CSS", "TypeScript", "Java", "C#", "C++", "C", "PHP", "Ruby", "Go", "Rust", "SQL", "Bash/Shell"]:
        if not _has_valid_structure(code, language):
            return f"{language} Syntax Error: No valid keywords or code structure found."
        else:
            return _check_brackets_and_quotes(code, language)
    else:
        return f"Syntax analysis for {language} is not yet implemented."

def check_syntax(code: str, language: str) -> str:
    """A wrapper function to perform syntax checks for various languages."""
    if not code.strip(): return "No code provided to check."
    if language == 'Python':
        try:
            compile(code, '<string>', 'exec')
            return f"Python syntax is valid."
        except Exception as e: return f"Invalid Python syntax: {e}"
    elif language == 'JSON':
        try:
            json.loads(code)
            return f"JSON syntax is valid."
        except Exception as e: return f"Invalid JSON syntax: {e}"
    elif language == 'HTML':
        if re.search(r'<[a-zA-Z][^>]*>', code): return "HTML syntax appears valid (basic tag check)."
        else: return "Invalid HTML: No valid tags found."
    elif language == 'XML': return syntax_analysis(code, language)
    else: return syntax_analysis(code, language)
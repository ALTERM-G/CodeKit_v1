from Data_code import *
import json
import xml.etree.ElementTree as ET
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding, ec, dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Cipher import DES as CryptoDES
from Crypto.Cipher import DES3 as Crypto3DES
from Crypto.Cipher import Blowfish as CryptoBlowfish
from argon2 import PasswordHasher
from fractions import Fraction
import math
import hashlib
import bcrypt
import zlib
import secrets
import random
import uuid
import base64
import re
import time
import os
from html.parser import HTMLParser
import string
import subprocess
import pyfiglet
from colorama import init
from termcolor import colored
import sys
import re
from termcolor import colored
import pyfiglet

init(strip=not sys.stdout.isatty())


def decimal_to_binary(decimal_str):
    try:
        if not decimal_str.strip():
            raise ValueError("Input is empty")
        n = int(decimal_str)
        return bin(n)[2:]
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["decimal_to_binary"].format(e=e))


def binary_to_decimal(binary_str):
    try:
        if not binary_str.strip():
            raise ValueError("Input is empty")
        return str(int(binary_str.strip(), 2))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["binary_to_decimal"].format(e=e))


def decimal_to_octal(decimal_str):
    try:
        if not decimal_str.strip():
            raise ValueError("Input is empty")
        return oct(int(decimal_str))[2:]
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["decimal_to_octal"].format(e=e))


def octal_to_decimal(octal_str):
    try:
        if not octal_str.strip():
            raise ValueError("Input is empty")
        return str(int(octal_str.strip(), 8))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["octal_to_decimal"].format(e=e))


def decimal_to_hexadecimal(decimal_str):
    try:
        if not decimal_str.strip():
            raise ValueError("Input is empty")
        return hex(int(decimal_str))[2:].upper()
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["decimal_to_hex"].format(e=e))


def hexadecimal_to_decimal(hex_str):
    try:
        if not hex_str.strip():
            raise ValueError("Input is empty")
        return str(int(hex_str.strip(), 16))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["hex_to_decimal"].format(e=e))


def decimal_to_custom_base(decimal_str, base):
    try:
        n = int(decimal_str)
    except Exception:
        raise ValueError(ERROR_MESSAGES["custom"])
    try:
        base = int(base)
    except Exception:
        raise ValueError(ERROR_MESSAGES["custom_2"])
    if base < 2 or base > len(digits):
        raise ValueError(
            ERROR_MESSAGES["base_range"].format(max_len=len(digits)))
    if n == 0:
        return "0"
    neg = n < 0
    n = abs(n)
    result = ""
    while n > 0:
        result = digits[n % base] + result
        n //= base
    if neg:
        result = "-" + result
    return result


def custom_base_to_decimal(number_str, base):
    try:
        base = int(base)
    except Exception:
        raise ValueError(ERROR_MESSAGES["custom_2"])
    if base < 2 or base > len(digits):
        raise ValueError(
            ERROR_MESSAGES["base_range"].format(max_len=len(digits)))
    mapping = {ch: i for i, ch in enumerate(digits[:base])}
    mapping.update({ch.lower(): i for ch, i in mapping.items()})
    num = 0
    for ch in number_str.strip():
        if ch not in mapping:
            raise ValueError(
                ERROR_MESSAGES["invalid_char_for_base"].format(char=ch, base=base))
        num = num * base + mapping[ch]
    return str(num)


def text_to_morse(text):
    try:
        words = text.upper().split()
        morse_words = []
        for word in words:
            morse_letters = [MORSE_DICT.get(letter, '?') for letter in word]
            morse_words.append(' '.join(morse_letters))
        return '   '.join(morse_words)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["text_to_morse"].format(e=e))


def morse_to_text(morse_code):
    try:
        words = morse_code.strip().split('   ')
        decoded_words = []
        for word in words:
            letters = word.split()
            decoded_letters = [MORSE_TO_TEXT.get(l, '?') for l in letters]
            decoded_words.append(''.join(decoded_letters))
        return ' '.join(decoded_words)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["morse_to_text"].format(e=e))


def cesar_encrypt(text, shift=3):
    try:
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["cesar_encrypt"].format(e=e))


def cesar_decrypt(text, shift=3):
    try:
        return cesar_encrypt(text, -shift)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["cesar_decrypt"].format(e=e))


def text_to_braille(text):
    result = []
    for char in text:
        if char.isdigit():
            if not result or result[-1] != BRAILLE_NUMBER_PREFIX:
                result.append(BRAILLE_NUMBER_PREFIX)
            result.append(BRAILLE_DICT[char])
        else:
            result.append(BRAILLE_DICT.get(char.upper(), '?'))
    return ''.join(result)


def braille_to_text(braille_code):
    try:
        result = []
        i = 0
        while i < len(braille_code):
            ch = braille_code[i]
            if ch == BRAILLE_NUMBER_PREFIX and i + 1 < len(braille_code):
                next_ch = braille_code[i+1]
                key = BRAILLE_NUMBER_PREFIX + next_ch
                result.append(BRAILLE_TO_TEXT.get(key, '?'))
                i += 2
            else:
                result.append(BRAILLE_TO_TEXT.get(ch, '?'))
                i += 1
        return ''.join(result).upper()
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["braille_to_text"].format(e=e))


def rot_n_encrypt(text, n):
    n = int(n)
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + n) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + n) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)


def rot_n_decrypt(text, n):
    n = int(n)
    return rot_n_encrypt(text, -n)


def text_to_grid_cipher(text):
    try:
        text = text.upper()
        grid_cipher = []
        for char in text:
            if char in GRID_DICT:
                grid_cipher.append(GRID_DICT[char])
            else:
                grid_cipher.append('?')
        return '\u200B'.join(grid_cipher)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["text_to_pigpen"].format(e=e))


def grid_cipher_to_text(grid_cipher):
    try:
        inverse_grid_dict = {v: k for k, v in GRID_DICT.items()}
        symbols = grid_cipher.split('\u200B')
        decoded_text = [inverse_grid_dict.get(s, '?') for s in symbols]
        return ''.join(decoded_text)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["pigpen_to_text"].format(e=e))


def text_to_emoji(text):
    try:
        result = []
        for char in text.upper():
            if char in EMOJI_MAP:
                result.append(EMOJI_MAP[char])
            else:
                result.append(char)
        return "".join(result)
    except Exception as e:
        return f"Error: {e}"


def emoji_to_text(cipher_text):
    try:
        result = []
        for symbol in cipher_text:
            if symbol in REVERSE_EMOJI_MAP:
                result.append(REVERSE_EMOJI_MAP[symbol])
            else:
                result.append(symbol)
        return "".join(result)
    except Exception as e:
        return f"Error: {e}"


def _format_coef_var(coef, var="x", power=1):
    if coef == 0:
        return None
    abs_coef = abs(coef)
    if power == 0:
        body = f"{abs_coef}"
    elif power == 1:
        body = f"{var}" if abs_coef == 1 else f"{abs_coef}{var}"
    else:
        body = f"{var}^{power}" if abs_coef == 1 else f"{abs_coef}{var}^{power}"
    sign = "-" if coef < 0 else "+"
    return sign, body


def _join_terms(terms):
    if not terms:
        return "0"
    out = ""
    first = True
    for sign, body in terms:
        if first:
            out += (f"-{body}" if sign == "-" else f"{body}")
            first = False
        else:
            out += f" {sign} {body}"
    return out


def _format_linear(a, b):
    terms = []
    t = _format_coef_var(a, power=1)
    if t:
        terms.append(t)
    t = _format_coef_var(b, power=0)
    if t:
        terms.append(t)
    return _join_terms(terms)


def _format_quadratic(a, b, c):
    terms = []
    t = _format_coef_var(a, power=2)
    if t:
        terms.append(t)
    t = _format_coef_var(b, power=1)
    if t:
        terms.append(t)
    t = _format_coef_var(c, power=0)
    if t:
        terms.append(t)
    return _join_terms(terms)


def _format_cubic(a, b, c, d):
    terms = []
    t = _format_coef_var(a, power=3)
    if t:
        terms.append(t)
    t = _format_coef_var(b, power=2)
    if t:
        terms.append(t)
    t = _format_coef_var(c, power=1)
    if t:
        terms.append(t)
    t = _format_coef_var(d, power=0)
    if t:
        terms.append(t)
    return _join_terms(terms)


def _format_coeff_x_pair(coef, var="x"):
    if coef == 1:
        return var
    if coef == -1:
        return "-" + var
    return f"{coef}{var}"


def generate_random_equation():
    equation_types = [
        "polynomial", "exponential", "fractional",
        "radical", "logarithmic", "trigonometric",
        "exponential_polynomial", "log_polynomial", "radical_polynomial",
        "composite"
    ]
    weights = [0.2, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.1]
    eq_type = random.choices(equation_types, weights=weights, k=1)[0]
    if eq_type == "polynomial":
        return generate_polynomial()
    elif eq_type == "exponential":
        return generate_exponential()
    elif eq_type == "fractional":
        return generate_fractional()
    elif eq_type == "radical":
        return generate_radical()
    elif eq_type == "logarithmic":
        return generate_logarithmic()
    elif eq_type == "trigonometric":
        return generate_trigonometric()
    elif eq_type == "exponential_polynomial":
        return generate_exponential_polynomial()
    elif eq_type == "log_polynomial":
        return generate_log_polynomial()
    elif eq_type == "radical_polynomial":
        return generate_radical_polynomial()
    else:
        return generate_composite()


def generate_polynomial():
    if random.random() < 0.3:
        root1 = random.randint(-5, 5)
        root2 = random.randint(-5, 5)

        def factor(r):
            if r == 0:
                return "(x)"
            if r > 0:
                return f"(x - {r})"
            return f"(x + {abs(r)})"
        if root1 == root2:
            return f"$({factor(root1)})^2 = 0$".replace("($(", "(")
        else:
            return f"${factor(root1)}{factor(root2)} = 0$"
    elif random.random() < 0.65:
        a = random.randint(1, 5)
        b = random.randint(-5, 5)
        c = random.randint(-10, 10)
        d = random.randint(1, 5)
        e = random.randint(-10, 10)
        left = _format_quadratic(a, b, c)
        right = _format_linear(d, e)
        return f"${left} = {right}$"
    else:
        a = random.randint(1, 3)
        b = random.randint(-3, 3)
        c = random.randint(-5, 5)
        d = random.randint(-5, 5)
        poly = _format_cubic(a, b, c, d)
        return f"${poly} = 0$"


def generate_exponential():
    bases = [2, 3, 5]
    base1 = random.choice(bases)
    exponent_coeff = random.randint(1, 4)
    left_exp = "x" if exponent_coeff == 1 else f"{exponent_coeff}x"
    return f"${base1}^{{{left_exp}}} = ?$"


def generate_fractional():
    numerator_coeff = random.randint(1, 3)
    denominator = random.randint(2, 9)
    constant = random.randint(1, 5)
    numerator_term = "x" if numerator_coeff == 1 else f"{numerator_coeff}x"
    if random.random() < 0.5:
        return f"$\frac{{{numerator_term}}}{{{denominator}}} = {constant}$"
    else:
        numerator_const = random.randint(1, 5)
        return f"$\frac{{{numerator_term} + {numerator_const}}}{{{denominator}}} = {constant}$"


def generate_radical():
    coefficient = random.randint(1, 3)
    radicand_coeff = random.randint(1, 3)
    constant = random.randint(2, 5)
    radicand_term = "x" if radicand_coeff == 1 else f"{radicand_coeff}x"
    outside = "" if coefficient == 1 else f"{coefficient}"
    if random.random() < 0.5:
        return rf"${outside}\sqrt{{{radicand_term}}} = {constant}$"
    else:
        offset = random.randint(1, 5)
        return rf"$\sqrt{{{radicand_term} + {offset}}} = {constant}$"


def generate_logarithmic():
    coefficient = random.randint(1, 3)
    constant = random.randint(1, 5)
    term = "x" if coefficient == 1 else f"{coefficient}x"
    if random.random() < 0.5:
        return rf"$\ln({term}) = {constant}$"
    else:
        offset = random.randint(1, 3)
        return rf"$\ln({term} + {offset}) = {constant}$"


def generate_trigonometric():
    func = random.choice([r"\\sin", r"\\cos", r"\\tan"])
    coefficient = random.randint(1, 3)
    coeff_str = "" if coefficient == 1 else f"{coefficient}"
    angles = ["0", r"\\frac{\\pi}{6}", r"\\frac{\\pi}{4}",
              r"\\frac{\\pi}{3}", r"\\frac{\\pi}{2}"]
    constant = random.choice(angles)
    inside = "x" if coefficient == 1 else f"{coefficient}x"
    if random.random() < 0.5:
        return f"${func}({inside}) = {constant}$"
    else:
        offset = random.choice(
            ["0", r"\\frac{\\pi}{6}", r"\\frac{\\pi}{4}", r"\\frac{\\pi}{3}"])
        return f"${func}({inside} + {offset}) = {constant}$"


def generate_exponential_polynomial():
    base = random.choice([2, 3, 5])
    exponent_coeff = random.randint(1, 2)
    exponent_part = "x" if exponent_coeff == 1 else f"{exponent_coeff}x"
    poly_coeff = random.randint(1, 3)
    constant = random.randint(1, 5)
    rhs = _format_linear(poly_coeff, constant)
    return f"${base}^{{{exponent_part}}} = {rhs}$"


def generate_log_polynomial():
    log_coeff = random.randint(1, 2)
    poly_coeff = random.randint(1, 3)
    constant = random.randint(1, 5)
    left = "x" if log_coeff == 1 else f"{log_coeff}x"
    right = _format_linear(poly_coeff, constant)
    return rf"$\ln({left}) = {right}$"


def generate_radical_polynomial():
    radical_coeff = random.randint(1, 2)
    poly_coeff = random.randint(1, 3)
    constant = random.randint(1, 5)
    rad = "x" if radical_coeff == 1 else f"{radical_coeff}x"
    rhs = _format_linear(poly_coeff, constant)
    return rf"$\sqrt{{{rad}}} = {rhs}$"


def generate_composite():
    num_operations = random.randint(2, 3)
    operations = []
    for _ in range(num_operations):
        op_type = random.choice(["exp", "log", "rad", "frac", "poly", "trig"])
        if op_type == "exp":
            base = random.choice([2, 3, 5])
            exp = random.randint(1, 2)
            exp_part = "x" if exp == 1 else f"{exp}x"
            operations.append(f"{base}^{{{exp_part}}}")
        elif op_type == "log":
            coeff = random.randint(1, 2)
            left = "x" if coeff == 1 else f"{coeff}x"
            operations.append(f"\\ln({left})")
        elif op_type == "rad":
            coeff = random.randint(1, 2)
            rad = "x" if coeff == 1 else f"{coeff}x"
            operations.append(f"\\sqrt{{{rad}}}")
        elif op_type == "frac":
            num_coeff = random.randint(1, 2)
            den = random.randint(2, 5)
            num = "x" if num_coeff == 1 else f"{num_coeff}x"
            operations.append(f"\\frac{{{num}}}{{{den}}}")
        elif op_type == "poly":
            coeff = random.randint(1, 3)
            const = random.randint(0, 3)
            rhs = _format_linear(coeff, const)
            operations.append(f"{rhs}")
        else:
            func = random.choice([r"\\sin", r"\\cos", r"\\tan"])
            coeff = random.randint(1, 2)
            inside = "x" if coeff == 1 else f"{coeff}x"
            operations.append(f"{func}({inside})")

    operators = [random.choice(["+", "-"]) for _ in range(num_operations - 1)]
    equation = operations[0]
    for i in range(num_operations - 1):
        equation += f" {operators[i]} {operations[i+1]}"
    constant = random.randint(1, 10)
    return f"${equation} = {constant}$"


def generate_multiple_equations(n):
    try:
        n = int(n)
        if n < 1:
            return "Error: Number must be at least 1"
        if n > 10000:
            return "Error: Maximum 10000 equations"
        equations = []
        generated_equations = set()
        for i in range(min(n, 10000)):
            for _ in range(10):
                eq = generate_random_equation()
                if eq not in generated_equations:
                    generated_equations.add(eq)
                    equations.append(f"Equation {i+1}: {eq}")
                    break
            else:
                equations.append(f"Equation {i+1}: {eq}")
        return "\n".join(equations)
    except ValueError:
        return "Error: Please enter a valid number"
    except Exception as e:
        return f"Error: {e}"


def _egcd(a: int, b: int):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = _egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def _modinv(a: int, m: int):
    g, x, _ = _egcd(a % m, m)
    if g != 1:
        raise ValueError(f"No modular inverse for a={a} (gcd != 1) modulo {m}")
    return x % m


def _parse_affine_key(key):
    if key is None or key == "":
        return (5, 8)
    if isinstance(key, (tuple, list)):
        if len(key) >= 2:
            return (int(key[0]), int(key[1]))
        elif len(key) == 1:
            return (int(key[0]), 0)
    if isinstance(key, str):
        s = key.strip()
        if "," in s:
            parts = [p.strip() for p in s.split(",") if p.strip() != ""]
            if len(parts) >= 2:
                return (int(parts[0]), int(parts[1]))
            elif len(parts) == 1:
                return (int(parts[0]), 0)
        elif " " in s:
            parts = [p.strip() for p in s.split() if p.strip() != ""]
            if len(parts) >= 2:
                return (int(parts[0]), int(parts[1]))
            elif len(parts) == 1:
                return (int(parts[0]), 0)
        else:
            try:
                return (int(s), 0)
            except Exception:
                pass
    try:
        return (int(key), 0)
    except Exception:
        raise ValueError(ERROR_MESSAGES["affine_key_format"])


def affine_encrypt(text: str, key=None) -> str:
    try:
        a, b = _parse_affine_key(key)
        a = int(a)
        b = int(b) % 26
        g, _, _ = _egcd(a, 26)
        if g != 1:
            raise ValueError(ERROR_MESSAGES["affine_coprime"].format(a=a))
        out = []
        for ch in text:
            if ch.isalpha():
                if ch.isupper():
                    base = ord('A')
                else:
                    base = ord('a')
                x = ord(ch) - base
                y = (a * x + b) % 26
                out.append(chr(y + base))
            else:
                out.append(ch)
        return ''.join(out)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["affine_encrypt"].format(e=e))


def affine_decrypt(cipher_text: str, key=None) -> str:
    try:
        a, b = _parse_affine_key(key)
        a = int(a)
        b = int(b) % 26
        a_inv = _modinv(a, 26)
        out = []
        for ch in cipher_text:
            if ch.isalpha():
                if ch.isupper():
                    base = ord('A')
                else:
                    base = ord('a')
                y = ord(ch) - base
                x = (a_inv * (y - b)) % 26
                out.append(chr(x + base))
            else:
                out.append(ch)
        return ''.join(out)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["affine_decrypt"].format(e=e))


def ascii_encode(text: str) -> str:
    try:
        codes = []
        for c in text:
            if ord(c) > 127:
                raise ValueError(ERROR_MESSAGES["non_ascii_char"].format(c=c))
            codes.append(str(ord(c)))
        return " ".join(codes)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["ascii_encode"].format(e=e))


def ascii_decode(ascii_str: str) -> str:
    try:
        codes = ascii_str.strip().split()
        return ''.join(chr(int(c)) for c in codes)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["ascii_decode"].format(e=e))


def iso_n_encode(text: str, encoding="iso-8859-1", n=None) -> str:
    try:
        if n is not None:
            text = ''.join(chr((ord(c) + int(n)) % 256) for c in text)
        encoded_bytes = text.encode(encoding)
        return base64.b64encode(encoded_bytes).decode('ascii')
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["iso_encode"].format(encoding=encoding, e=e))


def iso_n_decode(encoded: str, encoding="iso-8859-1", n=None) -> str:
    try:
        encoded_bytes = base64.b64decode(encoded)
        text = encoded_bytes.decode(encoding)
        if n is not None:
            text = ''.join(chr((ord(c) - int(n)) % 256) for c in text)
        return text
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["iso_decode"].format(encoding=encoding, e=e))


def utf_n_encode(text: str, encoding="utf-8", n=None) -> str:
    try:
        if n is not None:
            text = ''.join(chr((ord(c) + int(n)) % 0x110000) for c in text)
        encoded_bytes = text.encode(encoding)
        return base64.b64encode(encoded_bytes).decode('ascii')
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["utf_encode"].format(encoding=encoding, e=e))


def utf_n_decode(encoded: str, encoding="utf-8", n=None) -> str:
    try:
        encoded_bytes = base64.b64decode(encoded)
        text = encoded_bytes.decode(encoding)
        if n is not None:
            text = ''.join(chr((ord(c) - int(n)) % 0x110000) for c in text)
        return text
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["utf_decode"].format(encoding=encoding, e=e))


def _add_padding(s: str, block: int) -> str:
    missing = (-len(s)) % block
    return s + ("=" * missing if missing else "")


def int_to_base(n: int, alphabet: str) -> str:
    if n == 0:
        return alphabet[0]
    base = len(alphabet)
    neg = n < 0
    n = abs(n)
    res = ""
    while n > 0:
        n, r = divmod(n, base)
        res = alphabet[r] + res
    return "-" + res if neg else res


def base_to_int(s: str, alphabet: str) -> int:
    s = s.strip()
    if not s:
        return 0
    neg = s.startswith('-')
    if neg:
        s = s[1:]
    base = len(alphabet)
    val = 0
    for ch in s:
        idx = alphabet.find(ch)
        if idx == -1:
            raise ValueError(
                ERROR_MESSAGES["invalid_char_for_base"].format(char=ch, base=base))
        val = val * base + idx
    return -val if neg else val


def word_to_basen(text: str, base: int) -> str:
    data = text.encode("utf-8")
    if base == 2:
        return " ".join(f"{b:08b}" for b in data)
    if base == 8:
        return " ".join(f"{b:03o}" for b in data)
    if base == 10:
        return " ".join(str(b) for b in data)
    if base == 16:
        return " ".join(f"{b:02X}" for b in data)
    if base == 32:
        return base64.b32encode(data).decode("ascii")
    if base == 36:
        n = int.from_bytes(data, "big")
        return int_to_base(n, alphabet_base36)
    if base == 58:
        n = int.from_bytes(data, "big")
        return int_to_base(n, alphabet_base58)
    if base == 62:
        n = int.from_bytes(data, "big")
        return int_to_base(n, alphabet_base62)
    if base == 64:
        return base64.b64encode(data).decode("ascii")
    if base == 85:
        return base64.b85encode(data).decode("ascii")
    if base == -1:
        return base64.urlsafe_b64encode(data).decode("ascii")
    raise ValueError(ERROR_MESSAGES["unsupported_base"].format(base=base))


def basen_to_word(encoded: str, base: int) -> str:
    encoded = encoded.strip()
    if base == 2:
        data = bytes(int(t, 2) for t in encoded.split())
        return data.decode("utf-8")
    if base == 8:
        data = bytes(int(t, 8) for t in encoded.split())
        return data.decode("utf-8")
    if base == 10:
        data = bytes(int(t) for t in encoded.split())
        return data.decode("utf-8")
    if base == 16:
        hex_str = encoded.replace(" ", "")
        data = bytes.fromhex(hex_str)
        return data.decode("utf-8")
    if base == 32:
        s = _add_padding(encoded.replace(" ", "").upper(), 8)
        data = base64.b32decode(s, casefold=True)
        return data.decode("utf-8")
    if base == 36:
        n = base_to_int(encoded.upper(), alphabet_base36)
        data = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big")
        return data.decode("utf-8")
    if base == 58:
        n = base_to_int(encoded, alphabet_base58)
        data = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big")
        return data.decode("utf-8")
    if base == 62:
        n = base_to_int(encoded, alphabet_base62)
        data = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big")
        return data.decode("utf-8")
    if base == 64:
        s = _add_padding(encoded.replace(" ", ""), 4)
        data = base64.b64decode(s)
        return data.decode("utf-8")
    if base == 85:
        data = base64.b85decode(encoded)
        return data.decode("utf-8")
    if base == -1:
        s = _add_padding(encoded.replace(" ", ""), 4)
        data = base64.urlsafe_b64decode(s)
        return data.decode("utf-8")
    raise ValueError(ERROR_MESSAGES["unsupported_base"].format(base=base))


def password_generator(length):
    try:
        length = int(length)
        if length < 4:
            raise ValueError(ERROR_MESSAGES["password_error"])
        if length > max_length:
            raise ValueError(f"Password length must not exceed {max_length}")
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["password_generator"].format(e=e))


def letters_generator(length):
    try:
        length = int(length)
        if length < 4:
            raise ValueError(ERROR_MESSAGES["letter_error"])
        if length > max_length:
            raise ValueError(f"Password length must not exceed {max_length}")
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["password_generator"].format(e=e))


def number_generator(length):
    try:
        length = int(length)
        if length < 1:
            raise ValueError(ERROR_MESSAGES["number_error"])
        elif length > max_length:
            raise ValueError(f"Number length must not exceed {max_length}")
        number = ''.join(secrets.choice(numbers) for _ in range(length))
        return number
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["number_generator"].format(e=e))


def generate_coprimes(n):
    try:
        n = int(n)
        if n < 1:
            raise ValueError("Count must be at least 1")
        if n > 1000000:
            raise ValueError("Count cannot exceed 1,000,000")
        coprimes = set()
        max_attempts = n * 10
        while len(coprimes) < n and max_attempts > 0:
            a = random.randint(2, 1000000)
            b = random.randint(1, a-1)
            if math.gcd(a, b) == 1:
                coprimes.add((a, b))
            max_attempts -= 1
        return list(coprimes)[:n]
    except Exception as e:
        raise ValueError(f"Coprime generation failed: {e}")


def random_id_generator(count: int) -> list:
    try:
        count = int(count)
        if count < 1:
            raise ValueError("Count must be at least 1")
        if count > max_length_3:
            raise ValueError("Count cannot exceed 1000")

        return [str(uuid.uuid4()) for _ in range(count)]
    except Exception as e:
        raise ValueError(f"ID generation failed: {e}")


def random_ip_generator(count: int) -> list:
    try:
        count = int(count)
        if count < 1:
            raise ValueError("Count must be at least 1")
        if count > max_length_3:
            raise ValueError("Count cannot exceed 1000")
        ips = []
        for _ in range(count):
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            ips.append(ip)
        return ips
    except Exception as e:
        raise ValueError(f"IP generation failed: {e}")


def derive_key(password: str, length: int = 32) -> bytes:
    salt = b'salt1234'
    kdf = Scrypt(salt=salt, length=length, n=2**14,
                 r=8, p=1, backend=default_backend())
    return kdf.derive(password.encode())


def pad_data(data: bytes, block_size: int = 128) -> bytes:
    padder = padding.PKCS7(block_size).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(data: bytes, block_size: int = 128) -> bytes:
    unpadder = padding.PKCS7(block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def aes_encrypt(text: str, password: str) -> str:
    key = derive_key(password, 32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    padded_text = pad_data(text.encode())
    ct = encryptor.update(padded_text) + encryptor.finalize()
    return base64.b64encode(iv + ct).decode()


def aes_decrypt(ciphertext_b64: str, password: str) -> str:
    key = derive_key(password, 32)
    data = base64.b64decode(ciphertext_b64)
    iv = data[:16]
    ct = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ct) + decryptor.finalize()
    return unpad_data(padded_text).decode()


def chacha20_encrypt(text: str, password: str) -> str:
    key = derive_key(password, 32)
    nonce = os.urandom(16)
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(text.encode()) + encryptor.finalize()
    return base64.b64encode(nonce + ct).decode()


def chacha20_decrypt(ciphertext_b64: str, password: str) -> str:
    key = derive_key(password, 32)
    data = base64.b64decode(ciphertext_b64)
    nonce = data[:16]
    ct = data[16:]
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(ct) + decryptor.finalize()).decode()


def des_encrypt(text: str, password: str) -> str:
    key = derive_key(password, 8)
    iv = os.urandom(8)
    cipher = CryptoDES.new(key, CryptoDES.MODE_CBC, iv)
    padded_text = pad_data(text.encode(), 64)
    ct = cipher.encrypt(padded_text)
    return base64.b64encode(iv + ct).decode()


def des_decrypt(ciphertext_b64: str, password: str) -> str:
    key = derive_key(password, 8)
    data = base64.b64decode(ciphertext_b64)
    iv, ct = data[:8], data[8:]
    cipher = CryptoDES.new(key, CryptoDES.MODE_CBC, iv)
    padded_text = cipher.decrypt(ct)
    return unpad_data(padded_text, 64).decode()


def triple_des_encrypt(text: str, password: str) -> str:
    key = derive_key(password, 24)
    iv = os.urandom(8)
    cipher = Crypto3DES.new(key, Crypto3DES.MODE_CBC, iv)
    padded_text = pad_data(text.encode(), 64)
    ct = cipher.encrypt(padded_text)
    return base64.b64encode(iv + ct).decode()


def triple_des_decrypt(ciphertext_b64: str, password: str) -> str:
    key = derive_key(password, 24)
    data = base64.b64decode(ciphertext_b64)
    iv, ct = data[:8], data[8:]
    cipher = Crypto3DES.new(key, Crypto3DES.MODE_CBC, iv)
    padded_text = cipher.decrypt(ct)
    return unpad_data(padded_text, 64).decode()


def blowfish_encrypt(text: str, password: str) -> str:
    key = derive_key(password, 32)
    iv = os.urandom(8)
    cipher = CryptoBlowfish.new(key, CryptoBlowfish.MODE_CBC, iv)
    padded_text = pad_data(text.encode(), 64)
    ct = cipher.encrypt(padded_text)
    return base64.b64encode(iv + ct).decode()


def blowfish_decrypt(ciphertext_b64: str, password: str) -> str:
    key = derive_key(password, 32)
    data = base64.b64decode(ciphertext_b64)
    iv, ct = data[:8], data[8:]
    cipher = CryptoBlowfish.new(key, CryptoBlowfish.MODE_CBC, iv)
    padded_text = cipher.decrypt(ct)
    return unpad_data(padded_text, 64).decode()


def rsa_generate_keys(password: str = None, key_size: int = 2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    encryption_algo = serialization.BestAvailableEncryption(
        password.encode()) if password else serialization.NoEncryption()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption_algo
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem.decode(), public_pem.decode()


def rsa_encrypt(text: str, public_key_pem: str) -> str:
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    ciphertext = public_key.encrypt(
        text.encode(),
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode()


def rsa_decrypt(ciphertext_b64: str, private_key_pem: str, password: str = None) -> str:
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=password.encode() if password else None
    )
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = private_key.decrypt(
        ciphertext,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()


def rsa_sign(text: str, private_key_pem: str, password: str = None) -> str:
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=password.encode() if password else None
    )
    signature = private_key.sign(
        text.encode(),
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()


def rsa_verify(text: str, signature_b64: str, public_key_pem: str) -> bool:
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    signature = base64.b64decode(signature_b64)
    try:
        public_key.verify(
            signature,
            text.encode(),
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def ecc_generate_keys(curve_name: str = "SECP256R1"):
    curve_map = {
        "SECP256R1": ec.SECP256R1(),
        "SECP384R1": ec.SECP384R1(),
        "SECP521R1": ec.SECP521R1(),
        "SECP256K1": ec.SECP256K1(),
    }
    curve = curve_map.get(curve_name)
    private_key = ec.generate_private_key(curve)
    public_key = private_key.public_key()
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return priv_pem.decode(), pub_pem.decode()


def ecc_encrypt(plaintext: str, public_pem: str) -> str:
    try:
        public_key = serialization.load_pem_public_key(public_pem.encode())
        ephemeral_private = ec.generate_private_key(public_key.curve)
        ephemeral_public = ephemeral_private.public_key()
        shared_key = ephemeral_private.exchange(ec.ECDH(), public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256
            salt=None,
            info=b'ECIES encryption'
        ).derive(shared_key)
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(
            plaintext.encode()) + encryptor.finalize()
        ephemeral_pub_bytes = ephemeral_public.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        return base64.b64encode(ephemeral_pub_bytes + iv + encryptor.tag + ciphertext).decode()
    except Exception as e:
        raise ValueError(f"ECC encryption failed: {e}")


def ecc_decrypt(ciphertext_b64: str, private_pem: str) -> str:
    try:
        private_key = serialization.load_pem_private_key(
            private_pem.encode(), password=None
        )
        data = base64.b64decode(ciphertext_b64)
        ephemeral_pub_bytes = data[:65]
        iv = data[65:77]
        tag = data[77:93]
        ciphertext = data[93:]
        ephemeral_public = ec.EllipticCurvePublicKey.from_encoded_point(
            ec.SECP256R1(), ephemeral_pub_bytes
        )
        shared_key = private_key.exchange(ec.ECDH(), ephemeral_public)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ECIES encryption'
        ).derive(shared_key)
        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()
    except Exception as e:
        raise ValueError(f"ECC decryption failed: {e}")


def ecc_sign(message: str, private_pem: str) -> str:
    private_key = serialization.load_pem_private_key(
        private_pem.encode(), password=None)
    signature = private_key.sign(
        message.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    return base64.b64encode(signature).decode()


def ecc_verify(message: str, signature_b64: str, public_pem: str) -> bool:
    public_key = serialization.load_pem_public_key(public_pem.encode())
    signature = base64.b64decode(signature_b64)
    try:
        public_key.verify(signature, message.encode(),
                          ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False


script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")
ELGAMAL_CACHE_FILE = os.path.join(data_dir, "elgamal_params.json")


def _load_elgamal_params():
    if os.path.isfile(ELGAMAL_CACHE_FILE):
        try:
            with open(ELGAMAL_CACHE_FILE, 'r') as f:
                cached_data = json.load(f)
                for size, pem_data in cached_data.items():
                    if int(size) not in ELGAMAL_PARAMETERS:
                        ELGAMAL_PARAMETERS[int(size)] = serialization.load_pem_parameters(
                            pem_data.encode()
                        )
        except (json.JSONDecodeError, IOError):
            pass


def _save_elgamal_params():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    with open(ELGAMAL_CACHE_FILE, 'w') as f:
        json.dump({size: params.parameter_bytes(serialization.Encoding.PEM,
                  serialization.ParameterFormat.PKCS3).decode() for size, params in ELGAMAL_PARAMETERS.items()}, f)


def elgamal_generate_keys(key_size: int = 2048):
    try:
        if key_size < 2048:
            raise ValueError(ERROR_MESSAGES["elgamal_keysize"])
        if key_size > 4096:
            raise ValueError("Key size too large (max 4096 bits)")

        _load_elgamal_params()

        if key_size not in ELGAMAL_PARAMETERS:
            ELGAMAL_PARAMETERS[key_size] = dh.generate_parameters(
                generator=2,
                key_size=key_size
            )
            _save_elgamal_params()
        parameters = ELGAMAL_PARAMETERS.get(key_size)
        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return priv_pem.decode(), pub_pem.decode()
    except Exception as e:
        raise ValueError(f"ElGamal key generation failed: {e}")


def elgamal_encrypt(plaintext: str, public_pem: str) -> str:
    try:
        public_key = serialization.load_pem_public_key(public_pem.encode())
        parameters = public_key.parameters()
        ephemeral_private = parameters.generate_private_key()
        ephemeral_public = ephemeral_private.public_key()
        shared_key = ephemeral_private.exchange(public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ElGamal encryption'
        ).derive(shared_key)
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(
            plaintext.encode()) + encryptor.finalize()
        ephemeral_pub_der = ephemeral_public.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        ephemeral_len = len(ephemeral_pub_der).to_bytes(4, 'big')
        return base64.b64encode(ephemeral_len + ephemeral_pub_der + iv + encryptor.tag + ciphertext).decode()
    except Exception as e:
        raise ValueError(f"ElGamal encryption failed: {e}")


def elgamal_decrypt(ciphertext_b64: str, private_pem: str) -> str:
    try:
        private_key = serialization.load_pem_private_key(
            private_pem.encode(), password=None
        )
        data = base64.b64decode(ciphertext_b64)
        ephemeral_len = int.from_bytes(data[:4], 'big')
        ephemeral_pub_der = data[4:4 + ephemeral_len]
        iv_start = 4 + ephemeral_len
        tag_start = iv_start + 12
        ciphertext_start = tag_start + 16
        iv = data[iv_start:tag_start]
        tag = data[tag_start:ciphertext_start]
        ciphertext = data[ciphertext_start:]
        ephemeral_public = serialization.load_der_public_key(
            ephemeral_pub_der
        )
        shared_key = private_key.exchange(ephemeral_public)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ElGamal encryption'
        ).derive(shared_key)
        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()
    except Exception as e:
        raise ValueError(f"ElGamal decryption failed: {e}")


def _wrap_base64_body(body: str, header: str) -> str:
    b = "".join(body.split())
    lines = [b[i:i+64] for i in range(0, len(b), 64)]
    return f"-----BEGIN {header}-----\n" + "\n".join(lines) + f"\n-----END {header}-----\n"


def parse_pem_and_type(key_text: str) -> tuple[str, str]:
    if not key_text or not key_text.strip():
        raise ValueError("Empty key")
    s = key_text.strip().replace("\\n", "\n")
    if "-----BEGIN " in s and "-----END " in s:
        try:
            serialization.load_pem_private_key(s.encode(), password=None)
            return (s if s.endswith("\n") else s + "\n", "private")
        except Exception:
            pass
        try:
            serialization.load_pem_public_key(s.encode())
            return (s if s.endswith("\n") else s + "\n", "public")
        except Exception:
            pass
        raise ValueError(
            "PEM found but type not recognized (neither private nor public)")
    body = "".join(s.split())
    for header in ("RSA PRIVATE KEY", "PRIVATE KEY"):
        cand = _wrap_base64_body(body, header)
        try:
            serialization.load_pem_private_key(cand.encode(), password=None)
            return (cand, "private")
        except Exception:
            pass
    cand = _wrap_base64_body(body, "PUBLIC KEY")
    try:
        serialization.load_pem_public_key(cand.encode())
        return (cand, "public")
    except Exception:
        pass
    raise ValueError("Could not interpret key as public or private PEM")


ph = PasswordHasher()


def sha3_hash(text: str) -> str:
    try:
        return hashlib.sha3_256(text.encode()).hexdigest()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} SHA-3: {e}"


def sha256_hash(text: str) -> str:
    try:
        return hashlib.sha256(text.encode()).hexdigest()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} SHA-256: {e}"


def sha512_hash(text: str) -> str:
    try:
        return hashlib.sha512(text.encode()).hexdigest()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} SHA-512: {e}"


def bcrypt_hash(text: str) -> str:
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(text.encode(), salt)
        return hashed.decode()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} bcrypt: {e}"


def scrypt_hash(text: str, salt: bytes = None) -> str:
    try:
        if salt is None:
            salt = bcrypt.gensalt()
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
        )
        key = kdf.derive(text.encode())
        return key.hex()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} scrypt: {e}"


def argon2_hash(text: str) -> str:
    try:
        return ph.hash(text)
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} Argon2: {e}"


def md5_checksum(text: str) -> str:
    try:
        if not text:
            raise ValueError(ERROR_MESSAGES["empty_input"])
        return hashlib.md5(text.encode()).hexdigest()
    except Exception as e:
        raise ValueError(f"MD5 checksum failed: {e}")


def sha1_checksum(text: str) -> str:
    try:
        if not text:
            raise ValueError(ERROR_MESSAGES["empty_input"])
        return hashlib.sha1(text.encode()).hexdigest()
    except Exception as e:
        raise ValueError(f"SHA-1 checksum failed: {e}")


def crc32_checksum(text: str) -> str:
    try:
        if not text:
            raise ValueError(ERROR_MESSAGES["empty_input"])
        return format(zlib.crc32(text.encode()) & 0xFFFFFFFF, '08x')
    except Exception as e:
        raise ValueError(f"CRC32 checksum failed: {e}")


def adler32_checksum(text: str) -> str:
    try:
        if not text:
            raise ValueError(ERROR_MESSAGES["empty_input"])
        return format(zlib.adler32(text.encode()) & 0xFFFFFFFF, '08x')
    except Exception as e:
        raise ValueError(f"Adler-32 checksum failed: {e}")


def sha1_hash(text: str) -> str:
    try:
        text_bytes = text.encode('utf-8')
        sha1 = hashlib.sha1()
        sha1.update(text_bytes)
        return sha1.hexdigest()
    except Exception as e:
        raise ValueError(f"SHA-1 hashing failed: {e}")


def is_prime_check(n):
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
    try:
        n = int(n)
        divisor = int(divisor)
        if divisor == 0:
            return "Error: Division by zero"
        return "True" if n % divisor == 0 else "False"
    except Exception:
        return "Error: Invalid input"


def find_divisors(n):
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
    try:
        n = int(n)
        if n < 0:
            return "False"
        root = math.isqrt(n)
        return "True" if root * root == n else "False"
    except Exception:
        return "Error: Invalid input"


def is_perfect_cube(n):
    try:
        n = int(n)
        root = round(n ** (1/3))
        return "True" if root * root * root == n else "False"
    except Exception:
        return "Error: Invalid input"


def convert_length(value, from_unit, to_unit):
    to_meter = {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'km': 1000.0,
        'inch': 0.0254,
        'ft': 0.3048,
        'yard': 0.9144,
        'mile': 1609.344
    }
    meters = value * to_meter[from_unit]
    return meters / to_meter[to_unit]


def convert_mass(value, from_unit, to_unit):
    to_gram = {
        'g': 1.0,
        'kg': 1000.0,
        'mg': 0.001,
        'ton': 1000000.0,
        'lb': 453.592,
        'oz': 28.3495
    }
    grams = value * to_gram[from_unit]
    return grams / to_gram[to_unit]


def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'C':
        celsius = value
    elif from_unit == 'K':
        celsius = value - 273.15
    elif from_unit == 'F':
        celsius = (value - 32) * 5/9
    if to_unit == 'C':
        return celsius
    elif to_unit == 'K':
        return celsius + 273.15
    elif to_unit == 'F':
        return (celsius * 9/5) + 32


def convert_speed(value, from_unit, to_unit):
    to_mps = {
        'm/s': 1.0,
        'km/h': 1000/3600,
        'mph': 1609.344/3600,
        'knot': 1852/3600
    }
    mps = value * to_mps[from_unit]
    return mps / to_mps[to_unit]


def convert_pressure(value, from_unit, to_unit):
    to_pascal = {
        'Pa': 1.0,
        'kPa': 1000.0,
        'bar': 100000.0,
        'atm': 101325.0,
        'psi': 6894.76,
        'torr': 133.322
    }
    pascals = value * to_pascal[from_unit]
    return pascals / to_pascal[to_unit]


def convert_energy(value, from_unit, to_unit):
    to_joule = {
        'J': 1.0,
        'kJ': 1000.0,
        'cal': 4.184,
        'kcal': 4184.0,
        'Wh': 3600.0,
        'kWh': 3600000.0
    }
    joules = value * to_joule[from_unit]
    return joules / to_joule[to_unit]


def convert_power(value, from_unit, to_unit):
    to_watt = {
        'W': 1.0,
        'kW': 1000.0,
        'hp': 745.7
    }
    watts = value * to_watt[from_unit]
    return watts / to_watt[to_unit]


def convert_time(value, from_unit, to_unit):
    to_second = {
        's': 1.0,
        'min': 60.0,
        'h': 3600.0,
        'day': 86400.0,
        'week': 604800.0,
        'month': 2592000.0,
        'year': 31536000.0
    }
    seconds = value * to_second[from_unit]
    return seconds / to_second[to_unit]


def convert_digital(value, from_unit, to_unit):
    to_byte = {
        'bit': 0.125,
        'B': 1.0,
        'KB': 1024.0,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
        'PB': 1024**5
    }
    bytes_val = value * to_byte[from_unit]
    return bytes_val / to_byte[to_unit]


def unit_converter(value, category, from_unit, to_unit):
    try:
        value = float(value)
        if category == "Length":
            return str(convert_length(value, from_unit, to_unit))
        elif category == "Mass":
            return str(convert_mass(value, from_unit, to_unit))
        elif category == "Temperature":
            return str(convert_temperature(value, from_unit, to_unit))
        elif category == "Speed":
            return str(convert_speed(value, from_unit, to_unit))
        elif category == "Pressure":
            return str(convert_pressure(value, from_unit, to_unit))
        elif category == "Energy":
            return str(convert_energy(value, from_unit, to_unit))
        elif category == "Power":
            return str(convert_power(value, from_unit, to_unit))
        elif category == "Time":
            return str(convert_time(value, from_unit, to_unit))
        elif category == "Digital":
            return str(convert_digital(value, from_unit, to_unit))
        else:
            return "Error: Unknown category"
    except Exception as e:
        return f"Error: {str(e)}"


def integer_to_roman(n):
    try:
        n = int(n)
        if n <= 0 or n > 3999:
            raise ValueError("Number must be between 1 and 3999")

        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        roman_num = ''
        i = 0
        while n > 0:
            for _ in range(n // val[i]):
                roman_num += syb[i]
                n -= val[i]
            i += 1
        return roman_num
    except Exception as e:
        raise ValueError(f"Integer to Roman conversion error: {e}")


def roman_to_integer(s):
    try:
        roman_dict = {'I': 1, 'V': 5, 'X': 10,
                      'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        int_val = 0
        for i in range(len(s)):
            if i > 0 and roman_dict[s[i]] > roman_dict[s[i - 1]]:
                int_val += roman_dict[s[i]] - 2 * roman_dict[s[i - 1]]
            else:
                int_val += roman_dict[s[i]]
        return str(int_val)
    except Exception as e:
        raise ValueError(f"Roman to Integer conversion error: {e}")


def character_stats(text: str) -> dict:
    try:
        if not text:
            return {"error": "No text provided"}
        # Basic statistics
        total_chars = len(text)
        whitespace_count = text.count(
            ' ') + text.count('\t') + text.count('\n')
        non_whitespace_chars = total_chars - whitespace_count
        digit_count = sum(c.isdigit() for c in text)
        letter_count = sum(c.isalpha() for c in text)
        uppercase_count = sum(c.isupper() for c in text)
        lowercase_count = sum(c.islower() for c in text)
        punctuation_count = sum(c in string.punctuation for c in text)
        line_count = text.count('\n') + 1 if text else 0
        words = text.split()
        word_count = len(words)
        avg_word_length = sum(len(word) for word in words) / \
            word_count if word_count > 0 else 0

        return {
            "total_characters": total_chars,
            "whitespace_characters": whitespace_count,
            "non_whitespace_characters": non_whitespace_chars,
            "digit_count": digit_count,
            "letter_count": letter_count,
            "uppercase_count": uppercase_count,
            "lowercase_count": lowercase_count,
            "punctuation_count": punctuation_count,
            "line_count": line_count,
            "word_count": word_count,
            "average_word_length": round(avg_word_length, 2)
        }
    except Exception as e:
        return {"error": f"Character analysis failed: {str(e)}"}


def format_character_stats(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]
    output = []
    output.append("=== CHARACTER STATISTICS ===")
    output.append(f"Total characters: {stats['total_characters']}")
    output.append(f"Whitespace characters: {stats['whitespace_characters']}")
    output.append(
        f"Non-whitespace characters: {stats['non_whitespace_characters']}")
    output.append(f"Digits: {stats['digit_count']}")
    output.append(f"Letters: {stats['letter_count']}")
    output.append(f"Uppercase letters: {stats['uppercase_count']}")
    output.append(f"Lowercase letters: {stats['lowercase_count']}")
    output.append(f"Punctuation marks: {stats['punctuation_count']}")
    output.append(f"Lines: {stats['line_count']}")
    output.append(f"Words: {stats['word_count']}")
    output.append(f"Average word length: {stats['average_word_length']}")
    return "\n".join(output)


def format_character_frequency(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]
    output = []
    output.append("=== CHARACTER FREQUENCY ANALYSIS ===")
    output.append(f"Unique characters: {stats['unique_characters']}")
    output.append("\nMost common characters:")
    for char, count in stats['most_common_characters']:
        char_repr = repr(char)[1:-1]
        percentage = (count / len(stats['character_frequency'])) * 100
        output.append(f"'{char_repr}': {count} ({percentage:.2f}%)")
    return "\n".join(output)


def extract_numbers(text: str) -> list:
    try:
        numbers = []
        number_pattern = r'-?\d+\.?\d*'
        for match in re.finditer(number_pattern, text):
            number_str = match.group()
            try:
                if '.' in number_str:
                    numbers.append(float(number_str))
                else:
                    numbers.append(int(number_str))
            except ValueError:
                continue
        return numbers
    except Exception as e:
        return []


def number_analysis(text: str) -> dict:
    try:
        numbers = extract_numbers(text)
        if not numbers:
            return {"error": "No numbers found in text"}
        total_numbers = len(numbers)
        sum_numbers = sum(numbers)
        avg_number = sum_numbers / total_numbers if total_numbers > 0 else 0
        min_number = min(numbers)
        max_number = max(numbers)
        integers = [n for n in numbers if isinstance(n, int)]
        floats = [n for n in numbers if isinstance(n, float)]
        positive = [n for n in numbers if n > 0]
        negative = [n for n in numbers if n < 0]
        zero = [n for n in numbers if n == 0]
        even = [n for n in integers if n % 2 == 0]
        odd = [n for n in integers if n % 2 != 0]
        return {
            "total_numbers": total_numbers,
            "sum": sum_numbers,
            "average": round(avg_number, 4),
            "min": min_number,
            "max": max_number,
            "integers": len(integers),
            "floats": len(floats),
            "positive": len(positive),
            "negative": len(negative),
            "zero": len(zero),
            "even": len(even),
            "odd": len(odd),
            "numbers_list": numbers
        }
    except Exception as e:
        return {"error": f"Number analysis failed: {str(e)}"}


def format_number_analysis(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]
    output = []
    output.append("=== NUMBER ANALYSIS ===")
    output.append(f"Total numbers found: {stats['total_numbers']}")
    output.append(f"Sum: {stats['sum']}")
    output.append(f"Average: {stats['average']}")
    output.append(f"Minimum: {stats['min']}")
    output.append(f"Maximum: {stats['max']}")
    output.append(f"Integers: {stats['integers']}")
    output.append(f"Floats: {stats['floats']}")
    output.append(f"Positive numbers: {stats['positive']}")
    output.append(f"Negative numbers: {stats['negative']}")
    output.append(f"Zero values: {stats['zero']}")
    output.append(f"Even numbers: {stats['even']}")
    output.append(f"Odd numbers: {stats['odd']}")
    if stats['numbers_list']:
        sample = stats['numbers_list'][:10]
        output.append(f"\nSample numbers: {sample}")
    return "\n".join(output)


def number_frequency_analysis(text: str) -> dict:
    try:
        numbers = extract_numbers(text)
        if not numbers:
            return {"error": "No numbers found in text"}
        number_frequency = {}
        for number in numbers:
            if number not in number_frequency:
                number_frequency[number] = 0
            number_frequency[number] += 1
        most_common = sorted(number_frequency.items(),
                             key=lambda x: x[1], reverse=True)[:15]
        return {
            "number_frequency": number_frequency,
            "most_common_numbers": most_common,
            "unique_numbers": len(number_frequency)
        }
    except Exception as e:
        return {"error": f"Number frequency analysis failed: {str(e)}"}


def format_number_frequency(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]
    output = []
    output.append("=== NUMBER FREQUENCY ANALYSIS ===")
    output.append(f"Unique numbers: {stats['unique_numbers']}")
    output.append("\nMost common numbers:")
    for number, count in stats['most_common_numbers']:
        percentage = (count / sum(stats['number_frequency'].values())) * 100
        output.append(f"{number}: {count} occurrences ({percentage:.2f}%)")
    return "\n".join(output)


def calculate_entropy(text: str) -> float:
    try:
        if not text:
            return 0.0
        char_frequency = {}
        text_length = len(text)
        for char in text:
            char_frequency[char] = char_frequency.get(char, 0) + 1
        entropy = 0.0
        for count in char_frequency.values():
            probability = count / text_length
            entropy -= probability * math.log2(probability)
        return entropy
    except Exception as e:
        return float("nan")


def character_frequency_analysis(text: str) -> dict:
    try:
        if not text:
            return {"error": "No text provided"}
        char_frequency = {}
        total_chars = len(text)
        for char in text:
            if char not in char_frequency:
                char_frequency[char] = 0
            char_frequency[char] += 1
        most_common = sorted(char_frequency.items(),
                             key=lambda x: x[1], reverse=True)[:20]
        letter_count = sum(c.isalpha() for c in text)
        digit_count = sum(c.isdigit() for c in text)
        space_count = sum(c.isspace() for c in text)
        punctuation_count = sum(c in string.punctuation for c in text)
        other_count = total_chars - \
            (letter_count + digit_count + space_count + punctuation_count)
        return {
            "total_characters": total_chars,
            "unique_characters": len(char_frequency),
            "character_frequency": char_frequency,
            "most_common_characters": most_common,
            "letter_count": letter_count,
            "digit_count": digit_count,
            "space_count": space_count,
            "punctuation_count": punctuation_count,
            "other_count": other_count,
            "entropy": calculate_entropy(text)
        }
    except Exception as e:
        return {"error": f"Character frequency analysis failed: {str(e)}"}


def format_character_frequency(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]
    output = []
    output.append("=== CHARACTER FREQUENCY ANALYSIS ===")
    output.append(f"Total characters: {stats['total_characters']}")
    output.append(f"Unique characters: {stats['unique_characters']}")
    output.append(f"Letters: {stats['letter_count']}")
    output.append(f"Digits: {stats['digit_count']}")
    output.append(f"Whitespace: {stats['space_count']}")
    output.append(f"Punctuation: {stats['punctuation_count']}")
    output.append(f"Other characters: {stats['other_count']}")
    output.append(f"Shannon entropy: {stats['entropy']:.4f} bits/character")
    output.append("\n=== MOST COMMON CHARACTERS ===")
    for char, count in stats['most_common_characters']:
        char_repr = repr(char)[1:-1]
        percentage = (count / stats['total_characters']) * 100
        output.append(f"'{char_repr}': {count} ({percentage:.2f}%)")
    return "\n".join(output)


def format_entropy_only(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]
    output = []
    output.append("=== ENTROPY ANALYSIS ===")
    output.append(f"Total characters: {stats['total_characters']}")
    output.append(f"Unique characters: {stats['unique_characters']}")
    output.append(f"Shannon entropy: {stats['entropy']:.4f} bits/character")
    entropy = stats['entropy']
    if entropy < 2.0:
        interpretation = "Low entropy (predictable text)"
    elif entropy < 4.0:
        interpretation = "Medium entropy (mixed content)"
    else:
        interpretation = "High entropy (random-looking data)"
    output.append(f"Interpretation: {interpretation}")
    output.append("\n=== ENTROPY REFERENCE ===")
    output.append("English text: ~4.0-4.5 bits/character")
    output.append("Random text: ~6.6 bits/character (for 95 printable ASCII)")
    output.append("Binary data: ~8.0 bits/character")
    return "\n".join(output)


def calculate_basic_statistics(text: str) -> dict:
    try:
        numbers = extract_numbers(text)
        if not numbers:
            return {"error": "No numbers found for statistical analysis"}

        n = len(numbers)
        mean = sum(numbers) / n

        sorted_numbers = sorted(numbers)
        if n % 2 == 0:
            mid1 = sorted_numbers[n//2 - 1]
            mid2 = sorted_numbers[n//2]
            median = (mid1 + mid2) / 2
        else:
            median = sorted_numbers[n//2]

        frequency = {}
        for num in numbers:
            frequency[num] = frequency.get(num, 0) + 1
        max_freq = max(frequency.values())
        modes = [num for num, freq in frequency.items() if freq == max_freq]

        variance = sum((x - mean) ** 2 for x in numbers) / n
        std_dev = variance ** 0.5

        return {
            "count": n,
            "mean": mean,
            "median": median,
            "modes": modes,
            "variance": variance,
            "standard_deviation": std_dev,
        }
    except Exception as e:
        return {"error": f"Statistics calculation failed: {e}"}


def format_basic_statistics(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]

    output = ["=== BASIC STATISTICS ==="]
    output.append(f"Count: {stats['count']}")
    output.append(f"Mean: {stats['mean']:.4f}")
    output.append(f"Median: {stats['median']}")
    output.append(f"Mode(s): {', '.join(map(str, stats['modes']))}")
    output.append(f"Variance: {stats['variance']:.4f}")
    output.append(f"Standard Deviation: {stats['standard_deviation']:.4f}")
    return "\n".join(output)


def _is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def _is_perfect_square_bool(n):
    if n < 0:
        return False
    return math.isqrt(n) ** 2 == n


def is_perfect(n):
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
    if n < 0:
        return False
    s = str(n)
    order = len(s)
    sum_val = sum(int(digit)**order for digit in s)
    return n == sum_val


def is_palindrome(n):
    return str(n) == str(n)[::-1]


def analyze_special_properties(text: str) -> dict:
    try:
        numbers = extract_numbers(text)
        integers = [n for n in numbers if isinstance(n, int)]
        if not integers:
            return {"error": "No integers found for property analysis"}

        results = {}
        for num in integers[:100]:
            properties = []

            properties.append("Even" if num % 2 == 0 else "Odd")

            if num >= 0:
                if is_palindrome(num):
                    properties.append("Palindrome")
                if _is_perfect_square_bool(num):
                    properties.append("Perfect Square")
                if is_perfect_cube(str(num)) == "True":
                    properties.append("Perfect Cube")

            if num > 0:
                if num <= 1_000_000:
                    if _is_prime(num):
                        properties.append("Prime")
                    if is_armstrong(num):
                        properties.append("Armstrong")
                    if is_perfect(num):
                        properties.append("Perfect")

            if properties:
                results[num] = properties

        return {"special_properties": results}
    except Exception as e:
        return {"error": f"Special property analysis failed: {e}"}


def format_special_properties(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]

    output = ["=== SPECIAL NUMBER PROPERTIES ==="]
    if not stats["special_properties"]:
        output.append("No notable properties found in the first 100 integers.")
    else:
        for num, props in stats["special_properties"].items():
            output.append(f"{num}: {', '.join(props)}")

    return "\n".join(output)


def detect_repeated_sequences(text: str, min_length: int = 2, max_length: int = 10) -> dict:
    try:
        sequences = {}
        text_length = len(text)
        if text_length < min_length * 2:
            return {"repeated_sequences": []}
        for seq_length in range(min_length, min(max_length, text_length // 2) + 1):
            for i in range(text_length - seq_length + 1):
                sequence = text[i:i + seq_length]
                if sequence.strip() == "":
                    continue
                count = text.count(sequence)
                if count > 1 and sequence not in sequences:
                    sequences[sequence] = count
        sorted_sequences = sorted(sequences.items(),
                                  key=lambda x: (-x[1], -len(x[0])))
        return {"repeated_sequences": sorted_sequences[:15]}
    except Exception as e:
        return {"error": f"Sequence detection failed: {str(e)}"}


def detect_language(code: str) -> str:
    if not code.strip():
        return "No code provided."
    scores = {lang: 0 for lang in LANGUAGE_PATTERNS}
    for lang, patterns in LANGUAGE_PATTERNS.items():
        for pattern, weight in patterns:
            if pattern.search(code):
                scores[lang] += weight

    detected_lang = max(scores, key=scores.get)
    if scores[detected_lang] > 0:
        return f"Detected language: {detected_lang}"
    return "Language not detected."


class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def error(self, message):
        self.errors.append(message)


def _check_brackets_and_quotes(code: str, lang: str) -> str:
    stack = []
    brackets = {"(": ")", "[": "]", "{": "}"}
    in_string = None
    for line_num, line in enumerate(code.splitlines(), 1):
        for char in line:
            if in_string:
                if char == in_string:
                    in_string = None
            elif char in ('"', "'"):
                in_string = char
            elif char in brackets:
                stack.append((char, line_num))
            elif char in brackets.values():
                if not stack or brackets[stack.pop()[0]] != char:
                    return f"{lang} Syntax Error: Mismatched bracket '{char}' on line {line_num}."
    if stack:
        unclosed_char, line = stack[-1]
        return f"{lang} Syntax Error: Unclosed bracket '{unclosed_char}' from line {line}."
    return f"{lang} syntax appears valid (bracket check)."


def _has_valid_structure(code: str, lang: str) -> bool:
    if lang not in LANGUAGE_PATTERNS:
        return False
    
    patterns = LANGUAGE_PATTERNS[lang]
    for pattern, weight in patterns:
        if pattern.search(code):
            return True
    return False

def syntax_analysis(code: str, language: str = "Python") -> str:
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


def text_to_ascii_art(text, font='standard'):
    try:
        if not text:
            return "Error: No text provided"
        available_fonts = pyfiglet.FigletFont.getFonts()
        if font not in available_fonts:
            font = 'standard'
        ascii_art = pyfiglet.figlet_format(text, font=font)
        return ascii_art
    except Exception as e:
        return f"Error generating ASCII art: {e}"


def setup_conversion_map():
    conversion_map = {
        "Decimal to Binary": lambda text, **kwargs: decimal_to_binary(text),
        "Binary to Decimal": lambda text, **kwargs: binary_to_decimal(text),
        "Decimal to Octal": lambda text, **kwargs: decimal_to_octal(text),
        "Octal to Decimal": lambda text, **kwargs: octal_to_decimal(text),
        "Decimal to Hexadecimal": lambda text, **kwargs: decimal_to_hexadecimal(text),
        "Hexadecimal to Decimal": lambda text, **kwargs: hexadecimal_to_decimal(text),

        "Text to Morse": lambda text, **kwargs: text_to_morse(text),
        "Morse to Text": lambda text, **kwargs: morse_to_text(text),
        "Text to Braille": lambda text, **kwargs: text_to_braille(text),
        "Braille to Text": lambda text, **kwargs: braille_to_text(text),
        "Text to Grid Cipher": lambda text, **kwargs: text_to_grid_cipher(text),
        "Grid Cipher to Text": lambda text, **kwargs: grid_cipher_to_text(text),
        "Text to Emoji Cipher": lambda text, **kwargs: text_to_emoji(text),
        "Emoji Cipher to Text": lambda text, **kwargs: emoji_to_text(text),

        "Text to Affine Cipher": lambda text, base, **kwargs: affine_encrypt(text, base),
        "Affine Cipher to Text": lambda text, base, **kwargs: affine_decrypt(text, base),
        "Text to ROT-N": lambda text, base, **kwargs: rot_n_encrypt(text, int(base)),
        "ROT-N to Text": lambda text, base, **kwargs: rot_n_decrypt(text, int(base)),

        "Text to ASCII": lambda text, **kwargs: ascii_encode(text),
        "ASCII to Text": lambda text, **kwargs: ascii_decode(text),
        "Text to UTF-N": lambda text, base, **kwargs: utf_n_encode(text, "utf-8", base),
        "UTF-N to Text": lambda text, base, **kwargs: utf_n_decode(text, "utf-8", base),
        "Text to ISO": lambda text, base, **kwargs: iso_n_encode(text, "iso-8859-1", base),
        "ISO to Text": lambda text, base, **kwargs: iso_n_decode(text, "iso-8859-1", base),

        "AES Encrypt": lambda text, base, **kwargs: aes_encrypt(text, base),
        "AES Decrypt": lambda text, base, **kwargs: aes_decrypt(text, base),
        "ChaCha20 Encrypt": lambda text, base, **kwargs: chacha20_encrypt(text, base),
        "ChaCha20 Decrypt": lambda text, base, **kwargs: chacha20_decrypt(text, base),
        "DES Encrypt": lambda text, base, **kwargs: des_encrypt(text, base),
        "DES Decrypt": lambda text, base, **kwargs: des_decrypt(text, base),
        "3DES Encrypt": lambda text, base, **kwargs: triple_des_encrypt(text, base),
        "3DES Decrypt": lambda text, base, **kwargs: triple_des_decrypt(text, base),
        "Blowfish Encrypt": lambda text, base, **kwargs: blowfish_encrypt(text, base),
        "Blowfish Decrypt": lambda text, base, **kwargs: blowfish_decrypt(text, base),

        "Generate RSA Keys": lambda text, base, **kwargs: (
            lambda keys: f"PRIVATE KEY:\n{keys[0]}\nPUBLIC KEY:\n{keys[1]}"
        )(rsa_generate_keys(key_size=int(base or 2048))),

        "Generate ECC Keys": lambda text, base, **kwargs: (
            lambda keys: f"PRIVATE KEY:\n{keys[0]}\nPUBLIC KEY:\n{keys[1]}"
        )(ecc_generate_keys(curve_name=base)),

        "Generate ElGamal Keys": lambda text, base, **kwargs: (
            lambda keys: f"PRIVATE KEY:\n{keys[0]}\nPUBLIC KEY:\n{keys[1]}"
        )(elgamal_generate_keys(key_size=int(base or 2048))),

        "RSA Encrypt": lambda text, base, **kwargs: rsa_encrypt(text, parse_pem_and_type(base)[0]),
        "RSA Decrypt": lambda text, base, **kwargs: rsa_decrypt(text, parse_pem_and_type(base)[0]),
        "ECC Encrypt": lambda text, base, **kwargs: ecc_encrypt(text, parse_pem_and_type(base)[0]),
        "ECC Decrypt": lambda text, base, **kwargs: ecc_decrypt(text, parse_pem_and_type(base)[0]),
        "ElGamal Encrypt": lambda text, base, **kwargs: elgamal_encrypt(text, parse_pem_and_type(base)[0]),
        "ElGamal Decrypt": lambda text, base, **kwargs: elgamal_decrypt(text, parse_pem_and_type(base)[0]),

        "SHA-3": lambda text, **kwargs: sha3_hash(text),
        "SHA-256": lambda text, **kwargs: sha256_hash(text),
        "SHA-512": lambda text, **kwargs: sha512_hash(text),
        "bcrypt": lambda text, **kwargs: bcrypt_hash(text),
        "scrypt": lambda text, **kwargs: scrypt_hash(text),
        "Argon2": lambda text, **kwargs: argon2_hash(text),

        "MD5": lambda text, **kwargs: md5_checksum(text),
        "CRC32": lambda text, **kwargs: crc32_checksum(text),
        "Adler-32": lambda text, **kwargs: adler32_checksum(text),
        "SHA-1": lambda text, **kwargs: sha1_hash(text),

        "P. Checker": lambda text, **kwargs: is_prime_check(text),
        "Divisibility Checker": lambda text, base, **kwargs: is_divisible(text, base),
        "Divisors Finder": lambda text, **kwargs: str(find_divisors(text)),
        "Factors Finder": lambda text, **kwargs: str(prime_factors(text)),
        "Perfect Square Checker": lambda text, **kwargs: is_perfect_square(text),
        "Perfect Cube Checker": lambda text, **kwargs: is_perfect_cube(text),

        "Num to Roman": lambda text, **kwargs: integer_to_roman(text),
        "Roman to Num": lambda text, **kwargs: roman_to_integer(text.upper()),

        "Characters": lambda text, **kwargs: format_character_stats(character_stats(text)),
        "Character Frequency": lambda text, **kwargs: format_character_frequency(character_frequency_analysis(text)),
        "Repeated sequences detection": lambda text, **kwargs: (
            lambda seqs: "\n".join(["=== REPEATED SEQUENCES ==="] +
                                   [f"'{repr(s)[1:-1]}': {c} occurrences" for s, c in seqs])
            if seqs
            else "No repeated sequences found"
        )(detect_repeated_sequences(text).get("repeated_sequences")),
        "Entropy": lambda text, **kwargs: format_entropy_only(character_frequency_analysis(text)),
        "Extract Number": lambda text, **kwargs: f"Extracted numbers: {extract_numbers(text)}" if len(extract_numbers(text)) <= 20 else f"Extracted {len(extract_numbers(text))} numbers. First 20: {extract_numbers(text)[:20]}",
        "Number Frequency": lambda text, **kwargs: format_number_frequency(number_frequency_analysis(text)),
        "Basic Statistics": lambda text, **kwargs: format_basic_statistics(calculate_basic_statistics(text)),
        "Special Properties": lambda text, **kwargs: format_special_properties(analyze_special_properties(text)),

        "Language Detection": lambda text, **kwargs: detect_language(text),
        "Syntax Analysis": lambda text, mode, **kwargs: syntax_analysis(text, mode),

        "ASCII Art": lambda text, mode, **kwargs: text_to_ascii_art(text, font=mode), }

    conversion_map.update({
        "Random Password Generator": lambda text, **kwargs: password_generator(text),
        "Random Letters Generator": lambda text, **kwargs: letters_generator(text),
        "Random Number Generator": lambda text, **kwargs: number_generator(text),
        "Random ID Generator": lambda text, **kwargs: "\n".join(random_id_generator(text)),
        "Random IP adress Generator": lambda text, **kwargs: "\n".join(random_ip_generator(text)),
        "Coprimes Generator": lambda text, **kwargs: "\n".join(map(str, generate_coprimes(text))),
        "Random Equation Generator": lambda text, **kwargs: generate_multiple_equations(text),
    })
    return conversion_map


CONVERSION_MAP = setup_conversion_map()


def detect_conversion_type(text, tab_name, base=None, mode=None, mode2=None):
    try:
        if isinstance(text, bytes):
            try:
                text = text.decode("utf-8", errors="replace")
            except Exception:
                text = str(text)
        elif text is None:
            text = ""
        else:
            text = str(text).strip()

        if tab_name is None:
            raise ValueError("tab_name is required")
        tab_name = str(tab_name)

        def _normalize_mode(m):
            if isinstance(m, str):
                return m.strip()
            try:
                if hasattr(m, "currentText"):
                    return m.currentText()
                if hasattr(m, "text"):
                    return m.text()
            except Exception:
                pass
            return None

        mode = _normalize_mode(mode)
        mode2 = _normalize_mode(mode2)
        m_base = re.match(r"Base\s*(\d+|URL)$", tab_name.strip(), re.I)

        if base is not None:
            try:
                if hasattr(base, "text"):
                    base_val = base.text()
                elif hasattr(base, "toPlainText"):
                    base_val = base.toPlainText()
                else:
                    base_val = base
            except Exception:
                base_val = base

            if isinstance(base_val, bytes):
                try:
                    base_val = base_val.decode("utf-8", errors="replace")
                except Exception:
                    base_val = str(base_val)

            if isinstance(base_val, str):
                base_val = base_val.strip()
                if base_val == "":
                    base_val = None
            base = base_val

        if tab_name in CONVERSION_MAP:
            return CONVERSION_MAP[tab_name](text=text, base=base, mode=mode, mode2=mode2)

        if "Custom" in tab_name:
            b_int = int(base)
            if "Decimal to Custom" in tab_name:
                return decimal_to_custom_base(text, b_int)
            elif "Custom to Decimal" in tab_name:
                return custom_base_to_decimal(text, b_int)

        elif tab_name in UNIT_CATEGORIES:
            if mode is None or mode2 is None:
                raise ValueError("Please select both source and target units")
            return unit_converter(text, tab_name, mode, mode2)

        elif m_base:
            val = m_base.group(1).upper()
            b = -1 if val == "URL" else int(val)
            if b not in Bases_set:
                raise ValueError(f"Unsupported binary encoding: Base{val}")
            if mode == "Text → Base":
                return word_to_basen(text, b)
            elif mode == "Base → Text":
                return basen_to_word(text, b)
            else:
                if all(c.isprintable() and not c.isspace() for c in text):
                    return word_to_basen(text, b)
                else:
                    return basen_to_word(text, b)

        raise ValueError(f"Conversion not supported: {tab_name}")

    except Exception as e:
        raise ValueError(f"Error converting ({tab_name}): {e}")

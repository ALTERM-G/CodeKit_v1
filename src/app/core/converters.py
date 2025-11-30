from .data import (
    MORSE_DICT, MORSE_TO_TEXT, BRAILLE_DICT, BRAILLE_NUMBER_PREFIX, BRAILLE_TO_TEXT,
    GRID_DICT, EMOJI_MAP, REVERSE_EMOJI_MAP, ERROR_MESSAGES, digits, alphabet_base36,
    alphabet_base58, alphabet_base62, ELGAMAL_PARAMETERS, COLOR_NAME_MAP
)
import sys
import base64
import bcrypt
import hashlib
import json
import math
import os
import random
import re
import secrets
import time
import uuid
import zlib
import pyfiglet
from argon2 import PasswordHasher
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding, ec, dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Cipher import DES as CryptoDES
from Crypto.Cipher import DES3 as Crypto3DES
from Crypto.Cipher import Blowfish as CryptoBlowfish
from PyQt6.QtGui import QColor


def decimal_to_binary(decimal_str):
    """Converts a decimal string to a binary string."""
    try:
        if not decimal_str.strip():
            raise ValueError("Input is empty.")
        n = int(decimal_str)
        return bin(n)[2:]
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["decimal_to_binary"].format(e=e))


def binary_to_decimal(binary_str):
    """Converts a binary string to a decimal string."""
    try:
        if not binary_str.strip():
            raise ValueError("Input is empty.")
        return str(int(binary_str.strip(), 2))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["binary_to_decimal"].format(e=e))


def decimal_to_octal(decimal_str):
    """Converts a decimal string to an octal string."""
    try:
        if not decimal_str.strip():
            raise ValueError("Input is empty.")
        return oct(int(decimal_str))[2:]
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["decimal_to_octal"].format(e=e))


def octal_to_decimal(octal_str):
    """Converts an octal string to a decimal string."""
    try:
        if not octal_str.strip():
            raise ValueError("Input is empty.")
        return str(int(octal_str.strip(), 8))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["octal_to_decimal"].format(e=e))


def decimal_to_hexadecimal(decimal_str):
    """Converts a decimal string to a hexadecimal string."""
    try:
        if not decimal_str.strip():
            raise ValueError("Input is empty.")
        return hex(int(decimal_str))[2:].upper()
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["decimal_to_hex"].format(e=e))


def hexadecimal_to_decimal(hex_str):
    """Converts a hexadecimal string to a decimal string."""
    try:
        if not hex_str.strip():
            raise ValueError("Input is empty.")
        return str(int(hex_str.strip(), 16))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["hex_to_decimal"].format(e=e))


def decimal_to_custom_base(decimal_str, base):
    """Converts a decimal string to a string in a custom base (2-62)."""
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
    """Converts a number string from a custom base to a decimal string."""
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
    """Converts a text string to Morse code."""
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
    """Converts a Morse code string to text."""
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


def text_to_braille(text):
    """Converts a text string to Braille characters."""
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
    """Converts a Braille string back to text."""
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
    """Encrypts text using the ROT-N (Caesar) cipher."""
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
    """Decrypts text from the ROT-N (Caesar) cipher."""
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
    """Converts a Grid Cipher string back to text."""
    try:
        inverse_grid_dict = {v: k for k, v in GRID_DICT.items()}
        symbols = grid_cipher.split('\u200B')
        decoded_text = [inverse_grid_dict.get(s, '?') for s in symbols]
        return ''.join(decoded_text)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["pigpen_to_text"].format(e=e))


def text_to_emoji(text):
    """Converts a text string to an Emoji cipher."""
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
    """Converts an Emoji cipher string back to text."""
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


def _egcd(a: int, b: int):
    """Extended Euclidean Algorithm to find gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b)."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = _egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def _modinv(a: int, m: int):
    """Calculates the modular multiplicative inverse of a modulo m."""
    g, x, _ = _egcd(a % m, m)
    if g != 1:
        raise ValueError(f"No modular inverse for a={a} (gcd != 1) modulo {m}")
    return x % m


def _parse_affine_key(key):
    """Parses an affine cipher key from various input formats."""
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


def _vigenere_process(text: str, key: str, mode: str) -> str:
    """Core processing logic for Vigenere cipher (encryption and decryption)."""
    if not key or not key.isalpha():
        raise ValueError("Vigenère key must be a non-empty alphabetic string.")
    
    processed_text = []
    key = key.upper()
    key_len = len(key)
    key_index = 0

    for char in text:
        if 'a' <= char <= 'z':
            base = ord('a')
            shift = ord(key[key_index % key_len]) - ord('A')
            if mode == 'decrypt':
                shift = -shift
            processed_char = chr((ord(char) - base + shift) % 26 + base)
            processed_text.append(processed_char)
            key_index += 1
        elif 'A' <= char <= 'Z':
            base = ord('A')
            shift = ord(key[key_index % key_len]) - ord('A')
            if mode == 'decrypt':
                shift = -shift
            processed_char = chr((ord(char) - base + shift) % 26 + base)
            processed_text.append(processed_char)
            key_index += 1
        else:
            processed_text.append(char)
            
    return "".join(processed_text)

def vigenere_encrypt(text: str, key: str) -> str:
    return _vigenere_process(text, key, 'encrypt')

def vigenere_decrypt(text: str, key: str) -> str:
    return _vigenere_process(text, key, 'decrypt')


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
    """Encodes text using ISO-8859-1 with an optional ROT-N shift, then Base64 encodes the result."""
    try:
        if n is not None:
            text = ''.join(chr((ord(c) + int(n)) % 256) for c in text)
        encoded_bytes = text.encode(encoding)
        return base64.b64encode(encoded_bytes).decode('ascii')
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["iso_encode"].format(encoding=encoding, e=e))


def iso_n_decode(encoded: str, encoding="iso-8859-1", n=None) -> str:
    """Decodes a Base64 string, then decodes from ISO-8859-1 with an optional ROT-N shift."""
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
    """Encodes text using UTF-8 with an optional ROT-N shift, then Base64 encodes the result."""
    try:
        if n is not None:
            text = ''.join(chr((ord(c) + int(n)) % 0x110000) for c in text)
        encoded_bytes = text.encode(encoding)
        return base64.b64encode(encoded_bytes).decode('ascii')
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["utf_encode"].format(encoding=encoding, e=e))


def utf_n_decode(encoded: str, encoding="utf-8", n=None) -> str:
    """Decodes a Base64 string, then decodes from UTF-8 with an optional ROT-N shift."""
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
    """Adds padding characters to a string to make its length a multiple of 'block'."""
    missing = (-len(s)) % block
    return s + ("=" * missing if missing else "")


def int_to_base(n: int, alphabet: str) -> str:
    """Converts an integer to a string representation in a custom base defined by an alphabet."""
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
    """Converts a string representation in a custom base (defined by an alphabet) to an integer."""
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
    """Encodes a text string into a specified base (e.g., Base64, Base32, custom bases)."""
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
    """Decodes a string from a specified base (e.g., Base64, Base32, custom bases) back to text."""
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


def derive_key(password: str, salt: bytes, length: int = 32) -> bytes:
    """Derives a cryptographic key from a password and salt using Scrypt."""
    kdf = Scrypt(salt=salt, length=length, n=2**14,
                 r=8, p=1, backend=default_backend())
    return kdf.derive(password.encode())


def pad_data(data: bytes, block_size: int = 128) -> bytes:
    """Pads data to be a multiple of the block size using PKCS7 padding."""
    padder = padding.PKCS7(block_size).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(data: bytes, block_size: int = 128) -> bytes:
    """Removes PKCS7 padding from data."""
    unpadder = padding.PKCS7(block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def aes_encrypt(text: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt, 32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    padded_text = pad_data(text.encode())
    ct = encryptor.update(padded_text) + encryptor.finalize()
    return base64.b64encode(salt + iv + ct).decode()


def aes_decrypt(ciphertext_b64: str, password: str) -> str:
    """Decrypts AES-encrypted ciphertext using a password."""
    data = base64.b64decode(ciphertext_b64)
    salt = data[:16]
    iv = data[16:32]
    ct = data[32:]
    key = derive_key(password, salt, 32)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ct) + decryptor.finalize()
    return unpad_data(padded_text).decode()


def chacha20_encrypt(text: str, password: str) -> str:
    """Encrypts text using the ChaCha20 algorithm with a password."""
    salt = os.urandom(16)
    key = derive_key(password, salt, 32)
    nonce = os.urandom(16)
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(text.encode()) + encryptor.finalize()
    return base64.b64encode(salt + nonce + ct).decode()


def chacha20_decrypt(ciphertext_b64: str, password: str) -> str:
    """Decrypts ChaCha20-encrypted ciphertext using a password."""
    data = base64.b64decode(ciphertext_b64)
    salt = data[:16]
    nonce = data[16:32]
    ct = data[32:]
    key = derive_key(password, salt, 32)
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(ct) + decryptor.finalize()).decode()


def des_encrypt(text: str, password: str) -> str:
    """Encrypts text using the DES algorithm with a password."""
    salt = os.urandom(16)
    key = derive_key(password, salt, 8)
    iv = os.urandom(8)
    cipher = CryptoDES.new(key, CryptoDES.MODE_CBC, iv)
    padded_text = pad_data(text.encode(), 64)
    ct = cipher.encrypt(padded_text)
    return base64.b64encode(salt + iv + ct).decode()


def des_decrypt(ciphertext_b64: str, password: str) -> str:
    """Decrypts DES-encrypted ciphertext using a password."""
    data = base64.b64decode(ciphertext_b64)
    salt = data[:16]
    iv, ct = data[16:24], data[24:]
    key = derive_key(password, salt, 8)
    cipher = CryptoDES.new(key, CryptoDES.MODE_CBC, iv)
    padded_text = cipher.decrypt(ct)
    return unpad_data(padded_text, 64).decode()


def triple_des_encrypt(text: str, password: str) -> str:
    """Encrypts text using the Triple DES (3DES) algorithm with a password."""
    salt = os.urandom(16)
    key = derive_key(password, salt, 24)
    iv = os.urandom(8)
    cipher = Crypto3DES.new(key, Crypto3DES.MODE_CBC, iv)
    padded_text = pad_data(text.encode(), 64)
    ct = cipher.encrypt(padded_text)
    return base64.b64encode(salt + iv + ct).decode()


def triple_des_decrypt(ciphertext_b64: str, password: str) -> str:
    data = base64.b64decode(ciphertext_b64)
    salt = data[:16]
    iv, ct = data[16:24], data[24:]
    key = derive_key(password, salt, 24)
    cipher = Crypto3DES.new(key, Crypto3DES.MODE_CBC, iv)
    padded_text = cipher.decrypt(ct)
    return unpad_data(padded_text, 64).decode()


def blowfish_encrypt(text: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt, 32)
    iv = os.urandom(8)
    cipher = CryptoBlowfish.new(key, CryptoBlowfish.MODE_CBC, iv)
    padded_text = pad_data(text.encode(), 64)
    ct = cipher.encrypt(padded_text)
    return base64.b64encode(salt + iv + ct).decode()


def blowfish_decrypt(ciphertext_b64: str, password: str) -> str:
    """Decrypts text using the Blowfish algorithm."""
    data = base64.b64decode(ciphertext_b64)
    salt = data[:16]
    iv, ct = data[16:24], data[24:]
    key = derive_key(password, salt, 32)
    cipher = CryptoBlowfish.new(key, CryptoBlowfish.MODE_CBC, iv)
    padded_text = cipher.decrypt(ct)
    return unpad_data(padded_text, 64).decode()


def rsa_generate_keys(password: str = None, key_size: int = 2048):
    """Generates RSA private and public keys."""
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
    """Encrypts text using an RSA public key (hybrid encryption)."""
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    symmetric_key = os.urandom(32)
    iv = os.urandom(12) 
    cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(text.encode()) + encryptor.finalize()
    tag = encryptor.tag 
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    key_len_bytes = len(encrypted_symmetric_key).to_bytes(2, 'big')
    return base64.b64encode(key_len_bytes + encrypted_symmetric_key + iv + tag + encrypted_data).decode()


def rsa_decrypt(ciphertext_b64: str, private_key_pem: str, password: str = None) -> str:
    """Decrypts text using an RSA private key (hybrid encryption)."""
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=password.encode() if password else None)
    data = base64.b64decode(ciphertext_b64)
    
    # Unbundle components
    key_len = int.from_bytes(data[:2], 'big')
    encrypted_symmetric_key = data[2:2 + key_len]
    iv = data[2 + key_len : 2 + key_len + 12]
    tag = data[2 + key_len + 12 : 2 + key_len + 12 + 16]
    encrypted_data = data[2 + key_len + 12 + 16:]

    symmetric_key = private_key.decrypt(
        encrypted_symmetric_key,
        asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    cipher = Cipher(algorithms.AES(symmetric_key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
    return plaintext.decode()


def rsa_sign(text: str, private_key_pem: str, password: str = None) -> str:
    """Signs a message using an RSA private key."""
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
    """Verifies a signature using an RSA public key."""
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
    """Generates ECC private and public keys for a given curve."""
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
    """Encrypts text using an ECC public key (ECIES)."""
    try:
        # ECIES implementation (hybrid)
        public_key = serialization.load_pem_public_key(public_pem.encode())
        
        # Generate ephemeral key for this encryption
        ephemeral_private_key = ec.generate_private_key(public_key.curve)
        ephemeral_public_key = ephemeral_private_key.public_key()
        
        # Derive shared secret
        shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)
        derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'ecc-encryption').derive(shared_key)
        
        # Encrypt data with AES-GCM
        iv = os.urandom(12)
        encryptor = Cipher(algorithms.AES(derived_key), modes.GCM(iv)).encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        
        # Prepend ephemeral public key and IV to ciphertext
        ephemeral_pub_bytes = ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.X962, format=serialization.PublicFormat.UncompressedPoint
        )
        
        return base64.b64encode(ephemeral_pub_bytes + iv + encryptor.tag + ciphertext).decode()
    except Exception as e:
        raise ValueError(f"ECC encryption failed: {e}")


def ecc_decrypt(ciphertext_b64: str, private_pem: str) -> str:
    """Decrypts text using an ECC private key (ECIES)."""
    try:
        private_key = serialization.load_pem_private_key(private_pem.encode(), password=None)
        data = base64.b64decode(ciphertext_b64)
        
        # Dynamically determine point length based on the curve
        point_len = (private_key.curve.key_size + 7) // 8 * 2 + 1

        ephemeral_pub_bytes = data[:point_len]
        iv_start = point_len
        tag_start = iv_start + 12
        iv = data[iv_start:tag_start]
        tag = data[tag_start:tag_start + 16]
        ciphertext = data[point_len + 12 + 16:]
        
        ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(private_key.curve, ephemeral_pub_bytes)
        shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)
        derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'ecc-encryption').derive(shared_key)
        
        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()
    except Exception as e:
        raise ValueError(f"ECC decryption failed: {e}")


def ecc_sign(message: str, private_pem: str) -> str:
    """Signs a message using an ECC private key."""
    private_key = serialization.load_pem_private_key(
        private_pem.encode(), password=None)
    signature = private_key.sign(
        message.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    return base64.b64encode(signature).decode()


def ecc_verify(message: str, signature_b64: str, public_pem: str) -> bool:
    """Verifies a signature using an ECC public key."""
    public_key = serialization.load_pem_public_key(public_pem.encode())
    signature = base64.b64decode(signature_b64)
    try:
        public_key.verify(signature, message.encode(),
                          ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False


def elgamal_generate_keys(key_size: int = 2048) -> tuple[str, str]:
    """
    Generates ElGamal private and public keys using standard, hardcoded DH parameters
    to ensure speed and reliability.
    """
    try:
        # The standard 2048-bit MODP group from RFC 3526.
        # Hardcoding these values is the most robust way to avoid all previous errors.
        p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
        g = 2

        params_numbers = dh.DHParameterNumbers(p, g)
        parameters = params_numbers.parameters(default_backend())

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
    """Encrypts text using an ElGamal public key (DHIES)."""
    try:
        public_key = serialization.load_pem_public_key(public_pem.encode())
        if not isinstance(public_key, dh.DHPublicKey):
            raise TypeError("Public key is not a valid DH (ElGamal) key.")
        parameters = public_key.parameters()
        ephemeral_private_key = parameters.generate_private_key()
        shared_key = ephemeral_private_key.exchange(public_key)
        derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'elgamal-dhies-encryption').derive(shared_key)
        iv = os.urandom(12)
        encryptor = Cipher(algorithms.AES(derived_key), modes.GCM(iv)).encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        ephemeral_public_pem = ephemeral_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        key_len_bytes = len(ephemeral_public_pem).to_bytes(2, 'big')
        tag = encryptor.tag

        return base64.b64encode(key_len_bytes + ephemeral_public_pem + iv + tag + ciphertext).decode()
    except Exception as e:
        raise ValueError(f"ElGamal encryption failed: {e}")


def elgamal_decrypt(ciphertext_b64: str, private_pem: str) -> str:
    """Decrypts text using an ElGamal private key (DHIES)."""
    try:
        private_key = serialization.load_pem_private_key(private_pem.encode(), password=None)
        if not isinstance(private_key, dh.DHPrivateKey):
            raise TypeError("Private key is not a valid DH (ElGamal) key.")
            
        data = base64.b64decode(ciphertext_b64)

        # Unbundle components
        key_len = int.from_bytes(data[:2], 'big')
        ephemeral_public_pem = data[2:2 + key_len]
        iv = data[2 + key_len : 2 + key_len + 12]
        tag = data[2 + key_len + 12 : 2 + key_len + 12 + 16]
        ciphertext = data[2 + key_len + 12 + 16:]

        ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_pem)

        shared_key = private_key.exchange(ephemeral_public_key)
        derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'elgamal-dhies-encryption').derive(shared_key)

        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()
    except Exception as e:
        raise ValueError(f"ElGamal decryption failed: {e}")


def _wrap_base64_body(body: str, header: str) -> str:
    """Wraps a base64 string in PEM-style headers and footers."""
    b = "".join(body.split())
    lines = [b[i:i+64] for i in range(0, len(b), 64)]
    return f"-----BEGIN {header}-----\n" + "\n".join(lines) + f"\n-----END {header}-----\n"


def parse_pem_and_type(key_text: str) -> tuple[str, str]:
    """Parses a string to determine if it's a PEM key and returns its type (public/private)."""
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
    """Hashes text using the SHA3-256 algorithm."""
    try:
        return hashlib.sha3_256(text.encode()).hexdigest()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} SHA-3: {e}"


def sha256_hash(text: str) -> str:
    """Hashes text using the SHA-256 algorithm."""
    try:
        return hashlib.sha256(text.encode()).hexdigest()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} SHA-256: {e}"


def sha512_hash(text: str) -> str:
    """Hashes text using the SHA-512 algorithm."""
    try:
        return hashlib.sha512(text.encode()).hexdigest()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} SHA-512: {e}"


def bcrypt_hash(text: str) -> str:
    """Hashes text using the bcrypt algorithm."""
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(text.encode(), salt)
        return hashed.decode()
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} bcrypt: {e}"


def scrypt_hash(text: str, salt: bytes = None) -> str:
    """Hashes text using the scrypt algorithm."""
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
    """Hashes text using the Argon2 algorithm."""
    try:
        return ph.hash(text)
    except Exception as e:
        return f"{ERROR_MESSAGES.get('custom', 'Error')} Argon2: {e}"


def md5_checksum(text: str) -> str:
    """Calculates the MD5 checksum for a given text."""
    try:
        if not text:
            raise ValueError(ERROR_MESSAGES["empty_input"])
        return hashlib.md5(text.encode()).hexdigest()
    except Exception as e:
        raise ValueError(f"MD5 checksum failed: {e}")


def crc32_checksum(text: str) -> str:
    """Calculates the CRC32 checksum for a given text."""
    try:
        if not text:
            raise ValueError(ERROR_MESSAGES["empty_input"])
        return format(zlib.crc32(text.encode()) & 0xFFFFFFFF, '08x')
    except Exception as e:
        raise ValueError(f"CRC32 checksum failed: {e}")


def adler32_checksum(text: str) -> str:
    """Calculates the Adler-32 checksum for a given text."""
    try:
        if not text:
            raise ValueError(ERROR_MESSAGES["empty_input"])
        return format(zlib.adler32(text.encode()) & 0xFFFFFFFF, '08x')
    except Exception as e:
        raise ValueError(f"Adler-32 checksum failed: {e}")


def sha1_hash(text: str) -> str:
    """Hashes text using the SHA-1 algorithm."""
    try:
        text_bytes = text.encode('utf-8')
        sha1 = hashlib.sha1()
        sha1.update(text_bytes)
        return sha1.hexdigest()
    except Exception as e:
        raise ValueError(f"SHA-1 hashing failed: {e}")


def convert_color(color_input, target_format):
    """Converts a color from one format (e.g., HEX, RGB) to another."""
    try:
        color_input = color_input.strip().lower()
        color = QColor()
        if color_input.startswith('#'):
            color.setNamedColor(color_input)
        elif color_input.startswith('rgb'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 3:
                r, g, b = map(int, values)
                color.setRgb(r, g, b)
        elif color_input.startswith('hsl'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 3:
                h, s, l = map(int, values)
                color.setHsl(h % 360, s * 255 // 100, l * 255 // 100)
        elif color_input.startswith('hsv'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 3:
                h, s, v = map(int, values)
                color.setHsv(h % 360, s * 255 // 100, v * 255 // 100)
        elif color_input.startswith('cmyk'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 4:
                c, m, y, k = map(int, values)
                color.setCmyk(c * 255 // 100, m * 255 // 100, y * 255 // 100, k * 255 // 100)
        elif color_input.startswith('hwb'):
            values = re.findall(r'\d+', color_input)
            if len(values) == 3:
                h, w_percent, b_percent = map(int, values)
                h_float = (h % 360) / 360.0
                w_float = w_percent / 100.0
                b_float = b_percent / 100.0
                v_float = 1.0 - b_float
                s_float = 1.0 - (w_float / v_float) if v_float != 0 else 0
                color.setHsvF(h_float, s_float, v_float)
        else:
            color.setNamedColor(color_input)
        if not color.isValid():
            return "Invalid color input."
        if target_format == "Name":
            r, g, b = color.red(), color.green(), color.blue()
            min_dist = float('inf')
            closest_color_name = "Unknown Color"
            for name, (r_known, g_known, b_known) in COLOR_NAME_MAP.items():
                dist = (r - r_known)**2 + (g - g_known)**2 + (b - b_known)**2
                if dist < min_dist:
                    min_dist = dist
                    closest_color_name = name
            return closest_color_name
        elif target_format == "RGB":
            return f"rgb({color.red()}, {color.green()}, {color.blue()})"
        elif target_format == "HSL":
            return f"hsl({color.hslHue()}, {round(color.hslSaturationF()*100)}%, {round(color.lightnessF()*100)}%)"
        elif target_format == "HSV":
            return f"hsv({color.hsvHue()}, {round(color.hsvSaturationF()*100)}%, {round(color.valueF()*100)}%)"
        elif target_format == "HWB":
            h, s, v, _ = color.getHsvF()
            h_deg = round(h * 360) if h != -1 else 0
            w_percent = round((1 - s) * v * 100)
            b_percent = round((1 - v) * 100)
            return f"hwb({h_deg}, {w_percent}%, {b_percent}%)"
        elif target_format == "CMYK":
            c, m, y, k, _ = color.getCmykF()
            return f"cmyk({round(c*100)}%, {round(m*100)}%, {round(y*100)}%, {round(k*100)}%)"
        return color.name()
    except Exception as e:
        return f"Error: {str(e)}"


def convert_length(value, from_unit, to_unit):
    """Converts a value between different units of length."""
    to_meter = {'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0, 'inch': 0.0254, 'ft': 0.3048, 'yard': 0.9144, 'mile': 1609.344}
    meters = value * to_meter[from_unit]
    return meters / to_meter[to_unit]


def convert_mass(value, from_unit, to_unit):
    """Converts a value between different units of mass."""
    to_gram = {'g': 1.0, 'kg': 1000.0, 'mg': 0.001, 'ton': 1000000.0, 'lb': 453.592, 'oz': 28.3495}
    grams = value * to_gram[from_unit]
    return grams / to_gram[to_unit]


def convert_temperature(value, from_unit, to_unit):
    """Converts a value between different units of temperature."""
    if from_unit == 'C': celsius = value
    elif from_unit == 'K': celsius = value - 273.15
    elif from_unit == 'F': celsius = (value - 32) * 5/9
    if to_unit == 'C': return celsius
    elif to_unit == 'K': return celsius + 273.15
    elif to_unit == 'F': return (celsius * 9/5) + 32


def convert_speed(value, from_unit, to_unit):
    """Converts a value between different units of speed."""
    to_mps = {'m/s': 1.0, 'km/h': 1000/3600, 'mph': 1609.344/3600, 'knot': 1852/3600}
    mps = value * to_mps[from_unit]
    return mps / to_mps[to_unit]


def convert_pressure(value, from_unit, to_unit):
    """Converts a value between different units of pressure."""
    to_pascal = {'Pa': 1.0, 'kPa': 1000.0, 'bar': 100000.0, 'atm': 101325.0, 'psi': 6894.76, 'torr': 133.322}
    pascals = value * to_pascal[from_unit]
    return pascals / to_pascal[to_unit]


def convert_energy(value, from_unit, to_unit):
    """Converts a value between different units of energy."""
    to_joule = {'J': 1.0, 'kJ': 1000.0, 'cal': 4.184, 'kcal': 4184.0, 'Wh': 3600.0, 'kWh': 3600000.0}
    joules = value * to_joule[from_unit]
    return joules / to_joule[to_unit]


def convert_power(value, from_unit, to_unit):
    """Converts a value between different units of power."""
    to_watt = {'W': 1.0, 'kW': 1000.0, 'hp': 745.7}
    watts = value * to_watt[from_unit]
    return watts / to_watt[to_unit]


def convert_time(value, from_unit, to_unit):
    """Converts a value between different units of time."""
    to_second = {'s': 1.0, 'min': 60.0, 'h': 3600.0, 'day': 86400.0, 'week': 604800.0, 'month': 2592000.0, 'year': 31536000.0}
    seconds = value * to_second[from_unit]
    return seconds / to_second[to_unit]


def convert_digital(value, from_unit, to_unit):
    """Converts a value between different units of digital storage."""
    to_byte = {'bit': 0.125, 'B': 1.0, 'KB': 1024.0, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4, 'PB': 1024**5}
    bytes_val = value * to_byte[from_unit]
    return bytes_val / to_byte[to_unit]


def unit_converter(value, category, from_unit, to_unit):
    """A general-purpose unit converter that dispatches to the correct specific converter."""
    try:
        value = float(value)
        converters = {
            "Length": convert_length, "Mass": convert_mass, "Temperature": convert_temperature,
            "Speed": convert_speed, "Pressure": convert_pressure, "Energy": convert_energy,
            "Power": convert_power, "Time": convert_time, "Digital": convert_digital
        }
        if category in converters:
            return str(converters[category](value, from_unit, to_unit))
        else:
            return "Error: Unknown category"
    except Exception as e:
        return f"Error: {str(e)}"


def integer_to_roman(n):
    """Converts an integer to a Roman numeral string."""
    try:
        n = int(n)
        if n <= 0 or n > 3999:
            raise ValueError("Number must be between 1 and 3999")
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
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
    """Converts a Roman numeral string to an integer."""
    try:
        roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        int_val = 0
        for i in range(len(s)):
            if i > 0 and roman_dict[s[i]] > roman_dict[s[i - 1]]:
                int_val += roman_dict[s[i]] - 2 * roman_dict[s[i - 1]]
            else:
                int_val += roman_dict[s[i]]
        return str(int_val)
    except Exception as e:
        raise ValueError(f"Roman to Integer conversion error: {e}")


def text_to_ascii_art(text, font='standard'):
    """Converts a text string to ASCII art using a specified font."""
    try:
        if not text: return "Error: No text provided"
        available_fonts = pyfiglet.FigletFont.getFonts()
        if font not in available_fonts: font = 'standard'
        ascii_art = pyfiglet.figlet_format(text, font=font)
        return ascii_art
    except Exception as e:
        return f"Error generating ASCII art: {e}"
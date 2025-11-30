from .data import (
    Bases_set, UNIT_CATEGORIES, ERROR_MESSAGES
)
from .analyzers import (
    detect_cipher,
    character_stats, format_character_stats, extract_numbers, number_analysis,
    format_number_analysis, number_frequency_analysis, format_number_frequency, format_special_properties,
    character_frequency_analysis, format_character_frequency, format_entropy_only, analyze_special_properties, calculate_basic_statistics, format_basic_statistics,
    detect_repeated_sequences,
)
from .converters import (
    decimal_to_binary, binary_to_decimal, decimal_to_octal, octal_to_decimal,
    decimal_to_hexadecimal, hexadecimal_to_decimal, text_to_morse, morse_to_text,
    text_to_braille, braille_to_text, text_to_grid_cipher, grid_cipher_to_text,
    text_to_emoji, emoji_to_text, affine_encrypt, affine_decrypt, rot_n_encrypt,
    rot_n_decrypt, ascii_encode, ascii_decode, utf_n_encode, utf_n_decode,
    iso_n_encode, iso_n_decode, vigenere_encrypt, vigenere_decrypt, aes_encrypt, aes_decrypt, chacha20_encrypt,
    chacha20_decrypt, des_encrypt, des_decrypt, triple_des_encrypt, triple_des_decrypt,
    blowfish_encrypt, blowfish_decrypt, rsa_generate_keys, ecc_generate_keys,
    elgamal_generate_keys, rsa_encrypt, rsa_decrypt, ecc_encrypt, ecc_decrypt,
    elgamal_encrypt, elgamal_decrypt, parse_pem_and_type,
    sha3_hash, sha256_hash, sha512_hash, bcrypt_hash, scrypt_hash, argon2_hash,
    md5_checksum, crc32_checksum, adler32_checksum, sha1_hash,
    decimal_to_custom_base, custom_base_to_decimal, word_to_basen, basen_to_word,
    integer_to_roman, roman_to_integer, unit_converter, text_to_ascii_art,
    convert_color,
)
from .generators import (
    password_generator, letters_generator, number_generator, random_id_generator,
    random_ip_generator, generate_coprimes,
)
from .equation_generator import generate_multiple_equations
from .checkers import (
    is_prime_check, is_divisible, find_divisors, prime_factors,
    is_perfect_square, is_perfect_cube, syntax_analysis
)

import re

def setup_conversion_map():
    """Initializes and returns a map of conversion names to their corresponding functions."""
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
        "Text to Vigenere Cipher": lambda text, base, **kwargs: vigenere_encrypt(text, base),
        "Vigenere Cipher to Text": lambda text, base, **kwargs: vigenere_decrypt(text, base),
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
        )(rsa_generate_keys(key_size=int(base))),

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
        "SHA-256": lambda text, **kwargs: sha256_hash(text), # ChaCha20 Encrypt/Decrypt are missing
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
        "Extract Num": lambda text, **kwargs: f"Extracted numbers: {extract_numbers(text)}" if len(extract_numbers(text)) <= 20 else f"Extracted {len(extract_numbers(text))} numbers. First 20: {extract_numbers(text)[:20]}",
        "Number Frequency": lambda text, **kwargs: format_number_frequency(number_frequency_analysis(text)),
        "Basic Statistics": lambda text, **kwargs: format_basic_statistics(calculate_basic_statistics(text)),
        "Special Properties": lambda text, **kwargs: format_special_properties(analyze_special_properties(text)),

        "Syntax Analysis": lambda text, mode, **kwargs: syntax_analysis(text, mode),

        "ASCII Art": lambda text, mode, **kwargs: text_to_ascii_art(text, font=mode),
        "Cipher Detection": lambda text, **kwargs: detect_cipher(text),
    }

    conversion_map.update({
        "Random Password Generator": lambda text, **kwargs: password_generator(text),
        "Random Letters Generator": lambda text, **kwargs: letters_generator(text),
        "Random Number Generator": lambda text, **kwargs: number_generator(text),
        "Random ID Generator": lambda text, **kwargs: "\n".join(random_id_generator(text)),
        "Random IP adress Generator": lambda text, **kwargs: "\n".join(random_ip_generator(text)),
        "Coprimes Generator": lambda text, **kwargs: ", ".join(map(str, generate_coprimes(text))),
        "Random Equation Generator": lambda text, **kwargs: generate_multiple_equations(text),
    })
    return conversion_map


CONVERSION_MAP = setup_conversion_map()


def detect_conversion_type(text, tab_name, base=None, mode=None, mode2=None):
    """Dispatches the conversion task based on the tab name and other parameters."""
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
            return str(unit_converter(text, tab_name, mode, mode2))

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

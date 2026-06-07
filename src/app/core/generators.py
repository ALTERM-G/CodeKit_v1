import math
import random
import secrets
import uuid
from .data import ERROR_MESSAGES, characters, alphabet, numbers


def password_generator(length):
    """Generates a random password of a given length."""
    try:
        length = int(length)
        if length < 4:
            raise ValueError(ERROR_MESSAGES.get("password_error", "Password length must be at least 4"))
        if length > 100000:
            raise ValueError(f"Password length must not exceed 100,000")
        num_chars = len(characters)
        return "".join(characters[b % num_chars] for b in secrets.token_bytes(length))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["password_generator"].format(e=e))


def letters_generator(length):
    """Generates a random string of letters of a given length."""
    try:
        length = int(length)
        if length < 4:
            raise ValueError(ERROR_MESSAGES.get("letter_error", "String length must be at least 4"))
        if length > 100000:
            raise ValueError(f"Password length must not exceed 100,000")
        
        num_chars = len(alphabet)
        return "".join(alphabet[b % num_chars] for b in secrets.token_bytes(length))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["password_generator"].format(e=e))


def number_generator(length):
    """Generates a random string of numbers of a given length."""
    try:
        length = int(length)
        if length < 1:
            raise ValueError(ERROR_MESSAGES.get("number_error", "Number length must be at least 1"))
        elif length > 100000:
            raise ValueError(f"Number length must not exceed 100,000")
        
        num_chars = len(numbers)
        return "".join(numbers[b % num_chars] for b in secrets.token_bytes(length))
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["number_generator"].format(e=e))


def generate_coprimes(n: int):
    """Generates n coprime pairs using a generator."""
    try:
        n = int(n)
        if n < 1:
            raise ValueError("Count must be at least 1")
        if n > 1000000:
            raise ValueError("Count cannot exceed 1,000,000")
        
        generated_pairs = set()
        count = 0
        while count < n:
            a = random.randint(2, 1000000)
            b = random.randint(1, a-1)
            if math.gcd(a, b) == 1 and (a, b) not in generated_pairs:
                yield (a, b)
                generated_pairs.add((a, b))
                count += 1
    except Exception as e:
        raise ValueError(f"Coprime generation failed: {e}")


def random_id_generator(count: int) -> list:
    try:
        count = int(count)
        if count < 1:
            raise ValueError("Count must be at least 1")
        if count > 10000:
            raise ValueError("Count cannot exceed 10,000")

        return [str(uuid.uuid4()) for _ in range(count)]
    except Exception as e:
        raise ValueError(f"ID generation failed: {e}")


def random_ip_generator(count: int) -> list:
    try:
        count = int(count)
        if count < 1:
            raise ValueError("Count must be at least 1")
        if count > 10000:
            raise ValueError("Count cannot exceed 10,000")
        ips = []
        for _ in range(count):
            ip = ".".join(str(secrets.randbelow(256)) for _ in range(4))
            ips.append(ip)
        return ips
    except Exception as e:
        raise ValueError(f"IP generation failed: {e}")
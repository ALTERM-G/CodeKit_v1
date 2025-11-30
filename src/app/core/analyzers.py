import math
import re
import string
from collections import Counter
from .checkers import (
    is_prime_check, is_perfect, is_happy, is_palindrome, is_perfect_square,
    is_perfect_cube, is_increasing, is_decreasing, is_fibonacci, is_armstrong,
    get_proper_divisors, is_binary
)


def calculate_ic(text):
    """Calculates the Index of Coincidence for the given text."""
    text = "".join(filter(str.isalpha, text)).upper()
    n = len(text)
    if n <= 1:
        return 0.0
    
    counts = Counter(text)
    numerator = sum(count * (count - 1) for count in counts.values())
    denominator = n * (n - 1)
    
    return numerator / denominator if denominator != 0 else 0.0


def calculate_entropy(text: str) -> float:
    """Calculates the Shannon entropy for the given text."""
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


def cesar_encrypt(text, shift):
    """Encrypts text using the Caesar cipher with a given shift."""
    encrypted_text = ""
    for char in text:
        if 'a' <= char <= 'z':
            encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text


def cesar_decrypt(text):
    """Analyzes and decrypts a Caesar cipher by finding the most likely shift."""
    text_upper = "".join(filter(str.isalpha, text)).upper()
    if not text_upper:
        return "No alphabetic characters to analyze."

    english_freq = {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
        'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
        'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
        'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
        'Q': 0.10, 'Z': 0.07
    }

    best_shift = 0
    min_chi_squared = float('inf')

    for shift in range(26):
        decrypted_text = cesar_encrypt(text_upper, -shift)
        observed_counts = Counter(decrypted_text)
        chi_squared = 0
        
        text_len = len(decrypted_text)
        if text_len == 0: continue

        for char_code in range(ord('A'), ord('Z') + 1):
            char = chr(char_code)
            observed = observed_counts.get(char, 0)
            expected = text_len * (english_freq.get(char, 0) / 100.0)
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected

        if chi_squared < min_chi_squared:
            min_chi_squared = chi_squared
            best_shift = shift

    return f"Detected Caesar cipher with shift {best_shift}. Decrypted text: {cesar_encrypt(text, -best_shift)}"


def detect_cipher(text):
    """Analyzes text to detect the type of encoding or cipher used."""
    if not text or not text.strip():
        return {"error": "Input is empty."}

    analysis = {}
    cleaned_text = text.replace(" ", "").replace("\n", "")

    # 1. Check for common non-alphabetic encodings first
    if all(c in '01' for c in cleaned_text):
        analysis["Conclusion"] = "Looks like Binary (Base2)."
    elif all(c in '01234567' for c in cleaned_text):
        analysis["Conclusion"] = "Looks like Octal (Base8)."
    elif all(c in '0123456789abcdefABCDEF' for c in cleaned_text):
        analysis["Conclusion"] = "Looks like Hexadecimal (Base16)."
    elif len(cleaned_text) > 20 and re.fullmatch(r'[A-Za-z0-9+/=]*', cleaned_text):
        try:
            import base64
            padded_text = cleaned_text + '=' * (-len(cleaned_text) % 4)
            decoded = base64.b64decode(padded_text)
            if sum(31 < x < 127 or x in b'\t\n\r' for x in decoded) / len(decoded) > 0.8:
                analysis["Conclusion"] = "Looks like Base64 encoding."
        except:
            pass

    # 2. If no encoding was detected, perform statistical analysis on the text
    if not analysis:
        ic = calculate_ic(text)
        entropy = calculate_entropy(text)
        ic_english = 0.067
        ic_random = 1.0 / 26.0  # Approximately 0.0385

        # Determine the most likely category based on IC and Entropy
        unique_chars = len(set(text))
        if unique_chars == 1:
            conclusion = "The text consists of a single repeating character."
        elif ic > 0.1:
             conclusion = "Very high IC. The text is highly repetitive and not standard English. It might be a simple pattern or a single-character substitution from a small alphabet."
        elif abs(ic - ic_english) < 0.01:
            conclusion = "High probability of being a monoalphabetic substitution cipher (e.g., Caesar, Atbash, Simple Substitution)."
        elif abs(ic - ic_random) < 0.01:
            conclusion = "Likely a polyalphabetic cipher (e.g., Vigenère), modern encryption, or compressed data. The character distribution is close to random."
        else:
            conclusion = "The statistical properties are inconclusive. It might be a complex cipher, non-standard text, or too short for an accurate analysis."

        analysis = {
            "Index of Coincidence (IC)": f"{ic:.4f} (Random is ~0.038, English is ~0.067)",
            "Shannon Entropy": f"{entropy:.4f} bits/char (English is ~4.0-4.5, Random is >7.5)",
            "Conclusion": conclusion
        }

    return analysis


def character_stats(text: str) -> dict:
    """Calculates various statistics about the characters in a given text."""
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
    """Formats the character statistics dictionary into a readable string."""
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


def extract_numbers(text: str) -> list:
    """Extracts all integer and float numbers from a string."""
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
    """Performs a detailed analysis of the numbers found in a text."""
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
    """Formats the number analysis dictionary into a readable string."""
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
    """Analyzes the frequency of each number in a text."""
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
    """Formats the number frequency analysis into a readable string."""
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


def _is_triangular(n):
    """Checks if a number is a triangular number."""
    if n < 0: return False
    if n == 0: return True
    val = 8 * n + 1
    sqrt_val = int(val**0.5)
    return sqrt_val * sqrt_val == val

def analyze_special_properties(text: str) -> dict:
    try:
        numbers = extract_numbers(text)
        if not numbers or not isinstance(numbers[0], int):
            return {"error": "No valid integer found at the start of the text."}

        num = numbers[0]
        divisors = get_proper_divisors(num)
        div_sum = sum(divisors)
        is_perf = (div_sum == num and num != 0)

        return {
            f"Analysis for {num}": {
                "Is Prime": is_prime_check(str(num)) == "True",
                "Is Perfect": is_perf,
                "Is Abundant": not is_perf and div_sum > num,
                "Is Deficient": not is_perf and div_sum < num,
                "Is Happy": is_happy(num),
                "Is Palindromic": is_palindrome(num),
                "Is Perfect Square": is_perfect_square(str(num)) == "True",
                "Is Perfect Cube": is_perfect_cube(str(num)) == "True",
                "Is Binary (string)": is_binary(num),
                "Has Increasing Digits": is_increasing(num),
                "Has Decreasing Digits": is_decreasing(num),
                "Is Fibonacci": is_fibonacci(num),
                "Is Narcissistic (Armstrong)": is_armstrong(num),
                "Is Triangular": _is_triangular(num),
                "Proper Divisors": str(divisors) if divisors else "None"
            }
        }
    except Exception as e:
        return {"error": f"Special property analysis failed: {e}"}

def format_special_properties(stats: dict) -> str:
    if "error" in stats:
        return stats["error"]

    output = ["=== SPECIAL NUMBER PROPERTIES ==="]
    for title, properties in stats.items():
        if title == "error": continue
        output.append(title)
        for prop, value in properties.items():
            output.append(f"  - {prop}: {value}")
    
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
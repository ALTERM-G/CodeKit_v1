import string
import re

APP_CONFIG = {
    "window_title": "ALTERM Converter",
    "window_size": (800, 600),
    "background_style": """
        QWidget {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #1f1f1f, stop:1 #181818
            );
            border: 0px solid #000000;
        }
    """,
    "layout_margins": (5, 5, 5, 10),
    "background_normal": "background: #1f1f1f"
}

FONT_CONFIG = {
    "main": {
        "family": "JetBrains Mono",
        "size": 14,
        "bold": True
    },
    "secondary": {
        "family": "Quicksand",
        "size": 13,
        "bold": True
    }
}

MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

MORSE_TO_TEXT = {m: t for t, m in MORSE_DICT.items()}

BRAILLE_NUMBER_PREFIX = '⠼'

BRAILLE_DICT = {
    'A': '⠁', 'B': '⠃', 'C': '⠉', 'D': '⠙', 'E': '⠑', 'F': '⠋', 'G': '⠛', 'H': '⠓',
    'I': '⠊', 'J': '⠚', 'K': '⠅', 'L': '⠇', 'M': '⠍', 'N': '⠝', 'O': '⠕', 'P': '⠏',
    'Q': '⠟', 'R': '⠗', 'S': '⠎', 'T': '⠞', 'U': '⠥', 'V': '⠧', 'W': '⠺', 'X': '⠭',
    'Y': '⠽', 'Z': '⠵',
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓',
    'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏',
    'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵',
    '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊',
    '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ':': '⠱', ';': '⠰',
    "'": '⠄', '"': '⠶', '(': '⠐⠣', ')': '⠐⠜', '-': '⠤', '/': '⠌',
    '&': '⠯', '+': '⠬', '=': '⠿', '%': '⠨⠴', '@': '⠈⠁', '*': '⠔',
    '_': '⠸⠤', '#': '⠼⠶', '$': '⠈⠎', ' ': ' '
}

BRAILLE_TO_TEXT = {}

BRAILLE_CHARS = [chr(i) for i in range(0x2800, 0x28FF + 1)]

GRID_DICT = {
    "A": "⊔", "B": "⊓", "C": "⊏", "D": "⊐", "E": "⊑", "F": "⊒", "G": "⊔⊓", "H": "⊏⊐",
    "I": "⊑⊒", "J": "⊔⊏", "K": "⊓⊐", "L": "⊏⊑", "M": "⊐⊒", "N": "⊔⊑", "O": "⊓⊏",
    "P": "⊏⊓", "Q": "⊐⊔", "R": "⊑⊏", "S": "⊒⊓", "T": "⊔⊒", "U": "⊓⊑", "V": "⊏⊒",
    "W": "⊐⊑", "X": "⊑⊔", "Y": "⊒⊏", "Z": "⊔⊓⊏",
    " ": " ",
    "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8",
    "9": "9", "!": "!", "\"": "\"", "#": "#", "$": "$", "%": "%", "&": "&", "'": "'",
    "(": "(", ")": ")", "*": "*", "+": "+", ",": ",", "-": "-", ".": ".", "/": "/",
    ":": ":", ";": ";", "<": "<", "=": "=", ">": ">", "?": "?", "@": "@", "[": "[",
    "\\": "\\", "]": "]", "^": "^", "_": "_", "{": "{", "|": "|", "}": "}", "~": "~"
}

EMOJI_MAP = {
    "A": "😀", "B": "😃", "C": "😄", "D": "😁", "E": "😆", "F": "😅", "G": "😂", "H": "🤣",
    "I": "😊", "J": "😇", "K": "🙂", "L": "🙃", "M": "😉", "N": "😌", "O": "😍", "P": "🥰",
    "Q": "😘", "R": "😗", "S": "😙", "T": "😚", "U": "😋", "V": "😛", "W": "😜", "X": "🤪",
    "Y": "😝", "Z": "🤑",
    "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", "5": "5️⃣", "6": "6️⃣", "7": "7️⃣",
    "8": "8️⃣", "9": "9️⃣",
    " ": " ", "!": "❗", "\"": "\"", "#": "#", "$": "$", "%": "%", "&": "&", "'": "'",
    "(": "(", ")": ")", "*": "*", "+": "+", ",": ",", "-": "-", ".": ".", "/": "/",
    ":": ":", ";": ";", "<": "<", "=": "=", ">": ">", "?": "?", "@": "@", "[": "[",
    "\\": "\\", "]": "]", "^": "^", "_": "_", "{": "{", "|": "|", "}": "}", "~": "~"
}

REVERSE_EMOJI_MAP = {v: k for k, v in EMOJI_MAP.items()}

ENGLISH_FREQUENCIES = { # Expected English letter frequencies for statistical analysis
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
    'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
    'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
    'Y': 0.01974, 'Z': 0.00074
}

ERROR_MESSAGES = {
    "invalid_input": "Invalid Input",
    "decimal_to_binary": "Error Decimal→Binary: {e}",
    "binary_to_decimal": "Error Binary→Decimal: {e}",
    "decimal_to_octal": "Error Decimal→Octal: {e}",
    "octal_to_decimal": "Error Octal→Decimal: {e}",
    "decimal_to_hex": "Error Decimal→Hexadecimal: {e}",
    "hex_to_decimal": "Error Hexadecimal→Decimal: {e}",
    "text_to_morse": "Error Text→Morse: {e}",
    "morse_to_text": "Error Morse→Text: {e}",
    "cesar_encrypt": "Error Cesar Encrypt: {}",
    "cesar_decrypt": "Error Cesar Decrypt: {}",
    "text_to_braille": "Error Text→Braille: {e}",
    "braille_to_text": "Error Braille→Text: {e}",
    "custom": "Invalid decimal for Custom conversion",
    "custom_2": "Invalid base for Custom conversion",
    "password_error": "Password length must be at least 4",
    "password_generator": "Error Password Generation: {}",
    "letters_generator": "Error Letters Generation: {}",
    "letter_error": "Letters length must be at least 4",
    "number_error": "Number length must be at least 1",
    "number_generator": "Error Number Generation: {}",
    "prime_generator": "Error generating primes: {}",
    "fibonacci_generator": "Error generating Fibonacci sequence: {}",
    "triangular_number_generator": "Error generating triangular numbers: {}",
    "catalan_number_generator": "Error generating Catalan numbers: {}",
    "text_to_pigpen": "Error converting text to Grid Cipher: {}",
    "pigpen_to_text": "Error converting Grid Cipher to text: {}",
    "base_range": "The base must be between 2 and {max_len}",
    "invalid_char_for_base": "Invalid character '{char}' for base {base}",
    "affine_coprime": "Key 'a' ({a}) is not coprime with 26; choose a with gcd(a,26)=1.",
    "affine_key_format": "Invalid affine key format. Use None, 'a,b', 'a' or (a,b).",
    "affine_encrypt": "Affine encrypt error: {e}",
    "affine_decrypt": "Affine decrypt error: {e}",
    "non_ascii_char": "Character '{c}' is not ASCII",
    "ascii_encode": "ASCII encode error: {e}",
    "ascii_decode": "ASCII decode error: {e}",
    "iso_encode": "Error ISO-N encode ({encoding}): {e}",
    "iso_decode": "Error ISO-N decode ({encoding}): {e}",
    "utf_encode": "Error UTF-N encode ({encoding}): {e}",
    "utf_decode": "Error UTF-N decode ({encoding}): {e}",
    "unsupported_base": "Unsupported binary encoding base: {base}",
    "empty_input": "Input cannot be empty",
    "elgamal_keysize": "Key size must be at least 2048 bits"
}
SHORT_NAMES = {
    "Decimal to Binary": "Dec→Bin",
    "Binary to Decimal": "Bin→Dec",
    "Decimal to Octal": "Dec→Oct",
    "Octal to Decimal": "Oct→Dec",
    "Decimal to Hexadecimal": "Dec→Hex",
    "Hexadecimal to Decimal": "Hex→Dec",
    "Custom to Decimal": "Custom→Dec",
    "Decimal to Custom": "Dec→Custom",
    "Text to Morse": "Text→Morse",
    "Morse to Text": "Morse→Text",
    "Text to Braille": "Text→Braille",
    "Braille to Text": "Braille→Text",
    "Text to Grid Cipher": "Text→Grid",
    "Grid Cipher to Text": "Grid→Text",
    "Text to Emoji Cipher": "Text→Emoji",
    "Emoji Cipher to Text": "Emoji→Text",
    "Text to Affine Cipher": "Text→Affine",
    "Affine Cipher to Text": "Affine→Text",
    "Text to Vigenere Cipher": "Text→Vigenere",
    "Vigenere Cipher to Text": "Vigenere→Text",
    "Prime numbers": "Primes",
    "Coprimes Generator": "Coprime",
    "Coprimes generator": "Coprimes",
    "Fibonacci sequence": "Fibonacci",
    "Triangular numbers": "Triangular",
    "Text to ROT-N": "word→ROT-N",
    "ROT-N to Text": "ROT-N→word",
    "Text to ASCII": "Text→ASCII",
    "ASCII to Text": "ASCII→Text",
    "Text to ISO": "Text→ISO",
    "ISO to Text": "ISO→Text",
    "Text to UTF-N": "Text→UTF-N",
    "UTF-N to Text": "UTF-N→Text",
    "Base2": "B2",
    "Base8": "B8",
    "Base10": "B10",
    "Base16": "B16",
    "Base32": "B32",
    "Base36": "B36",
    "Base58": "B58",
    "Base62": "B62",
    "Base64": "B64",
    "Base85": "B85",
    "BaseURL": "BURL",
    "Random Password Generator": "Password",
    "Random Letters Generator": "Letters",
    "Random Number Generator": "Number",
    "Random ID Generator": "ID",
    "Random IP adress Generator": "IP adress",
    "Random Equation Generator": "Equation",
    "Generate RSA Keys": "RSA Keys",
    "Generate ECC Keys": "ECC Keys",
    "Generate ElGamal Keys": "ElGamal Keys",
    "P. Checker": "P_check",
    "Divisibility Checker": "DC",
    "Divisors Finder": "DF",
    "Factors Finder": "Factors",
    "Perfect Square Checker": "P. Square",
    "Perfect Cube Checker": "P. Cube",
    "Num to Roman": "Num",
    "Roman to Num": "Roman",
    "Character Frequency": "Frequency",
    "Repeated sequences detection": "Repeated",
    "Extract Num": "Extract",
    "Number Frequency": "Frequency",
    "Temperature": "Temp",
    "Digital": "Digital",
    "Length": "Len",
    "Speed": "Speed",
    "Pressure": "Press",
    "Energy": "Energy",
    "Power": "Power"
}

SOUNDS = {
    "intro": "sounds/sound_intro.mp3",
    "tab": "sounds/sound_tab.mp3",
    "click": "sounds/sound_1.mp3",
    "back": "sounds/sound_2.mp3"
}

REPL_CONTEXT = {
    "__builtins__": __import__("builtins"),
    "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
    "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10
}

ASCII_ART_FONTS = [
    'standard', 'small', 'mini', 'script', 'slant', 'italic', 'roman', 'serifcap', 
    'smslant', 'smscript', 'thin', '5lineoblique', 'block', 'big', 'banner', 
    'colossal', 'doom', 'epic', 'ogre', 'chunky', 'puffy', 'speed', 'thick', 
    'bigfig', 'cosmic', 'drpepper', 'eftifont', 'larry3d', 'rectangles', 'univers', 
    'stop', '3-d', '3d_diagonal', 'banner3-D', 'doh', 'isometric1', 'isometric2', 
    'isometric3', 'isometric4', 'shadow', 'dwhistled', 'rot13', 'alligator', 
    'alligator2', 'avatar', 'bubble', 'bulbhead', 'contessa', 'graffiti', 
    'hollywood', 'nancyj', 'starwars', 'sub-zero', 'swampwater', 'usaflag', 
    'weird', 'amcslash', 'caligraphy', 'catwalk', 'flowerpower', 'funky', 'ghost', 
    'jazmine', 'jerusalem', 'katakana', 'pawp', 'poison', 'tombstone', 'trek', 
    'wetletter', 'alligator3', 'danc4', 'dancingfont', 'defleppard', 'georgia11', 
    'graceful', 'sweet', 'digital', 'cyberlarge', 'cybermedium', 'cybersmall', 
    'binary', 'decimal', 'hex', 'octal', 'eftirobot', 'smkeyboard', 'morse', 
    'acrobatic', 'dosrebel', 'eftiwater', 'future', 'invita', 'keyboard', 'lcd', 
    'ntgreek', '3x5', '4max', 'bell', 'diamond', 'goofy', 'peaks', 'rounded', 
    'smisome1', 'stforek', 'tanja', 'twopoint', 'alphabet'
]

COLOR_FORMAT_LIST = ["HEX", "RGB", "HSL", "HSV", "HWB", "CMYK", "Name"]

COLOR_NAME_MAP = {
    "Black": (0, 0, 0), "White": (255, 255, 255), "Red": (255, 0, 0),
    "Lime": (0, 255, 0), "Blue": (0, 0, 255), "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255), "Magenta": (255, 0, 255), "Silver": (192, 192, 192),
    "Gray": (128, 128, 128), "Maroon": (128, 0, 0), "Olive": (128, 128, 0),
    "Green": (0, 128, 0), "Purple": (128, 0, 128), "Teal": (0, 128, 128),
    "Navy": (0, 0, 128), "Orange": (255, 165, 0), "Gold": (255, 215, 0),
    "Pink": (255, 192, 203), "Brown": (165, 42, 42), "Indigo": (75, 0, 130),
    "Violet": (238, 130, 238), "Turquoise": (64, 224, 208),
    "Salmon": (250, 128, 114), "SkyBlue": (135, 206, 235)
}
PRESERVE_NEWLINES_MODES = [
    "Random Equation Generator",
    "Random ID Generator",
    "Random IP adress Generator",
    "Coprimes Generator"
]

FULL_NAMES = {v: k for k, v in SHORT_NAMES.items()}

MENU_STRUCTURE = {
    "main": {
        "bases": [
            ("Base2", "Enter Text"),
            ("Base8", "Enter Text"),
            ("Base10", "Enter Text"),
            ("Base16", "Enter Text"),
            ("Base32", "Enter Text"),
            ("Base36", "Enter Text"),
            ("Base58", "Enter Text"),
            ("Base62", "Enter Text"),
            ("Base64", "Enter Text"),
            ("Base85", "Enter Text"),
            ("BaseURL", "Enter Text")
        ],
        "Random": [
            ("Random Password Generator", "Enter length"),
            ("Random Letters Generator", "Enter length"),
            ("Random Number Generator", "Enter length"),
            ("Coprimes Generator", "Enter first n"),
            ("Random ID Generator", "Enter how many IDs"),
            ("Random IP adress Generator", "Enter how many IP adresses"),
            ("Random Equation Generator", "Enter number")
        ],
        "Binary": [
            ("Decimal to Binary", "Enter a decimal number"),
            ("Binary to Decimal", "Enter a binary number"),
        ],
        "Octal": [
            ("Decimal to Octal", "Enter a decimal number"),
            ("Octal to Decimal", "Enter an octal number"),
        ],
        "Hexadecimal": [
            ("Decimal to Hexadecimal", "Enter a decimal number"),
            ("Hexadecimal to Decimal", "Enter a hexadecimal number"),
        ],
        "Custom": [
            ("Decimal to Custom", "Enter number"),
            ("Custom to Decimal", "Enter number"),
        ],
        "Morse": [
            ("Text to Morse", "Enter Text"),
            ("Morse to Text", "Enter a morse code"),
        ],
        "Braille": [
            ("Text to Braille", "Enter Text"),
            ("Braille to Text", "Enter a Braille code"),
        ],
        "Grid Cipher":  [
            ("Text to Grid Cipher", "Enter Text"),
            ("Grid Cipher to Text", "Enter a Grid Cipher"),
        ],
        "Emoji Cipher": [
            ("Text to Emoji Cipher", "Enter Text"),
            ("Emoji Cipher to Text", "Enter an Emoji Cipher"),
        ],
        "Affine Cipher": [
            ("Text to Affine Cipher", "Enter Text"),
            ("Affine Cipher to Text", "Enter an Affine Cipher"),
        ],
        "Vigenere Cipher": [
            ("Text to Vigenere Cipher", "Enter Text"),
            ("Vigenere Cipher to Text", "Enter a Vigenere Cipher"),
        ],
        "ROT-N": [
            ("Text to ROT-N", "Enter Text"),
            ("ROT-N to Text", "Enter a ROT-N code"),
        ],
        "ASCII": [
            ("Text to ASCII", "Enter Text"),
            ("ASCII to Text", "Enter an ASCII code"),
        ],
        "UTF-N": [
            ("Text to UTF-N", "Enter Text"),
            ("UTF-N to Text", "Enter a UTF-N code"),
        ],
        "ISO": [
            ("Text to ISO", "Enter Text"),
            ("ISO to Text", "Enter an ISO code"),
        ],
        "AES": [
            ("AES Encrypt", "Enter text"),
            ("AES Decrypt", "Enter text"),
        ],
        "ChaCha20": [
            ("ChaCha20 Encrypt", "Enter text"),
            ("ChaCha20 Decrypt", "Enter text"),
        ],
        "DES": [
            ("DES Encrypt", "Enter text"),
            ("DES Decrypt", "Enter text"),
        ],
        "3DES": [
            ("3DES Encrypt", "Enter text"),
            ("3DES Decrypt", "Enter text"),
        ],
        "Blowfish": [
            ("Blowfish Encrypt", "Enter text"),
            ("Blowfish Decrypt", "Enter text"),
        ],
        "RSA": [
            ("RSA Encrypt", "Enter text"),
            ("RSA Decrypt", "Enter text"),
            ("Generate RSA Keys", "Enter key size (e.g., 2048)")
        ],
        "ECC": [
            ("ECC Encrypt", "Enter text"),
            ("ECC Decrypt", "Enter text"),
            ("Generate ECC Keys", "Select curve")
        ],
        "ElGamal": [
            ("ElGamal Encrypt", "Enter text"),
            ("ElGamal Decrypt", "Enter text"),
            ("Generate ElGamal Keys", "Enter key size (e.g., 2048)")
        ],
        "Number Checker": [
            ("P. Checker", "Enter Number"),
            ("Divisibility Checker", "Enter Number"),
            ("Divisors Finder", "Enter Number"),
            ("Factors Finder", "Enter Number"),
            ("Perfect Square Checker", "Enter Number"),
            ("Perfect Cube Checker", "Enter Number")
        ],
        "hash": [
            ("SHA-3", "Enter text"),
            ("SHA-256", "Enter text"),
            ("SHA-512", "Enter text"),
            ("bcrypt", "Enter text"),
            ("scrypt", "Enter text"),
            ("Argon2", "Enter text")
        ],
        "cheksum": [
            ("MD5", "Enter text"),
            ("CRC32", "Enter text"),
            ("Adler-32", "Enter text"),
            ("SHA-1", "Enter text")
        ],
        "Unit Converter": [
            ("Length", "Enter length"),
            ("Mass", "Enter mass"),
            ("Temperature", "Enter temperature"),
            ("Speed", "Enter speed"),
            ("Pressure", "Enter pressure"),
            ("Energy", "Enter energy"),
            ("Power", "Enter power"),
            ("Time", "Enter time"),
            ("Digital", "Enter digital")
        ],
        "Roman Num": [
            ("Num to Roman", "Enter Number"),
            ("Roman to Num", "Enter Number")
        ],
        "Code Analyzer": [
            ("Language Detection", "Enter Code"),
            ("Syntax Analysis", "Enter Code")
        ],
        "Character and Symbol": [
            ("Characters", "Enter Text"),
            ("Character Frequency", "Enter Text"),
            ("Repeated sequences detection", "Enter Text"),
            ("Entropy", "Enter Text")
        ],
        "Number analysis": [
            ("Extract Num", "Enter Numbers"),
            ("Number Frequency", "Enter Numbers"),
            ("Basic Statistics", "Enter Numbers"), 
            ("Special Properties", "Enter Numbers")
        ],
        "layout": "grid",
        "margins": (5, 5, 5, 10)
    }
}

MENU_DEFINITIONS = {
    "Base Converter": (
        "vbox", 
        [
            ("Binary", "Binary"), 
            ("Octal", "Octal"), 
            ("Hexadecimal", "Hexadecimal"), 
            ("Custom Base", "Custom", "Base"), 
            ("Roman Num", "Roman Num")
        ]
    ),
    "Binary Encoding": ("tabs", MENU_STRUCTURE["main"]["bases"]),
    "Character Encoding": (
        "vbox", 
        [
            ("ASCII", "ASCII"), 
            ("UTF-N", "UTF-N", "N"), 
            ("ISO", "ISO", "N")
        ]
    ),
    "Random Generators": ("tabs", MENU_STRUCTURE["main"]["Random"], "Enter number"),
    "Character Stats": ("tabs", MENU_STRUCTURE["main"]["Character and Symbol"], "Enter Text"),
    "Number Analysis": ("tabs", MENU_STRUCTURE["main"]["Number analysis"], "Enter Numbers"),
    "Number Checker": ("tabs", MENU_STRUCTURE["main"]["Number Checker"], "Enter Number"),
    "Unit Converter": ("tabs", MENU_STRUCTURE["main"]["Unit Converter"], "Enter value"),
    "Color Converter": ("custom", "_show_color_converter_ui"),
    "Cipher Detection": ("custom", "_show_cipher_detection_ui"),
    "Classical Ciphers": (
        "vbox", 
        [
            ("Morse", "Morse"), 
            ("Braille", "Braille"), 
            ("Grid Cipher", "Grid Cipher"), 
            ("Emoji Cipher", "Emoji Cipher"), 
            ("Affine Cipher", "Affine Cipher"), 
            ("ROT-N", "ROT-N", "N"),
            ("Vigenere Cipher", "Vigenere Cipher", "Key")
        ]
    ),
    "Symmetric Encryption": (
        "vbox", 
        [
            ("AES", "AES", "Key"), 
            ("ChaCha20", "ChaCha20", "Key"), 
            ("DES", "DES", "Key"), 
            ("3DES", "3DES", "Key"), 
            ("Blowfish", "Blowfish", "Key")
        ]
    ),
    "Asymmetric Encryption": (
        "vbox", 
        [
            ("RSA", "RSA", "Key Size"), 
            ("ECC", "ECC", "Curve"), 
            ("ElGamal", "ElGamal", "Key Size")
        ]
    ),
    "Hashing": (
        "vbox", 
        [
            ("Cryptographic", "hash"), 
            ("Checksum", "cheksum")
        ]
    )
}

STYLES = {
    "main_button": """
        QPushButton {
            background-color: white;
            border: 2px solid black;
            border-radius: 3px;
            padding: 10px;
            color: black;
        }
        QPushButton:hover {
            background-color: #dd1124;
            border-bottom: 5px solid black;
            border-right: 5px solid black;
        }  
        QPushButton:pressed {
            background-color: #b60f20;           
        }    
    """,
    "menu_button": """
        QPushButton {
            background-color: white;
            border: 2px solid black;
            border-radius: 3px;
            padding: 10px;
            color: black;
        }
        QPushButton:hover {
            background-color: #dd1124;
            border-bottom: 5px solid black;
            border-right: 5px solid black;
        }  
        QPushButton:pressed {
            background-color: #b60f20;           
        }   
    """,
    "main_title_label": """
        QLabel {
            color: white;                 
            font-weight: bold;
            font-size: 30px; 
            background: transparent;
        }
    """,
    "title_label": """
        QLabel {
            color: white;                 
            font-weight: bold;
            font-size: 30px; 
            background: transparent;
            border: 1px solid white;
            border-radius: 6px;
            padding: 0px 5px;
        }
    """,
    "settings_label": """
        QLabel {
            color: white;                 
            font-weight: bold;
            font-size: 14px; 
            background: transparent;    
        }
    """,
    "close_button": """
        QPushButton {
            background-color: transparent;                
            color: white;                    
            font-size: 25px;  
            font-weight: bold;         
        }         
        QPushButton:hover {
            color: #dd1124;           
        }
    """,
    "minimize_button": """
        QPushButton {
            background-color: transparent;                
            color: white;                    
            font-size: 27px;
            font-weight: bold;     
        }         
        QPushButton:hover {
            color: #dd1124;          
        }
    """,
    "back_button": """
        QPushButton {
            border: none;
        }
        QPushButton:hover {
            border: none;
            color: #dd1124;
        }
    """,
    "copy_button": """
        QPushButton { background-color: transparent; border: None; color: white; }
    """,
    "gen_btn": """
        QPushButton {
            background-color: white;
            border: 2px solid black;
            border-radius: 3px;
            padding: 10px 20px;
            color: black;
        }
        QPushButton:hover {
            background-color: #dd1124;
            border-bottom: 5px solid black;
            border-right: 5px solid black;
        }   
    """,
    "text_edit": """
        QTextEdit {
            color: white;
            background-color: black;
            border: 4px solid white;
            border-radius: 5px;
            font-weight: bold;
            padding: 5px;
            selection-background-color: #dd1124;
            selection-color: white;
        }
        QScrollBar:vertical {
            background: black;
            width: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #666666;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #888888;
        }
        QScrollBar::handle:vertical:pressed {
            background: #dd1124;
        }
        QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {
            background: black;
        }
        QScrollBar:horizontal {
            background: black;
            height: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background: #666666;
            min-width: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #888888;
        }
        QScrollBar::handle:horizontal:pressed {
            background: #dd1124;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background: black;
            width: 0px;
        }
    """,
    "line_edit": """
        QLineEdit {
            color: black;
            background-color: white;
            border: 2px solid black;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
            selection-background-color: transparent;
            selection-color: black;
        }
        QLineEdit:hover {
            background-color: #dd1124;
            color: white;
        }
        QLineEdit:focus {
            background-color: #dd1124;
            color: white;
        }
    """,
    "line_edit_v2": """
        QTextEdit {
            color: black;
            background-color: white;
            border: 4px solid black;
            border-radius: 5px;
            font-weight: bold;
            padding: 5px;
            selection-background-color: #dd1124;
            selection-color: white;
        }
        QScrollBar:vertical {
            background: white;
            width: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #666666;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #888888;
        }
        QScrollBar::handle:vertical:pressed {
            background: #dd1124;
        }
        QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {
            background: white;
        }
        QScrollBar:horizontal {
            background: white;
            height: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background: #666666;
            min-width: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #888888;
        }
        QScrollBar::handle:horizontal:pressed {
            background: #dd1124;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background: white;
            width: 0px;
        }
    """,
    "Run_Button": """
        QPushButton {
            color: black;
            background-color: transparent;
            border: None;
        }
    """,
    "combo_box": """
        QComboBox {{
            background-color: #2D2D30;
            border: 2px solid #555555;
            border-radius: 8px;
            font-family: "Quicksand";
            font-size: 14px;
            font-weight: bold;
            color: #FFFFFF;
            min-height: 35px;
        }}
        QComboBox:hover {{
            background-color: #3E3E42;
            border: 2px solid #777777;
        }}
        QComboBox:focus {{
            background-color: #3E3E42;
            border: 2px solid white;
        }}
        QComboBox:on {{ 
            background-color: #3E3E42;
            border: 2px solid white;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left: 1px solid #555555;
            border-radius: 0 5px 5px 0;
            background-color: #2D2D30;
        }}
        QComboBox::drop-down:hover {{
            background-color: #3E3E42;
        }}
        QComboBox::down-arrow {{
            image: url({arrow_down_path});
            width: 14px;
            height: 14px;
        }}
        QComboBox::down-arrow:on {{
            image: url({arrow_up_path});
        }}

        QComboBox QAbstractItemView {{
            background-color: #2D2D30;
            color: #FFFFFF;
            selection-background-color: #dd1124;
            selection-color: #FFFFFF;
            border: 2px solid #555555;
            border-radius: 5px;
            outline: none;
            padding: 5px;
        }}
        QComboBox QAbstractItemView::item {{
            height: 30px;
            padding: 5px;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: #dd1124;
            color: #FFFFFF;
            border-radius: 3px;
        }}
        QComboBox QAbstractItemView QScrollBar:vertical {{
            background: #1f1f1f;
            width: 12px;
            margin: 0px 0px 0px 0px;
            border: none;
        }}
        QComboBox QAbstractItemView QScrollBar::handle:vertical {{
            background: #666666;
            min-height: 20px;
            border-radius: 5px;
        }}
        QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {{
            background: #888888;
        }}
        QComboBox QAbstractItemView QScrollBar::handle:vertical:pressed {{
            background: #dd1124;
        }}
        QComboBox QAbstractItemView QScrollBar::add-line:vertical, 
        QComboBox QAbstractItemView QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """,
    "non_editable_combo_box": """
        QComboBox {{
            color: white;
            border: 2px solid white;
            border-radius: 10px;
            padding-left: 15px;
            background: #2D2D30;
            text-align: center;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 1px;
            border-left-color: darkgray;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }}
        QComboBox::down-arrow {{
            image: url({arrow_down_path});
            width: 20px;
            height: 20px;
        }}
        QComboBox::down-arrow:on {{
            image: url({arrow_up_path});
        }}
        QComboBox QAbstractItemView {{
            border: 2px solid darkgray;
            selection-background-color: #dd1124;
            background-color: #2D2D30;
            color: white;
        }}
    """,
    "spin_box": """
        QSpinBox {
            padding-right: 15px; 
            border: 2px solid #555555;
            border-radius: 5px;
            background-color: #2D2D30;
            color: #FFFFFF;
            min-height: 35px;
            font-family: "Quicksand";
            font-weight: bold;
        }}
        QComboBox::down-arrow {{
            image: url({arrow_down_path});
            width: 20px;
            height: 20px;
        }}
        QComboBox::down-arrow:on {{
            image: url({arrow_up_path});
        }}
        QComboBox QAbstractItemView {{
            border: 2px solid darkgray;
            selection-background-color: #dd1124;
            background-color: #2D2D30;
            color: white;
        }}
    """,
    "color_input": """
        QPushButton {
            background-color: %s; /* Placeholder for dynamic color */
            border: 2px solid white;
            border-radius: 6px;
            padding: 5px;
            color: white;
        }
        QPushButton:hover {
            background-color: #555555;     
        }  
    """,
    "tab_widget": """
        QTabWidget::pane {
            background: transparent;
            border: 0px;
        }
        QTabBar::tab {
            background: transparent;
            color: white;
            padding: 5px 10px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            font-size: 18px;
        }
        QTabBar::tab:selected {
            background: white;
            color: black;
            font-weight: bold;
        }
    """,
    "tab_title": """
        QLabel {
            color: white;
            font-weight: bold;
            font-size: 24px;
        }
    """,
    "central_widget": "background: #1f1f1f; border-radius: 10px;",
    "transparent": "background: transparent;",
    "checkbox": "QCheckBox { color: white; background: transparent; }",
    "slider": """
        QSlider::groove:horizontal {
            border: none;
            height: 14px;
            border-radius: 7px;
            background: transparent;
            margin: 0;
        }
        QSlider::sub-page:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dd1124, stop:1 #ff4455);
            border: none;
            height: 14px;
            border-radius: 7px;
        }
        QSlider::add-page:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #555, stop:1 #888);
            border: none;
            height: 14px;
            border-radius: 7px;
        }
        QSlider::handle:horizontal {
            background: white;
            border: none;
            width: 34px;
            height: 14px;
            margin: 0px 0;
            border-radius: 7px;
        }
        QSlider::handle:horizontal:hover, QSlider::handle:horizontal:pressed {
            background: #cccccc;
        }
    """,
    "slider_vertical": """
        QSlider::groove:vertical {
            background: black;
            width: 12px;
            margin: 0;
        }
        QSlider::handle:vertical {
            background: #666666;
            height: 20px;
            border-radius: 6px;
            margin: 0;
        }
        QSlider::handle:vertical:hover {
            background: #888888;
        }
        QSlider::handle:vertical:pressed {
            background: #dd1124;
        }
        QSlider::add-page:vertical {
            background: black;
        }
        QSlider::sub-page:vertical {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #dd1124, stop:1 #ff4455);
            border: none;
            border-radius: 6px;
        }
    """,
    "settings_group": """
        QFrame {
            border: 2px solid #CCCCCC;
            border-radius: 8px;
            background-color: transparent;
            margin-top: 10px;
        }
    """,
    "completer_popup": """
        QListView {
            background-color: #2D2D30;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 4px;
        }
        QListView::item {
            padding: 5px;
            border-radius: 3px;
        }
        QListView::item:selected {
            background-color: #dd1124;
            color: white;
        }
        QListView::item:hover:!selected {
            background-color: #3E3E42;
        }
        QListView QScrollBar:vertical {
            background: #2D2D30;
            width: 10px;
            margin: 0px 0px 0px 0px;
            border: none;
        }
        QListView QScrollBar::handle:vertical {
            background: #666666;
            min-height: 20px;
            border-radius: 5px;
        }
        QListView QScrollBar::handle:vertical:hover {
            background: #888888;
        }
        QListView QScrollBar::handle:vertical:pressed {
            background: #dd1124;
        }
        QListView QScrollBar::add-line:vertical, 
        QListView QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """
}

DARK_MODE_STYLES = {
    "background": "background-color: black;",
    "line_edit": """
        QLineEdit {
            color: #FFFFFF;
            background-color: #3C3C3C;
            border: 2px solid #CCCCCC;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
            selection-background-color: #dd1124;
            selection-color: #FFFFFF;
        }
        QLineEdit:focus, QLineEdit:hover {
            background-color: #3E3E42;
            border: 2px solid #777777;
        }
    """,
    "text_edit": """
        QTextEdit {
            color: white;
            background-color: #252526;
            border: 2px solid white;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
            selection-background-color: #dd1124;
            selection-color: white;
        }
        QTextEdit:focus, QTextEdit:hover {
            border: 2px solid #777777;
        }
        QScrollBar:vertical {
            background: #252526;
            width: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #666666;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #888888;
        }
        QScrollBar::handle:vertical:pressed {
            background: #dd1124;
        }
        QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {
            background: #252526;
        }
        QScrollBar:horizontal {
            background: #252526;
            height: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background: #666666;
            min-width: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #888888;
        }
        QScrollBar::handle:horizontal:pressed {
            background: #dd1124;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background: #252526;
            width: 0px;
        }
    """,
    "app_stylesheet_dark": """
        QLineEdit, QTextEdit {
            color: white;
            background-color: #3C3C3C;            
            border: 2px solid #CCCCCC;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
        }
        QComboBox QAbstractItemView {
            background-color: #2D2D30;
            color: #FFFFFF;
            border: 2px solid #CCCCCC;
        }
        QPushButton {
            background-color: #333333;
            border-radius: 3px;
            padding: 10px;
            color: white;
        }
        """,
    "mainMenuButton_dark": """
        QPushButton {
            background-color: #3C3C3C; 
            border: 2px solid #999999;
            border-radius: 3px;
            padding: 10px;
            color: white;
        }
        QPushButton:hover {
            background-color: #3C3C3C; 
            border-bottom: 5px solid #999999;
            border-right: 5px solid #999999;
        }
        QPushButton:pressed {
            background-color: #2A2A2A; 
        }
        QPushButton#run_button_color {
            background-color: white;
            color: black;
            border: 2px solid #CCCCCC;
        }
        QCheckBox#settingsDarkModeCheckbox {
            color: white;
            background: transparent;
        }
        QSlider::groove:horizontal {
            border: none;
            height: 14px;
            border-radius: 7px;
            background: transparent;
            margin: 0;
        }
        QSlider::sub-page:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dd1124, stop:1 #ff4455);
            border: none;
            height: 14px;
            border-radius: 7px;
        }
        QSlider::add-page:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #555, stop:1 #888);
            border: none;
            height: 14px;
            border-radius: 7px;
        }
        QSlider::handle:horizontal {
            background: white;
            border: none;
            width: 34px;
            height: 14px;
            margin: 0px 0;
            border-radius: 7px;
        }
        QSlider::handle:horizontal:hover, QSlider::handle:horizontal:pressed {
            background: #cccccc;
        }
    """
}
UNIT_CATEGORIES = {
    "Length", "Mass", "Temperature", "Speed", "Pressure",
    "Energy", "Power", "Time", "Digital"
}

LIST_COMBO_BOX = {
    "Characters": ["thing", "thing2"],
    "Basic Statistics": ["thing3", "thing4"]
}

Unit_Items = {
    "Length": (
        ["mm", "cm", "m", "km", "inch", "ft", "yard", "mile"],
        ["mm", "cm", "m", "km", "inch", "ft", "yard", "mile"]
    ),
    "Mass": (
        ["g", "kg", "mg", "ton", "lb", "oz"],
        ["g", "kg", "mg", "ton", "lb", "oz"]
    ),
    "Temperature": (
        ["C", "K", "F"],
        ["C", "K", "F"]
    ),
    "Speed": (
        ["m/s", "km/h", "mph", "knot"],
        ["m/s", "km/h", "mph", "knot"]
    ),
    "Pressure": (
        ["Pa", "kPa", "bar", "atm", "psi", "torr"],
        ["Pa", "kPa", "bar", "atm", "psi", "torr"]
    ),
    "Energy": (
        ["J", "kJ", "cal", "kcal", "Wh", "kWh"],
        ["J", "kJ", "cal", "kcal", "Wh", "kWh"]
    ),
    "Power": (
        ["W", "kW", "hp"],
        ["W", "kW", "hp"]
    ),
    "Time": (
        ["s", "min", "h", "day", "week", "month", "year"],
        ["s", "min", "h", "day", "week", "month", "year"]
    ),
    "Digital": (
        ["bit", "B", "KB", "MB", "GB", "TB", "PB"],
        ["bit", "B", "KB", "MB", "GB", "TB", "PB"]
    )
}

LANGUAGE_PATTERNS = {
    'HTML': [(re.compile(r'<!DOCTYPE html>', re.I), 10), (re.compile(r'<html.*?>', re.I), 5)],
    'XML': [(re.compile(r'<\?xml version=.*?\?>', re.I), 10)],
    'CSS': [(re.compile(r'[\w\s\.\#\*]+\s*\{[^\}]+\}', re.I), 5), (re.compile(r'font-family:|background-color:'), 2)],
    'Python': [(re.compile(r'^\s*def\s+\w+\(.*\):', re.M), 3), (re.compile(r'^\s*import\s+[\w\.]+', re.M), 4), (re.compile(r'from\s+[\w\.]+\s+import', re.M), 4), (re.compile(r'print\(|len\(|range\('), 1)],
    'JavaScript': [(re.compile(r'function\s*\w*\(.*\)\s*\{'), 2), (re.compile(r'\b(const|let|var)\s+\w+\s*='), 2), (re.compile(r'console\.log\(', re.I), 4)],
    'TypeScript': [(re.compile(r':\s*(string|number|boolean|any|void)'), 5), (re.compile(r'interface\s+\w+'), 5)],
    'Java': [(re.compile(r'public\s+class\s+\w+'), 5), (re.compile(r'System\.out\.println'), 4), (re.compile(r'public\s+static\s+void\s+main', re.M), 8)],
    'C#': [(re.compile(r'namespace\s+\w+'), 5), (re.compile(r'Console\.WriteLine'), 4), (re.compile(r'using\s+System;'), 6)],
    'C++': [(re.compile(r'#include\s*<iostream>'), 6), (re.compile(r'std::cout'), 4)],
    'C': [(re.compile(r'#include\s*<stdio\.h>'), 6), (re.compile(r'printf\s*\('), 4)],
    'PHP': [(re.compile(r'<\?php'), 10), (re.compile(r'\$\w+'), 2)],
    'Ruby': [(re.compile(r'^\s*def\s+\w+', re.M), 3), (re.compile(r'puts\s+'), 4), (re.compile(r'require\s+'), 5)],
    'Go': [(re.compile(r'package\s+\w+'), 8), (re.compile(r'func\s+\w+\(.*\)'), 3), (re.compile(r'fmt\.Println'), 4)],
    'Rust': [(re.compile(r'fn\s+\w+\(.*\)'), 4), (re.compile(r'let\s+mut\s+'), 4), (re.compile(r'println!'), 5)],
    'SQL': [(re.compile(r'\b(SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE\s+TABLE)\b', re.I), 8)],
    'Bash/Shell': [(re.compile(r'#!/bin/bash'), 10), (re.compile(r'\becho\s+'), 3)]
}
# Data :
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"
digits_base64_url = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
numbers = "0123456789"
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
alphabet_base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
alphabet_base62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
alphabet_base36 = digits[:36]
Bases_set = {2, 8, 10, 16, 32, 36, 58, 62, 64, 85, -1}
ELGAMAL_PARAMETERS = {}
characters = string.ascii_letters + string.digits + string.punctuation
max_length = 100_000
max_length_1 = 500_000
max_length_2 = 1_000
max_length_3 = 10_000
allowed = {2, 8, 10, 16, 32, 36, 58, 64, 85, -1}
for k, v in BRAILLE_DICT.items():
    if k.isdigit():
        BRAILLE_TO_TEXT[BRAILLE_NUMBER_PREFIX + v] = k
    else:
        BRAILLE_TO_TEXT[v] = k
generators_list = ["Random Password Generator", "Random Letters Generator", "Random Number Generator", "Random ID Generator",
                   "Random IP adress Generator", "Coprimes Generator", "Prime numbers", "Triangular numbers"]

UI_KEYWORDS_WITH_BASE = [
    "Custom", "ROT-N", "ISO", "UTF-N", "AES", "ChaCha20",
    "DES", "3DES", "Triple DES", "Blowfish", "Twofish", "Affine", "Vigenere Cipher",
    "Divisibility Checker"
]
UI_KEYWORDS_BINARY_ENCODING = [
    "Base2", "Base8", "Base10", "Base16", "Base32",
    "Base36", "Base58", "Base62", "Base64", "Base85", "BaseURL"
]
UI_KEYWORDS_ANALYZERS = [
    "Characters", "Character Frequency", "Repeated sequences detection",
    "Entropy", "Extract Num", "Number Frequency", "Basic Statistics",
    "Language Detection", "Syntax Analysis", "Special Properties"
]

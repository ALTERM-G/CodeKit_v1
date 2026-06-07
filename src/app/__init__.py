import json
import os
import sys
from typing import Dict
from .ui.main_window import Window

_translations: Dict[str, Dict[str, str]] = {}
_current_language: str = "English"

def load_translations():
    """Loads translation data from the translations.json file."""
    global _translations
    # Get the path of the current file (__init__.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    translations_path = os.path.join(current_dir, '..', '..', 'data', 'translations.json')

    try:
        with open(translations_path, 'r', encoding='utf-8') as f:
            _translations = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading translations: {e}")
        _translations = {}

def set_language(language: str):
    """Sets the current language for translations."""
    global _current_language
    if language in _translations:
        _current_language = language

def translate(key: str) -> str:
    """Translates a given key to the current language."""
    return _translations.get(_current_language, {}).get(key, key)
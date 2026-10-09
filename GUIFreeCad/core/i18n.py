"""Localization system for the GUI."""

import json
from pathlib import Path
from typing import Dict, Any

_cache: Dict[str, dict] = {}
_DEFAULT_LANG = "es"

# Path to the i18n directory where translation files are stored
I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"


def _load(lang: str) -> dict:
    """Load translation strings for a language, with caching."""
    if lang in _cache:
        return _cache[lang]

    source = I18N_DIR / f"{lang}.json"
    if source.is_file():
        try:
            # Use "utf-8-sig" to safely ignore any Byte Order Mark (BOM)
            _cache[lang] = json.loads(source.read_text(encoding="utf-8-sig"))
            return _cache[lang]
        except (json.JSONDecodeError, OSError) as e:
            print(f"[i18n] Error loading {lang}.json: {e}")

    _cache[lang] = {}
    return _cache[lang]


def tr(key: str, target_lang: str = _DEFAULT_LANG, **kwargs: Any) -> str:
    """Translate a key to the given language."""
    strings = _load(target_lang)
    if key not in strings:
        strings = _load(_DEFAULT_LANG)

    text = strings.get(key, key)

    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text


def get_available_languages() -> list[str]:
    """Return a list of available language codes."""
    if not I18N_DIR.is_dir():
        return [_DEFAULT_LANG]
    
    langs = []
    for p in I18N_DIR.glob("*.json"):
        langs.append(p.stem)
    
    if not langs:
        return [_DEFAULT_LANG]
    return sorted(langs)


def clear_cache() -> None:
    """Clear the translation cache to force reloading."""
    _cache.clear()
# ATRIA GUI commands package
import importlib
import sys as _sys

for _sub in ("core", "integration", "speech", "navigation", "ui", "InputPrompts"):
    try:
        _mod = importlib.import_module(f"GUIFreeCad.{_sub}")
        _sys.modules.setdefault(_sub, _mod)
    except Exception:
        pass

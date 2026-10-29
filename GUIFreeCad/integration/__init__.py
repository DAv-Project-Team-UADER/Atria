"""FreeCAD integration helpers for GUIFreeCad."""
import sys as _sys

_sys.modules.setdefault("integration", _sys.modules[__name__])
_sys.modules.setdefault("GUIFreeCad.integration", _sys.modules[__name__])

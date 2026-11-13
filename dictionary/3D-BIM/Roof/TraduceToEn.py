"""English spoken-word mapping for the Roof function of ATRIA (3D-BIM)."""

try:
    from .Roof import Roof
except ImportError:
    Roof = None

TraduceToEn = {
    "create covering":      Roof,
    "new covering":         Roof,
    "generate covering":    Roof,
    "add sloped covering":  Roof,
}
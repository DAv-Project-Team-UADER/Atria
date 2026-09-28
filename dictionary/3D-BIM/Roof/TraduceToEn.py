"""English spoken-word mapping for the Roof function of ATRIA (3D-BIM)."""

try:
    from .Roof import Roof
except ImportError:
    Roof = None

TraduceToEn = {
    "create roof":          Roof,
    "new roof":             Roof,
    "generate roof":        Roof,
    "add sloped roof":      Roof,
}
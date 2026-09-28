"""English spoken-word mapping for the Space function of ATRIA (3D-BIM)."""

try:
    from .Space import Space
except ImportError:
    Space = None

TraduceToEn = {
    "create space":         Space,
    "new ambience":         Space,
    "generate room":        Space,
    "add space":            Space,
}
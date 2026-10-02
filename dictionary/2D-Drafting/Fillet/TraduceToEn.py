"""English spoken-word mapping for the Fillet function of ATRIA (2D-Drafting)."""

try:
    from .Fillet import Fillet
except ImportError:
    Fillet = None

TraduceToEn = {
    "chamfer":        Fillet,
    "fillet":         Fillet,
    "fillet edge":    Fillet,
    "trim edge":      Fillet,
}
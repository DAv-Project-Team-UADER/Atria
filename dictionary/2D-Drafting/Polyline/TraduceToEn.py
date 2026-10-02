"""English spoken-word mapping for the Polyline function of ATRIA (2D-Drafting)."""

try:
    from .Polyline import Polyline
except ImportError:
    Polyline = None

TraduceToEn = {
    "polyline":         Polyline,
    "create polyline":  Polyline,
    "connect points":   Polyline,
}
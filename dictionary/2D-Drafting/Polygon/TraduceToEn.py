"""English spoken-word mapping for the Polygon function of ATRIA (2D-Drafting)."""

try:
    from .Polygon import Polygon
except ImportError:
    Polygon = None

TraduceToEn = {
    "polygon":                 Polygon,
    "create polygon":          Polygon,
    "create regular polygon":  Polygon,
    "regular polygon":         Polygon,
}
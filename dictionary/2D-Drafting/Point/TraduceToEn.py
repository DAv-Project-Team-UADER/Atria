"""English spoken-word mapping for the Point function of ATRIA (2D-Drafting)."""

try:
    from .Point import Point
except ImportError:
    Point = None

TraduceToEn = {
    "point":         Point,
    "create point":  Point,
}
"""English spoken-word mapping for the Rectangle function of ATRIA (2D-Drafting)."""

try:
    from .Rectangle import Rectangle
except ImportError:
    Rectangle = None

TraduceToEn = {
    "rectangle":         Rectangle,
    "create rectangle":  Rectangle,
}
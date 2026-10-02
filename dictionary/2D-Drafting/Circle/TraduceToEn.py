"""English spoken-word mapping for the Circle function of ATRIA (2D-Drafting)."""

try:
    from .Circle import Circle
except ImportError:
    Circle = None

TraduceToEn = {
    "create circle":        Circle,
    "circle":               Circle,
    "circumference":        Circle,
    "create circumference": Circle,
}
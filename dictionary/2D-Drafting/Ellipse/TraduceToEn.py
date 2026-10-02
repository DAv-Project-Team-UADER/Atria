"""English spoken-word mapping for the Ellipse function of ATRIA (2D-Drafting)."""

try:
    from .Ellipse import Ellipse
except ImportError:
    Ellipse = None

TraduceToEn = {
    "ellipse":         Ellipse,
    "create ellipse":  Ellipse,
}
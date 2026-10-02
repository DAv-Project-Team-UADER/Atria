"""English spoken-word mapping for the Arc function of ATRIA (2D-Drafting)."""

try:
    from .Arc import Arc
except ImportError:
    Arc = None

TraduceToEn = {
    "arc":             Arc,
    "curve":           Arc,
    "create arc":      Arc,
    "create curve":    Arc,
}
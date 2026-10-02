"""English spoken-word mapping for the Line function of ATRIA (2D-Drafting)."""

try:
    from .Line import Line
except ImportError:
    Line = None

TraduceToEn = {
    "line":                 Line,
    "create line":          Line,
    "create straight line": Line,
    "straight line":        Line,
}
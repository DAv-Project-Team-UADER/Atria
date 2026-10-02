"""English spoken-word mapping for the Arc from 3 points function of ATRIA (2D-Drafting)."""

try:
    from .ArcFrom3Points import ArcFrom3Points
except ImportError:
    ArcFrom3Points = None

TraduceToEn = {
    "arc from 3 points":            ArcFrom3Points,
    "curve from 3 points":          ArcFrom3Points,
    "curve by 3 points":            ArcFrom3Points,
    "arc by 3 points":              ArcFrom3Points,
    "create arc from 3 points":     ArcFrom3Points,
    "create curve from 3 points":   ArcFrom3Points,
    "create curve by 3 points":     ArcFrom3Points,
    "create arc by 3 points":       ArcFrom3Points,
}
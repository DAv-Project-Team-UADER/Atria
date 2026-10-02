"""English spoken-word mapping for the Bezier Curve function of ATRIA (2D-Drafting)."""

try:
    from .BezierCurve import BezierCurve
except ImportError:
    BezierCurve = None

TraduceToEn = {
    "bezier curve":        BezierCurve,
    "create bezier curve": BezierCurve,
}
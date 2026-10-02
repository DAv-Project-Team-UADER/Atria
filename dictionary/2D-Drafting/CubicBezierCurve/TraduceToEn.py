"""English spoken-word mapping for the Cubic Bezier Curve function of ATRIA (2D-Drafting)."""

try:
    from .CubicBezierCurve import CubicBezierCurve
except ImportError:
    CubicBezierCurve = None

TraduceToEn = {
    "cubic bezier curve":        CubicBezierCurve,
    "create cubic bezier curve": CubicBezierCurve,
    "cubic curve":               CubicBezierCurve,
}
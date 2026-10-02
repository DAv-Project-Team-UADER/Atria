"""Comandos de voz en español para la función Curva de Bezier cúbica (CubicBezierCurve) de ATRIA (2D-Drafting)."""

try:
    from .CubicBezierCurve import CubicBezierCurve
except ImportError:
    CubicBezierCurve = None

TraduceToEs = {
    "curva de bezier cúbica":      CubicBezierCurve,
    "curva bezier cúbica":         CubicBezierCurve,
    "crear curva bezier cúbica":   CubicBezierCurve,
    "crear curva de bezier cúbica": CubicBezierCurve,
    "curva cúbica":                CubicBezierCurve,
}
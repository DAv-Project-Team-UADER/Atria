"""Comandos de voz en español para la función Curva de Bezier (BezierCurve) de ATRIA (2D-Drafting)."""

try:
    from .BezierCurve import BezierCurve
except ImportError:
    BezierCurve = None

TraduceToEs = {
    "curva de bezier":          BezierCurve,
    "crear curva de bezier":    BezierCurve,
    "crear curva bezier":       BezierCurve,
    "curva bezier":             BezierCurve,
}
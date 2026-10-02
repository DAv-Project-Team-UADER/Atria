"""Comandos de voz en español para la función B-Spline (B-Spline) de ATRIA (2D-Drafting)."""

try:
    # El nombre del módulo lleva un guion, por eso no se puede importar con `from . import`.
    from importlib import import_module

    BSpline = import_module(".B-Spline", __package__).BSpline
except ImportError:
    BSpline = None

TraduceToEs = {
    "b spline":             BSpline,
    "curva b":              BSpline,
    "curva b spline":       BSpline,
    "crear curva b":        BSpline,
    "crear curva b spline": BSpline,
}
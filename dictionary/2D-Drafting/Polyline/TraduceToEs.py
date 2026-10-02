"""Comandos de voz en español para la función Polilínea (Polyline) de ATRIA (2D-Drafting)."""

try:
    from .Polyline import Polyline
except ImportError:
    Polyline = None

TraduceToEs = {
    "polilínea":        Polyline,
    "crear polilínea":  Polyline,
    "conectar puntos":  Polyline,
}
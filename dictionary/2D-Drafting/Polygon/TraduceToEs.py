"""Comandos de voz en español para la función Polígono (Polygon) de ATRIA (2D-Drafting)."""

try:
    from .Polygon import Polygon
except ImportError:
    Polygon = None

TraduceToEs = {
    "polígono":                 Polygon,
    "crear polígono":           Polygon,
    "crear polígono regular":   Polygon,
    "polígono regular":         Polygon,
}
"""Comandos de voz en español para la función Elipse (Ellipse) de ATRIA (2D-Drafting)."""

try:
    from .Ellipse import Ellipse
except ImportError:
    Ellipse = None

TraduceToEs = {
    "elipse":         Ellipse,
    "crear elipse":   Ellipse,
}
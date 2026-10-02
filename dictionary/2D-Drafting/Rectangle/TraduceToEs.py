"""Comandos de voz en español para la función Rectángulo (Rectangle) de ATRIA (2D-Drafting)."""

try:
    from .Rectangle import Rectangle
except ImportError:
    Rectangle = None

TraduceToEs = {
    "rectángulo":         Rectangle,
    "crear rectángulo":   Rectangle,
}
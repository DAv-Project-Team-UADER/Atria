"""Comandos de voz en español para la función Círculo (Circle) de ATRIA (2D-Drafting)."""

try:
    from .Circle import Circle
except ImportError:
    Circle = None

TraduceToEs = {
    "crear círculo":            Circle,
    "círculo":                  Circle,
    "circunferencia":           Circle,
    "crear circunferencia":    Circle,
}
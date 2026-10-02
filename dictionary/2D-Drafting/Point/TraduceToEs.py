"""Comandos de voz en español para la función Punto (Point) de ATRIA (2D-Drafting)."""

try:
    from .Point import Point
except ImportError:
    Point = None

TraduceToEs = {
    "punto":         Point,
    "crear punto":   Point,
}
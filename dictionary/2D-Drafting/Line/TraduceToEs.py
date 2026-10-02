"""Comandos de voz en español para la función Línea (Line) de ATRIA (2D-Drafting)."""

try:
    from .Line import Line
except ImportError:
    Line = None

TraduceToEs = {
    "línea":               Line,
    "crear línea":         Line,
    "crear línea recta":   Line,
    "línea recta":         Line,
    "crear recta":         Line,
    "recta":               Line,
}
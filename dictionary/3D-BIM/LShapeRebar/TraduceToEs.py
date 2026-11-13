"""Comandos de voz en español para la función Armadura en L (LShapeRebar) de ATRIA (3D-BIM)."""

try:
    from .LShapeRebar import LShapeRebar
except ImportError:
    LShapeRebar = None

TraduceToEs = {
    "crear armadura en L":            LShapeRebar,
    "nueva barra en L":               LShapeRebar,
    "generar armadura en L":          LShapeRebar,
    "añadir barra de refuerzo en L":  LShapeRebar,
    "crear rebar en L":               LShapeRebar,
    "crear armadura en forma de L":   LShapeRebar,
    "crear armadura en forma de ele": LShapeRebar,
    "crear barra en forma de ele":    LShapeRebar,
}
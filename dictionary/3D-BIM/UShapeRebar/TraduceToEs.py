"""Comandos de voz en español para la función Armadura en U (UShapeRebar) de ATRIA (3D-BIM)."""

try:
    from .UShapeRebar import UShapeRebar
except ImportError:
    UShapeRebar = None

TraduceToEs = {
    "crear armadura en U":           UShapeRebar,
    "nueva barra en U":              UShapeRebar,
    "generar armadura en U":         UShapeRebar,
    "añadir barra de refuerzo en U": UShapeRebar,
    "crear rebar en U":              UShapeRebar,
}
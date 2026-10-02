"""Comandos de voz en español para la función Armadura doblada (BentShapeRebar) de ATRIA (3D-BIM)."""

try:
    from .BentShapeRebar import BentShapeRebar
except ImportError:
    BentShapeRebar = None

TraduceToEs = {
    "crear armadura doblada":           BentShapeRebar,
    "nueva barra doblada":              BentShapeRebar,
    "generar armadura doblada":         BentShapeRebar,
    "añadir barra de refuerzo doblada": BentShapeRebar,
    "crear rebar doblado":              BentShapeRebar,
}
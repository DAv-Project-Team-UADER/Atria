"""Comandos de voz en español para la función Armadura recta (StraightRebar) de ATRIA (3D-BIM)."""

try:
    from .StraightRebar import StraightRebar
except ImportError:
    StraightRebar = None

TraduceToEs = {
    "crear armadura recta":           StraightRebar,
    "nueva barra recta":              StraightRebar,
    "generar armadura recta":         StraightRebar,
    "añadir barra de refuerzo recta": StraightRebar,
    "crear rebar recto":              StraightRebar,
}
"""Comandos de voz en español para la función Armadura helicoidal (HelicalRebar) de ATRIA (3D-BIM)."""

try:
    from .HelicalRebar import HelicalRebar
except ImportError:
    HelicalRebar = None

TraduceToEs = {
    "crear armadura helicoidal":   HelicalRebar,
    "nueva barra helicoidal":      HelicalRebar,
    "generar armadura en espiral": HelicalRebar,
    "añadir barra helicoidal":     HelicalRebar,
    "crear rebar helicoidal":      HelicalRebar,
}
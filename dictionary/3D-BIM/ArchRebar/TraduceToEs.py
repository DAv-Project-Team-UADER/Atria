"""Comandos de voz en español para la función Armadura personalizada (ArchRebar) de ATRIA (3D-BIM)."""

try:
    from .ArchRebar import ArchRebar
except ImportError:
    ArchRebar = None

TraduceToEs = {
    "crear armadura personalizada": ArchRebar,
    "nueva barra de refuerzo":      ArchRebar,
    "generar armadura":             ArchRebar,
    "añadir rebar":                 ArchRebar,
    "crear barra personalizada":    ArchRebar,
}
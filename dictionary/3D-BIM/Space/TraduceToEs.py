"""Comandos de voz en español para la función Espacio (Space) de ATRIA (3D-BIM)."""

try:
    from .Space import Space
except ImportError:
    Space = None

TraduceToEs = {
    "crear espacio":        Space,
    "nuevo ambiente":       Space,
    "generar habitación":   Space,
    "añadir espacio":       Space,
}
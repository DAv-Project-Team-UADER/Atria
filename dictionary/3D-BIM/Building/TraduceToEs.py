"""Comandos de voz en español para la función Edificio (Building) de ATRIA (3D-BIM)."""

try:
    from .Building import Building
except ImportError:
    Building = None

TraduceToEs = {
    "crear edificio":       Building,
    "nuevo edificio":       Building,
    "generar edificio":     Building,
    "añadir edificio":      Building,
}
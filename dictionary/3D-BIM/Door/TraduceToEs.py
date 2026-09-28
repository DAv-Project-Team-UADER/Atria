"""Comandos de voz en español para la función Puerta (Door) de ATRIA (3D-BIM)."""

try:
    from .Door import Door
except ImportError:
    Door = None

TraduceToEs = {
    "crear puerta":         Door,
    "nueva puerta":         Door,
    "generar puerta":       Door,
    "añadir puerta":        Door,
}
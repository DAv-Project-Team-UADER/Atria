"""Comandos de voz en español para la función Losa (Slab) de ATRIA (3D-BIM)."""

try:
    from .Slab import Slab
except ImportError:
    Slab = None

TraduceToEs = {
    "crear losa":           Slab,
    "nueva losa":           Slab,
    "generar placa":        Slab,
    "añadir losa":          Slab,
}
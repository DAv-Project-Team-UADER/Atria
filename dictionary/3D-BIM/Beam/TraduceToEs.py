"""Comandos de voz en español para la función Haz / Viga (Beam) de ATRIA (3D-BIM)."""

try:
    from .Beam import Beam
except ImportError:
    Beam = None

TraduceToEs = {
    "crear viga":           Beam,
    "nueva viga":           Beam,
    "generar haz":          Beam,
    "añadir viga":          Beam,
}
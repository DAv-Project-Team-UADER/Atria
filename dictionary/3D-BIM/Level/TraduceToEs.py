"""Comandos de voz en español para la función Nivel (Level) de ATRIA (3D-BIM)."""

try:
    from .Level import Level
except ImportError:
    Level = None

TraduceToEs = {
    "crear nivel":          Level,
    "nuevo nivel":          Level,
    "generar piso":         Level,
    "añadir nivel":         Level,
    "crear planta":         Level,
}
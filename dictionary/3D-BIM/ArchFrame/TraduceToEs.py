"""Comandos de voz en español para la función Marco (ArchFrame) de ATRIA (3D-BIM)."""

try:
    from .ArchFrame import ArchFrame
except ImportError:
    ArchFrame = None

TraduceToEs = {
    "crear marco":   ArchFrame,
    "nuevo marco":   ArchFrame,
    "generar marco": ArchFrame,
    "añadir marco":  ArchFrame,
}
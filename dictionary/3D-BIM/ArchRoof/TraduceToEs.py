"""Comandos de voz en español para la función Techo (ArchRoof) de ATRIA (3D-BIM)."""

try:
    from .ArchRoof import ArchRoof
except ImportError:
    ArchRoof = None

TraduceToEs = {
    "crear techo":   ArchRoof,
    "nuevo techo":   ArchRoof,
    "generar techo": ArchRoof,
    "añadir techo":  ArchRoof,
}
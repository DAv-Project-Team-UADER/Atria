"""Comandos de voz en español para la función Cerca (ArchFence) de ATRIA (3D-BIM)."""

try:
    from .ArchFence import ArchFence
except ImportError:
    ArchFence = None

TraduceToEs = {
    "crear cerca":   ArchFence,
    "nueva cerca":   ArchFence,
    "generar cerca": ArchFence,
    "añadir cerca":  ArchFence,
}
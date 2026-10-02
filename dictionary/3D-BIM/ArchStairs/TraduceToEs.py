"""Comandos de voz en español para la función Escalera (ArchStairs) de ATRIA (3D-BIM)."""

try:
    from .ArchStairs import ArchStairs
except ImportError:
    ArchStairs = None

TraduceToEs = {
    "crear escalera":   ArchStairs,
    "nueva escalera":   ArchStairs,
    "generar escalera": ArchStairs,
    "añadir escalera":  ArchStairs,
}
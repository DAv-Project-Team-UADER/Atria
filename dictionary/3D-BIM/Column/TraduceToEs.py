"""Comandos de voz en español para la función Columna (Column) de ATRIA (3D-BIM)."""

try:
    from .Column import Column
except ImportError:
    Column = None

TraduceToEs = {
    "crear columna":        Column,
    "nueva columna":        Column,
    "generar pilar":        Column,
    "añadir columna":       Column,
}
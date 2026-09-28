"""Comandos de voz en español para la función Muro (Wall) de ATRIA (3D-BIM)."""

try:
    from .Wall import Wall
except ImportError:
    Wall = None

TraduceToEs = {
    "crear muro":           Wall,
    "nuevo muro":           Wall,
    "generar pared":        Wall,
    "añadir muro":          Wall,
}
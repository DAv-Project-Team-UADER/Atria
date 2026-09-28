"""Comandos de voz en español para la función Cubierta (Roof) de ATRIA (3D-BIM)."""

try:
    from .Roof import Roof
except ImportError:
    Roof = None

TraduceToEs = {
    "crear cubierta":       Roof,
    "nuevo techo":          Roof,
    "generar cubierta":     Roof,
    "añadir techo inclinado": Roof,
}
"""Comandos de voz en español para la función Muro cortina (Curtain Wall) de ATRIA (3D-BIM)."""

try:
    from .CurtainWall import CurtainWall
except ImportError:
    CurtainWall = None

TraduceToEs = {
    "crear muro cortina":   CurtainWall,
    "nuevo muro cortina":   CurtainWall,
    "generar fachada de cristal": CurtainWall,
    "añadir curtain wall":  CurtainWall,
}
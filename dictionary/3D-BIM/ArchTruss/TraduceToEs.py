"""Comandos de voz en español para la función Armadura (ArchTruss) de ATRIA (3D-BIM)."""

try:
    from .ArchTruss import ArchTruss
except ImportError:
    ArchTruss = None

TraduceToEs = {
    "crear armadura":   ArchTruss,
    "nueva armadura":   ArchTruss,
    "generar armadura": ArchTruss,
    "añadir armadura":  ArchTruss,
    "crear celosía":    ArchTruss,
}
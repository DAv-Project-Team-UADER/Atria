"""Comandos de voz en español para la función Panel (ArchPanel) de ATRIA (3D-BIM)."""

try:
    from .ArchPanel import ArchPanel
except ImportError:
    ArchPanel = None

TraduceToEs = {
    "crear panel":   ArchPanel,
    "nuevo panel":   ArchPanel,
    "generar panel": ArchPanel,
    "añadir panel":  ArchPanel,
}
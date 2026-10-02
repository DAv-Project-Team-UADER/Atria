"""English spoken-word mapping for the Arch Panel function of ATRIA (3D-BIM)."""

try:
    from .ArchPanel import ArchPanel
except ImportError:
    ArchPanel = None

TraduceToEn = {
    "create panel":   ArchPanel,
    "new panel":      ArchPanel,
    "generate panel": ArchPanel,
    "add panel":      ArchPanel,
}
"""English spoken-word mapping for the Arch Frame function of ATRIA (3D-BIM)."""

try:
    from .ArchFrame import ArchFrame
except ImportError:
    ArchFrame = None

TraduceToEn = {
    "create frame":   ArchFrame,
    "new frame":      ArchFrame,
    "generate frame": ArchFrame,
    "add frame":      ArchFrame,
}
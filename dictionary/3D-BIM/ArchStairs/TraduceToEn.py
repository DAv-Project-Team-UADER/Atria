"""English spoken-word mapping for the Arch Stairs function of ATRIA (3D-BIM)."""

try:
    from .ArchStairs import ArchStairs
except ImportError:
    ArchStairs = None

TraduceToEn = {
    "create stairs":   ArchStairs,
    "new stairs":      ArchStairs,
    "generate stairs": ArchStairs,
    "add stairs":      ArchStairs,
}
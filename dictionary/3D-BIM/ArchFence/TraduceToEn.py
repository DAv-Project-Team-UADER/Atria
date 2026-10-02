"""English spoken-word mapping for the Arch Fence function of ATRIA (3D-BIM)."""

try:
    from .ArchFence import ArchFence
except ImportError:
    ArchFence = None

TraduceToEn = {
    "create fence":   ArchFence,
    "new fence":      ArchFence,
    "generate fence": ArchFence,
    "add fence":      ArchFence,
}
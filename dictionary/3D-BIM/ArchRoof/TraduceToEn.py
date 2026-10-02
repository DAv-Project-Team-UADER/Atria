"""English spoken-word mapping for the Arch Roof function of ATRIA (3D-BIM)."""

try:
    from .ArchRoof import ArchRoof
except ImportError:
    ArchRoof = None

TraduceToEn = {
    "create roof":   ArchRoof,
    "new roof":      ArchRoof,
    "generate roof": ArchRoof,
    "add roof":      ArchRoof,
}
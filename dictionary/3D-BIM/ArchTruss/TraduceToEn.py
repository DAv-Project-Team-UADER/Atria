"""English spoken-word mapping for the Arch Truss function of ATRIA (3D-BIM)."""

try:
    from .ArchTruss import ArchTruss
except ImportError:
    ArchTruss = None

TraduceToEn = {
    "create truss":   ArchTruss,
    "new truss":      ArchTruss,
    "generate truss": ArchTruss,
    "add truss":      ArchTruss,
    "create lattice": ArchTruss,
}
"""English spoken-word mapping for the Slab function of ATRIA (3D-BIM)."""

try:
    from .Slab import Slab
except ImportError:
    Slab = None

TraduceToEn = {
    "create slab":          Slab,
    "new slab":             Slab,
    "generate plate":       Slab,
    "add slab":             Slab,
}
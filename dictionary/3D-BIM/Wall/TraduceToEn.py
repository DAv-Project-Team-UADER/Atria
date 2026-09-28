"""English spoken-word mapping for the Wall function of ATRIA (3D-BIM)."""

try:
    from .Wall import Wall
except ImportError:
    Wall = None

TraduceToEn = {
    "create wall":          Wall,
    "new wall":             Wall,
    "generate wall":        Wall,
    "add wall":             Wall,
}
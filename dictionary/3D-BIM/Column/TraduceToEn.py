"""English spoken-word mapping for the Column function of ATRIA (3D-BIM)."""

try:
    from .Column import Column
except ImportError:
    Column = None

TraduceToEn = {
    "create column":        Column,
    "new column":           Column,
    "generate pillar":      Column,
    "add column":           Column,
}
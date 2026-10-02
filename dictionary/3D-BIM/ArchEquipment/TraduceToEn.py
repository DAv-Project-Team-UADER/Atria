"""English spoken-word mapping for the Arch Equipment function of ATRIA (3D-BIM)."""

try:
    from .ArchEquipment import ArchEquipment
except ImportError:
    ArchEquipment = None

TraduceToEn = {
    "create equipment": ArchEquipment,
    "new equipment":    ArchEquipment,
    "insert equipment": ArchEquipment,
    "add furniture":    ArchEquipment,
}
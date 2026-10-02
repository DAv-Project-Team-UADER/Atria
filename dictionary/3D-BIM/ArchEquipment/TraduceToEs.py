"""Comandos de voz en español para la función Equipamiento (ArchEquipment) de ATRIA (3D-BIM)."""

try:
    from .ArchEquipment import ArchEquipment
except ImportError:
    ArchEquipment = None

TraduceToEs = {
    "crear equipamiento":    ArchEquipment,
    "nuevo equipamiento":    ArchEquipment,
    "insertar equipamiento": ArchEquipment,
    "añadir mobiliario":     ArchEquipment,
    "crear equipo":          ArchEquipment,
}
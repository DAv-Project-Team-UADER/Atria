# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Voice map (EN) for ATRIA base context."""

try:
    from .base import Base
except ImportError:
    from base import Base

TraduceToEn = {
    # 2D-Drafting
    "two d": Base.get("2D-Drafting"),
    "drafting": Base.get("2D-Drafting"),
    "drawing": Base.get("2D-Drafting"),

    # 3D-BIM
    "three d": Base.get("3D-BIM"),
    "bim": Base.get("3D-BIM"),
    "architecture": Base.get("3D-BIM"),

    # Sections
    "annotation": Base.get("Annotation"),
    "manage": Base.get("Manage"),
    "modify": Base.get("Modify"),
    "preferences": Base.get("Preferences"),
    "snapping": Base.get("Snapping"),
    "status bar": Base.get("StatusBar"),
    "utils": Base.get("Utils"),

    # Panel ATRIA
    "show panel": Base.get("show_atria_panel"),
    "maximize": Base.get("show_atria_panel"),
    "hide panel": Base.get("hide_atria_panel"),
    "minimize": Base.get("hide_atria_panel"),
}

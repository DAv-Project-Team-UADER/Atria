# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Voice map (EN) for ATRIA base context."""

try:
    from .base import Base
except ImportError:
    from base import Base

TraduceToEn = {
    # File and project explorer (first in base buttons)
    "explorer": Base.get("Explorer"),

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
    "views": Base.get("Views"),
    "view": Base.get("Views"),
    "camera": Base.get("Views"),

    # Panel ATRIA
    "show panel": Base.get("show_atria_panel"),
    "maximize": Base.get("show_atria_panel"),
    "hide panel": Base.get("hide_atria_panel"),
    "minimize": Base.get("hide_atria_panel"),
}

try:
    from .Views import commands as _view_cmds
except ImportError:
    try:
        from Views import commands as _view_cmds
    except ImportError:
        _view_cmds = None

if _view_cmds is not None:
    TraduceToEn.update({
        "perspective": _view_cmds.perspective,
        "orthographic": _view_cmds.orthographic,
        "isometric": _view_cmds.isometric,
        "fit all": _view_cmds.fit_all,
        "zoom in": _view_cmds.zoom_in,
        "zoom out": _view_cmds.zoom_out,
        "rotate left": _view_cmds.rotate_left,
        "rotate right": _view_cmds.rotate_right,
        "rotate up": _view_cmds.rotate_up,
        "rotate down": _view_cmds.rotate_down,
    })

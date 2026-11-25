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

    # Selection
    "select": Base.get("Select"),
    "selection": Base.get("Select"),

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
        # Camera perspective mode
        "perspective": _view_cmds.perspective,
        "perspective view": _view_cmds.perspective,
        "orthographic": _view_cmds.orthographic,
        "ortho": _view_cmds.orthographic,
        "orthographic view": _view_cmds.orthographic,

        # Standard views - Isometric
        "isometric": _view_cmds.isometric,
        "isometric view": _view_cmds.isometric,
        "iso": _view_cmds.isometric,
        "iso view": _view_cmds.isometric,
        "axonometric": _view_cmds.isometric,

        # Standard views - Dimetric & Trimetric
        "dimetric": getattr(_view_cmds, 'dimetric', _view_cmds.isometric),
        "dimetric view": getattr(_view_cmds, 'dimetric', _view_cmds.isometric),
        "trimetric": getattr(_view_cmds, 'trimetric', _view_cmds.isometric),
        "trimetric view": getattr(_view_cmds, 'trimetric', _view_cmds.isometric),

        # Orthogonal views
        "front": _view_cmds.front,
        "front view": _view_cmds.front,
        "forward": _view_cmds.front,

        "top": _view_cmds.top,
        "top view": _view_cmds.top,
        "plan": _view_cmds.top,
        "plan view": _view_cmds.top,

        "right": _view_cmds.right,
        "right view": _view_cmds.right,

        "left": _view_cmds.left,
        "left view": _view_cmds.left,

        "rear": _view_cmds.rear,
        "rear view": _view_cmds.rear,
        "back view": _view_cmds.rear,
        "back": _view_cmds.rear,

        "bottom": _view_cmds.bottom,
        "bottom view": _view_cmds.bottom,

        # Framing & Zoom
        "fit all": _view_cmds.fit_all,
        "fit": _view_cmds.fit_all,
        "center view": _view_cmds.fit_all,
        "view all": _view_cmds.fit_all,

        "fit selection": _view_cmds.fit_selection,
        "focus selection": _view_cmds.fit_selection,
        "focus object": _view_cmds.fit_selection,
        "center selection": _view_cmds.fit_selection,

        "zoom in": _view_cmds.zoom_in,
        "closer": _view_cmds.zoom_in,
        "zoom out": _view_cmds.zoom_out,
        "farther": _view_cmds.zoom_out,

        # Camera rotation
        "rotate left": _view_cmds.rotate_left,
        "turn left": _view_cmds.rotate_left,
        "rotate right": _view_cmds.rotate_right,
        "turn right": _view_cmds.rotate_right,
        "rotate up": _view_cmds.rotate_up,
        "tilt up": _view_cmds.rotate_up,
        "rotate down": _view_cmds.rotate_down,
        "tilt down": _view_cmds.rotate_down,
    })

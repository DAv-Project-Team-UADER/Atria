# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Mapa de voz (ES) para el contexto base de ATRIA."""

try:
    from .base import Base
except ImportError:
    from base import Base

TraduceToEs = {
    # Explorador de archivos y proyectos (primero en la lista de iconos)
    "explorador": Base.get("Explorer"),
    "explorer": Base.get("Explorer"),

    # 2D-Drafting
    "2d": Base.get("2D-Drafting"),
    "dos d": Base.get("2D-Drafting"),
    "dos de": Base.get("2D-Drafting"),
    "dibujo": Base.get("2D-Drafting"),
    "dibujo dos d": Base.get("2D-Drafting"),
    "drafting": Base.get("2D-Drafting"),

    # 3D-BIM
    "3d": Base.get("3D-BIM"),
    "tres d": Base.get("3D-BIM"),
    "tres de": Base.get("3D-BIM"),
    "bim": Base.get("3D-BIM"),
    "arquitectura": Base.get("3D-BIM"),

    # Secciones
    "anotacion": Base.get("Annotation"),
    "anotaciones": Base.get("Annotation"),
    "acotacion": Base.get("Annotation"),
    "administracion": Base.get("Manage"),
    "gestion": Base.get("Manage"),
    "modificar": Base.get("Modify"),
    "modificacion": Base.get("Modify"),
    "preferencias": Base.get("Preferences"),
    "ajustes": Base.get("Preferences"),
    "configuracion": Base.get("Preferences"),
    "enganche": Base.get("Snapping"),
    "snapping": Base.get("Snapping"),
    "barra de estado": Base.get("StatusBar"),
    "utilidades": Base.get("Utils"),
    "herramientas": Base.get("Utils"),
    "utils": Base.get("Utils"),

    # Vistas y Cámara
    "vistas": Base.get("Views"),
    "vista": Base.get("Views"),
    "camara": Base.get("Views"),
    "cámara": Base.get("Views"),

    # Panel ATRIA
    "mostrar panel": Base.get("show_atria_panel"),
    "maximizar": Base.get("show_atria_panel"),
    "aumentar": Base.get("show_atria_panel"),
    "agrandar": Base.get("show_atria_panel"),
    "ocultar panel": Base.get("hide_atria_panel"),
    "minimizar": Base.get("hide_atria_panel"),
    "reducir": Base.get("hide_atria_panel"),
    "disminuir": Base.get("hide_atria_panel"),
}

try:
    from .Views import commands as _view_cmds
except ImportError:
    try:
        from Views import commands as _view_cmds
    except ImportError:
        _view_cmds = None

if _view_cmds is not None:
    TraduceToEs.update({
        "perspectiva": _view_cmds.perspective,
        "vista perspectiva": _view_cmds.perspective,
        "ortogonal": _view_cmds.orthographic,
        "vista ortogonal": _view_cmds.orthographic,
        "isometrica": _view_cmds.isometric,
        "isométrica": _view_cmds.isometric,
        "vista isometrica": _view_cmds.isometric,
        "vista isométrica": _view_cmds.isometric,
        "centrar vista": _view_cmds.fit_all,
        "ajustar todo": _view_cmds.fit_all,
        "acercar": _view_cmds.zoom_in,
        "alejar": _view_cmds.zoom_out,
        "girar izquierda": _view_cmds.rotate_left,
        "girar derecha": _view_cmds.rotate_right,
        "girar arriba": _view_cmds.rotate_up,
        "girar abajo": _view_cmds.rotate_down,
    })

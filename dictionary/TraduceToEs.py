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

    # Selección y Navegación de Objetos
    "seleccionar": Base.get("Select"),
    "seleccion": Base.get("Select"),
    "selección": Base.get("Select"),
    "select": Base.get("Select"),
    "navegar objetos": Base.get("Select"),
    "arbol de objetos": Base.get("Select"),
    "árbol de objetos": Base.get("Select"),

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
        # Perspectiva y modo de cámara
        "perspectiva": _view_cmds.perspective,
        "vista perspectiva": _view_cmds.perspective,
        "modo perspectiva": _view_cmds.perspective,
        "ortogonal": _view_cmds.orthographic,
        "vista ortogonal": _view_cmds.orthographic,
        "modo ortogonal": _view_cmds.orthographic,
        "ortografica": _view_cmds.orthographic,
        "ortográfica": _view_cmds.orthographic,
        "vista ortografica": _view_cmds.orthographic,
        "vista ortográfica": _view_cmds.orthographic,

        # Vista isométrica y variantes
        "isometrica": _view_cmds.isometric,
        "isométrica": _view_cmds.isometric,
        "vista isometrica": _view_cmds.isometric,
        "vista isométrica": _view_cmds.isometric,
        "isometrico": _view_cmds.isometric,
        "isométrico": _view_cmds.isometric,
        "vista isometrico": _view_cmds.isometric,
        "vista isométrico": _view_cmds.isometric,
        "iso": _view_cmds.isometric,
        "vista iso": _view_cmds.isometric,
        "isometria": _view_cmds.isometric,
        "isometría": _view_cmds.isometric,
        "modo isometrico": _view_cmds.isometric,
        "modo isométrico": _view_cmds.isometric,
        "axonometrica": _view_cmds.isometric,
        "axonométrica": _view_cmds.isometric,
        "vista axonometrica": _view_cmds.isometric,
        "vista axonométrica": _view_cmds.isometric,

        # Vistas dimétrica y trimétrica
        "dimetrica": getattr(_view_cmds, 'dimetric', _view_cmds.isometric),
        "dimétrica": getattr(_view_cmds, 'dimetric', _view_cmds.isometric),
        "vista dimetrica": getattr(_view_cmds, 'dimetric', _view_cmds.isometric),
        "vista dimétrica": getattr(_view_cmds, 'dimetric', _view_cmds.isometric),
        "trimetrica": getattr(_view_cmds, 'trimetric', _view_cmds.isometric),
        "trimétrica": getattr(_view_cmds, 'trimetric', _view_cmds.isometric),
        "vista trimetrica": getattr(_view_cmds, 'trimetric', _view_cmds.isometric),
        "vista trimétrica": getattr(_view_cmds, 'trimetric', _view_cmds.isometric),

        # Vistas ortogonales estándar
        "frontal": _view_cmds.front,
        "vista frontal": _view_cmds.front,
        "frente": _view_cmds.front,
        "de frente": _view_cmds.front,
        "alzado": _view_cmds.front,

        "superior": _view_cmds.top,
        "vista superior": _view_cmds.top,
        "planta": _view_cmds.top,
        "vista de planta": _view_cmds.top,
        "desde arriba": _view_cmds.top,

        "derecha": _view_cmds.right,
        "vista derecha": _view_cmds.right,
        "lateral derecha": _view_cmds.right,
        "perfil derecho": _view_cmds.right,

        "izquierda": _view_cmds.left,
        "vista izquierda": _view_cmds.left,
        "lateral izquierda": _view_cmds.left,
        "perfil izquierdo": _view_cmds.left,

        "posterior": _view_cmds.rear,
        "vista posterior": _view_cmds.rear,
        "trasera": _view_cmds.rear,
        "vista trasera": _view_cmds.rear,
        "de atras": _view_cmds.rear,
        "de atrás": _view_cmds.rear,
        "detras": _view_cmds.rear,
        "detrás": _view_cmds.rear,

        "inferior": _view_cmds.bottom,
        "vista inferior": _view_cmds.bottom,
        "abajo": _view_cmds.bottom,
        "desde abajo": _view_cmds.bottom,

        # Encuadre y Zoom
        "centrar vista": _view_cmds.fit_all,
        "centrar": _view_cmds.fit_all,
        "ajustar todo": _view_cmds.fit_all,
        "ajustar vista": _view_cmds.fit_all,
        "ver todo": _view_cmds.fit_all,
        "encuadrar": _view_cmds.fit_all,
        "encuadrar todo": _view_cmds.fit_all,
        "fit all": _view_cmds.fit_all,

        "enfocar seleccion": _view_cmds.fit_selection,
        "enfocar selección": _view_cmds.fit_selection,
        "centrar seleccion": _view_cmds.fit_selection,
        "centrar selección": _view_cmds.fit_selection,
        "ajustar seleccion": _view_cmds.fit_selection,
        "ajustar selección": _view_cmds.fit_selection,
        "ver seleccion": _view_cmds.fit_selection,
        "ver selección": _view_cmds.fit_selection,
        "centrar objeto": _view_cmds.fit_selection,

        "acercar": _view_cmds.zoom_in,
        "alejar": _view_cmds.zoom_out,

        # Rotación
        "girar izquierda": _view_cmds.rotate_left,
        "rotar izquierda": _view_cmds.rotate_left,
        "girar derecha": _view_cmds.rotate_right,
        "rotar derecha": _view_cmds.rotate_right,
        "girar arriba": _view_cmds.rotate_up,
        "rotar arriba": _view_cmds.rotate_up,
        "girar abajo": _view_cmds.rotate_down,
        "rotar abajo": _view_cmds.rotate_down,
    })

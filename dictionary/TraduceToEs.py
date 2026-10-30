# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Mapa de voz (ES) para el contexto base de ATRIA."""

try:
    from .base import Base
except ImportError:
    from base import Base

TraduceToEs = {
    # 2D-Drafting
    "dos d": Base.get("2D-Drafting"),
    "dos de": Base.get("2D-Drafting"),
    "dibujo": Base.get("2D-Drafting"),
    "dibujo dos d": Base.get("2D-Drafting"),
    "drafting": Base.get("2D-Drafting"),

    # 3D-BIM
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
    "explorador": Base.get("Explorer"),
    "explorer": Base.get("Explorer"),

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

# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Diccionario interno de funciones para la sección Views (Cámara y Vistas)."""

from . import commands
from .ayuda import ayuda

Views = {
    # Modo de cámara y perspectiva
    "perspective": commands.perspective,
    "orthographic": commands.orthographic,

    # Vistas estándar
    "isometric": commands.isometric,
    "dimetric": commands.dimetric,
    "trimetric": commands.trimetric,
    "front": commands.front,
    "top": commands.top,
    "right": commands.right,
    "left": commands.left,
    "rear": commands.rear,
    "bottom": commands.bottom,

    # Movimiento y encuadre
    "fitall": commands.fit_all,
    "fitselection": commands.fit_selection,
    "zoomin": commands.zoom_in,
    "zoomout": commands.zoom_out,

    # Rotación de cámara
    "rotateleft": commands.rotate_left,
    "rotateright": commands.rotate_right,
    "rotateup": commands.rotate_up,
    "rotatedown": commands.rotate_down,

    # Desplazamiento a coordenadas
    "movecamera": commands.move_camera,

    # Ayuda contextual
    "help": ayuda,
}

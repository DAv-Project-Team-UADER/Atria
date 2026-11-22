# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""English spoken-word mapping for Views and Camera section."""

from .Views import Views

TraduceToEn = {
    "perspective": Views["perspective"],
    "perspective view": Views["perspective"],
    "perspective camera": Views["perspective"],

    "orthographic": Views["orthographic"],
    "ortho": Views["orthographic"],
    "orthographic view": Views["orthographic"],
    "orthographic camera": Views["orthographic"],

    "isometric": Views["isometric"],
    "isometric view": Views["isometric"],

    "front": Views["front"],
    "front view": Views["front"],

    "top": Views["top"],
    "top view": Views["top"],

    "right": Views["right"],
    "right view": Views["right"],

    "left": Views["left"],
    "left view": Views["left"],

    "rear": Views["rear"],
    "rear view": Views["rear"],
    "back view": Views["rear"],

    "bottom": Views["bottom"],
    "bottom view": Views["bottom"],

    "fit all": Views["fitall"],
    "fit": Views["fitall"],
    "center view": Views["fitall"],

    "fit selection": Views["fitselection"],
    "focus object": Views["fitselection"],

    "zoom in": Views["zoomin"],
    "closer": Views["zoomin"],

    "zoom out": Views["zoomout"],
    "farther": Views["zoomout"],

    "rotate left": Views["rotateleft"],
    "turn left": Views["rotateleft"],

    "rotate right": Views["rotateright"],
    "turn right": Views["rotateright"],

    "rotate up": Views["rotateup"],
    "tilt up": Views["rotateup"],

    "rotate down": Views["rotatedown"],
    "tilt down": Views["rotatedown"],

    "move camera": Views["movecamera"],
    "pan camera": Views["movecamera"],

    "help": Views["help"],
}

# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""English spoken-word mapping for Views and Camera section."""

from .Views import Views

TraduceToEn = {
    # Camera perspective mode
    "perspective": Views["perspective"],
    "perspective view": Views["perspective"],
    "perspective camera": Views["perspective"],

    "orthographic": Views["orthographic"],
    "ortho": Views["orthographic"],
    "orthographic view": Views["orthographic"],
    "orthographic camera": Views["orthographic"],

    # Standard views - Isometric
    "isometric": Views["isometric"],
    "isometric view": Views["isometric"],
    "iso": Views["isometric"],
    "iso view": Views["isometric"],
    "axonometric": Views["isometric"],
    "axonometric view": Views["isometric"],

    # Standard views - Dimetric & Trimetric
    "dimetric": Views["dimetric"],
    "dimetric view": Views["dimetric"],

    "trimetric": Views["trimetric"],
    "trimetric view": Views["trimetric"],

    # Front
    "front": Views["front"],
    "front view": Views["front"],
    "forward": Views["front"],

    # Top
    "top": Views["top"],
    "top view": Views["top"],
    "plan": Views["top"],
    "plan view": Views["top"],

    # Right
    "right": Views["right"],
    "right view": Views["right"],

    # Left
    "left": Views["left"],
    "left view": Views["left"],

    # Rear / Back
    "rear": Views["rear"],
    "rear view": Views["rear"],
    "back view": Views["rear"],
    "back": Views["rear"],

    # Bottom
    "bottom": Views["bottom"],
    "bottom view": Views["bottom"],

    # Framing and Zoom
    "fit all": Views["fitall"],
    "fit": Views["fitall"],
    "center view": Views["fitall"],
    "view all": Views["fitall"],
    "frame all": Views["fitall"],

    "fit selection": Views["fitselection"],
    "focus selection": Views["fitselection"],
    "focus object": Views["fitselection"],
    "center selection": Views["fitselection"],

    "zoom in": Views["zoomin"],
    "closer": Views["zoomin"],

    "zoom out": Views["zoomout"],
    "farther": Views["zoomout"],

    # Camera rotation
    "rotate left": Views["rotateleft"],
    "turn left": Views["rotateleft"],

    "rotate right": Views["rotateright"],
    "turn right": Views["rotateright"],

    "rotate up": Views["rotateup"],
    "tilt up": Views["rotateup"],

    "rotate down": Views["rotatedown"],
    "tilt down": Views["rotatedown"],

    # Camera move
    "move camera": Views["movecamera"],
    "pan camera": Views["movecamera"],

    # Help
    "help": Views["help"],
}

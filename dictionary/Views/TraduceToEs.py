# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Mapeo de comandos por voz en español para Vistas y Cámara."""

from .Views import Views

TraduceToEs = {
    # Perspectiva y Modo de Cámara
    "perspectiva": Views["perspective"],
    "vista perspectiva": Views["perspective"],
    "modo perspectiva": Views["perspective"],
    "camara perspectiva": Views["perspective"],
    "cámara perspectiva": Views["perspective"],

    "ortogonal": Views["orthographic"],
    "vista ortogonal": Views["orthographic"],
    "modo ortogonal": Views["orthographic"],
    "ortografica": Views["orthographic"],
    "ortográfica": Views["orthographic"],
    "vista ortografica": Views["orthographic"],
    "vista ortográfica": Views["orthographic"],
    "camara ortogonal": Views["orthographic"],
    "cámara ortogonal": Views["orthographic"],

    # Vistas estándar - Isométrica
    "isometrica": Views["isometric"],
    "isométrica": Views["isometric"],
    "vista isometrica": Views["isometric"],
    "vista isométrica": Views["isometric"],
    "isometrico": Views["isometric"],
    "isométrico": Views["isometric"],
    "vista isometrico": Views["isometric"],
    "vista isométrico": Views["isometric"],
    "iso": Views["isometric"],
    "vista iso": Views["isometric"],
    "isometria": Views["isometric"],
    "isometría": Views["isometric"],
    "modo isometrico": Views["isometric"],
    "modo isométrico": Views["isometric"],
    "axonometrica": Views["isometric"],
    "axonométrica": Views["isometric"],
    "vista axonometrica": Views["isometric"],
    "vista axonométrica": Views["isometric"],

    # Vistas estándar - Dimétrica y Trimétrica
    "dimetrica": Views["dimetric"],
    "dimétrica": Views["dimetric"],
    "vista dimetrica": Views["dimetric"],
    "vista dimétrica": Views["dimetric"],

    "trimetrica": Views["trimetric"],
    "trimétrica": Views["trimetric"],
    "vista trimetrica": Views["trimetric"],
    "vista trimétrica": Views["trimetric"],

    # Frontal
    "frontal": Views["front"],
    "vista frontal": Views["front"],
    "frente": Views["front"],
    "de frente": Views["front"],
    "alzado": Views["front"],
    "vista alzado": Views["front"],

    # Superior / Planta
    "superior": Views["top"],
    "vista superior": Views["top"],
    "planta": Views["top"],
    "desde arriba": Views["top"],
    "vista de planta": Views["top"],
    "arriba": Views["top"],

    # Lateral Derecha
    "derecha": Views["right"],
    "vista derecha": Views["right"],
    "lateral derecha": Views["right"],
    "perfil derecho": Views["right"],
    "lado derecho": Views["right"],

    # Lateral Izquierda
    "izquierda": Views["left"],
    "vista izquierda": Views["left"],
    "lateral izquierda": Views["left"],
    "perfil izquierdo": Views["left"],
    "lado izquierdo": Views["left"],

    # Posterior / Trasera
    "posterior": Views["rear"],
    "vista posterior": Views["rear"],
    "trasera": Views["rear"],
    "vista trasera": Views["rear"],
    "de atras": Views["rear"],
    "de atrás": Views["rear"],
    "detras": Views["rear"],
    "detrás": Views["rear"],

    # Inferior
    "inferior": Views["bottom"],
    "vista inferior": Views["bottom"],
    "abajo": Views["bottom"],
    "desde abajo": Views["bottom"],

    # Encuadre y Zoom
    "centrar vista": Views["fitall"],
    "centrar": Views["fitall"],
    "ajustar todo": Views["fitall"],
    "ajustar vista": Views["fitall"],
    "ver todo": Views["fitall"],
    "encuadrar": Views["fitall"],
    "encuadrar todo": Views["fitall"],
    "fit all": Views["fitall"],
    "zoom todo": Views["fitall"],

    "enfocar seleccion": Views["fitselection"],
    "enfocar selección": Views["fitselection"],
    "centrar seleccion": Views["fitselection"],
    "centrar selección": Views["fitselection"],
    "ajustar seleccion": Views["fitselection"],
    "ajustar selección": Views["fitselection"],
    "encuadrar seleccion": Views["fitselection"],
    "encuadrar selección": Views["fitselection"],
    "centrar objeto": Views["fitselection"],
    "ver seleccion": Views["fitselection"],
    "ver selección": Views["fitselection"],

    "acercar": Views["zoomin"],
    "acercar camara": Views["zoomin"],
    "acercar cámara": Views["zoomin"],
    "acercar vista": Views["zoomin"],
    "zoom in": Views["zoomin"],
    "zoom mas": Views["zoomin"],
    "zoom más": Views["zoomin"],

    "alejar": Views["zoomout"],
    "alejar camara": Views["zoomout"],
    "alejar cámara": Views["zoomout"],
    "alejar vista": Views["zoomout"],
    "zoom out": Views["zoomout"],
    "zoom menos": Views["zoomout"],

    # Rotación / Giro de Cámara
    "girar izquierda": Views["rotateleft"],
    "rotar izquierda": Views["rotateleft"],
    "girar a la izquierda": Views["rotateleft"],
    "rotar a la izquierda": Views["rotateleft"],

    "girar derecha": Views["rotateright"],
    "rotar derecha": Views["rotateright"],
    "girar a la derecha": Views["rotateright"],
    "rotar a la derecha": Views["rotateright"],

    "girar arriba": Views["rotateup"],
    "rotar arriba": Views["rotateup"],
    "inclinar arriba": Views["rotateup"],

    "girar abajo": Views["rotatedown"],
    "rotar abajo": Views["rotatedown"],
    "inclinar abajo": Views["rotatedown"],

    # Desplazamiento de cámara
    "mover camara": Views["movecamera"],
    "mover cámara": Views["movecamera"],
    "posicion camara": Views["movecamera"],
    "posición cámara": Views["movecamera"],
    "desplazar camara": Views["movecamera"],
    "desplazar cámara": Views["movecamera"],

    # Ayuda
    "ayuda": Views["help"],
    "manual": Views["help"],
}

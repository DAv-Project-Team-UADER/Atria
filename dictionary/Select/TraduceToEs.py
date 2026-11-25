# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Mapeo de comandos por voz en español para Selección y Navegación de Objetos."""

from .Select import Select

TraduceToEs = {
    # Navegación por objetos
    "avanzar": Select["next"],
    "siguiente": Select["next"],
    "proximo": Select["next"],
    "próximo": Select["next"],
    "adelante": Select["next"],
    "avanza": Select["next"],

    "retroceder": Select["previous"],
    "anterior": Select["previous"],
    "atras": Select["previous"],
    "atrás": Select["previous"],
    "retrocede": Select["previous"],

    # Acciones de selección
    "seleccionar": Select["select"],
    "marcar": Select["select"],
    "elegir": Select["select"],
    "selecciona": Select["select"],
    "seleccionar actual": Select["select"],
    "seleccionar este": Select["select"],

    "deseleccionar": Select["deselect"],
    "desmarcar": Select["deselect"],
    "quitar seleccion": Select["deselect"],
    "quitar selección": Select["deselect"],
    "deselecciona": Select["deselect"],

    "seleccionar todos": Select["selectall"],
    "seleccionar todo": Select["selectall"],
    "marcar todos": Select["selectall"],
    "marcar todo": Select["selectall"],
    "elegir todos": Select["selectall"],

    "deseleccionar todos": Select["deselectall"],
    "deseleccionar todo": Select["deselectall"],
    "desmarcar todos": Select["deselectall"],
    "desmarcar todo": Select["deselectall"],
    "limpiar seleccion": Select["deselectall"],
    "limpiar selección": Select["deselectall"],
    "quitar todo": Select["deselectall"],

    # Edición y borrado del objeto seleccionado
    "editar": Select["edit"],
    "modo edicion": Select["edit"],
    "modo edición": Select["edit"],
    "modificar": Select["edit"],
    "editar objeto": Select["edit"],

    "borrar": Select["delete"],
    "eliminar": Select["delete"],
    "suprimir": Select["delete"],
    "borrar objeto": Select["delete"],
    "eliminar objeto": Select["delete"],

    # Ayuda contextual
    "ayuda": Select["help"],
    "manual": Select["help"],
}

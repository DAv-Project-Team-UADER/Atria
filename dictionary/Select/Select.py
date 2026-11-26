# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Diccionario interno de comandos para la sección Selección."""

from . import commands
from .ayuda import ayuda

Select = {
    "next": commands.next_object,
    "previous": commands.previous_object,
    "select": commands.select_current,
    "deselect": commands.deselect_current,
    "selectall": commands.select_all,
    "deselectall": commands.deselect_all,
    "edit": commands.edit_object,
    "delete": commands.delete_selected,
    "help": ayuda,
}

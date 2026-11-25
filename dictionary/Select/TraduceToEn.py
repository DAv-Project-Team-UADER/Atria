# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""English spoken-word mapping for Object Selection and Navigation."""

from .Select import Select

TraduceToEn = {
    "next": Select["next"],
    "advance": Select["next"],
    "forward": Select["next"],

    "previous": Select["previous"],
    "back": Select["previous"],
    "backward": Select["previous"],

    "select": Select["select"],
    "pick": Select["select"],
    "choose": Select["select"],

    "deselect": Select["deselect"],
    "unselect": Select["deselect"],

    "select all": Select["selectall"],
    "pick all": Select["selectall"],

    "deselect all": Select["deselectall"],
    "clear selection": Select["deselectall"],

    # Editing and deletion of selected object
    "edit": Select["edit"],
    "edit object": Select["edit"],
    "modify": Select["edit"],

    "delete": Select["delete"],
    "remove": Select["delete"],
    "erase": Select["delete"],
    "delete object": Select["delete"],

    "help": Select["help"],
}

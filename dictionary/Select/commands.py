# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Comandos de navegación y selección de objetos en FreeCAD."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except ImportError:
    App = None
    Gui = None

# Instancia de ObjectSelection
_selection_manager = None

def _get_manager():
    global _selection_manager
    if _selection_manager is None:
        try:
            from selection.object_selection import ObjectSelection
            _selection_manager = ObjectSelection()
        except ImportError:
            try:
                from object_selection import ObjectSelection
                _selection_manager = ObjectSelection()
            except ImportError:
                _selection_manager = None
    return _selection_manager


def next_object() -> None:
    """Avanza al siguiente objeto del documento activo, enfocándolo visualmente."""
    mgr = _get_manager()
    if mgr:
        mgr.SelectNext()


def previous_object() -> None:
    """Retrocede al objeto anterior del documento activo, enfocándolo visualmente."""
    mgr = _get_manager()
    if mgr:
        mgr.SelectPrevious()


def select_current() -> None:
    """Selecciona / añade a la selección el objeto actualmente apuntado."""
    mgr = _get_manager()
    if mgr:
        mgr.SelectCurrent()


def deselect_current() -> None:
    """Deselecciona el objeto actualmente apuntado."""
    mgr = _get_manager()
    if mgr:
        mgr.DeselectCurrent()


def select_all() -> None:
    """Selecciona todos los objetos del documento activo."""
    mgr = _get_manager()
    if mgr:
        mgr.SelectAll()


def deselect_all() -> None:
    """Limpia la selección completa (deselecciona todos)."""
    mgr = _get_manager()
    if mgr:
        mgr.DeselectAll()


def edit_object() -> None:
    """Pone el objeto seleccionado en modo de edición interactivo de FreeCAD/Draft."""
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Draft_Edit", 0)


def delete_selected() -> None:
    """Elimina el objeto actualmente seleccionado en FreeCAD."""
    mgr = _get_manager()
    if mgr:
        mgr.DeleteSelected()

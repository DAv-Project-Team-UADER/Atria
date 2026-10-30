# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg

"""Diccionario base de navegación de ATRIA (menú principal)."""

# Sub-contextos principales de ATRIA (FreeCAD BIM & Draft)
Drafting = {"name": "2D-Drafting"}
BIM = {"name": "3D-BIM"}
Annotation = {"name": "Annotation"}
Manage = {"name": "Manage"}
Modify = {"name": "Modify"}
Preferences = {"name": "Preferences"}
Snapping = {"name": "Snapping"}
StatusBar = {"name": "StatusBar"}
Utils = {"name": "Utils"}
Explorer = {"name": "Explorer"}

def show_atria_panel():
    try:
        from integration.voice_bootstrap import show_dock_panel
        show_dock_panel()
    except Exception:
        pass

def hide_atria_panel():
    try:
        import FreeCADGui as Gui
        from PySide6.QtWidgets import QDockWidget
        mw = Gui.getMainWindow()
        if mw:
            for dock in mw.findChildren(QDockWidget):
                if "ATRIA" in dock.objectName() or "Atria" in dock.windowTitle():
                    dock.hide()
    except Exception:
        pass

Base = {
    "2D-Drafting": Drafting,
    "3D-BIM": BIM,
    "Annotation": Annotation,
    "Manage": Manage,
    "Modify": Modify,
    "Preferences": Preferences,
    "Snapping": Snapping,
    "StatusBar": StatusBar,
    "Utils": Utils,
    "Explorer": Explorer,
    "show_atria_panel": show_atria_panel,
    "hide_atria_panel": hide_atria_panel,
}

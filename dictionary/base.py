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
Views = {"name": "Views"}
Select = {"name": "Select"}

def show_atria_panel():
    try:
        from GUIFreeCad.integration.atria_dock_panel import show_atria_panel as _show
        if _show():
            return True
    except ImportError:
        try:
            from integration.atria_dock_panel import show_atria_panel as _show
            if _show():
                return True
        except Exception:
            pass
    except Exception:
        pass
    try:
        from GUIFreeCad.integration.voice_bootstrap import show_dock_panel
        return show_dock_panel()
    except ImportError:
        try:
            from integration.voice_bootstrap import show_dock_panel
            return show_dock_panel()
        except Exception:
            pass
    except Exception:
        pass
    return False

def hide_atria_panel():
    try:
        from GUIFreeCad.integration.atria_dock_panel import hide_atria_panel as _hide
        if _hide():
            return True
    except ImportError:
        try:
            from integration.atria_dock_panel import hide_atria_panel as _hide
            if _hide():
                return True
        except Exception:
            pass
    except Exception:
        pass
    try:
        import FreeCADGui as Gui
        from PySide6.QtWidgets import QDockWidget
        mw = Gui.getMainWindow()
        if mw:
            for dock in mw.findChildren(QDockWidget):
                if "ATRIA" in dock.objectName() or "Atria" in dock.windowTitle():
                    dock.hide()
                    return True
    except Exception:
        pass
    return False

Base = {
    "Explorer": Explorer,
    "2D-Drafting": Drafting,
    "3D-BIM": BIM,
    "Annotation": Annotation,
    "Manage": Manage,
    "Modify": Modify,
    "Preferences": Preferences,
    "Snapping": Snapping,
    "StatusBar": StatusBar,
    "Utils": Utils,
    "Views": Views,
    "Select": Select,
    "show_atria_panel": show_atria_panel,
    "hide_atria_panel": hide_atria_panel,
}

# ATRIA (UADER) — InitGui: FreeCAD ejecuta este archivo en un namespace especial.
# Toda la lógica está en gui.freecad_wb (import normal).

import os
import sys

import FreeCAD as App
import FreeCADGui as Gui

_d = ""
for _p in getattr(App, "__ModDirs__", ()) or ():
    _n = os.path.normpath(_p)
    if os.path.basename(_n).upper() == "ATRIA":
        _d = _n
        break

if not _d:
    _e = os.environ.get("ATRIA_MOD_ROOT", "").strip()
    if _e and os.path.isdir(_e):
        _d = os.path.normpath(_e)

if not _d:
    _u = os.path.join(App.getUserAppDataDir(), "Mod", "Atria")
    if os.path.isdir(_u):
        _d = _u

if _d:
    _d_real = os.path.realpath(_d)
    if _d_real not in sys.path:
        sys.path.insert(0, _d_real)
    for _rel_icons in (("InterfazATRIA", "Icons"), ("GUIFreeCad", "ui", "Icons")):
        _icons_dir = os.path.join(_d_real, *_rel_icons)
        if os.path.isdir(_icons_dir):
            os.environ.setdefault("ATRIA_ICONS_ROOT", _icons_dir)
            try:
                Gui.addIconPath(_icons_dir)
                _sys_icons = os.path.join(_icons_dir, "system")
                if os.path.isdir(_sys_icons):
                    Gui.addIconPath(_sys_icons)
            except Exception:
                pass

try:
    import atriaGui.atria_commands as _atria_commands

    _atria_commands._ensure_selection_path()
    _atria_commands._ensure_validation_path()
except Exception as e:
    App.Console.PrintWarning(f"[Atria] Advertencia al cargar comandos iniciales: {e}\n")


class AtriaWorkbench(Gui.Workbench):
    MenuText = "Atria"
    ToolTip = "Atria (UADER)"

    def Initialize(self):
        import atriaGui.freecad_wb

        atriaGui.freecad_wb.setup_workbench(self)

    def GetClassName(self):
        return "Gui::PythonWorkbench"

_wb_registered = False
try:
    _wb_registered = Gui.getWorkbench("AtriaWorkbench") is not None
except Exception:
    _wb_registered = False

if not _wb_registered:
    Gui.addWorkbench(AtriaWorkbench())

if os.environ.get("ATRIA_AUTOLOAD_WORKBENCH") != "0":
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer

    def _activate_atria_workbench() -> None:
        try:
            Gui.activateWorkbench("AtriaWorkbench")
        except Exception:
            import traceback

            App.Console.PrintError("[Atria] No se pudo activar el workbench Atria:\n")
            App.Console.PrintError(traceback.format_exc())

    QTimer.singleShot(500, _activate_atria_workbench)
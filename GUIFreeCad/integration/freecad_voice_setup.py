"""Register ATRIA voice commands and hooks from GUIFreeCad."""

from __future__ import annotations

import os
import subprocess
import traceback
from pathlib import Path

_INSTALLED = False


def install_freecad_integration() -> None:
    """Called from apply_saved_settings when the ATRIA workbench loads."""
    global _INSTALLED
    if _INSTALLED:
        _maybe_autostart_voice()
        return

    try:
        import FreeCAD as App
        import FreeCADGui as Gui

        from GUIFreeCad.integration.atria_paths import ensure_gui_on_path
        from GUIFreeCad.integration.freecad_gui_bridge import init_gui_bridge

        ensure_gui_on_path()
        init_gui_bridge()
        _register_voice_commands(Gui)
        _extend_workbench_ui(Gui)
        _INSTALLED = True

        App.Console.PrintMessage(
            "[ATRIA] Workbench listo. Mensajes [ATRIA] van a esta pestaña Â«InformeÂ», "
            "no a la consola Python (>>>).\n"
        )
        _print_voice_startup_hint()
        _maybe_autostart_voice()
    except Exception:
        try:
            import FreeCAD as App

            App.Console.PrintError("[ATRIA] Error instalando integración GUIFreeCad:\n")
            App.Console.PrintError(traceback.format_exc())
        except ImportError:
            pass


def _register_voice_commands(Gui) -> None:
    class _StartVoice:
        def GetResources(self):
            return {
                "Pixmap": "media-playback-start",
                "MenuText": "Iniciar voz ATRIA",
                "ToolTip": "Activa comandos de voz CAD (motor unificado GUIFreeCad)",
            }

        def Activated(self):
            from GUIFreeCad.integration.voice_bootstrap import start_voice_engine

            start_voice_engine()

        def IsActive(self):
            return True

    class _StopVoice:
        def GetResources(self):
            return {
                "Pixmap": "media-playback-stop",
                "MenuText": "Detener voz ATRIA",
                "ToolTip": "Detiene el motor de comandos por voz",
            }

        def Activated(self):
            from GUIFreeCad.integration.voice_bootstrap import stop_voice_engine

            stop_voice_engine()

        def IsActive(self):
            return True

    for cmd_id, factory in (
        ("ATRIA_StartVoice", _StartVoice),
        ("ATRIA_StopVoice", _StopVoice),
    ):
        if Gui.listCommands().count(cmd_id) == 0:
            Gui.addCommand(cmd_id, factory())


def _extend_workbench_ui(Gui) -> None:
    try:
        wb = Gui.getWorkbench("ATRIAWorkbench")
    except Exception:
        return
    if wb is None:
        return
    cmds = [
        c
        for c in ("ATRIA_OpenPreferences", "ATRIA_StartVoice", "ATRIA_StopVoice")
        if Gui.listCommands().count(c) > 0
    ]
    if not cmds:
        return
    try:
        wb.appendMenu("ATRIA", cmds)
        wb.appendToolbar("ATRIA", cmds)
    except Exception:
        import traceback

        import FreeCAD as App

        App.Console.PrintWarning("[ATRIA] No se pudo actualizar menu/barra ATRIA:\n")
        App.Console.PrintWarning(traceback.format_exc())


def _print_voice_startup_hint() -> None:
    try:
        import FreeCAD as App
        from GUIFreeCad.core.settings import settings

        settings.load()
        auto = os.environ.get("ATRIA_AUTO_START_VOICE") == "1" or settings.startup_enabled
        if auto:
            App.Console.PrintMessage(
                "[ATRIA] Arranque de voz programado (~1,5 s). Esperá Â«Voz activaÂ» en Informe.\n"
            )
        else:
            App.Console.PrintMessage(
                "[ATRIA] Micrófono inactivo. Activá Â«Iniciar ATRIA y FreeCAD al encender la PCÂ» "
                "en Preferencias, o clic en Â«Iniciar voz ATRIAÂ».\n"
            )
    except Exception:
        pass


# _launch_interfaz_atria removed: launching is handled by atria_commands._launch_interfaz_atria()
# which has proper deduplication guards. Called from freecad_wb._schedule_interfaz_atria_launch().


def _maybe_autostart_voice() -> None:
    try:
        import os

        import FreeCAD as App
        from GUIFreeCad.core.settings import settings

        settings.load()
        if not (os.environ.get("ATRIA_AUTO_START_VOICE") == "1" or settings.startup_enabled or settings.auto_voice):
            return

        try:
            from PySide6.QtCore import QTimer
        except ImportError:
            from PySide2.QtCore import QTimer  # type: ignore[no-redef]

        def _start() -> None:
            from GUIFreeCad.integration.voice_bootstrap import start_voice_engine

            if not start_voice_engine():
                App.Console.PrintWarning(
                    "[ATRIA] No se pudo iniciar la voz. "
                    "Probá Â«Iniciar voz ATRIAÂ» manualmente.\n"
                )
            # InterfazATRIA launch handled by freecad_wb._schedule_interfaz_atria_launch()

        QTimer.singleShot(1500, _start)
    except Exception:
        try:
            import FreeCAD as App

            App.Console.PrintError("[ATRIA] Error programando arranque de voz:\n")
            App.Console.PrintError(traceback.format_exc())
        except ImportError:
            pass

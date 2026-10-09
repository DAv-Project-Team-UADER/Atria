"""Thread-safe bridge: voice worker thread -> Qt main thread (FreeCAD)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

try:
    from PySide6.QtCore import QObject, Qt, Signal, Slot
except ImportError:
    from PySide2.QtCore import QObject, Qt, Signal, Slot  # type: ignore[assignment]

_bridge: "FreecadGuiBridge | None" = None


class FreecadGuiBridge(QObject):
    open_preferences_requested = Signal()
    main_call_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self.open_preferences_requested.connect(
            self._open_preferences,
            Qt.ConnectionType.QueuedConnection,
        )
        self.main_call_requested.connect(
            self._run_main_call,
            Qt.ConnectionType.QueuedConnection,
        )

    @Slot(object)
    def _run_main_call(self, fn: object) -> None:
        if not callable(fn):
            return
        try:
            fn()
        except Exception as exc:
            try:
                import FreeCAD as App

                App.Console.PrintError(f"[ATRIA] Error ejecutando comando: {exc}\n")
            except ImportError:
                pass
            print(f"Error al ejecutar la función: {exc}")

    @Slot()
    def _open_preferences(self) -> None:
        import FreeCAD as App

        try:
            import FreeCADGui as Gui

            Gui.runCommand("ATRIA_OpenPreferences", 0)
            App.Console.PrintMessage("[ATRIA] Preferencias abiertas por voz.\n")
        except Exception as exc:
            try:
                from GUIFreeCad.integration.atria_paths import ensure_gui_on_path

                ensure_gui_on_path()
                from GUIFreeCad.integration.launch_preferences import open_preferences

                open_preferences()
                App.Console.PrintMessage("[ATRIA] Preferencias abiertas por voz.\n")
            except Exception as exc2:
                App.Console.PrintError(
                    f"[ATRIA] Error abriendo preferencias: {exc}; fallback: {exc2}\n"
                )


def init_gui_bridge() -> FreecadGuiBridge:
    global _bridge
    if _bridge is None:
        _bridge = FreecadGuiBridge()
    return _bridge


def request_open_preferences() -> None:
    """Safe to call from the ATRIA voice background thread."""
    init_gui_bridge().open_preferences_requested.emit()


def run_on_main_thread(fn: Callable[[], Any]) -> None:
    """Queue `fn` on the FreeCAD/Qt GUI thread (required for Gui.runCommand)."""
    init_gui_bridge().main_call_requested.emit(fn)

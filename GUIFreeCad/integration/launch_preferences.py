"""Open ATRIA preferences inside FreeCAD (or standalone for tests)."""

from __future__ import annotations

from GUIFreeCad.integration.freecad_host import (
    ensure_gui_on_path,
    get_freecad_main_window,
    get_qt_application,
    in_freecad,
)
from GUIFreeCad.core.settings import settings
from GUIFreeCad.ui.preferences_dialog import PreferencesDialog
from GUIFreeCad.ui.theme import apply_theme


def open_preferences(parent=None) -> None:
    ensure_gui_on_path()

    if parent is None and in_freecad():
        parent = get_freecad_main_window()

    dlg = PreferencesDialog(parent)

    def on_changed() -> None:
        apply_theme(get_qt_application(), settings.theme)
        try:
            from GUIFreeCad.integration.atria_dock_panel import get_source
            src = get_source()
            if src is not None and src._panel is not None:
                src._panel.SetTheme(settings.theme)
        except Exception:
            pass
        try:
            from GUIFreeCad.integration.apply_settings import apply_report_palette
            apply_report_palette(settings.theme)
        except Exception:
            pass
        try:
            from GUIFreeCad.integration.apply_settings import apply_report_palette
            apply_report_palette(settings.theme)
        except Exception:
            pass

    dlg.settings_changed.connect(on_changed)
    dlg.exec()

    if in_freecad():
        from GUIFreeCad.integration.freecad_ui_setup import show_report_view_instead_of_python
        from GUIFreeCad.speech.atria_voice_service import AtriaVoiceService

        show_report_view_instead_of_python(persist_prefs=False)
        AtriaVoiceService.get().resume_cad_voice()
        _hint_after_preferences()


def _hint_after_preferences() -> None:
    try:
        import FreeCAD as App
        from GUIFreeCad.integration.voice_bootstrap import is_voice_running

        if is_voice_running():
            App.Console.PrintMessage(
                "[ATRIA] Preferencias cerradas. Voz CAD reanudada "
                "(Â«archivo enviarÂ», Â«preferencias enviarÂ», etc.).\n"
            )
    except ImportError:
        pass

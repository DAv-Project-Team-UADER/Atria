"""Load settings.json and apply theme (and related UI state)."""

from __future__ import annotations

from GUIFreeCad.core.settings import settings
from GUIFreeCad.ui.theme import apply_theme


def apply_report_palette(theme: str) -> None:
    """Set the report view text color via FreeCAD's parameter system and rehighlight.

    ``ReportOutput::OnChange`` observes ``OutputWindow/colorText`` and calls
    ``reportHl->setTextColor()`` when it changes, but does not call
    ``rehighlight()`` on existing lines. Furthermore, FreeCAD's built-in
    ``FreeCAD Dark.cfg`` preference pack omits ``colorText``, so if ATRIA
    previously wrote ``0x00000000`` (black) for light mode, switching to dark
    mode leaves ``colorText`` black unless updated and rehighlighted here.
    """
    is_dark = str(theme).strip().lower() == "dark"
    try:
        import FreeCAD as App

        hGrp = App.ParamGet("User parameter:BaseApp/Preferences/OutputWindow")
        # colorText is packed RGBA: (R << 24) | (G << 16) | (B << 8) | A
        target_text = 0xE0E0E0FF if is_dark else 0x222222FF
        # Force OnChange notification even if the stored value matches target_text
        if hGrp.GetUnsigned("colorText", 0) == target_text:
            hGrp.SetUnsigned("colorText", target_text ^ 0x00000100)
        hGrp.SetUnsigned("colorText", target_text)
        if is_dark:
            hGrp.SetUnsigned("colorLogging", 0x64B5F6FF)
            hGrp.SetUnsigned("colorWarning", 0xFFB74DFF)
            hGrp.SetUnsigned("colorError", 0xEF5350FF)
    except Exception:
        pass

    try:
        import FreeCADGui as Gui
        try:
            from PySide6.QtGui import QColor, QPalette, QSyntaxHighlighter
            from PySide6.QtWidgets import QDockWidget, QPlainTextEdit, QTextEdit
        except ImportError:
            from PySide2.QtGui import QColor, QPalette, QSyntaxHighlighter  # type: ignore[no-redef]
            from PySide2.QtWidgets import QDockWidget, QPlainTextEdit, QTextEdit  # type: ignore[no-redef]

        mw = Gui.getMainWindow()
        if mw is None:
            return

        fg_hex = "#e0e0e0" if is_dark else "#222222"
        bg_hex = "#1e1e1e" if is_dark else "#ffffff"
        fg_color = QColor(fg_hex)
        bg_color = QColor(bg_hex)

        report_editors = []
        for dock in mw.findChildren(QDockWidget):
            if dock.objectName() in ("Std_ReportView", "Report view", "Informe"):
                report_editors.extend(dock.findChildren(QTextEdit))
                report_editors.extend(dock.findChildren(QPlainTextEdit))
        for te in mw.findChildren(QTextEdit):
            cls_name = te.metaObject().className() if te.metaObject() else ""
            if te.objectName() in ("ReportOutput", "PythonConsole") or "ReportOutput" in cls_name:
                if te not in report_editors:
                    report_editors.append(te)

        for editor in report_editors:
            pal = editor.palette()
            pal.setColor(QPalette.Text, fg_color)
            pal.setColor(QPalette.WindowText, fg_color)
            pal.setColor(QPalette.Base, bg_color)
            editor.setPalette(pal)
            editor.setStyleSheet(f"background-color: {bg_hex}; color: {fg_hex};")

            # Rehighlight existing paragraphs so lines logged before the theme switch update color
            highlighters = list(editor.findChildren(QSyntaxHighlighter))
            doc = getattr(editor, "document", lambda: None)()
            if doc is not None:
                for hl in doc.findChildren(QSyntaxHighlighter):
                    if hl not in highlighters:
                        highlighters.append(hl)
            for hl in highlighters:
                try:
                    hl.rehighlight()
                except Exception:
                    pass
            editor.viewport().update()
    except Exception:
        pass


def sync_freecad_theme_state(theme: str) -> None:
    """Synchronize FreeCAD's MainWindow/Theme preference and Welcome screen buttons with ATRIA."""
    is_dark = str(theme).strip().lower() == "dark"
    fc_theme_name = "FreeCAD Dark" if is_dark else "FreeCAD Light"
    try:
        import FreeCAD as App

        mw_grp = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
        if mw_grp.GetString("Theme", "") != fc_theme_name:
            mw_grp.SetString("Theme", fc_theme_name)
    except Exception:
        pass

    try:
        import FreeCADGui as Gui
        try:
            from PySide6.QtWidgets import QToolButton, QWidget
        except ImportError:
            from PySide2.QtWidgets import QToolButton, QWidget  # type: ignore[no-redef]

        mw = Gui.getMainWindow()
        if mw is None:
            return

        for widget in mw.findChildren(QWidget):
            cls_name = widget.metaObject().className() if widget.metaObject() else ""
            if "ThemeSelectorWidget" in cls_name:
                for btn in widget.findChildren(QToolButton):
                    txt = (btn.text() or "").strip().lower()
                    should_check = ("dark" in txt or "oscuro" in txt) if is_dark else ("light" in txt or "claro" in txt)
                    if btn.isCheckable() and btn.isChecked() != should_check:
                        prev = btn.blockSignals(True)
                        btn.setChecked(should_check)
                        btn.blockSignals(prev)
    except Exception:
        pass


def hook_welcome_theme_selector() -> None:
    """Connect to FreeCAD's StartGui::ThemeSelectorWidget buttons so 1 click updates ATRIA."""
    try:
        import FreeCADGui as Gui
        try:
            from PySide6.QtCore import QTimer
            from PySide6.QtWidgets import QApplication, QToolButton, QWidget
        except ImportError:
            from PySide2.QtCore import QTimer  # type: ignore[no-redef]
            from PySide2.QtWidgets import QApplication, QToolButton, QWidget  # type: ignore[no-redef]

        mw = Gui.getMainWindow()
        if mw is None:
            return

        for widget in mw.findChildren(QWidget):
            cls_name = widget.metaObject().className() if widget.metaObject() else ""
            if "ThemeSelectorWidget" not in cls_name:
                continue
            for btn in widget.findChildren(QToolButton):
                if getattr(btn, "_atria_theme_hooked", False):
                    continue
                btn._atria_theme_hooked = True  # type: ignore[attr-defined]

                def _on_btn_clicked(_checked: bool = False, button: QToolButton = btn, parent: QWidget = widget) -> None:
                    txt = (button.text() or "").strip().lower()
                    new_theme = "dark" if ("dark" in txt or "oscuro" in txt) else "light"
                    # Ensure the clicked button stays checked and others are unchecked
                    if button.isCheckable():
                        for sibling in parent.findChildren(QToolButton):
                            prev = sibling.blockSignals(True)
                            sibling.setChecked(sibling is button)
                            sibling.blockSignals(prev)

                    def _apply() -> None:
                        settings.theme = new_theme
                        try:
                            settings.save()
                        except Exception:
                            pass
                        app = QApplication.instance()
                        if app is not None:
                            apply_theme(app, new_theme)
                        apply_report_palette(new_theme)
                        sync_freecad_theme_state(new_theme)
                        try:
                            from GUIFreeCad.integration.atria_dock_panel import get_source

                            src = get_source()
                            if src is not None and src._panel is not None:
                                src._panel.SetTheme(new_theme)
                        except Exception:
                            pass

                    QTimer.singleShot(0, _apply)

                btn.clicked.connect(_on_btn_clicked)
    except Exception:
        pass


def apply_saved_settings(app=None) -> None:
    """Re-read config/settings.json and apply theme to the running Qt app."""
    settings.load()
    if app is None:
        try:
            from PySide6.QtWidgets import QApplication
        except ImportError:
            from PySide2.QtWidgets import QApplication  # type: ignore[no-redef]

        app = QApplication.instance()
    if app is not None:
        apply_theme(app, settings.theme)

    try:
        from GUIFreeCad.integration.atria_dock_panel import get_source

        src = get_source()
        if src is not None and src._panel is not None:
            src._panel.SetTheme(settings.theme)
            src._panel.SetLanguage(settings.language)
    except Exception:
        pass

    apply_report_palette(settings.theme)
    sync_freecad_theme_state(settings.theme)
    hook_welcome_theme_selector()

    try:
        import FreeCAD  # noqa: F401

        from GUIFreeCad.integration.freecad_voice_setup import install_freecad_integration

        install_freecad_integration()
    except ImportError:
        pass

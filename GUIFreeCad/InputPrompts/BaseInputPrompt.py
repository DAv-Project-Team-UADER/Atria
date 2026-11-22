# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""Reusable base dialog for ATRIA voice-driven input prompts."""

from __future__ import annotations

from typing import Any

try:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import (
        QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
    )
except ImportError:
    try:
        from PySide2.QtCore import Qt, Signal  # type: ignore[assignment]
        from PySide2.QtWidgets import (  # type: ignore[assignment]
            QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
        )
    except ImportError:  # Running outside FreeCAD in headless/mock test mode
        class QDialog:
            def __init__(self, parent=None):
                self._parent = parent
            def setWindowTitle(self, t): pass
            def setModal(self, m): pass
            def setMinimumWidth(self, w): pass
            def setStyleSheet(self, s): pass
            def show(self): pass
            def raise_(self): pass
            def activateWindow(self): pass
            def accept(self): pass
            def reject(self): pass
            def exec(self): return 0
            def exec_(self): return 0

        class Signal:
            def __init__(self, *args): pass
            def emit(self, *args): pass
            def connect(self, slot): pass

        Qt = type("Qt", (), {"AlignCenter": 0, "AlignmentFlag": type("AlignmentFlag", (), {"AlignCenter": 0})})
        QApplication = type("QApplication", (), {"instance": lambda: None})

        class QLabel:
            def __init__(self, *args):
                self._text = ""
            def setText(self, t): self._text = t
            def text(self): return self._text
            def setWordWrap(self, w): pass
            def setAlignment(self, a): pass
            def setStyleSheet(self, s): pass

        class QPushButton:
            def __init__(self, *args):
                self.clicked = Signal()
                self._text = args[0] if args else ""
            def setText(self, t): self._text = t
            def text(self): return self._text
            def setToolTip(self, t): pass
            def setStyleSheet(self, s): pass
            def setCursor(self, c): pass
            def setAutoDefault(self, a): pass
            def setDefault(self, d): pass

        class QVBoxLayout:
            def __init__(self, *args): pass
            def setSpacing(self, s): pass
            def addWidget(self, w): pass
            def addLayout(self, l): pass

        class QHBoxLayout:
            def __init__(self, *args): pass
            def addStretch(self): pass
            def addWidget(self, w): pass

from InputPrompts.PromptResult import PromptResult
from InputPrompts.InputPromptI18n import ResolveLanguage, T


def _AlignCenter():
    if hasattr(Qt, "AlignmentFlag"):
        return Qt.AlignmentFlag.AlignCenter
    return Qt.AlignCenter


# Colores por tema: (fondo, texto, fondo del texto escuchado, borde, fondo botón, hover botón)
_LIGHT_THEME = ("#ffffff", "#000000", "#f3f3f3", "#d8d8d8", "#f0f0f0", "#e2e2e2")
_DARK_THEME = ("#2b2b2b", "#E03C1B", "#3a3a3a", "#555555", "#444444", "#555555")


def _IsDarkTheme() -> bool:
    """Return True when FreeCAD is running with a dark theme.

    FreeCAD aplica su tema oscuro con una hoja de estilos (.qss), por lo que la
    paleta de Qt sigue siendo clara: se consulta primero la preferencia del
    tema y solo si no dice nada se mira la paleta.
    """
    try:
        import FreeCAD as App

        grupo = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
        for clave in ("Theme", "StyleSheet"):
            valor = str(grupo.GetString(clave, "")).lower()
            if "dark" in valor or "oscuro" in valor:
                return True
            if valor:
                return False
    except Exception:
        pass
    app = QApplication.instance()
    if app is None:
        return False
    return app.palette().window().color().lightness() < 128


class BaseInputPrompt(QDialog):
    """Base Qt dialog used by concrete input prompt implementations."""

    ResultReady = Signal(object)

    def __init__(
        self,
        Title: str = "ATRIA Input",
        Message: str = "Say a value",
        Parent=None,
    ) -> None:
        super().__init__(Parent)
        self._Language = ResolveLanguage()
        self._Title = Title
        self._Message = Message
        self._Result = PromptResult.Pending()
        self._AccumulatedText = ""
        self._BuildUi()
        self.SetTitle(Title)
        self.SetMessage(Message)
        self.SetStatus(T(self._Language, "listening"))

    def _BuildUi(self) -> None:
        self.setModal(True)
        self.setMinimumWidth(420)
        # Colores segun el tema: texto negro sobre claro, rojo sobre oscuro.
        bg, fg, heard_bg, border, button_bg, button_hover = (
            _DARK_THEME if _IsDarkTheme() else _LIGHT_THEME
        )
        self._TextColor = fg
        self._HeardStyle = (
            f"background: {heard_bg}; color: {fg}; border: 1px solid {border}; padding: 8px;"
        )
        self.setStyleSheet(
            f"QDialog {{ background: {bg}; }}"
            f"QLabel {{ color: {fg}; background: transparent; }}"
            f"QPushButton {{ color: {fg}; background: {button_bg};"
            f" border: 1px solid {border}; padding: 4px 14px; }}"
            f"QPushButton:hover {{ background: {button_hover}; }}"
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self._MessageLabel = QLabel(self)
        self._MessageLabel.setWordWrap(True)
        self._MessageLabel.setAlignment(_AlignCenter())
        layout.addWidget(self._MessageLabel)

        self._StatusLabel = QLabel(self)
        self._StatusLabel.setAlignment(_AlignCenter())
        self._StatusLabel.setStyleSheet(f"color: {self._TextColor}; font-size: 9pt;")
        layout.addWidget(self._StatusLabel)

        self._HeardLabel = QLabel(self)
        self._HeardLabel.setWordWrap(True)
        self._HeardLabel.setAlignment(_AlignCenter())
        self._HeardLabel.setStyleSheet(self._HeardStyle)
        layout.addWidget(self._HeardLabel)

        button_row = QHBoxLayout()
        button_row.addStretch()

        ok_text = f"✓ {T(self._Language, 'ok')}"
        cancel_text = f"✕ {T(self._Language, 'cancel')}"

        self._OkButton = QPushButton(ok_text, self)
        self._CancelButton = QPushButton(cancel_text, self)
        self._OkButton.setAutoDefault(False)
        self._OkButton.setDefault(True)
        self._CancelButton.setAutoDefault(False)
        self._CancelButton.setDefault(False)

        self._OkButton.setToolTip(
            "Confirmar valor ingresado\n"
            "🎤 Di «ok», «listo» o «enviar»\n"
            "⌨️ Presiona Enter"
        )
        self._CancelButton.setToolTip(
            "Cancelar y descartar entrada\n"
            "🎤 Di «cancelar» o «anular»\n"
            "⌨️ Presiona Esc"
        )

        hand_cursor = getattr(Qt, "PointingHandCursor", None)
        if hand_cursor is not None:
            if hasattr(self._OkButton, "setCursor"):
                self._OkButton.setCursor(hand_cursor)
            if hasattr(self._CancelButton, "setCursor"):
                self._CancelButton.setCursor(hand_cursor)

        is_dark = _IsDarkTheme()
        if is_dark:
            self._OkButton.setStyleSheet(
                "QPushButton { background-color: #15803d; color: #ffffff;"
                " border: 1.5px solid #22c55e; border-radius: 6px; padding: 6px 18px;"
                " font-size: 10pt; font-weight: bold; }"
                "QPushButton:hover { background-color: #16a34a; border-color: #4ade80; }"
                "QPushButton:pressed { background-color: #14532d; }"
            )
            self._CancelButton.setStyleSheet(
                "QPushButton { background-color: #374151; color: #e5e7eb;"
                " border: 1.5px solid #4b5563; border-radius: 6px; padding: 6px 18px;"
                " font-size: 10pt; font-weight: 500; }"
                "QPushButton:hover { background-color: #4b5563; border-color: #9ca3af; }"
                "QPushButton:pressed { background-color: #1f2937; }"
            )
        else:
            self._OkButton.setStyleSheet(
                "QPushButton { background-color: #16a34a; color: #ffffff;"
                " border: 1.5px solid #15803d; border-radius: 6px; padding: 6px 18px;"
                " font-size: 10pt; font-weight: bold; }"
                "QPushButton:hover { background-color: #15803d; border-color: #166534; }"
                "QPushButton:pressed { background-color: #14532d; }"
            )
            self._CancelButton.setStyleSheet(
                "QPushButton { background-color: #f3f4f6; color: #374151;"
                " border: 1.5px solid #d1d5db; border-radius: 6px; padding: 6px 18px;"
                " font-size: 10pt; font-weight: 500; }"
                "QPushButton:hover { background-color: #e5e7eb; border-color: #9ca3af; }"
                "QPushButton:pressed { background-color: #d1d5db; }"
            )

        self._OkButton.clicked.connect(self._OnOkClicked)
        self._CancelButton.clicked.connect(self.Cancel)
        button_row.addWidget(self._OkButton)
        button_row.addWidget(self._CancelButton)
        button_row.addStretch()
        layout.addLayout(button_row)

        self.SetHeardText("")

    def _OnOkClicked(self) -> None:
        """Invoked when the OK button is clicked or Enter is pressed."""
        self.AcceptValue(self.GetCurrentText())

    def SetTitle(self, Title: str) -> None:
        """Update the dialog title."""
        self._Title = Title
        self.setWindowTitle(Title)

    def SetMessage(self, Message: str) -> None:
        """Update the main prompt message."""
        self._Message = Message
        self._MessageLabel.setText(Message)

    def SetStatus(self, Status: str) -> None:
        """Update the listening/status label."""
        self._StatusLabel.setText(Status)

    def SetHeardText(self, Text: str) -> None:
        """Update the recognized text preview."""
        display = Text.strip() if Text else ""
        self._HeardLabel.setText(display or "...")

    def GetCurrentText(self) -> str:
        """Return the current recognized text shown by the prompt."""
        text = self._HeardLabel.text()
        return "" if text == "..." else text

    def GetResult(self) -> PromptResult:
        """Return the current prompt result."""
        return self._Result

    def ProcessPartialText(self, Text: str) -> None:
        """Process partial recognized text."""
        self.SetHeardText(Text)
        self.SetStatus(T(self._Language, "listening"))

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Process final recognized text.

        Concrete prompts should override this method when they need parsing or
        validation before accepting the value.
        """
        self.SetHeardText(Text)
        return self.GetResult()

    def RequiresNumericGrammar(self) -> bool:
        """Return True when this prompt needs the Vosk numeric-word grammar.

        Overridden by prompts (see NumericInputPrompt) that collect spoken
        digits, so callers can switch grammar polymorphically instead of
        checking concrete prompt types.
        """
        return False

    @staticmethod
    def _HasConfirmation(Tokens: list[str]) -> bool:
        from InputPrompts.SpokenNumberParser import SpokenNumberParser

        return any(token in SpokenNumberParser.ConfirmationWords for token in Tokens)

    @staticmethod
    def _HasCancellation(Tokens: list[str]) -> bool:
        from InputPrompts.SpokenNumberParser import SpokenNumberParser

        return any(token in SpokenNumberParser.CancellationWords for token in Tokens)

    def AcceptValue(self, Value: Any | None = None) -> PromptResult:
        """Accept the prompt with a value and close the dialog."""
        if isinstance(Value, str) and not Value.strip():
            return self.Fail(T(self._Language, "value_not_empty"))
        self._Result = PromptResult.Ok(Value)
        self.SetStatus(T(self._Language, "accepted"))
        self.ResultReady.emit(self._Result)
        self.accept()
        return self._Result

    def Fail(self, Error: str) -> PromptResult:
        """Store a failed result and keep the dialog open."""
        self._Result = PromptResult.Fail(Error)
        self.SetStatus(Error)
        self.ResultReady.emit(self._Result)
        return self._Result

    def Cancel(self) -> PromptResult:
        """Cancel the prompt and close the dialog."""
        self._Result = PromptResult.Cancel()
        self.SetStatus(T(self._Language, "cancelled"))
        self.ResultReady.emit(self._Result)
        self.reject()
        return self._Result

    def Show(self) -> None:
        """Show the prompt without blocking the caller."""
        self.show()
        self.raise_()
        self.activateWindow()

    def RequestValue(self) -> PromptResult:
        """Show the prompt modally and return its result."""
        self._ExecDialog()
        return self.GetResult()

    def reject(self) -> None:
        """Treat closing the dialog as cancellation."""
        if self._Result.Success:
            super().reject()
            return
        self._Result = PromptResult.Cancel()
        super().reject()

    def _ExecDialog(self) -> int:
        if hasattr(self, "exec"):
            return self.exec()
        return self.exec_()

    def keyPressEvent(self, event) -> None:
        key = getattr(event, "key", lambda: -1)()
        return_keys = (getattr(Qt, "Key_Return", 16777220), getattr(Qt, "Key_Enter", 16777221))
        if key in return_keys:
            self._OnOkClicked()
            if hasattr(event, "accept"):
                event.accept()
            return
        if key == getattr(Qt, "Key_Escape", 16777216):
            self.Cancel()
            if hasattr(event, "accept"):
                event.accept()
            return
        if key == getattr(Qt, "Key_Backspace", 16777219):
            current = self.GetCurrentText()
            if current:
                new_text = current[:-1]
                self.SetHeardText(new_text)
                if hasattr(self, "_AccumulatedText"):
                    self._AccumulatedText = new_text
            if hasattr(event, "accept"):
                event.accept()
            return
        text = getattr(event, "text", lambda: "")()
        if text and (text.isalnum() or text in ".,-+ "):
            current = self.GetCurrentText()
            new_text = current + text
            self.SetHeardText(new_text)
            if hasattr(self, "_AccumulatedText"):
                self._AccumulatedText = (getattr(self, "_AccumulatedText", "") + text).strip()
            if hasattr(event, "accept"):
                event.accept()
            return
        if hasattr(super(), "keyPressEvent"):
            super().keyPressEvent(event)

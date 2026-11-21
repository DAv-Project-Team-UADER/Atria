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

"""Ventana emergente de ayuda contextual y manual de comandos de ATRIA.

Muestra explicaciones claras sobre para qué se usa cada botón de la sección activa,
con soporte adaptativo para Modo Claro y Modo Oscuro según la configuración del usuario.
Permite consultar la ayuda por interfaz o por voz («ayuda» / «manual»)
y cerrarla mediante el comando «cerrar ayuda» o «cerrar» (o tecla Escape / botón Cerrar).
"""

from __future__ import annotations

import sys
from typing import Any

# Intentar importar bindings de Qt
QtWidgets = None
QtCore = None
QtGui = None

for mod_name in ("PySide", "PySide6", "PySide2"):
    try:
        mod = __import__(mod_name, fromlist=["QtWidgets", "QtCore", "QtGui"])
        QtWidgets = getattr(mod, "QtWidgets", None) or getattr(mod, "QtGui", None)
        QtCore = getattr(mod, "QtCore", None)
        QtGui = getattr(mod, "QtGui", None)
        if QtWidgets and hasattr(QtWidgets, "QDialog"):
            break
    except Exception:
        pass


def detect_theme(parent=None) -> str:
    """Detecta el tema activo (light o dark) según el panel, settings o FreeCAD."""
    if parent is not None and hasattr(parent, "_theme"):
        theme_val = str(getattr(parent, "_theme", "")).strip().lower()
        if theme_val in ("light", "dark"):
            return theme_val

    try:
        from GUIFreeCad.core.settings import settings
        if hasattr(settings, "theme") and settings.theme:
            return str(settings.theme).strip().lower()
    except Exception:
        pass

    try:
        import json
        from pathlib import Path
        cfg = Path(__file__).resolve().parents[1] / "config" / "settings.json"
        if cfg.exists():
            data = json.loads(cfg.read_text(encoding="utf-8-sig"))
            if "theme" in data and str(data["theme"]).strip().lower() in ("light", "dark"):
                return str(data["theme"]).strip().lower()
    except Exception:
        pass

    try:
        import FreeCADGui as Gui
        palette = Gui.getMainWindow().palette()
        colour = palette.color(palette.ColorRole.Window)
        luminance = (
            0.299 * colour.red() + 0.587 * colour.green() + 0.114 * colour.blue()
        ) / 255.0
        return "dark" if luminance < 0.5 else "light"
    except Exception:
        pass

    return "light"


_active_dialog: Any = None


class AtriaHelpDialog:
    """Controlador y diálogo de ayuda contextual de ATRIA."""

    _active_instance = None

    def __init__(
        self,
        title: str,
        items: list[tuple[str, str]],
        parent=None,
        theme: str | None = None,
    ) -> None:
        self.title = title
        self.items = items
        self._parent = parent
        self.theme = theme or detect_theme(parent)
        self._qt_dialog = None

        if QtWidgets and hasattr(QtWidgets, "QDialog"):
            self._create_qt_dialog()

    def _create_qt_dialog(self) -> None:
        QDialog = QtWidgets.QDialog
        QVBoxLayout = QtWidgets.QVBoxLayout
        QHBoxLayout = QtWidgets.QHBoxLayout
        QLabel = QtWidgets.QLabel
        QPushButton = QtWidgets.QPushButton
        QScrollArea = QtWidgets.QScrollArea
        QWidget = QtWidgets.QWidget
        QFrame = QtWidgets.QFrame
        QFont = QtGui.QFont if QtGui else None
        Qt = QtCore.Qt if QtCore else None

        parent_widget = self._parent
        if parent_widget is None:
            try:
                import FreeCADGui as Gui
                parent_widget = Gui.getMainWindow() if hasattr(Gui, "getMainWindow") else None
            except Exception:
                parent_widget = None

        dlg = QDialog(parent_widget)
        dlg.setObjectName("AtriaHelpDialog")
        dlg.setWindowTitle(f"ATRIA - Manual y Ayuda: {self.title}")
        dlg.setModal(False)
        dlg.resize(620, 520)
        dlg.setMinimumSize(480, 380)

        is_dark = self.theme == "dark"

        if is_dark:
            dlg.setStyleSheet("""
                QDialog#AtriaHelpDialog {
                    background-color: #1e1e24;
                    color: #e0e0e0;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLabel {
                    color: #f0f0f4;
                }
                QScrollArea {
                    background-color: #26262d;
                    border: 1px solid #383842;
                    border-radius: 6px;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #1e1e24;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #484854;
                    min-height: 25px;
                    border-radius: 5px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #00828A;
                }
                QFrame.cardFrame {
                    background-color: #2d2d36;
                    border: 1px solid #3c3c4a;
                    border-radius: 6px;
                    padding: 6px;
                }
                QFrame.cardFrame:hover {
                    border: 1px solid #00a896;
                    background-color: #33333e;
                }
                QPushButton#closeBtn {
                    background-color: #00828A;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11pt;
                    padding: 8px 24px;
                }
                QPushButton#closeBtn:hover {
                    background-color: #00a896;
                }
                QPushButton#closeBtn:pressed {
                    background-color: #005f66;
                }
            """)
            title_style = "color: #00e5ff; font-weight: bold;"
            sub_style = "color: #b0b0bc;"
            cmd_style = "color: #72efdd; font-weight: bold;"
            desc_style = "color: #e2e2e8;"
            hint_style = "color: #94d2bd; font-style: italic;"
        else:
            # Modo Claro: paleta limpia, profesional y de alto contraste
            dlg.setStyleSheet("""
                QDialog#AtriaHelpDialog {
                    background-color: #f8f9fa;
                    color: #1a202c;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLabel {
                    color: #1a202c;
                }
                QScrollArea {
                    background-color: #ffffff;
                    border: 1.5px solid #dcdfe4;
                    border-radius: 6px;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #f1f5f9;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #cbd5e1;
                    min-height: 25px;
                    border-radius: 5px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #00828A;
                }
                QFrame.cardFrame {
                    background-color: #ffffff;
                    border: 1.5px solid #e2e8f0;
                    border-radius: 6px;
                    padding: 6px;
                }
                QFrame.cardFrame:hover {
                    border: 1.5px solid #00828A;
                    background-color: #f0fdfa;
                }
                QPushButton#closeBtn {
                    background-color: #00828A;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11pt;
                    padding: 8px 24px;
                }
                QPushButton#closeBtn:hover {
                    background-color: #006d77;
                }
                QPushButton#closeBtn:pressed {
                    background-color: #00535a;
                }
            """)
            title_style = "color: #006d77; font-weight: bold;"
            sub_style = "color: #4a5568;"
            cmd_style = "color: #007a82; font-weight: bold;"
            desc_style = "color: #2d3748;"
            hint_style = "color: #0d9488; font-style: italic;"

        main_layout = QVBoxLayout(dlg)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        # Encabezado
        header_box = QVBoxLayout()
        header_box.setSpacing(3)

        title_lbl = QLabel(self.title)
        if QFont:
            title_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_lbl.setStyleSheet(title_style)
        header_box.addWidget(title_lbl)

        sub_lbl = QLabel("Pronuncia el comando por voz o haz clic sobre su botón en la pantalla:")
        if QFont:
            sub_lbl.setFont(QFont("Segoe UI", 9))
        sub_lbl.setStyleSheet(sub_style)
        header_box.addWidget(sub_lbl)

        main_layout.addLayout(header_box)

        # Área de scroll con cada botón y su explicación
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        cards_layout = QVBoxLayout(container)
        cards_layout.setContentsMargins(10, 10, 10, 10)
        cards_layout.setSpacing(8)

        for cmd, desc in self.items:
            card = QFrame()
            card.setProperty("class", "cardFrame")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(8, 6, 8, 6)
            card_layout.setSpacing(3)

            cmd_lbl = QLabel(f"🎤 {cmd}")
            if QFont:
                cmd_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
            cmd_lbl.setStyleSheet(cmd_style)
            card_layout.addWidget(cmd_lbl)

            desc_lbl = QLabel(desc)
            desc_lbl.setWordWrap(True)
            if QFont:
                desc_lbl.setFont(QFont("Segoe UI", 9))
            desc_lbl.setStyleSheet(desc_style)
            card_layout.addWidget(desc_lbl)

            cards_layout.addWidget(card)

        cards_layout.addStretch(1)
        scroll.setWidget(container)
        main_layout.addWidget(scroll, stretch=1)

        # Pie de ventana
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 4, 0, 0)

        voice_hint = QLabel("💡 Di: «cerrar ayuda» o «cerrar» para cerrar esta ventana")
        if QFont:
            voice_hint.setFont(QFont("Segoe UI", 9))
        voice_hint.setStyleSheet(hint_style)
        footer_layout.addWidget(voice_hint)

        footer_layout.addStretch(1)

        close_btn = QPushButton("Cerrar")
        close_btn.setObjectName("closeBtn")
        if Qt and hasattr(Qt, "PointingHandCursor"):
            close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(dlg.close)
        footer_layout.addWidget(close_btn)

        main_layout.addLayout(footer_layout)

        # Limpiar referencia al cerrarse
        def _on_destroyed(*_args):
            if AtriaHelpDialog._active_instance is self:
                AtriaHelpDialog._active_instance = None

        dlg.destroyed.connect(_on_destroyed)
        dlg.finished.connect(lambda _res: self.close())

        self._qt_dialog = dlg

    def show(self) -> None:
        """Muestra la ventana y la trae al frente."""
        if self._qt_dialog is not None:
            self._qt_dialog.show()
            self._qt_dialog.raise_()
            self._qt_dialog.activateWindow()
        AtriaHelpDialog._active_instance = self

    def close(self) -> None:
        """Cierra la ventana emergente."""
        if self._qt_dialog is not None:
            try:
                self._qt_dialog.close()
            except Exception:
                pass
        if AtriaHelpDialog._active_instance is self:
            AtriaHelpDialog._active_instance = None

    def isVisible(self) -> bool:
        """Verifica si la ventana está actualmente visible."""
        if self._qt_dialog is not None:
            try:
                return bool(self._qt_dialog.isVisible())
            except Exception:
                return False
        return AtriaHelpDialog._active_instance is self

    # ------------------------------------------------------------------
    # Métodos de clase para gestión centralizada (Singleton / Voz)
    # ------------------------------------------------------------------

    @classmethod
    def ShowHelp(
        cls,
        title: str,
        content: str | list[tuple[str, str]],
        parent=None,
        theme: str | None = None,
    ) -> AtriaHelpDialog:
        """Crea y muestra la ventana de ayuda emergente en el tema correspondiente."""
        # Cerrar ventana previa si está abierta
        cls.CloseHelp()

        items: list[tuple[str, str]] = []
        if isinstance(content, list):
            items = content
        elif isinstance(content, str):
            # Parsear texto plano en pares (comando, descripcion)
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("==="):
                    continue
                if " - " in line:
                    parts = line.split(" - ", 1)
                    items.append((parts[0].strip(), parts[1].strip()))
                elif ":" in line:
                    parts = line.split(":", 1)
                    items.append((parts[0].strip(), parts[1].strip()))
                else:
                    items.append((line, ""))

        dialog = cls(title, items, parent=parent, theme=theme)
        dialog.show()
        cls._active_instance = dialog
        return dialog

    @classmethod
    def CloseHelp(cls) -> bool:
        """Cierra la ventana de ayuda si está abierta."""
        if cls._active_instance is not None:
            try:
                cls._active_instance.close()
            except Exception:
                pass
            cls._active_instance = None
            return True
        return False

    @classmethod
    def IsHelpOpen(cls) -> bool:
        """Retorna True si hay una ventana de ayuda activa y visible."""
        if cls._active_instance is not None:
            return cls._active_instance.isVisible()
        return False

    @classmethod
    def GetActiveDialog(cls) -> AtriaHelpDialog | None:
        """Retorna la instancia activa del diálogo de ayuda, si existe."""
        return cls._active_instance

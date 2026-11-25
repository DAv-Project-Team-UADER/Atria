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

"""Pure Atria panel widget: renders voice state, emits user intent."""

from __future__ import annotations

import os
from datetime import datetime

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QIcon, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QTextEdit,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtSvgWidgets import QSvgWidget

try:
    from InterfazATRIA.ContextView import ContextView
    from InterfazATRIA.FlashOverlay import FlashOverlay
    from InterfazATRIA.IconLocator import IconLocator
    from InterfazATRIA.Paletas import DARK, FONT_MONO, FONT_SANS, LIGHT
    from InterfazATRIA.Textos import TEXTS, format_section_title
except ImportError:
    try:
        from .ContextView import ContextView
        from .FlashOverlay import FlashOverlay
        from .IconLocator import IconLocator
        from .Paletas import DARK, FONT_MONO, FONT_SANS, LIGHT
        from .Textos import TEXTS, format_section_title
    except ImportError:
        from ContextView import ContextView
        from FlashOverlay import FlashOverlay
        from IconLocator import IconLocator
        from Paletas import DARK, FONT_MONO, FONT_SANS, LIGHT
        from Textos import TEXTS, format_section_title


class AtriaPanel(QWidget):
    """ATRIA panel: context buttons, recognised text, history and object tree.

    Deliberately knows nothing about FreeCAD, the ``Browser`` or the file
    bridge. It is fed through ``RenderContext`` / ``AddToHistory`` / ``SetStatus``
    and reports user intent through signals, so the same widget works as a
    standalone window today and as a ``QDockWidget`` inside FreeCAD after the
    migration (see ``Atria/docs/en/gui-unification-plan.md``).

    Signals:
        CommandRequested(str): the user picked an entry; carries the spoken
            phrase, exactly as if it had been said out loud.
        HelpRequested(): the help button was pressed.
        PreferencesRequested(): the preferences button was pressed.
        DockToggleRequested(): the user asked to detach the panel from the
            FreeCAD window, or to dock it back in. Whoever owns the dock
            decides what that means and calls ``SetDockState`` back.

    Example::

        panel = AtriaPanel()
        panel.CommandRequested.connect(browser.ProcessPhrase)
        panel.RenderContext(view)
    """

    CommandRequested = Signal(str)
    HelpRequested = Signal()
    PreferencesRequested = Signal()
    DockToggleRequested = Signal()

    #: Dimensiones del boton y del icono, en px.
    #: Con icono arriba y comando hablado abajo (Opción A), 74x70 px brinda
    #: perfecta legibilidad a las palabras de activación manteniendo armonía.
    BUTTON_WIDTH = 74
    BUTTON_HEIGHT = 70
    BUTTON_SIZE = BUTTON_HEIGHT  # retrocompatibilidad
    ICON_SIZE = 30

    #: Filas visibles antes de que la grilla empiece a scrollear.
    TOOL_AREA_MAX_ROWS = 3

    def __init__(
        self,
        Parent: QWidget | None = None,
        Theme: str = "light",
        Lang: str = "es",
        Locator: IconLocator | None = None,
    ) -> None:
        super().__init__(Parent)
        self._locator = Locator or IconLocator()
        self._context = ContextView()
        self._toolButtons: list[QToolButton] = []
        self._treeWidget: QTreeWidget | None = None
        self._treeItems: dict[str, QTreeWidgetItem] = {}
        self._lastColumns = 0

        self._theme = Theme
        self._palette = LIGHT if Theme == "light" else DARK
        self._lang = Lang
        self._texts = TEXTS.get(Lang, TEXTS["es"])

        self._BuildUi()
        self.RenderContext(self._context)

    # ================================================================
    # API publica: entrada de datos
    # ================================================================

    def RenderContext(self, Context: ContextView) -> None:
        """Redraw the button area for the given context.

        Args:
            Context: snapshot of the active voice context.
        """
        self._context = Context or ContextView()
        self._UpdateSectionTitle()
        self._ClearToolArea()

        if self._context.IsEmpty():
            self._ShowEmptyHint()
            return

        if hasattr(self, "_emptyHint") and self._emptyHint is not None:
            self._emptyHint.hide()
            self._toolAreaLayout.removeWidget(self._emptyHint)

        # Las entradas sin .svg no generan boton (siguen andando por voz).
        # El boton "subir" va primero (indice 0) para estar siempre visible arriba
        # a la izquierda, sin importar cuantos botones haya ni el scroll horizontal.
        # El botón de ayuda contextual va al inicio, cerca del botón volver (indice 1).
        buttons = []
        if not self._context.IsRoot():
            buttons.append(self._MakeBackButton())
            buttons.append(self._MakeContextHelpButton())

        entries = list(self._context.Entries())
        # Filtrar posibles duplicados de 'ayuda'/'manual' para que no haya dos botones de ayuda
        entries = [
            e for e in entries
            if e.InternalKey.lower() not in ("help", "ayuda")
            and e.Spoken.lower() not in ("ayuda", "help", "manual", "manual de usuario")
        ]

        if self._context.IsRoot():
            # El botón de Explorador debe estar primero en la lista de iconos del menú principal
            explorer_idx = next(
                (i for i, e in enumerate(entries)
                 if e.InternalKey.lower() == "explorer" or e.Spoken.lower() in ("explorador", "explorer")),
                None,
            )
            if explorer_idx is not None and explorer_idx > 0:
                entries.insert(0, entries.pop(explorer_idx))

            entry_buttons = [b for b in map(self._MakeEntryButton, entries) if b is not None]
            if entry_buttons:
                buttons.append(entry_buttons[0])
                buttons.append(self._MakeContextHelpButton())
                buttons.extend(entry_buttons[1:])
            else:
                buttons.append(self._MakeContextHelpButton())
        else:
            buttons.extend(
                b for b in map(self._MakeEntryButton, entries)
                if b is not None
            )
        self._toolButtons = list(buttons)

        # Se llena por columnas, no por filas: con scroll horizontal la altura
        # es la dimension fija (TOOL_AREA_MAX_ROWS) y el ancho es el que crece.
        rows = self._RowCount(len(buttons))
        self._lastColumns = rows
        for index, button in enumerate(buttons):
            self._toolAreaLayout.addWidget(button, index % rows, index // rows)

        # Volver al principio: viniendo de un contexto largo, el nuevo
        # aparecia desplazado.
        self._toolScroll.horizontalScrollBar().setValue(0)

    def _RowCount(self, Total: int) -> int:
        """Cuantas filas usar para repartir ``Total`` botones.

        Nunca mas de TOOL_AREA_MAX_ROWS, y con pocos botones se usan menos
        filas para no dejar una sola columna alta al costado.
        """
        if Total <= 0:
            return 1
        columns_that_fit = max(1, self._VisibleColumns())
        needed = -(-Total // columns_that_fit)  # ceil
        return max(1, min(self.TOOL_AREA_MAX_ROWS, needed))

    def _VisibleColumns(self) -> int:
        """Columnas que entran sin scroll, segun el ancho actual."""
        cell = self.BUTTON_WIDTH + self._toolAreaLayout.spacing()
        available = max(self._toolScroll.viewport().width() - 24, cell)
        return max(1, available // cell)

    def AddToHistory(self, Text: str, FromVoice: bool = True, Unknown: bool = False) -> None:
        """Append a line to the history panel, colour-coded by origin.

        Args:
            Text: line to append.
            FromVoice: True when it came from speech, False for clicks.
            Unknown: True to mark it as an error / unrecognised command.
        """
        if not Text:
            return

        palette = self._palette
        colour = palette["red"] if Unknown else (
            palette["green"] if FromVoice else palette["dark_text"]
        )

        cursor = self._historyList.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(QColor(colour)))
        cursor.insertText(f"[{datetime.now():%H:%M:%S}] {Text}\n", fmt)
        self._historyList.setTextCursor(cursor)
        self._historyList.ensureCursorVisible()

    def SetCurrentText(self, Text: str) -> None:
        """Show the phrase currently being recognised."""
        self._currentText.setText(Text)

    def SetStatus(self, Status: str, Detail: str = "") -> None:
        """Update the microphone status banner.

        Args:
            Status: ``"active"``, ``"inactive"`` or ``"error"``.
            Detail: optional text shown instead of the default label.
        """
        labels = {
            "active": self._texts["mic_active"],
            "inactive": self._texts["mic_inactive"],
            "error": self._texts["mic_error"],
        }
        self._statusLabel.setText(Detail or labels.get(Status, Status))

    def SetTree(self, Objects: list[dict], DocumentName: str | None = None) -> None:
        """Rebuild the object tree.

        Args:
            Objects: dicts with ``name``, ``label``, ``type``, ``visible`` and
                optional ``parent``. Same contract the JSON bridge used, so the
                caller can switch to reading FreeCAD directly without touching
                this widget.
            DocumentName: shown as root item; a placeholder when None.
        """
        tree = self._treeWidget
        if tree is None:
            return

        tree.clear()
        self._treeItems = {}
        if not Objects:
            tree.addTopLevelItem(QTreeWidgetItem(["(sin documento abierto)"]))
            return

        root = QTreeWidgetItem([DocumentName or "Documento"])
        tree.addTopLevelItem(root)

        items: dict[str, QTreeWidgetItem] = {}
        self._treeItems = items
        for obj in Objects:
            label = obj.get("label") or obj.get("name") or "?"
            if not obj.get("visible", True):
                label = f"{label}  (oculto)"
            items[obj.get("name", label)] = QTreeWidgetItem([label])

        for obj in Objects:
            item = items.get(obj.get("name", ""))
            if item is None:
                continue
            parent = items.get(obj.get("parent") or "")
            (parent or root).addChild(item)

        tree.expandAll()

    def HighlightSelection(self, Names: list[str]) -> None:
        """Mirror FreeCAD's current selection in the panel tree.

        Called by the selection observer so that objects picked by voice
        (``ObjectSelection.SelectNext``) light up here too, not only in
        FreeCAD's own tree. Names that are not in the tree are ignored.

        Args:
            Names: FreeCAD object ``Name`` values that are currently selected.
        """
        tree = self._treeWidget
        if tree is None:
            return

        Wanted = set(Names or [])
        Current = None
        # blockSignals: setSelected dispara itemSelectionChanged, y si el panel
        # llegara a reenviar eso a FreeCAD se realimentaria en bucle.
        tree.blockSignals(True)
        try:
            for name, item in self._treeItems.items():
                Selected = name in Wanted
                item.setSelected(Selected)
                if Selected and Current is None:
                    Current = item
        finally:
            tree.blockSignals(False)

        if Current is not None:
            tree.scrollToItem(Current)

    def SetTheme(self, Theme: str) -> None:
        """Switch between the light and dark palettes."""
        self._theme = Theme
        self._palette = LIGHT if Theme == "light" else DARK
        self._ApplyStyles()
        self.RenderContext(self._context)

    def SetLanguage(self, Lang: str) -> None:
        """Switch the interface language."""
        self._lang = Lang
        self._texts = TEXTS.get(Lang, TEXTS["es"])
        self._listenLabel.setText(self._texts["section_listen"])
        self._histLabel.setText(self._texts["section_history"])
        self._modelLabel.setText(self._texts["section_model"])
        if hasattr(self, "_emptyHint") and self._emptyHint is not None:
            self._emptyHint.setText(self._texts["empty_context"])
        self._UpdateSectionTitle()

    def SetDockState(self, Floating: bool) -> None:
        """Reflect whether the panel is detached, on the dock/undock button.

        Called by whoever owns the dock, both after the button is pressed and
        when the user drags the title bar, so the icon never lies about the
        current state.

        Args:
            Floating: True when the panel is a separate window.
        """
        button = getattr(self, "_dockButton", None)
        if button is None:
            return
        button.setText("⧈" if Floating else "⧉")
        button.setToolTip(
            "Volver a unir a la ventana de FreeCAD" if Floating
            else "Separar de la ventana de FreeCAD"
        )

    def Flash(self) -> None:
        """Blink the overlay to acknowledge a recognised command."""
        self._flash.setGeometry(self.rect())
        self._flash.raise_()
        self._flash.Trigger()

    # ================================================================
    # Construccion de la UI
    # ================================================================

    def _BuildUi(self) -> None:
        palette = self._palette
        texts = self._texts

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 10, 14, 10)

        layout.addLayout(self._BuildHeader())

        self._statusLabel = QLabel(texts.get("status_idle", "Micrófono inactivo"))
        self._statusLabel.setFont(QFont(FONT_SANS, 13, QFont.Bold))
        self._statusLabel.setAlignment(Qt.AlignCenter)
        self._statusLabel.setFixedHeight(44)
        self._statusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self._statusLabel)

        self._listenLabel = QLabel(texts["section_listen"])
        self._listenLabel.setFont(QFont(FONT_SANS, 12, QFont.Bold))
        layout.addWidget(self._listenLabel)

        self._currentText = QTextEdit()
        self._currentText.setFixedHeight(46)
        self._currentText.setFont(QFont(FONT_MONO, 12, QFont.Bold))
        self._currentText.setReadOnly(True)
        layout.addWidget(self._currentText)

        tree_panel = QWidget()
        tree_panel.setLayout(self._BuildTreeColumn())
        hist_panel = QWidget()
        hist_panel.setLayout(self._BuildHistoryColumn())

        self._centerSplitter = QSplitter(Qt.Horizontal)
        self._centerSplitter.addWidget(tree_panel)
        self._centerSplitter.addWidget(hist_panel)
        self._centerSplitter.setStretchFactor(0, 1)
        self._centerSplitter.setStretchFactor(1, 2)
        self._centerSplitter.setChildrenCollapsible(False)
        layout.addWidget(self._centerSplitter, stretch=1)

        self._sectionTitleLabel = QLabel()
        self._sectionTitleLabel.setFont(QFont(FONT_SANS, 12, QFont.Bold))
        layout.addWidget(self._sectionTitleLabel)

        # Grilla, no fila: hay contextos de 47 entradas (Part) contra 5 de la
        # raiz. En una sola fila el ancho pedido crecia con la cantidad y
        # estiraba la ventana. La grilla envuelve y el scroll acota la altura,
        # asi el panel mide siempre lo mismo entre en el contexto que entre.
        self._toolArea = QWidget()
        self._toolArea.setObjectName("toolArea")
        self._toolArea.setAutoFillBackground(False)
        self._toolAreaLayout = QGridLayout(self._toolArea)
        self._toolAreaLayout.setSpacing(10)
        self._toolAreaLayout.setContentsMargins(10, 10, 10, 10)
        self._toolAreaLayout.setAlignment(Qt.AlignCenter)

        self._emptyHint = QLabel(self._texts["empty_context"], self._toolArea)
        self._emptyHint.setObjectName("emptyHintLabel")
        self._emptyHint.setAlignment(Qt.AlignCenter)
        self._emptyHint.setFont(QFont(FONT_SANS, 12))
        self._emptyHint.hide()

        self._toolScroll = QScrollArea()
        self._toolScroll.setObjectName("toolScroll")
        self._toolScroll.setWidget(self._toolArea)
        self._toolScroll.setWidgetResizable(True)
        self._toolScroll.setFrameShape(QFrame.NoFrame)
        self._toolScroll.setAutoFillBackground(False)
        if self._toolScroll.viewport() is not None:
            self._toolScroll.viewport().setAutoFillBackground(False)
        # Scroll horizontal: los botones se mantienen en filas de altura fija
        # y, si no entran a lo ancho, se corren en vez de empujar el borde de
        # la ventana. Asi el panel conserva el alto en cualquier contexto.
        self._toolScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._toolScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._toolScroll.setFixedHeight(
            self.TOOL_AREA_MAX_ROWS * (self.BUTTON_HEIGHT + 8) + 24
        )
        layout.addWidget(self._toolScroll)

        self._flash = FlashOverlay(self)
        self._flash.setGeometry(self.rect())

        self._ApplyStyles()

    def _BuildHeader(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(8)

        logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Logos", "color.svg")
        if os.path.exists(logo):
            widget = QSvgWidget(logo)
            widget.setFixedSize(40, 36)
            widget.setStyleSheet("background-color: transparent;")
            row.addWidget(widget)

        self._titleLabel = QLabel("ATRIA")
        self._titleLabel.setFont(QFont(FONT_SANS, 22, QFont.Bold))
        row.addWidget(self._titleLabel, stretch=1)

        self._dockButton = QPushButton("⧉")
        self._dockButton.setFixedSize(38, 34)
        self._dockButton.setFont(QFont(FONT_SANS, 15, QFont.Bold))
        self._dockButton.setToolTip("⧉ Desacoplar / Acoplar panel ATRIA\n(Permite flotar o fijar el panel en FreeCAD)")
        hand_cursor = getattr(Qt, "PointingHandCursor", None)
        if hand_cursor is not None:
            self._dockButton.setCursor(hand_cursor)
        self._dockButton.clicked.connect(self.DockToggleRequested.emit)
        row.addWidget(self._dockButton)

        self._prefsButton = QPushButton("⚙")
        self._prefsButton.setFixedSize(38, 34)
        self._prefsButton.setFont(QFont(FONT_SANS, 15, QFont.Bold))
        self._prefsButton.setToolTip(
            "⚙ Preferencias y Configuración de Voz\n"
            "🎤 Di: «preferencias»\n"
            "🖱️ O haz clic para abrir opciones"
        )
        if hand_cursor is not None:
            self._prefsButton.setCursor(hand_cursor)
        self._prefsButton.clicked.connect(self.PreferencesRequested.emit)
        row.addWidget(self._prefsButton)

        self._helpButton = QPushButton("?")
        self._helpButton.setFixedSize(38, 34)
        self._helpButton.setFont(QFont(FONT_SANS, 15, QFont.Bold))
        self._helpButton.setToolTip(
            "? Ayuda y Manual de la Sección\n"
            "🎤 Di: «ayuda» o «manual»\n"
            "🖱️ Abre una ventana emergente que explica cada botón de la sección\n"
            "🎤 Para cerrar di: «cerrar ayuda» o «cerrar»"
        )
        if hand_cursor is not None:
            self._helpButton.setCursor(hand_cursor)
        self._helpButton.clicked.connect(self.HelpRequested.emit)
        row.addWidget(self._helpButton)

        return row

    def _BuildTreeColumn(self) -> QVBoxLayout:
        column = QVBoxLayout()
        column.setSpacing(4)

        self._modelLabel = QLabel(self._texts["section_model"])
        self._modelLabel.setFont(QFont(FONT_SANS, 12, QFont.Bold))
        column.addWidget(self._modelLabel)

        self._treeWidget = QTreeWidget()
        self._treeWidget.setHeaderHidden(True)
        self._treeWidget.setMinimumHeight(70)
        self._treeWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        column.addWidget(self._treeWidget, stretch=1)

        self.SetTree([])
        return column

    def _BuildHistoryColumn(self) -> QVBoxLayout:
        column = QVBoxLayout()
        column.setSpacing(4)

        self._histLabel = QLabel(self._texts["section_history"])
        self._histLabel.setFont(QFont(FONT_SANS, 12, QFont.Bold))
        column.addWidget(self._histLabel)

        self._historyList = QTextEdit()
        self._historyList.setFont(QFont(FONT_MONO, 11, QFont.Bold))
        self._historyList.setReadOnly(True)
        self._historyList.setMinimumHeight(70)
        self._historyList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        column.addWidget(self._historyList, stretch=1)

        return column

    # ================================================================
    # Botones del contexto
    # ================================================================

    def _ClearToolArea(self) -> None:
        self._toolButtons.clear()
        if hasattr(self, "_emptyHint") and self._emptyHint is not None:
            self._emptyHint.hide()
            self._toolAreaLayout.removeWidget(self._emptyHint)
        while self._toolAreaLayout.count():
            item = self._toolAreaLayout.takeAt(0)
            widget = item.widget()
            if widget is not None and widget is not getattr(self, "_emptyHint", None):
                widget.hide()
                widget.setParent(None)
                widget.deleteLater()

    def _ShowEmptyHint(self) -> None:
        if hasattr(self, "_emptyHint") and self._emptyHint is not None:
            self._emptyHint.setText(self._texts["empty_context"])
            self._emptyHint.show()
            self._toolAreaLayout.addWidget(self._emptyHint, 0, 0, 1, 1, Qt.AlignCenter)

    def _MakeEntryButton(self, Entry) -> QToolButton:
        icon = self._locator.Find(Entry.InternalKey)
        if not icon and getattr(Entry, "Spoken", ""):
            icon = self._locator.Find(Entry.Spoken)

        is_sub = getattr(Entry, "IsSubContext", False)
        button = QToolButton()
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

        hand_cursor = getattr(Qt, "PointingHandCursor", None)
        if hand_cursor is not None:
            button.setCursor(hand_cursor)

        spoken_text = getattr(Entry, "Spoken", "") or getattr(Entry, "InternalKey", "")
        clean_name = spoken_text.replace("_", " ").strip().title()

        if is_sub:
            tooltip = (
                f"📂 Submenú: {clean_name}\n"
                f"🎤 Di «{spoken_text}»\n"
                f"🖱️ Clic para explorar herramientas"
            )
            button.setStyleSheet(self._SubmenuButtonQss())
        else:
            tooltip = (
                f"⚡ Herramienta: {clean_name}\n"
                f"🎤 Di «{spoken_text}»\n"
                f"🖱️ Clic para ejecutar"
            )
            button.setStyleSheet(self._ButtonQss())

        button.setToolTip(tooltip)

        if icon:
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
        else:
            # Fallback cuando no hay icono SVG
            prefix = "📁\n" if is_sub else ""
            button.setText(f"{prefix}{self._FormatButtonText(spoken_text)}")

        button.setText(self._FormatButtonText(spoken_text))
        button.setFont(QFont(FONT_SANS, 8, QFont.Bold))

        spoken = Entry.Spoken
        button.clicked.connect(lambda _checked=False, s=spoken: self._OnEntryClicked(s))
        return button

    def _MakeBackButton(self) -> QToolButton:
        button = QToolButton()
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        button.setToolTip(
            "⬅ Volver al nivel anterior\n"
            "🎤 Di: «volver» o «subir»\n"
            "🖱️ O haz clic para regresar"
        )
        button.setFont(QFont(FONT_SANS, 8, QFont.Bold))
        hand_cursor = getattr(Qt, "PointingHandCursor", None)
        if hand_cursor is not None:
            button.setCursor(hand_cursor)
        button.setStyleSheet(self._BackButtonQss())

        icon = self._locator.Find("selback")
        if icon:
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))

        back_text = self._BackPhrase().capitalize()
        button.setText(f"⬅ {back_text}")

        button.clicked.connect(lambda _checked=False: self._OnEntryClicked(self._BackPhrase()))
        return button

    def _MakeContextHelpButton(self) -> QToolButton:
        """Crea el botón de ayuda contextual situado al inicio, cerca del botón volver."""
        button = QToolButton()
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        button.setToolTip(
            "❓ Ayuda y Manual de la Sección\n"
            "🎤 Di: «ayuda» o «manual»\n"
            "🖱️ Haz clic para abrir la ventana de ayuda de esta sección\n"
            "🎤 Di: «cerrar ayuda» o «cerrar» para cerrarla"
        )
        button.setFont(QFont(FONT_SANS, 8, QFont.Bold))
        hand_cursor = getattr(Qt, "PointingHandCursor", None)
        if hand_cursor is not None:
            button.setCursor(hand_cursor)
        button.setStyleSheet(self._HelpButtonQss())

        icon = (
            self._locator.Find("help")
            or self._locator.Find("Help_WhatsThis")
            or self._locator.Find("manual")
            or self._locator.Find("ayuda")
        )
        if icon:
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))

        button.setText("❓ Ayuda")
        button.clicked.connect(lambda _checked=False: self._OnEntryClicked("ayuda"))
        return button

    def _FormatButtonText(self, spoken: str) -> str:
        """Formatea el comando de activación hablado para que quepa armoniosamente en el botón."""
        s = (spoken or "").strip().replace("_", " ")
        if not s:
            return ""

        short_overrides = {
            "3d": "3D",
            "2d": "2D",
            "bim": "BIM",
            "ifc": "IFC",
            "pdf": "PDF",
            "administracion": "Adminis-\ntración",
            "administración": "Adminis-\ntración",
            "barra de estado": "Barra\nEstado",
            "sistema de ejes": "Sistema\nEjes",
            "corte de sección": "Corte\nSección",
            "corte de seccion": "Corte\nSección",
            "plano de sección": "Plano\nSección",
            "plano de seccion": "Plano\nSección",
            "vista de sección": "Vista\nSección",
            "vista de seccion": "Vista\nSección",
            "crear muro cortina": "Muro\nCortina",
            "referencia externa": "Ref.\nExterna",
            "superficie desde caras": "Superficie\nCaras",
            "biblioteca de objetos": "Biblioteca\nObjetos",
            "convertir a croquis": "Convertir\nCroquis",
            "desplazar contorno plano": "Desplazar\nContorno",
            "repetir objetos a lo largo de una curva": "Repetir en\nCurva",
            "agregar al grupo de construcción": "Grupo\nConstruc.",
            "comprobar modelo bim": "Comprobar\nBIM",
            "editar estilos de anotación": "Estilos\nAnotación",
            "gestionar puertas y ventanas": "Puertas y\nVentanas",
            "gestionar elementos ifc": "Elementos\nIFC",
            "gestionar cantidades ifc": "Cantidades\nIFC",
            "configurar proyecto bim": "Proyecto\nBIM",
            "arco de 3 puntos": "Arco\n3 Puntos",
            "curva de bezier": "Curva\nBezier",
            "curva de bezier cúbica": "Bezier\nCúbica",
            "curva de bezier cubica": "Bezier\nCúbica",
            "idioma espanol": "Español",
            "idioma ingles": "Inglés",
            "unidades milimetros": "Milímetros",
            "unidades metros": "Metros",
            "unidades pulgadas": "Pulgadas",
            "mostrar panel": "Mostrar\nPanel",
            "ocultar panel": "Ocultar\nPanel",
            "centrar vista": "Centrar\nVista",
            "ajustar todo": "Ajustar\nTodo",
            "enfocar seleccion": "Enfocar\nSelec.",
            "enfocar selección": "Enfocar\nSelec.",
            "girar izquierda": "Girar\nIzq.",
            "girar derecha": "Girar\nDer.",
            "girar arriba": "Girar\nArriba",
            "girar abajo": "Girar\nAbajo",
            "mover camara": "Mover\nCámara",
            "mover cámara": "Mover\nCámara",
        }
        low = s.lower()
        if low in short_overrides:
            return short_overrides[low]

        words = s.split()
        if len(words) == 1:
            w = words[0].capitalize()
            if len(w) > 11:
                return w[:9] + "."
            return w
        elif len(words) == 2:
            return f"{words[0].capitalize()}\n{words[1].capitalize()}"
        elif len(words) == 3:
            if words[1].lower() in ("de", "a", "en", "y"):
                return f"{words[0].capitalize()}\n{words[2].capitalize()}"
            return f"{words[0].capitalize()} {words[1]}\n{words[2].capitalize()}"
        else:
            meaningful = [w for w in words if w.lower() not in ("de", "a", "en", "el", "la", "los", "las", "un", "una", "al", "del")]
            if len(meaningful) >= 2:
                return f"{meaningful[0].capitalize()}\n{meaningful[1].capitalize()}"
            return f"{words[0].capitalize()}\n{words[1].capitalize()}"

    def _BackPhrase(self) -> str:
        """Frase para subir un nivel segun el idioma activo (o fallback universal)."""
        lang = getattr(self, "_lang", "es")
        if str(lang).lower().startswith("en"):
            return "up"
        return self.BACK_PHRASE

    #: Frase que el Browser interpreta como "subir un nivel" (Atria/dictionary/NavCommands).
    BACK_PHRASE = "subir"

    @property
    def CurrentSectionTitle(self) -> str:
        """Titulo legible de la seccion activa de comandos."""
        return self._FormatSectionTitle()

    def _FormatSectionTitle(self) -> str:
        return format_section_title(self._context.ContextPath, self._lang)

    def _UpdateSectionTitle(self) -> None:
        if hasattr(self, "_sectionTitleLabel") and self._sectionTitleLabel is not None:
            self._sectionTitleLabel.setText(self._FormatSectionTitle())

    def _OnEntryClicked(self, Spoken: str) -> None:
        self.Flash()
        self.CommandRequested.emit(Spoken)

    # ================================================================
    # Estilos
    # ================================================================

    def _ApplyStyles(self) -> None:
        palette = self._palette
        self.setObjectName("AtriaPanel")
        self.setStyleSheet(
            f"QWidget#AtriaPanel {{ background-color: {palette['bg']} !important; }}"
            f"QWidget#AtriaPanel > * {{ background-color: transparent !important; }}"
            f"QScrollArea {{ background-color: transparent !important; border: none; }}"
            f"QScrollArea > QWidget {{ background-color: transparent !important; }}"
            f"QWidget#toolArea {{ background-color: transparent !important; }}"
            f"QLabel {{ background-color: transparent !important; }}"
        )
        if hasattr(self, "_toolScroll") and self._toolScroll is not None:
            self._toolScroll.setStyleSheet("background-color: transparent !important; border: none;")
            if self._toolScroll.viewport() is not None:
                self._toolScroll.viewport().setAutoFillBackground(False)
                self._toolScroll.viewport().setStyleSheet("background-color: transparent !important;")
        if hasattr(self, "_toolArea") and self._toolArea is not None:
            self._toolArea.setAutoFillBackground(False)
            self._toolArea.setStyleSheet("background-color: transparent !important;")
        if hasattr(self, "_emptyHint") and self._emptyHint is not None:
            self._emptyHint.setStyleSheet(
                f"color: {palette['dark_text']}; background-color: transparent !important;"
            )
        self._titleLabel.setStyleSheet(
            f"color: {palette['black']}; background-color: transparent !important;"
            f" font-size: 22pt; font-weight: bold;"
        )
        self._statusLabel.setStyleSheet(self._StatusQss())
        self._currentText.setStyleSheet(self._TextPanelQss(palette["dark_text"], 12))
        self._historyList.setStyleSheet(self._TextPanelQss(palette["green"], 11))

        if hasattr(self, "_centerSplitter") and self._centerSplitter is not None:
            self._centerSplitter.setStyleSheet(
                f"QSplitter::handle {{ background-color: {palette['panel_border']}; width: 2px; }}"
                f"QSplitter::handle:hover {{ background-color: #3b82f6; }}"
            )

        section_label = getattr(self, "_sectionTitleLabel", None)
        labels = [self._listenLabel, self._histLabel, self._modelLabel]
        if section_label is not None:
            labels.append(section_label)

        for label in labels:
            label.setStyleSheet(
                f"color: {palette['black']}; background-color: transparent !important;"
                f" font-size: 12pt; font-weight: bold;"
            )

        for button in (
            self._helpButton,
            self._prefsButton,
            self._dockButton,
        ):
            button.setStyleSheet(self._HeaderButtonQss())

        if self._treeWidget is not None:
            self._treeWidget.setStyleSheet(self._TreeQss())

    def _StatusQss(self) -> str:
        palette = self._palette
        return (
            f"QLabel {{ background-color: transparent !important;"
            f" border-top: 1.5px solid {palette['mic_border']};"
            f" border-bottom: 1.5px solid {palette['mic_border']};"
            f" padding: 8px; color: {palette['dark_text']};"
            f" font-family: {FONT_SANS}; font-size: 13px; font-weight: 700; }}"
        )

    def _TextPanelQss(self, Colour: str, Size: int) -> str:
        palette = self._palette
        return (
            f"QTextEdit {{ background-color: {palette['panel']} !important; color: {Colour};"
            f" border: 1.5px solid {palette['panel_border']}; border-radius: 0px;"
            f" padding: 10px; font-family: {FONT_MONO}; font-size: {Size}px;"
            f" font-weight: 600; }}"
        )

    def _TreeQss(self) -> str:
        palette = self._palette
        return (
            f"QTreeWidget {{ background-color: {palette['panel']} !important;"
            f" color: {palette['dark_text']};"
            f" border: 1.5px solid {palette['panel_border']};"
            f" padding: 6px; font-family: {FONT_MONO}; font-size: 11px; }}"
            f"QTreeWidget::item {{ padding: 2px; }}"
        )

    def _ButtonQss(self) -> str:
        palette = self._palette
        return (
            f"QToolButton, QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {palette['btn_top']}, stop:1 {palette['btn_bot']}) !important;"
            f" border: 1.5px solid {palette['btn_border']}; border-radius: 8px;"
            f" color: {palette['dark_text']}; font-family: {FONT_SANS};"
            f" font-size: 8.5pt; font-weight: bold; text-align: center;"
            f" padding: 2px 2px 3px 2px; }}"
            f"QToolButton:hover, QPushButton:hover {{ background: {palette['btn_hover']} !important; border-color: #3b82f6; }}"
            f"QToolButton:pressed, QPushButton:pressed {{ background: {palette['highlight']} !important; border-color: #2563eb; }}"
        )

    def _SubmenuButtonQss(self) -> str:
        palette = self._palette
        bg_val = str(palette.get("bg", "#")).lower()
        is_dark = bg_val.startswith("#1") or bg_val.startswith("#2")
        if is_dark:
            top = "#203a5e"
            bot = "#162842"
            border = "#3b82f6"
            hover = "#2563eb"
            text_color = "#ffffff"
        else:
            top = "#ebf3fe"
            bot = "#dceafc"
            border = "#3b82f6"
            hover = "#bfdbfe"
            text_color = "#1e3a8a"

        return (
            f"QToolButton, QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {top}, stop:1 {bot}) !important;"
            f" border: 2px solid {border}; border-radius: 8px;"
            f" color: {text_color}; font-family: {FONT_SANS};"
            f" font-size: 8.5pt; font-weight: bold; text-align: center;"
            f" padding: 2px 2px 3px 2px; }}"
            f"QToolButton:hover, QPushButton:hover {{ background: {hover} !important; border-color: #2563eb; }}"
            f"QToolButton:pressed, QPushButton:pressed {{ background: {hover} !important; }}"
        )

    def _BackButtonQss(self) -> str:
        palette = self._palette
        bg_val = str(palette.get("bg", "#")).lower()
        is_dark = bg_val.startswith("#1") or bg_val.startswith("#2")
        border = "#f59e0b" if is_dark else "#d97706"
        top = "#3d2b12" if is_dark else "#fef3c7"
        bot = "#291c0a" if is_dark else "#fde68a"
        hover = "#f59e0b" if is_dark else "#fcd34d"
        text = "#ffffff" if is_dark else "#78350f"

        return (
            f"QToolButton, QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {top}, stop:1 {bot}) !important;"
            f" border: 2px solid {border}; border-radius: 8px;"
            f" color: {text}; font-family: {FONT_SANS};"
            f" font-size: 8.5pt; font-weight: bold; text-align: center;"
            f" padding: 2px 2px 3px 2px; }}"
            f"QToolButton:hover, QPushButton:hover {{ background: {hover} !important; border-color: #d97706; }}"
            f"QToolButton:pressed, QPushButton:pressed {{ background: {border} !important; }}"
        )

    def _HelpButtonQss(self) -> str:
        palette = self._palette
        bg_val = str(palette.get("bg", "#")).lower()
        is_dark = bg_val.startswith("#1") or bg_val.startswith("#2") or getattr(self, "_theme", "light") == "dark"

        if is_dark:
            border = "#00a896"
            top = "#0e3838"
            bot = "#092323"
            hover = "#00828a"
            text = "#72efdd"
        else:
            border = "#00828a"
            top = "#e6f7f7"
            bot = "#ccefed"
            hover = "#99dfdc"
            text = "#005055"

        return (
            f"QToolButton, QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {top}, stop:1 {bot}) !important;"
            f" border: 2px solid {border}; border-radius: 8px;"
            f" color: {text}; font-family: {FONT_SANS};"
            f" font-size: 8.5pt; font-weight: bold; text-align: center;"
            f" padding: 2px 2px 3px 2px; }}"
            f"QToolButton:hover, QPushButton:hover {{ background: {hover} !important; border-color: {border}; }}"
            f"QToolButton:pressed, QPushButton:pressed {{ background: {border} !important; }}"
        )

    def _HeaderButtonQss(self) -> str:
        palette = self._palette
        return (
            f"QPushButton {{"
            f" background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {palette['btn_top']}, stop:1 {palette['btn_bot']}) !important;"
            f" border: 1.5px solid {palette['btn_border']}; border-radius: 6px;"
            f" color: {palette['black']}; font-family: {FONT_SANS};"
            f" font-size: 14px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: {palette['btn_hover']} !important; border-color: #3b82f6; }}"
            f"QPushButton:pressed {{ background: {palette['highlight']} !important; }}"
        )

    def resizeEvent(self, Event) -> None:  # noqa: N802 (API de Qt)
        super().resizeEvent(Event)
        self._flash.setGeometry(self.rect())
        # Al cambiar el ancho cambia cuantos botones entran por fila. Se
        # redibuja solo si el numero de columnas cambio, para no rehacer la
        # grilla en cada pixel del arrastre.
        if not self._context.IsEmpty():
            total = len(self._toolButtons)
            if self._RowCount(total) != self._lastColumns:
                self.RenderContext(self._context)

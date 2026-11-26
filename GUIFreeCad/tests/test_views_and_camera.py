# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

"""Tests para la sección Vistas y Cámara (perspectiva, vistas estándar, zoom, rotación y navegación)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

GUI_ROOT = Path(__file__).resolve().parents[1]
ATRIA_DIR = GUI_ROOT.parent

if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(ATRIA_DIR) not in sys.path:
    sys.path.insert(0, str(ATRIA_DIR))

from GUIFreeCad.core.language_code import LanguageCode
from GUIFreeCad.core.preferences import Preferences
from GUIFreeCad.navigation.browser import Browser
from GUIFreeCad.ui.HelpContent import get_help_for_category
from GUIFreeCad.ui.IconLocator import IconLocator
from GUIFreeCad.ui.Textos import format_section_title
from dictionary.Views import commands
from dictionary.Views.Views import Views
from dictionary.Views.TraduceToEn import TraduceToEn
from dictionary.Views.TraduceToEs import TraduceToEs


class TestViewsAndCameraModule(unittest.TestCase):
    """Verifica que los comandos y diccionarios de Views estén completos y funcionales."""

    def test_commands_callable_without_gui(self) -> None:
        """Los comandos de cámara deben ejecutarse de forma segura sin interfaz gráfica."""
        commands.perspective()
        commands.orthographic()
        commands.isometric()
        commands.dimetric()
        commands.trimetric()
        commands.front()
        commands.top()
        commands.right()
        commands.left()
        commands.rear()
        commands.bottom()
        commands.fit_all()
        commands.fit_selection()
        commands.zoom_in()
        commands.zoom_out()
        commands.rotate_left()
        commands.rotate_right()
        commands.rotate_up()
        commands.rotate_down()

    def test_views_dictionary_contains_all_actions(self) -> None:
        required_keys = [
            "perspective", "orthographic", "isometric", "dimetric", "trimetric",
            "front", "top", "right", "left", "rear", "bottom", "fitall",
            "fitselection", "zoomin", "zoomout", "rotateleft", "rotateright",
            "rotateup", "rotatedown", "movecamera", "help",
        ]
        for key in required_keys:
            self.assertIn(key, Views, f"Falta clave {key} en Views dictionary")
            self.assertIsNotNone(Views[key], f"La clave {key} en Views no puede ser None")

    def test_traduce_to_es_mappings(self) -> None:
        self.assertIn("perspectiva", TraduceToEs)
        self.assertIn("ortogonal", TraduceToEs)
        self.assertIn("isometrica", TraduceToEs)
        self.assertIn("isométrica", TraduceToEs)
        self.assertIn("isometrico", TraduceToEs)
        self.assertIn("isométrico", TraduceToEs)
        self.assertIn("iso", TraduceToEs)
        self.assertIn("vista isometrica", TraduceToEs)
        self.assertIn("vista isométrica", TraduceToEs)
        self.assertIn("dimetrica", TraduceToEs)
        self.assertIn("trimetrica", TraduceToEs)
        self.assertIn("frontal", TraduceToEs)
        self.assertIn("superior", TraduceToEs)
        self.assertIn("planta", TraduceToEs)
        self.assertIn("derecha", TraduceToEs)
        self.assertIn("izquierda", TraduceToEs)
        self.assertIn("trasera", TraduceToEs)
        self.assertIn("inferior", TraduceToEs)
        self.assertIn("centrar vista", TraduceToEs)
        self.assertIn("enfocar seleccion", TraduceToEs)
        self.assertIn("acercar", TraduceToEs)
        self.assertIn("alejar", TraduceToEs)
        self.assertIn("girar izquierda", TraduceToEs)
        self.assertIn("girar derecha", TraduceToEs)
        self.assertIn("mover camara", TraduceToEs)

    def test_traduce_to_en_mappings(self) -> None:
        self.assertIn("perspective", TraduceToEn)
        self.assertIn("orthographic", TraduceToEn)
        self.assertIn("isometric", TraduceToEn)
        self.assertIn("iso", TraduceToEn)
        self.assertIn("dimetric", TraduceToEn)
        self.assertIn("trimetric", TraduceToEn)
        self.assertIn("front", TraduceToEn)
        self.assertIn("top", TraduceToEn)
        self.assertIn("right", TraduceToEn)
        self.assertIn("left", TraduceToEn)
        self.assertIn("rear", TraduceToEn)
        self.assertIn("bottom", TraduceToEn)
        self.assertIn("fit all", TraduceToEn)
        self.assertIn("fit selection", TraduceToEn)
        self.assertIn("zoom in", TraduceToEn)
        self.assertIn("zoom out", TraduceToEn)
        self.assertIn("rotate left", TraduceToEn)
        self.assertIn("rotate right", TraduceToEn)
        self.assertIn("move camera", TraduceToEn)

    def test_help_content_views_category(self) -> None:
        title, items, text = get_help_for_category("Views")
        self.assertIn("Vistas", title)
        self.assertGreaterEqual(len(items), 15)
        cmds = [cmd for cmd, _ in items]
        self.assertIn("perspectiva", cmds)
        self.assertIn("ortogonal", cmds)
        self.assertIn("isometrica", cmds)
        self.assertIn("centrar vista", cmds)
        self.assertIn("girar izquierda", cmds)

    def test_icon_locator_resolves_view_icons(self) -> None:
        loc = IconLocator()
        for key in ["views", "perspective", "orthographic", "isometric", "front", "top", "fitall", "zoomin", "zoomout", "rotateleft"]:
            icon = loc.Find(key)
            self.assertTrue(len(icon) > 0, f"No se encontró icono SVG para {key}")
            self.assertTrue(icon.endswith(".svg"), f"Icono para {key} no termina en .svg")

    def test_section_title_views(self) -> None:
        title_es = format_section_title("Base > Views", "es")
        self.assertEqual(title_es, "Sección: Vistas y Cámara")

        title_en = format_section_title("Base > Views", "en")
        self.assertEqual(title_en, "Section: Views & Camera")


class TestGlobalCameraVoiceCommands(unittest.TestCase):
    """Verifica que comandos de cámara puedan ejecutarse globalmente desde cualquier contexto."""

    def test_camera_commands_accessible_from_real_base(self) -> None:
        dic_root = ATRIA_DIR / "dictionary"
        prefs = Preferences()
        prefs.SetLanguage = LanguageCode.Es
        browser = Browser(dictionary_root=dic_root, prefs=prefs)
        # En Base, decir 'vistas' debe entrar a Views
        res_vistas = browser.ProcessPhrase("vistas")
        self.assertTrue(res_vistas.Success)
        self.assertIn("views", browser.ContextPath.lower())

        # Dentro de Views, decir 'perspectiva'
        res_persp = browser.ProcessPhrase("perspectiva")
        self.assertTrue(res_persp.Success)
        self.assertEqual(res_persp.Action, "execute")

        # Decir 'isometrica'
        res_iso = browser.ProcessPhrase("isometrica")
        self.assertTrue(res_iso.Success)
        self.assertEqual(res_iso.Action, "execute")

        # Subir de nuevo a Base
        res_up = browser.ProcessPhrase("subir")
        self.assertTrue(res_up.Success)
        self.assertEqual(browser.ContextPath, "Base")

    def test_camera_and_views_from_inside_bim_context(self) -> None:
        """Verifica que desde dentro de 3D-BIM las vistas estándar e isométrica se detecten y ejecuten por búsqueda ascendente."""
        dic_root = ATRIA_DIR / "dictionary"
        prefs = Preferences()
        prefs.SetLanguage = LanguageCode.Es
        browser = Browser(dictionary_root=dic_root, prefs=prefs)
        # Entrar a 3D-BIM
        res_bim = browser.ProcessPhrase("bim")
        self.assertTrue(res_bim.Success)
        self.assertIn("bim", browser.ContextPath.lower())

        # Probar isométrica y variantes desde dentro de BIM
        for phrase in ["isometrica", "isométrica", "isométrico", "iso", "vista isométrica", "vista isometrica"]:
            res = browser.ProcessPhrase(phrase)
            self.assertTrue(res.Success, f"Falló comando '{phrase}' en contexto BIM")
            self.assertEqual(res.Action, "execute")
            # El contexto debe mantenerse en BIM tras la búsqueda ascendente
            self.assertIn("bim", browser.ContextPath.lower())

        # Probar vistas ortogonales y encuadre desde dentro de BIM
        for phrase in ["frontal", "superior", "planta", "derecha", "izquierda", "trasera", "inferior", "centrar vista", "enfocar seleccion"]:
            res = browser.ProcessPhrase(phrase)
            self.assertTrue(res.Success, f"Falló comando '{phrase}' en contexto BIM")
            self.assertEqual(res.Action, "execute")
            self.assertIn("bim", browser.ContextPath.lower())

    def test_views_commands_invoke_view_api(self) -> None:
        """Verifica que los comandos de Views invoquen la API directa de la vista activa y llamen a redraw."""
        mock_view = MagicMock()
        mock_gui = MagicMock()
        mock_gui.ActiveDocument.ActiveView = mock_view
        commands.Gui = mock_gui

        commands.isometric()
        mock_view.viewIsometric.assert_called_once()
        mock_view.redraw.assert_called_once()

        mock_view.reset_mock()
        commands.dimetric()
        mock_view.viewDimetric.assert_called_once()
        mock_view.redraw.assert_called_once()

        mock_view.reset_mock()
        commands.trimetric()
        mock_view.viewTrimetric.assert_called_once()
        mock_view.redraw.assert_called_once()

        mock_view.reset_mock()
        commands.front()
        mock_view.viewFront.assert_called_once()
        mock_view.redraw.assert_called_once()

        mock_view.reset_mock()
        commands.top()
        mock_view.viewTop.assert_called_once()

        mock_view.reset_mock()
        commands.fit_all()
        mock_view.fitAll.assert_called_once()

        mock_view.reset_mock()
        commands.fit_selection()
        mock_view.fitSelection.assert_called_once()

        mock_view.reset_mock()
        commands.perspective()
        mock_view.setCameraType.assert_called_once_with("Perspective")

        mock_view.reset_mock()
        commands.orthographic()
        mock_view.setCameraType.assert_called_once_with("Orthographic")


if __name__ == "__main__":
    unittest.main()

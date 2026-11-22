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
            "perspective", "orthographic", "isometric", "front", "top",
            "right", "left", "rear", "bottom", "fitall", "fitselection",
            "zoomin", "zoomout", "rotateleft", "rotateright", "rotateup",
            "rotatedown", "movecamera", "help",
        ]
        for key in required_keys:
            self.assertIn(key, Views, f"Falta clave {key} en Views dictionary")
            self.assertIsNotNone(Views[key], f"La clave {key} en Views no puede ser None")

    def test_traduce_to_es_mappings(self) -> None:
        self.assertIn("perspectiva", TraduceToEs)
        self.assertIn("ortogonal", TraduceToEs)
        self.assertIn("isometrica", TraduceToEs)
        self.assertIn("frontal", TraduceToEs)
        self.assertIn("superior", TraduceToEs)
        self.assertIn("centrar vista", TraduceToEs)
        self.assertIn("acercar", TraduceToEs)
        self.assertIn("alejar", TraduceToEs)
        self.assertIn("girar izquierda", TraduceToEs)
        self.assertIn("girar derecha", TraduceToEs)
        self.assertIn("mover camara", TraduceToEs)

    def test_traduce_to_en_mappings(self) -> None:
        self.assertIn("perspective", TraduceToEn)
        self.assertIn("orthographic", TraduceToEn)
        self.assertIn("isometric", TraduceToEn)
        self.assertIn("front", TraduceToEn)
        self.assertIn("top", TraduceToEn)
        self.assertIn("fit all", TraduceToEn)
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
        self.assertEqual(title_es, "📍 Sección: Vistas y Cámara")

        title_en = format_section_title("Base > Views", "en")
        self.assertEqual(title_en, "📍 Section: Views & Camera")


class TestGlobalCameraVoiceCommands(unittest.TestCase):
    """Verifica que comandos de cámara puedan ejecutarse globalmente desde cualquier contexto."""

    def test_camera_commands_accessible_from_real_base(self) -> None:
        dic_root = ATRIA_DIR / "dictionary"
        browser = Browser(dictionary_root=dic_root)
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


if __name__ == "__main__":
    unittest.main()

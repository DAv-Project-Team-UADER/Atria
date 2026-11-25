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

"""Unit tests verifying 100% SVG icon coverage across target categories."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "dictionary") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "dictionary"))

from GUIFreeCad.core.language_code import LanguageCode
from GUIFreeCad.navigation.browser import Browser
from GUIFreeCad.ui.IconLocator import IconLocator


class TestIconLocatorCoverage(unittest.TestCase):
    """Ensure every command button has a valid SVG icon resolved."""

    TARGET_CATEGORIES = [
        ("3D-BIM", "3D-BIM"),
        ("2D-Drafting", "2D-Drafting"),
        ("Annotation", "Anotacion"),
        ("Manage", "Administración"),
        ("Modify", "Modificar"),
        ("Preferences", "Preferencias"),
        ("Snapping", "Enganche"),
        ("StatusBar", "Barra de enganche"),
        ("Utils", "Utilidades"),
        ("Explorer", "Explorador"),
    ]

    def setUp(self) -> None:
        self.locator = IconLocator()
        self.dict_root = REPO_ROOT / "dictionary"

    def test_locator_indexes_icons(self) -> None:
        index = self.locator._BuildIndex()
        self.assertGreater(len(index), 500, "Expected over 500 indexed icons")

    def test_target_categories_have_complete_icons_spanish(self) -> None:
        self._check_categories_for_language(LanguageCode.Es)

    def test_target_categories_have_complete_icons_english(self) -> None:
        self._check_categories_for_language(LanguageCode.En)

    def _check_categories_for_language(self, lang: LanguageCode) -> None:
        for cat_name, label in self.TARGET_CATEGORIES:
            with self.subTest(category=cat_name, lang=lang.value):
                browser = Browser(dictionary_root=self.dict_root)
                browser.SetLanguage = lang
                entry = next(
                    (e for e in browser.BaseContext if e.InternalKey.lower() == cat_name.lower()),
                    None,
                )
                self.assertIsNotNone(entry, f"Base entry not found for category {cat_name}")
                descended = browser._DescendToSubContext(entry)
                self.assertTrue(descended, f"Could not descend into category {cat_name}")

                missing = []
                for item in browser.Context:
                    icon = self.locator.Find(item.InternalKey)
                    if not icon and item.Spoken:
                        icon = self.locator.Find(item.Spoken)
                    if not icon:
                        missing.append(f"Key='{item.InternalKey}', Spoken='{item.Spoken}'")

                self.assertEqual(
                    missing,
                    [],
                    f"Category {cat_name} ({label}) has {len(missing)} entries without an SVG icon: {missing[:5]}",
                )


if __name__ == "__main__":
    unittest.main()

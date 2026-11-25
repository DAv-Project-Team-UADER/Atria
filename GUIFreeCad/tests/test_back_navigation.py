# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

"""Tests for back/ascend button and navigation across all ATRIA categories."""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
ATRIA_DIR = GUI_ROOT.parent
DIC_ROOT = ATRIA_DIR / "dictionary"

if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(ATRIA_DIR) not in sys.path:
    sys.path.insert(0, str(ATRIA_DIR))
if str(DIC_ROOT) not in sys.path:
    sys.path.insert(0, str(DIC_ROOT))


def _install_stubs() -> None:
    if "FreeCADGui" not in sys.modules:
        gui = types.ModuleType("FreeCADGui")
        gui.runCommand = lambda name, idx=0: None  # type: ignore[attr-defined]
        sys.modules["FreeCADGui"] = gui
    if "FreeCAD" not in sys.modules:
        sys.modules["FreeCAD"] = types.ModuleType("FreeCAD")
    app = sys.modules["FreeCAD"]
    if not hasattr(app, "ActiveDocument"):
        app.ActiveDocument = None
    class Vector:
        def __init__(self, *args, **kwargs): pass
    class Placement:
        def __init__(self, *args, **kwargs): pass
    class Rotation:
        def __init__(self, *args, **kwargs): pass
    class Matrix:
        def __init__(self, *args, **kwargs): pass
    for attr, cls in [("Vector", Vector), ("Placement", Placement), ("Rotation", Rotation), ("Matrix", Matrix)]:
        if not hasattr(app, attr):
            setattr(app, attr, cls)
    for mod in ("Part", "PartDesign", "Sketcher", "Draft", "TechDraw", "Assembly", "Mesh", "Fem"):
        if mod not in sys.modules:
            sys.modules[mod] = types.ModuleType(mod)
    if "integration.launch_preferences" not in sys.modules:
        preferences = types.ModuleType("integration.launch_preferences")
        preferences.open_preferences = lambda: None  # type: ignore[attr-defined]
        sys.modules["integration.launch_preferences"] = preferences


class TestBackNavigationAllCategories(unittest.TestCase):
    """Verifies that every category and subcategory can ascend cleanly."""

    @classmethod
    def setUpClass(cls) -> None:
        _install_stubs()

    def test_universal_nav_fallback_in_browser(self) -> None:
        """Universal navigation words must work in any language."""
        from navigation.browser import Browser

        b = Browser(dictionary_root=DIC_ROOT)
        b._prefs.SetLanguage = "en"
        b.ResetFromBase()

        # Enter 3D-BIM
        res_enter = b.ProcessPhrase("three d")
        self.assertTrue(res_enter.Success)
        self.assertIn("3D-BIM", b.ContextPath)

        # 'subir' in English should still ascend via universal fallback
        res_back = b.ProcessPhrase("subir")
        self.assertTrue(res_back.Success)
        self.assertEqual(res_back.Action, "back")
        self.assertEqual(b.ContextPath, "Base")

        # 'volver' in English should also ascend
        b.ProcessPhrase("three d")
        res_volver = b.ProcessPhrase("volver")
        self.assertTrue(res_volver.Success)
        self.assertEqual(res_volver.Action, "back")
        self.assertEqual(b.ContextPath, "Base")

        # 'up' and 'back' in Spanish should ascend
        b._prefs.SetLanguage = "es"
        b.ResetFromBase()
        b.ProcessPhrase("3d")
        res_up = b.ProcessPhrase("up")
        self.assertTrue(res_up.Success)
        self.assertEqual(res_up.Action, "back")
        self.assertEqual(b.ContextPath, "Base")

        b.ProcessPhrase("3d")
        res_b = b.ProcessPhrase("back")
        self.assertTrue(res_b.Success)
        self.assertEqual(res_b.Action, "back")
        self.assertEqual(b.ContextPath, "Base")

    def test_ascend_from_every_category(self) -> None:
        """Every subcontext in Base must descend and cleanly ascend back to Base."""
        from navigation.browser import Browser

        b = Browser(dictionary_root=DIC_ROOT)
        b._prefs.SetLanguage = "es"
        b.ResetFromBase()

        base_subs = [e for e in b.Context if e.IsSubContext()]
        seen_targets = []
        unique_subs = []
        for s in base_subs:
            if not any(b.IsSameTarget(s.Target, t) for t in seen_targets):
                seen_targets.append(s.Target)
                unique_subs.append(s)

        # Must have all main categories (3D-BIM, 2D-Drafting, Annotation, etc.)
        self.assertGreaterEqual(len(unique_subs), 8)

        for sub in unique_subs:
            spoken = sub.Spoken
            key = sub.InternalKey
            with self.subTest(category=key, spoken=spoken):
                # Descend
                res_desc = b.ProcessPhrase(spoken)
                self.assertTrue(res_desc.Success, f"Failed to descend to {key} with '{spoken}'")
                self.assertTrue(b._IsDescended())
                self.assertEqual(b.CurrentContextName, key)

                # Ascend with 'subir'
                res_asc = b.ProcessPhrase("subir")
                self.assertTrue(res_asc.Success, f"Failed to ascend from {key} with 'subir'")
                self.assertEqual(res_asc.Action, "back")
                self.assertEqual(b.ContextPath, "Base")

    def test_ascend_from_nested_explorer_subcontexts(self) -> None:
        """Explorer has multi-level subcontexts (file, edit, print...). All must ascend."""
        from navigation.browser import Browser

        b = Browser(dictionary_root=DIC_ROOT)
        b._prefs.SetLanguage = "es"
        b.ResetFromBase()

        # Descend to Explorer
        res_exp = b.ProcessPhrase("explorador")
        self.assertTrue(res_exp.Success)
        self.assertEqual(b.ContextPath, "Base > Explorer")

        # Descend into 'archivo'
        res_file = b.ProcessPhrase("archivo")
        self.assertTrue(res_file.Success)
        self.assertEqual(b.ContextPath, "Base > Explorer > file")

        # Ascend one level -> back to Explorer
        res_up1 = b.ProcessPhrase("subir")
        self.assertTrue(res_up1.Success)
        self.assertEqual(res_up1.Action, "back")
        self.assertEqual(b.ContextPath, "Base > Explorer")

        # Ascend again -> back to Base
        res_up2 = b.ProcessPhrase("subir")
        self.assertTrue(res_up2.Success)
        self.assertEqual(res_up2.Action, "back")
        self.assertEqual(b.ContextPath, "Base")


class TestAtriaPanelBackButtonPlacement(unittest.TestCase):
    """Verifies that the back button is at index 0 and has correct signal connections."""

    def test_back_button_first_position_and_signal(self) -> None:
        """If Context is not root, back button must be first (index 0)."""
        try:
            from PySide6.QtWidgets import QApplication
            from ui.AtriaPanel import AtriaPanel
            app = QApplication.instance() or QApplication([])
        except ImportError:
            self.skipTest("PySide6 not available in test runner")

        from ui.ContextView import ContextEntryView, ContextView

        view = ContextView(
            "Base > 3D-BIM",
            [],
            [ContextEntryView("muro", "wall"), ContextEntryView("columna", "column")]
        )
        self.assertFalse(view.IsRoot())

        panel = AtriaPanel()
        panel.RenderContext(view)

        # Back button must be at index 0 in toolButtons and display back command
        self.assertGreaterEqual(len(panel._toolButtons), 1)
        first_button = panel._toolButtons[0]
        self.assertIn("⬅", first_button.text())
        self.assertIn("subir", first_button.text().lower())

        # Test clicking the back button
        emitted_commands = []
        panel.CommandRequested.connect(emitted_commands.append)
        # Calling click() emits clicked(bool)
        first_button.click()
        self.assertEqual(emitted_commands, ["subir"])

        # Test in English
        panel.SetLanguage("en")
        first_button_en = panel._MakeBackButton()
        self.assertIn("⬅", first_button_en.text())
        self.assertIn("up", first_button_en.text().lower())
        emitted_commands.clear()
        panel.CommandRequested.connect(emitted_commands.append)
        first_button_en.click()
        self.assertEqual(emitted_commands, ["up"])


if __name__ == "__main__":
    unittest.main()

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

"""Comprehensive test suite for ATRIA modular dictionaries and voice navigation."""

from __future__ import annotations

import importlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))

from integration.atria_paths import atria_repo_root, ensure_atria_repo_on_path  # noqa: E402

ensure_atria_repo_on_path()
ATRIA_DIR = atria_repo_root()
DIC_ROOT = ATRIA_DIR / "dictionary"
if str(DIC_ROOT) not in sys.path:
    sys.path.insert(0, str(DIC_ROOT))


def _install_full_stubs() -> types.ModuleType:
    if "FreeCADGui" not in sys.modules:
        gui = types.ModuleType("FreeCADGui")
        gui.calls = []
        gui.runCommand = lambda name, idx=0: gui.calls.append(("run", name))
        gui.Selection = types.SimpleNamespace(getSelection=lambda: [], getSelectionEx=lambda: [])
        gui.activeView = lambda: types.SimpleNamespace(getSceneGraph=lambda: None)
        gui.ActiveDocument = types.SimpleNamespace()
        gui.getMainWindow = lambda: None
        sys.modules["FreeCADGui"] = gui
    else:
        gui = sys.modules["FreeCADGui"]
        if not hasattr(gui, "calls"):
            gui.calls = []
            gui.runCommand = lambda name, idx=0: gui.calls.append(("run", name))

    if "FreeCAD" not in sys.modules:
        app = types.ModuleType("FreeCAD")
        app.ActiveDocument = types.SimpleNamespace(
            recompute=lambda: None,
            getObject=lambda name: None,
            addObject=lambda kind, name: types.SimpleNamespace(Name=name, Label=name),
        )
        sys.modules["FreeCAD"] = app
    else:
        app = sys.modules["FreeCAD"]
        if not hasattr(app, "ActiveDocument") or app.ActiveDocument is None:
            app.ActiveDocument = types.SimpleNamespace(
                recompute=lambda: None,
                getObject=lambda name: None,
                addObject=lambda kind, name: types.SimpleNamespace(Name=name, Label=name),
            )

    arch = sys.modules.get("Arch") or types.ModuleType("Arch")
    arch.makeBuilding = lambda *a, **k: types.SimpleNamespace(Label="Building")
    arch.makeSite = lambda *a, **k: types.SimpleNamespace(Label="Site")
    arch.makeFloor = lambda *a, **k: types.SimpleNamespace(Label="Level")
    arch.makePipe = lambda *a, **k: types.SimpleNamespace(Label="Pipe")
    arch.makePipeConnector = lambda *a, **k: types.SimpleNamespace(Label="PipeConnector")
    arch.makeStairs = lambda *a, **k: types.SimpleNamespace(Label="Stairs")
    sys.modules["Arch"] = arch

    draft = sys.modules.get("Draft") or types.ModuleType("Draft")
    draft.autogroup = lambda *a, **k: None
    draft.getType = lambda *a, **k: "Structure"
    sys.modules["Draft"] = draft

    wp = sys.modules.get("WorkingPlane") or types.ModuleType("WorkingPlane")
    wp.get_working_plane = lambda: types.SimpleNamespace(get_placement=lambda: None)
    sys.modules["WorkingPlane"] = wp

    for mod in ("Part", "BIM", "DraftVecUtils", "Show"):
        if mod not in sys.modules:
            sys.modules[mod] = types.ModuleType(mod)

    return sys.modules["FreeCADGui"]


class TestAtriaAllDictionaries(unittest.TestCase):
    """Verifies all 9 ATRIA dictionary sections and end-to-end voice browser navigation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.gui = _install_full_stubs()

    def setUp(self) -> None:
        if hasattr(self.gui, "calls"):
            self.gui.calls.clear()

    def test_all_nine_sections_exist_on_disk(self) -> None:
        expected_sections = [
            "2D-Drafting",
            "3D-BIM",
            "Annotation",
            "Manage",
            "Modify",
            "Preferences",
            "Snapping",
            "StatusBar",
            "Utils",
        ]
        for section in expected_sections:
            section_dir = DIC_ROOT / section
            self.assertTrue(
                section_dir.is_dir(),
                f"Missing ATRIA section directory: {section_dir}",
            )
            # Verify each section has commands.py or equivalent
            commands_file = section_dir / "commands.py"
            self.assertTrue(
                commands_file.is_file(),
                f"Missing commands.py in {section_dir}",
            )

    def test_base_py_exports_all_sections(self) -> None:
        from navigation.dictionary_loader import DictionaryLoader

        loader = DictionaryLoader(DIC_ROOT)
        self.assertTrue(loader.IsReady)
        base_dict = loader.LoadBaseModuleDict()

        expected_sections = [
            "2D-Drafting",
            "3D-BIM",
            "Annotation",
            "Manage",
            "Modify",
            "Preferences",
            "Snapping",
            "StatusBar",
            "Utils",
            "show_atria_panel",
            "hide_atria_panel",
        ]
        for key in expected_sections:
            self.assertIn(key, base_dict, f"base.py is missing key '{key}'")

    def test_all_translations_resolve_without_none(self) -> None:
        """Ensure no translation in 2D-Drafting or 3D-BIM resolved to None."""
        from core.language_code import LanguageCode
        from navigation.dictionary_loader import DictionaryLoader

        loader = DictionaryLoader(DIC_ROOT)
        for section in ("2D-Drafting", "3D-BIM"):
            section_dir = DIC_ROOT / section
            for lang in (LanguageCode.Es, LanguageCode.En):
                translate_map = loader.LoadTranslateMap(section_dir, lang)
                self.assertGreater(
                    len(translate_map),
                    0,
                    f"Empty translation map for {section} in {lang}",
                )
                for spoken, target in translate_map.items():
                    self.assertIsNotNone(
                        target,
                        f"Unresolved target (None) for spoken phrase '{spoken}' in {section}/{lang}",
                    )

    def test_ayuda_files(self) -> None:
        """Ensure ayuda.py exists and defines Ayuda/Help where implemented."""
        for section in ("2D-Drafting", "3D-BIM", "Utils"):
            ayuda_path = DIC_ROOT / section / "ayuda.py"
            self.assertTrue(ayuda_path.is_file(), f"Missing ayuda.py in {section}")

            spec = importlib.util.spec_from_file_location(f"atria_ayuda_{section}", ayuda_path)
            self.assertIsNotNone(spec)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            has_help = any(
                hasattr(mod, attr) for attr in ("Ayuda", "ayuda", "Help", "help", "Comandos")
            )
            self.assertTrue(has_help, f"{ayuda_path} must expose help data")

    def test_browser_voice_navigation_spanish_e2e(self) -> None:
        """End-to-end multi-step voice navigation in Spanish."""
        from core.language_code import LanguageCode
        from core.preferences import Preferences
        from navigation.browser import Browser

        prefs = Preferences()
        prefs.SetLanguage = LanguageCode.Es
        executed_entries = []

        browser = Browser(
            dictionary_root=DIC_ROOT,
            prefs=prefs,
            on_execute=lambda e: executed_entries.append(e),
        )

        # 1. Descend to 2D-Drafting
        res = browser.ProcessPhrase("dos d")
        self.assertTrue(res.Success, f"Failed saying 'dos d': {res.Message}")
        self.assertIn(res.Action, ("descend", "base_jump"))
        self.assertEqual(browser.CurrentContextName, "2D-Drafting")

        # 2. Execute Arc
        res = browser.ProcessPhrase("arco")
        self.assertTrue(res.Success, f"Failed saying 'arco': {res.Message}")
        self.assertEqual(res.Action, "execute")
        self.assertGreaterEqual(len(executed_entries), 1)

        # 3. Ascend back to root
        res = browser.ProcessPhrase("volver")
        self.assertTrue(res.Success, f"Failed saying 'volver': {res.Message}")
        self.assertEqual(res.Action, "back")
        self.assertEqual(browser.CurrentContextName, "Base")

        # 4. Descend to 3D-BIM
        res = browser.ProcessPhrase("bim")
        self.assertTrue(res.Success, f"Failed saying 'bim': {res.Message}")
        self.assertIn(res.Action, ("descend", "base_jump"))
        self.assertEqual(browser.CurrentContextName, "3D-BIM")

        # 5. Execute Roof
        res = browser.ProcessPhrase("crear techo")
        self.assertTrue(res.Success, f"Failed saying 'crear techo': {res.Message}")
        self.assertEqual(res.Action, "execute")

        # 6. Ascend back to root
        res = browser.ProcessPhrase("subir")
        self.assertTrue(res.Success)
        self.assertEqual(browser.CurrentContextName, "Base")

    def test_browser_voice_navigation_english_e2e(self) -> None:
        """End-to-end multi-step voice navigation in English."""
        from core.language_code import LanguageCode
        from core.preferences import Preferences
        from navigation.browser import Browser

        prefs = Preferences()
        prefs.SetLanguage = LanguageCode.En
        executed_entries = []

        browser = Browser(
            dictionary_root=DIC_ROOT,
            prefs=prefs,
            on_execute=lambda e: executed_entries.append(e),
        )

        # 1. Descend to 2D-Drafting
        res = browser.ProcessPhrase("two d")
        self.assertTrue(res.Success, f"Failed saying 'two d': {res.Message}")
        self.assertIn(res.Action, ("descend", "base_jump"))
        self.assertEqual(browser.CurrentContextName, "2D-Drafting")

        # 2. Execute Arc
        res = browser.ProcessPhrase("arc")
        self.assertTrue(res.Success, f"Failed saying 'arc': {res.Message}")
        self.assertEqual(res.Action, "execute")

        # 3. Ascend back to root
        res = browser.ProcessPhrase("up")
        self.assertTrue(res.Success)
        self.assertEqual(browser.CurrentContextName, "Base")

        # 4. Descend to 3D-BIM
        res = browser.ProcessPhrase("bim")
        self.assertTrue(res.Success)
        self.assertIn(res.Action, ("descend", "base_jump"))
        self.assertEqual(browser.CurrentContextName, "3D-BIM")

        # 5. Execute Wall
        res = browser.ProcessPhrase("create wall")
        self.assertTrue(res.Success, f"Failed saying 'create wall': {res.Message}")
        self.assertEqual(res.Action, "execute")


if __name__ == "__main__":
    unittest.main()

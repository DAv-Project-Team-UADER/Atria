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

"""
Integration tests for real dictionary hierarchy (Atria/dic).

Enforces Rule 4 (Nested subcontexts convention):
- Submenus MUST be nested under their own key (e.g. explorer.update({'file': file})).
- Submenus MUST NOT be flattened (e.g. explorer.update(file) is forbidden).
- Ensures no dead code overrides dictionary updates.
- Verifies base.py loads cleanly and subfolders remain navigable.
"""

from __future__ import annotations

import ast
import os
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


def _install_freecad_stub() -> None:
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


class TestRealDictionariesConvention(unittest.TestCase):
    """Audits ATRIA dictionary for mandatory nesting convention and navigation integrity."""

    @classmethod
    def setUpClass(cls) -> None:
        _install_freecad_stub()

    def test_no_flattened_updates_in_dic(self) -> None:
        """
        Rule 4: Verify that no .update() call in ATRIA/dictionary flattens a sub-dictionary.
        All update calls must pass a dict literal mapping a key string to a sub-dict,
        e.g., dict.update({'key': sub_dict}).
        """
        violations: list[str] = []

        for root, _, files in os.walk(DIC_ROOT):
            for file in files:
                if not file.endswith(".py"):
                    continue
                filepath = Path(root) / file
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    source = f.read()

                try:
                    tree = ast.parse(source, filename=str(filepath))
                except SyntaxError as e:
                    violations.append(f"Syntax error in {filepath}: {e}")
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                        call = node.value
                        if isinstance(call.func, ast.Attribute) and call.func.attr == "update":
                            if len(call.args) == 1:
                                arg = call.args[0]
                                # If argument is a variable/name or call instead of a dict literal {}, record violation
                                if not isinstance(arg, ast.Dict):
                                    rel_path = filepath.relative_to(DIC_ROOT)
                                    violations.append(
                                        f"{rel_path}:{node.lineno} -> {ast.unparse(call)} "
                                        f"(Flattened update! Must wrap in dict literal like update({{'key': sub_dict}}))"
                                    )

        self.assertEqual(
            violations,
            [],
            "Found flattened .update(...) calls violating Rule 4:\n" + "\n".join(violations),
        )

    def test_base_py_imports_and_has_top_level_keys(self) -> None:
        """Verify that base.py loads clean top level dictionaries."""
        from navigation.dictionary_loader import DictionaryLoader

        loader = DictionaryLoader(DIC_ROOT)
        self.assertTrue(loader.IsReady, f"DictionaryLoader should find DIC_ROOT at {DIC_ROOT}")

        base_dict = loader.LoadBaseModuleDict()
        self.assertIn("2D-Drafting", base_dict)
        self.assertIn("3D-BIM", base_dict)
        self.assertIn("Annotation", base_dict)
        self.assertIn("Manage", base_dict)
        self.assertIn("Modify", base_dict)
        self.assertIn("Preferences", base_dict)
        self.assertIn("Snapping", base_dict)
        self.assertIn("StatusBar", base_dict)
        self.assertIn("Utils", base_dict)

    def test_top_level_workbenches_are_nested(self) -> None:
        """Verify that 2D-Drafting and 3D-BIM sections exist at top level."""
        from navigation.dictionary_loader import DictionaryLoader

        loader = DictionaryLoader(DIC_ROOT)
        base_dict = loader.LoadBaseModuleDict()
        self.assertIn("2D-Drafting", base_dict)
        self.assertIn("3D-BIM", base_dict)

    def test_atria_panel_visibility_commands_are_global_in_spanish(self) -> None:
        """Verify Spanish panel visibility aliases resolve from the base dictionary."""
        from core.language_code import LanguageCode
        from navigation.dictionary_loader import DictionaryLoader

        loader = DictionaryLoader(DIC_ROOT)
        base_dict = loader.LoadBaseModuleDict()
        spanish = loader.LoadTranslateMap(DIC_ROOT, LanguageCode.Es)

        self.assertIn("hide_atria_panel", base_dict)
        self.assertIn("show_atria_panel", base_dict)

        for phrase in ("minimizar", "reducir", "disminuir"):
            self.assertIs(spanish[phrase], base_dict["hide_atria_panel"])
        for phrase in ("maximizar", "aumentar", "agrandar"):
            self.assertIs(spanish[phrase], base_dict["show_atria_panel"])

    def test_techdraw_and_geometry_translations_populated(self) -> None:
        """Verify that 2D-Drafting and 3D-BIM translations are populated and not empty stubs."""
        from navigation.dictionary_loader import DictionaryLoader
        from core.language_code import LanguageCode

        loader = DictionaryLoader(DIC_ROOT)

        drafting_dir = DIC_ROOT / "2D-Drafting"
        es_map = loader.LoadTranslateMap(drafting_dir, LanguageCode.Es)
        self.assertGreater(
            len(es_map),
            0,
            "2D-Drafting TraduceToEs.py is empty or invalid! Spoken commands in Spanish won't work.",
        )
        norm_es = [DictionaryLoader.NormalizeSpoken(k) for k in es_map]
        self.assertIn("arco", norm_es)
        self.assertIn("circulo", norm_es)

        en_map = loader.LoadTranslateMap(drafting_dir, LanguageCode.En)
        self.assertGreater(len(en_map), 0, "2D-Drafting TraduceToEn.py is empty!")
        norm_en = [DictionaryLoader.NormalizeSpoken(k) for k in en_map]
        self.assertIn("arc", norm_en)
        self.assertIn("circle", norm_en)

        bim_dir = DIC_ROOT / "3D-BIM"
        es_bim_map = loader.LoadTranslateMap(bim_dir, LanguageCode.Es)
        en_bim_map = loader.LoadTranslateMap(bim_dir, LanguageCode.En)
        self.assertGreater(len(es_bim_map), 0, "3D-BIM TraduceToEs.py is empty!")
        self.assertGreater(len(en_bim_map), 0, "3D-BIM TraduceToEn.py is empty!")
        norm_bim_es = [DictionaryLoader.NormalizeSpoken(k) for k in es_bim_map]
        norm_bim_en = [DictionaryLoader.NormalizeSpoken(k) for k in en_bim_map]
        self.assertIn("crear muro", norm_bim_es)
        self.assertIn("create wall", norm_bim_en)


if __name__ == "__main__":
    unittest.main()

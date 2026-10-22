# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad AutÃ³noma de Entre RÃ­os (UADER FCYT, sede ConcepciÃ³n del Uruguay)
# Bajo la direcciÃ³n de Ernesto Ledesma
# Encargados: Micaela SaÃ¼l, Tadeo Rochas y Camila ViÃ±eg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los tÃ©rminos de la Licencia PÃºblica General GNU tal como fue publicada
# por la FundaciÃ³n para el Software Libre, en la versiÃ³n 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea Ãºtil,
# pero SIN NINGUNA GARANTÃA; incluso sin la garantÃ­a implÃ­cita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÃ“SITO PARTICULAR. Consulte la
# Licencia PÃºblica General GNU para mÃ¡s detalles.
#
# DeberÃ­as haber recibido una copia de la Licencia PÃºblica General GNU
# junto con este programa. Si no es asÃ­, consulte <http://www.gnu.org/licenses/>.

"""
Tests for Draft dictionaries (Atria/dic/Workbench/DraftWork).

Los comandos ``Draft_*`` solo existen una vez que el workbench Draft fue
inicializado. Estos tests aseguran que cada callable del Ã¡rbol Draft activa el
workbench antes de ejecutar su comando (bug: "No such command 'Draft_Circle'").
"""

from __future__ import annotations

import importlib
import sys
import types
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))

from integration.atria_paths import atria_repo_root, ensure_atria_repo_on_path  # noqa: E402

ATRIA_DIR = atria_repo_root()
DIC_ROOT = ATRIA_DIR / "dictionary"
if str(DIC_ROOT) not in sys.path:
    sys.path.insert(0, str(DIC_ROOT))


class _FakeGui:
    """FreeCADGui falso: registra llamadas runCommand."""

    def __init__(self) -> None:
        self.active = "StartWorkbench"
        self.calls: list[tuple] = []

    def reset(self, active: str = "StartWorkbench") -> None:
        self.active = active
        self.calls = []

    def runCommand(self, name: str, idx: int = 0) -> None:
        self.calls.append(("run", name))


class _FakeCreateObjects:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def Execute(self) -> None:
        pass


def _install_stubs(fake_gui: _FakeGui) -> None:
    sys.modules["FreeCADGui"] = fake_gui  # type: ignore[assignment]
    app = sys.modules.get("FreeCAD") or types.ModuleType("FreeCAD")
    app.ActiveDocument = types.SimpleNamespace(recompute=lambda: None)
    sys.modules["FreeCAD"] = app
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

    for mod in ("Part", "BIM", "WorkingPlane", "DraftVecUtils"):
        sys.modules.setdefault(mod, types.ModuleType(mod))
    createobjects = types.ModuleType("selection.createobjects")
    createobjects.CreateObjects = _FakeCreateObjects  # type: ignore[attr-defined]
    sys.modules.setdefault("selection.createobjects", createobjects)
    sys.modules.setdefault("createobjects", createobjects)


def _load_module(path: Path, name: str):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class TestDraftWorkbenchActivation(unittest.TestCase):
    """Verifica que cada comando de 2D-Drafting y 3D-BIM de ATRIA ejecuta FreeCADGui.runCommand."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.gui = _FakeGui()
        _install_stubs(cls.gui)

        drafting_commands_path = DIC_ROOT / "2D-Drafting" / "commands.py"
        bim_commands_path = DIC_ROOT / "3D-BIM" / "commands.py"

        cls.drafting = _load_module(drafting_commands_path, "atria_test_2d_commands")
        cls.bim = _load_module(bim_commands_path, "atria_test_3d_commands")

    def setUp(self) -> None:
        self.gui.reset()

    def test_2d_drafting_commands_execute_run_command(self) -> None:
        """Todos los comandos de 2D-Drafting deben llamar a Gui.runCommand con Draft_*."""
        checked = 0
        for attr_name in (
            "Arc",
            "ArcFrom3Points",
            "BSpline",
            "BezierCurve",
            "Circle",
            "CubicBezierCurve",
            "Ellipse",
            "Fillet",
            "Line",
            "Point",
            "Polygon",
            "Polyline",
            "Rectangle",
        ):
            tool_dict = getattr(self.drafting, attr_name, None)
            self.assertIsInstance(tool_dict, dict, f"{attr_name} no es un diccionario")
            for cmd_key, func in tool_dict.items():
                if callable(func):
                    self.gui.reset()
                    func()
                    self.assertTrue(
                        any(c[0] == "run" for c in self.gui.calls),
                        f"{attr_name}['{cmd_key}'] no ejecutó Gui.runCommand",
                    )
                    checked += 1
        self.assertGreaterEqual(checked, 13)

    def test_3d_bim_commands_execute_run_command(self) -> None:
        """Todos los comandos de 3D-BIM deben ejecutarse limpiamente."""
        checked = 0
        for attr_name in (
            "Beam",
            "Building",
            "Column",
            "CurtainWall",
            "Door",
            "Level",
            "Pipe",
            "PipeConnector",
            "Roof",
            "Site",
            "Slab",
            "Space",
            "Wall",
            "Window",
            "ArchEquipment",
            "ArchFence",
            "ArchFrame",
            "ArchPanel",
            "ArchRebar",
            "ArchRoof",
            "ArchStairs",
            "ArchTruss",
            "BentShapeRebar",
            "HelicalRebar",
            "LShapeRebar",
            "StirrupRebar",
            "StraightRebar",
            "UShapeRebar",
        ):
            tool_dict = getattr(self.bim, attr_name, None)
            self.assertIsInstance(tool_dict, dict, f"{attr_name} no es un diccionario")
            for cmd_key, func in tool_dict.items():
                if callable(func):
                    self.gui.reset()
                    func()
                    checked += 1
        self.assertGreaterEqual(checked, 25)


if __name__ == "__main__":
    unittest.main()

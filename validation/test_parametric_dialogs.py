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

"""Unit and integration tests for voice-driven parametric commands and input dialogs."""

from __future__ import annotations

import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = ROOT / "GUIFreeCad"
VAL_PATH = ROOT / "validation"
DIC_PATH = ROOT / "dictionary"

for p in (ROOT, GUI_PATH, VAL_PATH, DIC_PATH):
    text = str(p)
    if text not in sys.path:
        sys.path.insert(0, text)

# Install mocks for FreeCAD headless testing
class FakeVector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, (tuple, list)):
            self.x = float(x[0])
            self.y = float(x[1]) if len(x) > 1 else 0.0
            self.z = float(x[2]) if len(x) > 2 else 0.0
        elif isinstance(x, FakeVector):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def isEqual(self, other, tol=1e-7):
        ox = getattr(other, "x", other[0] if isinstance(other, (tuple, list)) else 0)
        oy = getattr(other, "y", other[1] if isinstance(other, (tuple, list)) else 0)
        oz = getattr(other, "z", other[2] if isinstance(other, (tuple, list)) else 0)
        return abs(self.x - ox) < tol and abs(self.y - oy) < tol and abs(self.z - oz) < tol

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


if "FreeCAD" not in sys.modules:
    fc = types.ModuleType("FreeCAD")
    fc.Vector = FakeVector
    fc.Placement = lambda base=None, rot=None: types.SimpleNamespace(Base=base, Rotation=rot)
    fc.Rotation = lambda: None
    fc.ActiveDocument = types.SimpleNamespace(
        recompute=lambda: None,
        addObject=lambda k, n: types.SimpleNamespace(Name=n, Label=n),
        openTransaction=lambda n: None,
        commitTransaction=lambda: None,
        abortTransaction=lambda: None,
    )
    fc.activeDocument = lambda: fc.ActiveDocument
    fc.newDocument = lambda: fc.ActiveDocument
    sys.modules["FreeCAD"] = fc
else:
    sys.modules["FreeCAD"].Vector = FakeVector

if "FreeCADGui" not in sys.modules:
    gui = types.ModuleType("FreeCADGui")
    gui.runCommand = lambda *a, **k: None
    gui.Selection = types.SimpleNamespace(getSelection=lambda: [types.SimpleNamespace(Label="Obj", Name="Obj")])
    gui.activeView = lambda: types.SimpleNamespace(getSceneGraph=lambda: None)
    gui.ActiveDocument = sys.modules["FreeCAD"].ActiveDocument
    sys.modules["FreeCADGui"] = gui

if "Draft" not in sys.modules:
    draft = types.ModuleType("Draft")
    draft.make_line = lambda *a, **k: types.SimpleNamespace(Name="Line", Label="Line")
    draft.make_circle = lambda *a, **k: types.SimpleNamespace(Name="Circle", Label="Circle")
    draft.make_rectangle = lambda *a, **k: types.SimpleNamespace(Name="Rectangle", Label="Rectangle")
    draft.make_polygon = lambda *a, **k: types.SimpleNamespace(Name="Polygon", Label="Polygon")
    draft.make_ellipse = lambda *a, **k: types.SimpleNamespace(Name="Ellipse", Label="Ellipse")
    draft.move = lambda *a, **k: [types.SimpleNamespace(Name="MovedObj")]
    draft.mirror = lambda *a, **k: [types.SimpleNamespace(Name="MirroredObj")]
    draft.scale = lambda *a, **k: [types.SimpleNamespace(Name="ScaledObj")]
    draft.rotate = lambda *a, **k: [types.SimpleNamespace(Name="RotatedObj")]
    draft.make_clone = lambda *a, **k: types.SimpleNamespace(Name="CloneObj")
    draft.make_wire = lambda *a, **k: types.SimpleNamespace(Name="Wire", Label="Wire")
    draft.autogroup = lambda *a, **k: None
    sys.modules["Draft"] = draft

if "Arch" not in sys.modules:
    arch = types.ModuleType("Arch")
    arch.makeWall = lambda *a, **k: types.SimpleNamespace(Name="Wall", Label="Wall")
    arch.makeStructure = lambda *a, **k: types.SimpleNamespace(Name="Structure", Label="Structure")
    arch.makeWindow = lambda *a, **k: types.SimpleNamespace(Name="Window", Label="Window")
    arch.makeRoof = lambda *a, **k: types.SimpleNamespace(Name="Roof", Label="Roof")
    arch.makePipe = lambda *a, **k: types.SimpleNamespace(Name="Pipe", Label="Pipe")
    arch.makeFloor = lambda *a, **k: types.SimpleNamespace(Name="Floor", Label="Floor")
    sys.modules["Arch"] = arch

from dictionary_resolver import GetDictionaryFunction
from GUIFreeCad.InputPrompts.CoordinateInputPrompt import CoordinateInputPrompt
from GUIFreeCad.InputPrompts.ParameterCollector import ParameterCollector
from GUIFreeCad.InputPrompts.PromptedCommandExecutor import PromptedCommandExecutor
from GUIFreeCad.InputPrompts.SpokenNumberParser import SpokenNumberParser
from GUIFreeCad.navigation.context_entry import ContextEntry
from validator import Validator


class TestParametricVoiceDialogs(unittest.TestCase):
    def setUp(self) -> None:
        self.collector = ParameterCollector(Language="es", DelayMs=0)
        self.executor = PromptedCommandExecutor(Collector=self.collector)

        fc = sys.modules.get("FreeCAD")
        if fc is not None:
            doc = types.SimpleNamespace(
                recompute=lambda: None,
                addObject=lambda k, n: types.SimpleNamespace(Name=n, Label=n),
                openTransaction=lambda n: None,
                commitTransaction=lambda: None,
                abortTransaction=lambda: None,
            )
            fc.ActiveDocument = doc
            fc.activeDocument = lambda: doc
            fc.newDocument = lambda: doc
            fc.Vector = FakeVector
            fc.Placement = lambda base=None, rot=None: types.SimpleNamespace(Base=base, Rotation=rot)
            fc.Rotation = lambda: None

        gui = sys.modules.get("FreeCADGui")
        if gui is not None:
            gui.runCommand = lambda *a, **k: None
            gui.Selection = types.SimpleNamespace(
                getSelection=lambda: [types.SimpleNamespace(Label="Obj", Name="Obj")],
                getSelectionEx=lambda: [
                    types.SimpleNamespace(
                        Object=types.SimpleNamespace(Label="Obj"), SubElementNames=["Face1"]
                    )
                ],
                clearSelection=lambda: None,
                addSelection=lambda *a: None,
            )
            gui.activeView = lambda: types.SimpleNamespace(getSceneGraph=lambda: object())
            if fc is not None:
                gui.ActiveDocument = fc.ActiveDocument

    def test_spoken_number_parser_hundreds_and_thousands(self) -> None:
        self.assertEqual(SpokenNumberParser.ParseFloat("cero"), 0.0)
        self.assertEqual(SpokenNumberParser.ParseFloat("diez"), 10.0)
        self.assertEqual(SpokenNumberParser.ParseFloat("cien ok"), 100.0)
        self.assertEqual(SpokenNumberParser.ParseFloat("ciento cincuenta"), 150.0)
        self.assertEqual(SpokenNumberParser.ParseFloat("doscientos treinta y cinco"), 235.0)
        self.assertEqual(SpokenNumberParser.ParseFloat("quinientos"), 500.0)
        self.assertEqual(SpokenNumberParser.ParseFloat("mil doscientos"), 1200.0)
        self.assertEqual(SpokenNumberParser.ParseFloat("dos mil quinientos"), 2500.0)

    def test_coordinate_input_prompt_parsing(self) -> None:
        prompt = CoordinateInputPrompt()
        res1 = prompt.ProcessFinalText("diez veinte ok")
        self.assertTrue(res1.Success)
        self.assertEqual(res1.Value, (10.0, 20.0))

        res2 = prompt.ProcessFinalText("cien doscientos cincuenta enviar")
        self.assertTrue(res2.Success)
        self.assertEqual(res2.Value, (100.0, 250.0))

        res_cancel = prompt.ProcessFinalText("cancelar")
        self.assertTrue(res_cancel.Cancelled)

    def test_friendly_dialog_prompts_for_coordinates(self) -> None:
        spec_x1 = types.SimpleNamespace(index=1, name="x1", kind="float")
        title = self.collector._BuildPromptTitle(spec_x1)
        msg = self.collector._BuildPromptMessage(spec_x1)
        self.assertIn("Coordenada X inicial", title)
        self.assertIn("Coordenada X inicial", msg)

        spec_radius = types.SimpleNamespace(index=2, name="radius", kind="float")
        title_r = self.collector._BuildPromptTitle(spec_radius)
        self.assertIn("Radio", title_r)

    def test_execute_line_by_voice_dictation(self) -> None:
        line_fn = GetDictionaryFunction("2d-drafting", "line")
        entry = ContextEntry(Spoken="linea", InternalKey="line", Target=line_fn)

        # User dictates: x1=0, y1=0, x2=100, y2=50
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["cero ok", "cero ok", "cien ok", "cincuenta ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"x1": 0.0, "y1": 0.0, "x2": 100.0, "y2": 50.0},
        )
        self.assertIsNotNone(result)

    def test_execute_circle_by_voice_dictation(self) -> None:
        circle_fn = GetDictionaryFunction("2d-drafting", "circle")
        entry = ContextEntry(Spoken="circulo", InternalKey="circle", Target=circle_fn)

        # User dictates: x=10, y=20, radius=50
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["diez ok", "veinte ok", "cincuenta ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"x": 10.0, "y": 20.0, "radius": 50.0},
        )
        self.assertIsNotNone(result)

    def test_execute_rectangle_by_voice_dictation(self) -> None:
        rect_fn = GetDictionaryFunction("2d-drafting", "rectangle")
        entry = ContextEntry(Spoken="rectangulo", InternalKey="rectangle", Target=rect_fn)

        # User dictates: x=0, y=0, length=200, width=100
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["cero ok", "cero ok", "doscientos ok", "cien ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"x": 0.0, "y": 0.0, "length": 200.0, "width": 100.0},
        )
        self.assertIsNotNone(result)

    def test_execute_box_3d_by_voice_dictation(self) -> None:
        box_fn = GetDictionaryFunction("3d-bim", "box")
        entry = ContextEntry(Spoken="caja", InternalKey="box", Target=box_fn)

        # User dictates: length=100, width=50, height=30, x=10, y=20, z=0
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["cien ok", "cincuenta ok", "treinta ok", "diez ok", "veinte ok", "cero ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"length": 100.0, "width": 50.0, "height": 30.0, "x": 10.0, "y": 20.0, "z": 0.0},
        )
        self.assertIsNotNone(result)

    def test_execute_wall_3d_by_voice_dictation(self) -> None:
        wall_fn = GetDictionaryFunction("3d-bim", "wall")
        entry = ContextEntry(Spoken="muro", InternalKey="wall", Target=wall_fn)

        # User dictates: length=5000, width=200, height=3000, x=0, y=500, z=0
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["cinco mil ok", "doscientos ok", "tres mil ok", "cero ok", "quinientos ok", "cero ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"length": 5000.0, "width": 200.0, "height": 3000.0, "x": 0.0, "y": 500.0, "z": 0.0},
        )
        self.assertIsNotNone(result)

    def test_execute_door_3d_by_voice_dictation(self) -> None:
        door_fn = GetDictionaryFunction("3d-bim", "door")
        entry = ContextEntry(Spoken="puerta", InternalKey="door", Target=door_fn)

        # User dictates: width=900, height=2100, x=1000, y=0, z=0
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["novecientos ok", "dos mil cien ok", "mil ok", "cero ok", "cero ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"width": 900.0, "height": 2100.0, "x": 1000.0, "y": 0.0, "z": 0.0},
        )
        self.assertIsNotNone(result)

    def test_execute_window_3d_by_voice_dictation(self) -> None:
        window_fn = GetDictionaryFunction("3d-bim", "window")
        entry = ContextEntry(Spoken="ventana", InternalKey="window", Target=window_fn)

        # User dictates: width=1200, height=1200, x=2500, y=0, z=1000
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["mil doscientos ok", "mil doscientos ok", "dos mil quinientos ok", "cero ok", "mil ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"width": 1200.0, "height": 1200.0, "x": 2500.0, "y": 0.0, "z": 1000.0},
        )
        self.assertIsNotNone(result)

    def test_execute_roof_3d_by_voice_dictation(self) -> None:
        roof_fn = GetDictionaryFunction("3d-bim", "roof")
        entry = ContextEntry(Spoken="techo", InternalKey="roof", Target=roof_fn)

        # User dictates: length=6000, width=4000, thickness=150, x=0, y=0, z=3000
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["seis mil ok", "cuatro mil ok", "ciento cincuenta ok", "cero ok", "cero ok", "tres mil ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"length": 6000.0, "width": 4000.0, "thickness": 150.0, "x": 0.0, "y": 0.0, "z": 3000.0},
        )
        self.assertIsNotNone(result)

    def test_voice_dialog_cancellation_aborts_execution(self) -> None:
        line_fn = GetDictionaryFunction("2d-drafting", "line")
        entry = ContextEntry(Spoken="linea", InternalKey="line", Target=line_fn)

        # User dictates x1, but then cancels on y1
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["diez ok", "cancelar"],
        )
        self.assertIsNone(result)
        self.assertTrue(self.executor.LastResult.Cancelled)

    def test_move_command_by_voice_dictation(self) -> None:
        move_fn = GetDictionaryFunction("modify", "move")
        entry = ContextEntry(Spoken="mover", InternalKey="move", Target=move_fn)

        # User dictates dx=15, dy=25
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["quince ok", "veinticinco ok"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(self.executor.LastResult.Value, {"dx": 15.0, "dy": 25.0})

    def test_execute_circle_with_direct_digits_and_no_ok(self) -> None:
        circle_fn = GetDictionaryFunction("2d-drafting", "circle")
        entry = ContextEntry(Spoken="circulo", InternalKey="circle", Target=circle_fn)

        # User provides parameters: 5, 6, 7 directly
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["5", "6", "7"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"x": 5.0, "y": 6.0, "radius": 7.0},
        )
        self.assertIsNotNone(result)

    def test_execute_circle_with_direct_spanish_words_and_no_ok(self) -> None:
        circle_fn = GetDictionaryFunction("2d-drafting", "circle")
        entry = ContextEntry(Spoken="circulo", InternalKey="circle", Target=circle_fn)

        # User provides parameters: cinco, seis, siete
        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["cinco", "seis", "siete"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"x": 5.0, "y": 6.0, "radius": 7.0},
        )
        self.assertIsNotNone(result)

    def test_float_input_prompt_on_ok_clicked(self) -> None:
        from GUIFreeCad.InputPrompts.FloatInputPrompt import FloatInputPrompt

        prompt = FloatInputPrompt()
        prompt.SetHeardText("cinco")
        prompt._OnOkClicked()
        self.assertTrue(prompt.GetResult().Success)
        self.assertEqual(prompt.GetResult().Value, 5.0)

    def test_integer_input_prompt_on_ok_clicked(self) -> None:
        from GUIFreeCad.InputPrompts.IntegerInputPrompt import IntegerInputPrompt

        prompt = IntegerInputPrompt()
        prompt.SetHeardText("ocho")
        prompt._OnOkClicked()
        self.assertTrue(prompt.GetResult().Success)
        self.assertEqual(prompt.GetResult().Value, 8)

    def test_execute_polygon_by_voice_dictation(self) -> None:
        poly_fn = GetDictionaryFunction("2d-drafting", "polygon")
        entry = ContextEntry(Spoken="poligono", InternalKey="polygon", Target=poly_fn)

        result = self.executor.ExecuteEntry(
            entry,
            SimulatedFinalTexts=["seis", "diez coma cinco"],
        )
        self.assertTrue(self.executor.LastResult.Success)
        self.assertEqual(
            self.executor.LastResult.Value,
            {"nfaces": 6, "radius": 10.5},
        )
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()

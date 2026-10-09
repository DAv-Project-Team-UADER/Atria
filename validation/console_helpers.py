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

"""FreeCAD console helpers for Validator (zero-config after iniciar_atria.bat)."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _BootstrapPath() -> str:
    env = os.environ.get("ATRIA_VALIDATION_ROOT", "").strip()
    folder = str(Path(env).resolve()) if env else str(Path(__file__).resolve().parent)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    return folder


_BootstrapPath()


def DemoGeometryLine(Language: str = "es") -> None:
    from dictionary_resolver import GetDictionaryFunction
    from validator import Validator

    fn = GetDictionaryFunction("geometry.line", "create_by_points")
    validator = Validator()
    validator.GetRequirements(Language, fn)
    print("---")
    validator.CallIfValid(
        Language,
        fn,
        {"x1": 0, "y1": 0, "x2": "100", "y2": 50.0, "label": "LineaDemo"},
    )


def DemoAdditivePad(Language: str = "es", sketch_name: str = "Sketch") -> None:
    from dictionary_resolver import GetDictionaryFunction
    from validator import Validator

    fn = GetDictionaryFunction("additive", "pad_sketch")
    validator = Validator()
    validator.GetRequirements(Language, fn)
    print("---")
    validator.CallIfValid(
        Language,
        fn,
        {"sketch": sketch_name, "length": "12.5"},
    )

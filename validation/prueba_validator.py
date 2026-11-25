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

"""Guided Validator demo for FreeCAD console."""


def _EnsureActiveDocument(name: str = "ValidatorTest") -> None:
    import FreeCAD as App

    if App.ActiveDocument is None:
        App.newDocument(name)
        print(f"[ATRIA] Documento creado: '{name}'")


def RunFullDemo(sketch_name: str = "Sketch") -> None:
    from console_helpers import DemoAdditivePad, DemoGeometryLine

    _EnsureActiveDocument()
    print("\n========== ATRIA Validator — demo consola ==========\n")

    for language in ("es", "en", "pt"):
        print(f"=== geometry.line / create_by_points ({language}) ===")
        DemoGeometryLine(language)
        print()

    for language in ("es", "en", "pt"):
        print(f"=== additive / pad_sketch ({language}) ===")
        DemoAdditivePad(language, sketch_name=sketch_name)
        print()

    print("=== caso error: sketch inexistente ===")
    from dictionary_resolver import GetDictionaryFunction
    from validator import Validator

    fn = GetDictionaryFunction("additive", "pad_sketch")
    Validator().CallIfValid("es", fn, {"sketch": "NoExiste", "length": 10})
    print("========== Fin demo Validator ==========\n")

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

"""Guided Validator demo for FreeCAD console."""


def _EnsureActiveDocument(name: str = "ValidatorTest") -> None:
    import FreeCAD as App

    if App.ActiveDocument is None:
        App.newDocument(name)
        print(f"[ATRIA] Documento creado: '{name}'")


def RunFullDemo(sketch_name: str = "Sketch") -> None:
    from console_helpers import DemoAdditivePad, DemoGeometryLine

    _EnsureActiveDocument()
    print("\n========== ATRIA Validator â€” demo consola ==========\n")

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

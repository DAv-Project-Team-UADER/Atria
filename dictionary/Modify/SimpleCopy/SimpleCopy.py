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

"""Simple Copy — Menú BIM → Modify → Simple Copy.

Crea una copia no paramétrica ("congelada") de la forma de cada objeto
seleccionado, sin historial ni vínculo con el original.
Comando FreeCAD: BIM_SimpleCopy (delega en Part_SimpleCopy).
"""

import FreeCAD
import FreeCADGui


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def simple_copy():
    """Crea un Part::Feature con la forma actual de cada objeto seleccionado.

    Devuelve
    --------
    Lista de copias creadas.
    """
    doc = _require_document()

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para copiar.")

    import Part

    doc.openTransaction("Simple Copy")
    try:
        copies = []
        for obj in selection:
            shape = Part.getShape(obj, "", needSubElement=False, refine=False)
            if shape.isNull():
                FreeCAD.Console.PrintWarning(
                    "{} no tiene forma, se omite.\n".format(obj.Label)
                )
                continue
            new = doc.addObject("Part::Feature", obj.Name)
            new.Shape = shape
            new.Label = obj.Label + " (copia)"
            copies.append(new)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return copies

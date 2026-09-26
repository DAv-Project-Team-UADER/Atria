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

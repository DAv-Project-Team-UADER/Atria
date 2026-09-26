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

"""Compound — Menú BIM → Modify → Compound.

Agrupa las formas seleccionadas en un único objeto Part::Compound.
Comando FreeCAD: BIM_Compound (delega en Part_Compound).
"""

import FreeCAD
import FreeCADGui


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def compound():
    """Crea un Part::Compound con los objetos seleccionados.

    Igual que Part_Compound, oculta los objetos originales, que pasan a ser
    hijos del compuesto.

    Devuelve
    --------
    El objeto Part::Compound creado.
    """
    doc = _require_document()

    selection = FreeCADGui.Selection.getSelection()
    if len(selection) < 2:
        raise RuntimeError("Seleccioná al menos dos objetos para crear un compuesto.")

    doc.openTransaction("Compound")
    try:
        result = doc.addObject("Part::Compound", "Compound")
        result.Links = selection
        for obj in selection:
            if obj.ViewObject:
                obj.ViewObject.Visibility = False
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result

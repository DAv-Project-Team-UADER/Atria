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

"""Facebinder — Menú BIM → 3D/BIM → Generic 3D tools → Facebinder.

Crea una superficie paramétrica a partir de las caras seleccionadas. Se
actualiza cuando cambia el objeto origen y puede extruirse, por ejemplo para
revestimientos de muros.
Comando FreeCAD: Draft_Facebinder (atajo F, F en Draft).
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Facebinder"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _selection_set():
    """Devuelve [(objeto, (caras...)), ...] a partir de la selección actual."""
    selection_set = []
    for sel in FreeCADGui.Selection.getSelectionEx():
        faces = tuple(sub for sub in sel.SubElementNames if sub.startswith("Face"))
        if faces:
            selection_set.append((sel.Object, faces))
    return selection_set


def facebinder(extrusion=None):
    """Crea un atrapacaras sobre las caras seleccionadas.

    Parámetros
    ----------
    extrusion : float, opcional
        Espesor en mm con el que se extruye la superficie resultante. Si se
        omite, el atrapacaras queda sin espesor.

    Devuelve
    --------
    El objeto facebinder creado.
    """
    doc = _require_document()

    selection_set = _selection_set()
    if not selection_set:
        raise RuntimeError("Seleccioná al menos una cara.")

    import Draft

    doc.openTransaction("Facebinder")
    try:
        result = Draft.make_facebinder(selection_set)
        if extrusion:
            result.Extrusion = extrusion
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result

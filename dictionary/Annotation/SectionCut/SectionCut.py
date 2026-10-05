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

"""Section Cut — Menú BIM → Annotation → Create 2D Views → Section Cut.

Produce un objeto Shape2DView en modo "cut lines", que muestra solo las líneas
de corte: la intersección entre el plano de sección y el modelo. La proyección
se crea sobre el plano XY y depende enteramente de la dirección del plano de
sección, ignorando la orientación de la cámara 3D.
Comando FreeCAD: BIM_Shape2DCut.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Shape2DCut"
CUT_FACES = "Cutfaces"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def _SectionPlane(target):
    """Devuelve el plano de sección seleccionado."""
    import Draft

    if target is None:
        selection = FreeCADGui.Selection.getSelection()
        target = selection[0] if len(selection) == 1 else None

    if target is None:
        raise ValueError("Seleccioná un plano de sección para el corte.")

    if Draft.getType(target) != "SectionPlane":
        raise ValueError("El corte necesita un objeto Arch SectionPlane.")

    return target


def _ProjectionVector(section):
    """Dirección de proyección: la normal del plano de sección, hacia el modelo."""
    return section.Placement.Rotation.multVec(FreeCAD.Vector(0, 0, 1)).negative()


def CreateSectionCut(target=None):
    """Crea las líneas de corte del plano de sección sobre el modelo.

    Parámetros
    ----------
    target : object, opcional
        Plano de sección Arch SectionPlane. Por defecto, el único objeto
        seleccionado; si no hay selección se activa el comando interactivo.

    Devuelve
    --------
    object: la vista de corte creada, o None si el comando quedó en modo
    interactivo.
    """
    doc = _RequireDocument()
    _Require3dView()

    if target is None and not FreeCADGui.Selection.getSelection():
        FreeCADGui.runCommand(COMMAND)
        return None

    import Draft

    section = _SectionPlane(target)
    view = Draft.make_shape2dview(section, _ProjectionVector(section))
    view.InPlace = False
    view.ProjectionMode = CUT_FACES
    Draft.autogroup(view)
    doc.recompute()
    return view


SectionCut = {
    "section cut": CreateSectionCut,
}

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

"""Draft WorkingPlaneProxy — Menú BIM → Utils → Create working plane proxy.

Guarda el estado actual del plano de trabajo y de la cámara en un objeto
"WorkingPlaneProxy" del documento. Al seleccionarlo después, FreeCAD restaura
esa misma orientación de plano y de vista, lo que permite saltar rápido entre
distintas áreas u orientaciones del proyecto.
Comando FreeCAD: Draft_WorkingPlaneProxy.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_WorkingPlaneProxy"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def DraftWorkingPlaneProxy(placement=None):
    """Crea un proxy con el plano de trabajo y la vista actuales.

    Parámetros
    ----------
    placement : FreeCAD.Placement, opcional
        Colocación del plano de trabajo a guardar. Si se omite, se toma la del
        plano de trabajo activo en la interfaz.

    Devuelve
    --------
    El objeto WorkingPlaneProxy creado.
    """
    doc = _RequireDocument()

    if placement is None:
        _Require3dView()
        FreeCADGui.runCommand(COMMAND)
        return None

    if not isinstance(placement, FreeCAD.Placement):
        raise TypeError("La colocación tiene que ser un FreeCAD.Placement.")

    import Draft

    doc.openTransaction("Create Working Plane Proxy")
    try:
        proxy = Draft.make_workingplaneproxy(placement)
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return proxy

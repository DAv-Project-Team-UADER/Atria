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

"""BIM Preflight — Menú BIM → Manage → Preflight checks.

Ejecuta las comprobaciones de calidad del modelo antes de exportarlo a IFC:
detecta objetos que no son sólidos coplanares, elementos superpuestos, ausencia
de materiales o de cuantidades, geometría mal asignada a la estructura del
edificio (sitio, edificio, planta) y casos que no cumplen los estándares.
El resultado se muestra en una ventana con las verificaciones superadas en
verde y las fallidas en rojo, y desde ahí se puede seleccionar el objeto
problemático.
Comando FreeCAD: BIM_Preflight.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Preflight"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def BIMPreflight():
    """Abre el informe de comprobaciones del modelo BIM activo.

    No lleva parámetros: la herramienta analiza el documento activo completo.

    Devuelve
    --------
    None: los resultados se muestran en la ventana de preflight.
    """
    _RequireDocument()
    _Require3dView()
    FreeCADGui.runCommand(COMMAND)

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

"""Arch Survey — Menú BIM → Utils → Survey.

Inicia el modo interactivo de inspección del modelo. A medida que se hace clic
en vértices, aristas o caras, la herramienta calcula la medida y la registra en
una lista: longitudes de aristas, áreas de caras y coordenadas de vértices, con
totales acumulados. La lista se puede usar como referencia o exportarla.

El modo se abre y se cierra con la misma llamada: si el survey ya está activo,
la siguiente ejecución lo termina y entrega los totales.
Comando FreeCAD: Arch_Survey.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Arch_Survey"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def ArchSurvey():
    """Abre el modo survey de inspección del modelo.

    Al activarlo, cada clic sobre una arista o una cara acumula su longitud o su
    área en una lista, y un clic en el vacío reinicia los totales. Llamarlo de
    nuevo con el modo ya abierto lo cierra y entrega el resultado.

    Devuelve
    --------
    None: las medidas se muestran en el panel de tareas.
    """
    _RequireDocument()
    _Require3dView()

    import Arch

    Arch.survey()

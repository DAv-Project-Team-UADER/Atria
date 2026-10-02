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

"""BIM Report — Menú BIM → Manage → Report Tools → Report.

Genera tablas de planificación e informes a partir del modelo usando un lenguaje
de consulta con dialecto SQL (BIM SQL) sobre las propiedades de los objetos, y
vuelca el resultado en una hoja de cálculo vinculada que se actualiza al
recomputar. Varias consultas se pueden encadenar a modo de tubería (pipeline)
para flujos de trabajo complejos.

FreeCAD no trae este módulo: viene con el addon externo "Reporting". Con el
addon instalado, el comando `Report_Create` reemplaza a Schedule en el menú
Manage.
Comando FreeCAD: Report_Create.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Report_Create"

ADDON_NAME = "Reporting"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def IsAvailable():
    """Devuelve True si el addon Reporting está instalado y el comando existe.

    Sin interfaz gráfica no hay registro de comandos, así que en ese caso no
    se puede confirmar nada y se responde False.
    """
    list_commands = getattr(FreeCADGui, "listCommands", None)
    if list_commands is None:
        return False
    return COMMAND in list_commands()


def _RequireAddon():
    if not IsAvailable():
        raise RuntimeError(
            f"BIM Report necesita el addon externo '{ADDON_NAME}', que no está instalado."
        )


def BIMReport(query=None):
    """Crea un informe BIM a partir de una consulta SQL.

    Parámetros
    ----------
    query : str, opcional
        Consulta en dialecto BIM SQL, por ejemplo
        "SELECT Label, Area FROM document". Si se omite, se abre el diálogo
        para escribirla, guardarla y ejecutarla.

    Devuelve
    --------
    El objeto Report creado, o None en modo interactivo.

    Nota
    ----
    La creación del informe y de su hoja de cálculo vinculada la resuelve el
    addon Reporting a partir del diálogo, así que la consulta se pasa como
    texto de arranque y el resto del flujo queda en la interfaz.
    """
    _RequireDocument()
    _RequireAddon()
    _Require3dView()

    if query is not None and not query.strip():
        raise ValueError("La consulta no puede estar vacía.")

    FreeCADGui.runCommand(COMMAND)

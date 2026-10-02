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

"""Profile — Menú BIM → 3D/BIM → Generic 3D tools → Profile.

Crea un perfil paramétrico 2D (tubo circular C, H/I, rectangular R,
rectangular hueco RH, U, L o T) para usar como base de extrusiones: Arch
Frame, Curtain Wall, Part Extrude o Arch Structure.
Comando FreeCAD: Arch_Profile.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Arch_Profile"

# Clases de perfil admitidas por Arch.makeProfile.
PROFILE_CLASSES = ("C", "H", "R", "RH", "U", "L", "T")


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def profile(preset=None):
    """Crea un perfil paramétrico.

    Parámetros
    ----------
    preset : list, opcional
        Descripción del perfil con el formato de Arch.makeProfile:
        ``[categoría, nombre, clase, dimensiones...]``, por ejemplo
        ``[0, "REC", "REC100x100", "R", 100, 100]``. Si se omite, se abre el
        panel interactivo para elegir el preset y el punto de inserción en la
        vista 3D.

    Devuelve
    --------
    El objeto de perfil creado, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if preset is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    if len(preset) < 4 or preset[3] not in PROFILE_CLASSES:
        raise RuntimeError(
            "Clase de perfil inválida. Usá una de: " + ", ".join(PROFILE_CLASSES) + "."
        )

    import Arch

    doc.openTransaction("Profile")
    try:
        result = Arch.makeProfile(list(preset))
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result

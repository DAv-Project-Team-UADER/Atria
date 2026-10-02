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

"""Comandos FreeCAD de la seccion 3D-BIM (consolidado).

Cada funcion conserva su comportamiento original; este modulo
reune lo que antes vivia en una carpeta por funcion.
"""
import FreeCAD
import FreeCADGui
import FreeCADGui as Gui


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc

def _require_addon(module):
    """Verifica que el addon Reinforcement esté instalado."""
    try:
        __import__(module)
    except ImportError:
        raise RuntimeError(
            "Falta el addon Reinforcement. Instalalo desde el Addon Manager."
        )

def _require_selected_face(que):
    """Devuelve (objeto, nombre de cara) de la única cara seleccionada."""
    import Draft

    selection = FreeCADGui.Selection.getSelectionEx()
    if not selection:
        raise RuntimeError("Seleccioná " + que + ".")
    sel = selection[0]
    faces = [sub for sub in sel.SubElementNames if sub.startswith("Face")]
    if len(faces) != 1:
        raise RuntimeError("Seleccioná exactamente una cara: " + que + ".")
    if Draft.getType(sel.Object) != "Structure":
        raise RuntimeError("El objeto seleccionado no es un Arch Structure.")
    return sel.Object, faces[0]

def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")

def _require_part_selection():
    """Devuelve los objetos seleccionados que tienen una forma de Part."""
    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná un objeto basado en Part.")
    sin_forma = [obj.Label for obj in selection if not hasattr(obj, "Shape")]
    if sin_forma:
        raise RuntimeError(
            "Estos objetos no están basados en Part: " + ", ".join(sin_forma) + "."
        )
    return selection

def _selection_set():
    """Devuelve [(objeto, (caras...)), ...] a partir de la selección actual."""
    selection_set = []
    for sel in FreeCADGui.Selection.getSelectionEx():
        faces = tuple(sub for sub in sel.SubElementNames if sub.startswith("Face"))
        if faces:
            selection_set.append((sel.Object, faces))
    return selection_set


# --- Beam_Reinforcement ---
"""Beam Reinforcement — Menú BIM → 3D/BIM → Reinforcement tools → Beam Reinforcement.

Crea las barras de refuerzo de una viga modelada como Arch Structure:
estribos, armaduras superior e inferior y armaduras de corte izquierda y
derecha.
Comando FreeCAD: Reinforcement_BeamRebars (addon Reinforcement).
"""

COMMAND_BEAM_REINFORCEMENT = "Reinforcement_BeamRebars"
ADDON_MODULE = "BeamReinforcement"

def beam_reinforcement():
    """Abre el diálogo de refuerzo de viga sobre la cara seleccionada.

    La cara a seleccionar depende de la orientación de la viga: la cara
    derecha si el largo va en X, la cara frontal si va en Y. Requiere el
    addon Reinforcement instalado.

    Devuelve
    --------
    None. El grupo de armaduras lo crea el diálogo al confirmar.
    """
    _require_document()
    _require_addon(ADDON_MODULE)
    _require_selected_face("la cara derecha (viga en X) o frontal (viga en Y)")
    FreeCADGui.runCommand(COMMAND_BEAM_REINFORCEMENT)

# --- Box ---
"""Box — Menú BIM → 3D/BIM → Generic 3D tools → Box.

Crea un Part Box definiendo sus dimensiones gráficamente con 4 clics
(esquina, arista, cara y espesor), sin tener que editar propiedades después.
Sirve como base de cualquier otro objeto BIM.
Comando FreeCAD: BIM_Box.
"""

COMMAND_BOX = "BIM_Box"

def box(length=None, width=None, height=None, placement=None):
    """Crea una caja.

    Parámetros
    ----------
    length, width, height : float, opcional
        Dimensiones en mm. Si se omite alguna, se abre la herramienta
        interactiva de 4 clics sobre el plano de trabajo.
    placement : FreeCAD.Placement, opcional
        Posición y orientación de la caja creada por script.

    Devuelve
    --------
    El objeto Part::Box creado, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if length is None or width is None or height is None:
        FreeCADGui.runCommand(COMMAND_BOX)
        return None

    if length <= 0 or width <= 0 or height <= 0:
        raise RuntimeError("Las dimensiones de la caja deben ser mayores que cero.")

    doc.openTransaction("Box")
    try:
        result = doc.addObject("Part::Box", "Box")
        result.Length = length
        result.Width = width
        result.Height = height
        if placement is not None:
            result.Placement = placement
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result

# --- Column_Reinforcement ---
"""Column Reinforcement — Menú BIM → 3D/BIM → Reinforcement tools → Column Reinforcement.

Crea las barras de refuerzo (estribos y armaduras principales y secundarias en
X/Y) dentro de una columna modelada como Arch Structure.
Comando FreeCAD: Reinforcement_ColumnRebars (addon Reinforcement).
"""

COMMAND_COLUMN_REINFORCEMENT = "Reinforcement_ColumnRebars"
ADDON_MODULE = "ColumnReinforcement"

def column_reinforcement():
    """Abre el diálogo de refuerzo de columna sobre la cara seleccionada.

    Requiere una columna (Arch Structure) existente con una de sus caras
    seleccionada en la vista 3D y el addon Reinforcement instalado.

    Devuelve
    --------
    None. El objeto RebarGroup lo crea el diálogo al confirmar.
    """
    _require_document()
    _require_addon(ADDON_MODULE)
    _require_selected_face("una cara de la columna")
    FreeCADGui.runCommand(COMMAND_COLUMN_REINFORCEMENT)

# --- Component ---
"""Component — Menú BIM → 3D/BIM → Generic 3D tools → Component.

Convierte un objeto basado en Part en un componente Arch no paramétrico: le
agrega los atributos de componente (Additions, Subtractions, Material, Base,
Description, Tag) y permite definir su tipo de exportación IFC.
Comando FreeCAD: Arch_Component.
"""

COMMAND_COMPONENT = "Arch_Component"

def component():
    """Convierte la selección en componentes Arch no paramétricos.

    Requiere al menos un objeto sólido o con forma basada en Part, creado con
    cualquier workbench.

    Devuelve
    --------
    None. El componente lo crea el comando de FreeCAD.
    """
    _require_document()
    _require_part_selection()
    FreeCADGui.runCommand(COMMAND_COMPONENT)

# --- External_Reference ---
"""External Reference — Menú BIM → 3D/BIM → Generic 3D tools → External reference.

Inserta un enlace que copia la forma y los colores de un objeto que vive en
otro archivo de FreeCAD. Si el archivo de origen cambia, el objeto queda
marcado para recargarse desde su menú contextual.
Comando FreeCAD: Arch_Reference.
"""

import os

COMMAND_EXTERNAL_REFERENCE = "Arch_Reference"

def external_reference(file_path=None, part=None):
    """Inserta una referencia a un objeto de otro archivo de FreeCAD.

    Parámetros
    ----------
    file_path : str, opcional
        Ruta al archivo .FCStd de origen. Si se omite, se abre el panel
        interactivo con el botón "Choose file...".
    part : str, opcional
        Nombre del objeto a enlazar dentro de ese archivo. Si el archivo tiene
        varios objetos, conviene agruparlos antes en un Arch BuildingPart.

    Devuelve
    --------
    El objeto reference creado, o None en modo interactivo.
    """
    doc = _require_document()

    if file_path is None:
        FreeCADGui.runCommand(COMMAND_EXTERNAL_REFERENCE)
        return None

    if not os.path.isfile(file_path):
        raise RuntimeError("No existe el archivo: " + file_path)

    import Arch

    doc.openTransaction("External reference")
    try:
        result = Arch.makeReference(file_path, part)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result

# --- Facebinder ---
"""Facebinder — Menú BIM → 3D/BIM → Generic 3D tools → Facebinder.

Crea una superficie paramétrica a partir de las caras seleccionadas. Se
actualiza cuando cambia el objeto origen y puede extruirse, por ejemplo para
revestimientos de muros.
Comando FreeCAD: Draft_Facebinder (atajo F, F en Draft).
"""

COMMAND_FACEBINDER = "Draft_Facebinder"

def facebinder(extrusion=None):
    """Crea un atrapacaras sobre las caras seleccionadas.

    Parámetros
    ----------
    extrusion : float, opcional
        Espesor en mm con el que se extruye la superficie resultante. Si se
        omite, se abre la herramienta interactiva en la vista 3D (para un
        atrapacaras plano por script, pasar extrusion=0).

    Devuelve
    --------
    El objeto facebinder creado, o None en modo interactivo.
    """
    doc = _require_document()

    if extrusion is None:
        _require_3d_view()
        FreeCADGui.runCommand(COMMAND_FACEBINDER)
        return None

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

# --- Footing_Reinforcement ---
"""Footing Reinforcement — Menú BIM → 3D/BIM → Reinforcement tools → Footing Reinforcement.

Crea el refuerzo de una zapata modelada como Arch Structure: la malla de
barras paralelas y transversales, y opcionalmente las columnas con sus
estribos y armaduras principales y secundarias en X/Y.
Comando FreeCAD: Reinforcement_FootingRebars (addon Reinforcement).
"""

COMMAND_FOOTING_REINFORCEMENT = "Reinforcement_FootingRebars"
ADDON_MODULE = "FootingReinforcement"

# Caras de la zapata sobre las que se puede apoyar la malla.
MESH_COVER_ALONG = ("Top", "Bottom", "Both")

def footing_reinforcement():
    """Abre el diálogo de refuerzo de zapata sobre la cara seleccionada.

    Requiere una zapata (Arch Structure) existente con una de sus caras
    verticales seleccionada y el addon Reinforcement instalado.

    Devuelve
    --------
    None. El footingReinforcementGroup lo crea el diálogo al confirmar.
    """
    _require_document()
    _require_addon(ADDON_MODULE)
    _require_selected_face("una cara vertical de la zapata")
    FreeCADGui.runCommand(COMMAND_FOOTING_REINFORCEMENT)

# --- Objects_Library ---
"""Objects Library — Menú BIM → 3D/BIM → Generic 3D tools → Objects library.

Inserta en el modelo un objeto de equipamiento o mobiliario desde la Parts
Library, con un navegador integrado de archivos FCStd, STEP y BREP, local o
en línea desde el repositorio Git.
Comando FreeCAD: BIM_Library (addon Parts Library para el modo offline).
"""

COMMAND_OBJECTS_LIBRARY = "BIM_Library"

# Puntos de inserción que ofrece el panel para los archivos STEP y BREP.
INSERTION_POINTS = (
    "Original",
    "Top left",
    "Top center",
    "Top right",
    "Middle left",
    "Middle center",
    "Middle right",
    "Bottom left",
    "Bottom center",
    "Bottom right",
)

def objects_library():
    """Abre el navegador de la biblioteca de objetos.

    El archivo a insertar se elige en el panel. Los FCStd entran con su
    posición interna; los STEP y BREP piden además un punto de inserción y
    entran como Arch Equipment. El modo offline necesita el addon Parts
    Library instalado; el modo en línea usa el repositorio Git.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_OBJECTS_LIBRARY)

# --- Profile ---
"""Profile — Menú BIM → 3D/BIM → Generic 3D tools → Profile.

Crea un perfil paramétrico 2D (tubo circular C, H/I, rectangular R,
rectangular hueco RH, U, L o T) para usar como base de extrusiones: Arch
Frame, Curtain Wall, Part Extrude o Arch Structure.
Comando FreeCAD: Arch_Profile.
"""

COMMAND_PROFILE = "Arch_Profile"

# Clases de perfil admitidas por Arch.makeProfile.
PROFILE_CLASSES = ("C", "H", "R", "RH", "U", "L", "T")

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
        FreeCADGui.runCommand(COMMAND_PROFILE)
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

# --- Shape_Builder ---
"""Shape Builder — Menú BIM → 3D/BIM → Generic 3D tools → Shape builder...

Abre el constructor de formas de Part, que arma geometría más compleja a
partir de primitivas: arista desde 2 vértices, alambre desde aristas, cara
desde vértices o aristas, cascarón desde caras y sólido desde un cascarón.
Comando FreeCAD: Part_Builder.
"""

COMMAND_SHAPE_BUILDER = "Part_Builder"

def shape_builder():
    """Abre el panel del constructor de formas.

    Cada operación pide sus propios subelementos (vértices, aristas o caras),
    que se seleccionan dentro del panel antes de pulsar "Create"; "Solid from
    shell" no necesita selección previa.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_SHAPE_BUILDER)

# --- Slab_Reinforcement ---
"""Slab Reinforcement — Menú BIM → 3D/BIM → Reinforcement tools → Slab Reinforcement.

Crea un mallado de refuerzo dentro de una losa modelada como Arch Structure:
barras paralelas y transversales (rectas, L, U o curvas) con barras de
distribución opcionales.
Comando FreeCAD: Reinforcement_SlabRebars (addon Reinforcement).
"""

COMMAND_SLAB_REINFORCEMENT = "Reinforcement_SlabRebars"
ADDON_MODULE = "SlabReinforcement"

# Caras de la losa sobre las que se puede apoyar la malla.
MESH_COVER_ALONG = ("Top", "Bottom")

def slab_reinforcement():
    """Abre el diálogo de refuerzo de losa sobre la cara seleccionada.

    Requiere una losa (Arch Structure) existente con una de sus caras
    seleccionada y el addon Reinforcement instalado.

    Devuelve
    --------
    None. El SlabReinforcementGroup lo crea el diálogo al confirmar.
    """
    _require_document()
    _require_addon(ADDON_MODULE)
    _require_selected_face("una cara de la losa")
    FreeCADGui.runCommand(COMMAND_SLAB_REINFORCEMENT)

# --- Beam ---
Beam = {
    "beam": lambda: Gui.runCommand('BIM_Beam',0)
}

# --- Building ---
def _building():
    import Arch
    import Draft
    obj = Arch.makeBuilding()
    Draft.autogroup(obj)

Building = {
    "building": _building
}

# --- Column ---
Column = {
    "column": lambda: Gui.runCommand('BIM_Column',0)
}

# --- CurtainWall ---
# (typo upstream "CuratainWall" corregido para que resuelva el diccionario)
CurtainWall = {
    "curtainwall": lambda: Gui.runCommand('Arch_CurtainWall',0)
}

# --- Door ---
Door = {
    "door": lambda: Gui.runCommand('BIM_Door',0)
}

# --- Level ---
def _level():
    import Draft
    import Arch
    import WorkingPlane
    obj = Arch.makeFloor(FreeCADGui.Selection.getSelection())
    obj.Placement = WorkingPlane.get_working_plane().get_placement()
    Draft.autogroup(obj)

Level = {
    "level": _level
}

# --- Pipe ---
def _pipe():
    import Arch
    import Draft
    obj = Arch.makePipe()
    Draft.autogroup(obj)

Pipe = {
    "pipe": _pipe
}

# --- PipeConnector ---
PipeConnector = {
    "pipe connector": lambda: Gui.runCommand('Arch_PipeConnector',0)
}

# --- Roof ---
Roof = {
    "roof": lambda: Gui.runCommand('Arch_Roof',0)
}

# --- Site ---
def _site():
    import Arch
    import Draft
    obj = Arch.makeSite()
    Draft.autogroup(obj)

Site = {
    "site": _site
}

# --- Slab ---
Slab = {
    "slab": lambda: Gui.runCommand('BIM_Slab',0)
}

# --- Space ---
Space = {
    "space": lambda: Gui.runCommand('Arch_Space',0)
}

# --- Wall ---
Wall = {
    "wall": lambda: Gui.runCommand('Arch_Wall',0)
}

# --- Window ---
Window = {
    "window": lambda: Gui.runCommand('Arch_Window',0)
}

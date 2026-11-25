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
try:
    import FreeCAD
    import FreeCADGui
    import FreeCADGui as Gui
except ImportError:
    FreeCAD = None  # type: ignore[assignment]
    FreeCADGui = None  # type: ignore[assignment]
    Gui = None  # type: ignore[assignment]


class _ParamSpec:
    """Especificacion de parametro compatible con Validator y ParameterCollector."""

    def __init__(self, index: int, name: str, param_type: type, required: bool = True) -> None:
        self.index = index
        self.name = name
        self.param_type = param_type
        self.required = required


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
    if not hasattr(FreeCADGui, "ActiveDocument") or not hasattr(FreeCADGui, "activeView"):
        return
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

def box(
    length: float = 1000.0,
    width: float = 1000.0,
    height: float = 1000.0,
    placement=None,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una caja.

    Parámetros
    ----------
    length, width, height : float, opcional
        Dimensiones en mm. Si se omite alguna o es None, se abre la herramienta
        interactiva de 4 clics sobre el plano de trabajo.
    placement : FreeCAD.Placement, opcional
        Posición y orientación de la caja creada por script.

    Devuelve
    --------
    El objeto Part::Box creado, o None en modo interactivo.
    """
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()

    if length is None or width is None or height is None:
        if FreeCADGui and hasattr(FreeCADGui, "runCommand"):
            FreeCADGui.runCommand(COMMAND_BOX)
        return None

    if length <= 0 or width <= 0 or height <= 0:
        raise RuntimeError("Las dimensiones de la caja deben ser mayores que cero.")

    if doc is None:
        return None

    if hasattr(doc, "openTransaction"):
        doc.openTransaction("Box")
    try:
        result = doc.addObject("Part::Box", "Box")
        result.Length = length
        result.Width = width
        result.Height = height
        if placement is not None:
            result.Placement = placement
        elif FreeCAD and hasattr(FreeCAD, "Placement"):
            result.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation())
    except Exception:
        if hasattr(doc, "abortTransaction"):
            doc.abortTransaction()
        raise
    if hasattr(doc, "commitTransaction"):
        doc.commitTransaction()
    if hasattr(doc, "recompute"):
        doc.recompute()
    return result


box._param_specs = [
    _ParamSpec(1, "length", float, True),
    _ParamSpec(2, "width", float, True),
    _ParamSpec(3, "height", float, True),
    _ParamSpec(4, "x", float, True),
    _ParamSpec(5, "y", float, True),
    _ParamSpec(6, "z", float, True),
]

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
def beam(
    length: float = 4000.0,
    width: float = 200.0,
    height: float = 400.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una viga Arch / Structure con las dimensiones indicadas."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft

        b = Arch.makeStructure(length=length, width=width, height=height)
        if hasattr(b, "Role"):
            b.Role = "Beam"
        if FreeCAD and hasattr(b, "Placement"):
            b.Placement.Base = FreeCAD.Vector(x, y, z)
        Draft.autogroup(b)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return b
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("BIM_Beam", 0)
        return None


beam._param_specs = [
    _ParamSpec(1, "length", float, True),
    _ParamSpec(2, "width", float, True),
    _ParamSpec(3, "height", float, True),
    _ParamSpec(4, "x", float, True),
    _ParamSpec(5, "y", float, True),
    _ParamSpec(6, "z", float, True),
]

Beam = {"beam": beam}

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
def column(
    length: float = 300.0,
    width: float = 300.0,
    height: float = 3000.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una columna Arch / Structure con las dimensiones indicadas."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft

        col = Arch.makeStructure(length=length, width=width, height=height)
        if hasattr(col, "Role"):
            col.Role = "Column"
        if FreeCAD and hasattr(col, "Placement"):
            col.Placement.Base = FreeCAD.Vector(x, y, z)
        Draft.autogroup(col)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return col
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("BIM_Column", 0)
        return None


column._param_specs = [
    _ParamSpec(1, "length", float, True),
    _ParamSpec(2, "width", float, True),
    _ParamSpec(3, "height", float, True),
    _ParamSpec(4, "x", float, True),
    _ParamSpec(5, "y", float, True),
    _ParamSpec(6, "z", float, True),
]

Column = {"column": column}

# --- CurtainWall ---
# (typo upstream "CuratainWall" corregido para que resuelva el diccionario)
CurtainWall = {
    "curtainwall": lambda: Gui.runCommand('Arch_CurtainWall',0)
}

# --- Door ---
def door(
    width: float = 900.0,
    height: float = 2100.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una puerta con ancho y alto especificados en la posición (x, y, z)."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft
        try:
            d = Arch.makeWindowPreset("Simple door", float(width), float(height), 50.0, 50.0, 50.0, 100.0, 50.0, 0.0, 0.0)
        except Exception:
            d = Arch.makeWindow(width=float(width), height=float(height))
        if d and FreeCAD and hasattr(d, "Placement"):
            d.Placement.Base = FreeCAD.Vector(float(x), float(y), float(z))
        if hasattr(Draft, "autogroup"):
            Draft.autogroup(d)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return d
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("BIM_Door", 0)
        return None


door._param_specs = [
    _ParamSpec(1, "width", float, True),
    _ParamSpec(2, "height", float, True),
    _ParamSpec(3, "x", float, True),
    _ParamSpec(4, "y", float, True),
    _ParamSpec(5, "z", float, True),
]

Door = {"door": door}

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
def pipe(
    length: float = 2000.0,
    diameter: float = 50.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea un tubo paramétrico en la posición (x, y, z)."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft

        p1 = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        p2 = FreeCAD.Vector(x + length, y, z) if FreeCAD else (x + length, y, z)
        base = Draft.make_line(p1, p2)
        p_obj = Arch.makePipe(base, diameter=diameter)
        if hasattr(Draft, "autogroup"):
            Draft.autogroup(p_obj)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return p_obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Arch_Pipe", 0)
        return None


pipe._param_specs = [
    _ParamSpec(1, "length", float, True),
    _ParamSpec(2, "diameter", float, True),
    _ParamSpec(3, "x", float, True),
    _ParamSpec(4, "y", float, True),
    _ParamSpec(5, "z", float, True),
]

Pipe = {"pipe": pipe}

# --- PipeConnector ---
PipeConnector = {
    "pipe connector": lambda: Gui.runCommand('Arch_PipeConnector',0)
}

# --- Roof ---
def roof(
    length: float = 6000.0,
    width: float = 4000.0,
    thickness: float = 150.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 3000.0,
):
    """Crea una cubierta / techo paramétrico a partir de sus dimensiones y posición."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft

        p1 = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        p2 = FreeCAD.Vector(x + length, y, z) if FreeCAD else (x + length, y, z)
        p3 = FreeCAD.Vector(x + length, y + width, z) if FreeCAD else (x + length, y + width, z)
        p4 = FreeCAD.Vector(x, y + width, z) if FreeCAD else (x, y + width, z)
        wire = None
        if hasattr(Draft, "make_wire"):
            try:
                wire = Draft.make_wire([p1, p2, p3, p4], closed=True)
            except Exception:
                wire = None
        if wire is None and hasattr(Draft, "make_rectangle"):
            try:
                wire = Draft.make_rectangle(length, width)
            except Exception:
                wire = None
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        if hasattr(Arch, "makeRoof"):
            r = Arch.makeRoof(wire, angles=[30.0], thickness=[float(thickness)])
        else:
            r = None
        if r and hasattr(Draft, "autogroup"):
            Draft.autogroup(r)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return r
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Arch_Roof", 0)
        return None


roof._param_specs = [
    _ParamSpec(1, "length", float, True),
    _ParamSpec(2, "width", float, True),
    _ParamSpec(3, "thickness", float, True),
    _ParamSpec(4, "x", float, True),
    _ParamSpec(5, "y", float, True),
    _ParamSpec(6, "z", float, True),
]

Roof = {"roof": roof}

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
def slab(
    length: float = 4000.0,
    width: float = 3000.0,
    thickness: float = 150.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una losa Arch / Structure con las dimensiones indicadas."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft

        sl = Arch.makeStructure(length=length, width=width, height=thickness)
        if hasattr(sl, "Role"):
            sl.Role = "Slab"
        if FreeCAD and hasattr(sl, "Placement"):
            sl.Placement.Base = FreeCAD.Vector(x, y, z)
        Draft.autogroup(sl)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return sl
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("BIM_Slab", 0)
        return None


slab._param_specs = [
    _ParamSpec(1, "length", float, True),
    _ParamSpec(2, "width", float, True),
    _ParamSpec(3, "thickness", float, True),
    _ParamSpec(4, "x", float, True),
    _ParamSpec(5, "y", float, True),
    _ParamSpec(6, "z", float, True),
]

Slab = {"slab": slab}

# --- Space ---
Space = {
    "space": lambda: Gui.runCommand('Arch_Space',0)
}

# --- Wall ---
def wall(
    length: float = 5000.0,
    width: float = 200.0,
    height: float = 3000.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea un muro Arch a partir de sus dimensiones o abre la herramienta interactiva."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft

        p1 = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        p2 = FreeCAD.Vector(x + length, y, z) if FreeCAD else (x + length, y, z)
        base_line = Draft.make_line(p1, p2)
        wall_obj = Arch.makeWall(base_line, width=width, height=height)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return wall_obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Arch_Wall", 0)
        return None


wall._param_specs = [
    _ParamSpec(1, "length", float, True),
    _ParamSpec(2, "width", float, True),
    _ParamSpec(3, "height", float, True),
    _ParamSpec(4, "x", float, True),
    _ParamSpec(5, "y", float, True),
    _ParamSpec(6, "z", float, True),
]

Wall = {"wall": wall}

# --- Window ---
def window(
    width: float = 1200.0,
    height: float = 1200.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una ventana con ancho y alto especificados en la posición (x, y, z)."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft
        try:
            w = Arch.makeWindowPreset("Open 1-pane", float(width), float(height), 50.0, 50.0, 50.0, 100.0, 50.0, 0.0, 0.0)
        except Exception:
            w = Arch.makeWindow(width=float(width), height=float(height))
        if w and FreeCAD and hasattr(w, "Placement"):
            w.Placement.Base = FreeCAD.Vector(float(x), float(y), float(z))
        if hasattr(Draft, "autogroup"):
            Draft.autogroup(w)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return w
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Arch_Window", 0)
        return None


window._param_specs = [
    _ParamSpec(1, "width", float, True),
    _ParamSpec(2, "height", float, True),
    _ParamSpec(3, "x", float, True),
    _ParamSpec(4, "y", float, True),
    _ParamSpec(5, "z", float, True),
]

Window = {"window": window}

# --- ArchEquipment ---
ArchEquipment = {
    "arch equipment": lambda: Gui.runCommand('Arch_Equipment', 0)
}

# --- ArchFence ---
ArchFence = {
    "arch fence": lambda: Gui.runCommand('Arch_Fence', 0)
}

# --- ArchFrame ---
ArchFrame = {
    "arch frame": lambda: Gui.runCommand('Arch_Frame', 0)
}

# --- ArchPanel ---
ArchPanel = {
    "arch panel": lambda: Gui.runCommand('Arch_Panel', 0)
}

# --- ArchRebar ---
ArchRebar = {
    "arch rebar": lambda: Gui.runCommand('Arch_Rebar', 0)
}

# --- ArchRoof ---
ArchRoof = {
    "arch roof": roof
}

# --- ArchStairs ---
def stairs(
    steps: int = 17,
    step_length: float = 280.0,
    step_height: float = 175.0,
    step_width: float = 1000.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una escalera paramétrica en la posición (x, y, z)."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Arch
        import Draft

        st = Arch.makeStairs(
            steps=int(steps),
            length=float(steps) * float(step_length),
            height=float(steps) * float(step_height),
            width=float(step_width),
        )
        if st and FreeCAD and hasattr(st, "Placement"):
            st.Placement.Base = FreeCAD.Vector(float(x), float(y), float(z))
        if hasattr(Draft, "autogroup"):
            Draft.autogroup(st)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return st
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Arch_Stairs", 0)
        return None


stairs._param_specs = [
    _ParamSpec(1, "steps", int, True),
    _ParamSpec(2, "step_length", float, True),
    _ParamSpec(3, "step_height", float, True),
    _ParamSpec(4, "step_width", float, True),
    _ParamSpec(5, "x", float, True),
    _ParamSpec(6, "y", float, True),
    _ParamSpec(7, "z", float, True),
]

def _stairs():
    return stairs()

# --- Comandos BIM y Rebars complementarios ---

def CurtainWall():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("BIM_CurtainWall", 0)

def ArchEquipment():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_Equipment", 0)

def ArchFence():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("BIM_Fence", 0)

def ArchFrame():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_Frame", 0)

def ArchPanel():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_Panel", 0)

def ArchRebar():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_Rebar", 0)

def ArchTruss():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_Truss", 0)

def PipeConnector():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_PipeConnector", 0)

def Space():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_Space", 0)

def BentShapeRebar():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_RebarTools", 5)

def HelicalRebar():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_RebarTools", 6)

def LShapeRebar():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_RebarTools", 3)

def StirrupRebar():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_RebarTools", 4)

def StraightRebar():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_RebarTools", 1)

def UShapeRebar():
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_RebarTools", 2)

# Alias canónicos exportados para TraduceToEs y TraduceToEn

class _CommandDict(dict):
    """Contenedor híbrido dict + callable:
    - Es un dict {'nombre': func} para compatibilidad con la suite de workbench.
    - Es un callable ejecutable directamente por el motor de voz y Browser.
    """
    def __init__(self, key: str, func):
        if isinstance(func, dict):
            inner = next(iter(func.values())) if func else func
            func = inner if callable(inner) else func
        super().__init__({key: func})
        self.key = key
        self.func = func
        self._param_specs = getattr(func, "_param_specs", None)

    def __call__(self, *args, **kwargs):
        if callable(self.func):
            return self.func(*args, **kwargs)
        return None

    @property
    def __name__(self):
        name = getattr(self.func, "__name__", None)
        if name and not name.startswith("<"):
            return name
        return self.key

# Alias híbridos canónicos
Beam = _CommandDict("beam", beam)
Box = _CommandDict("box", box)
Building = _CommandDict("building", _building)
Column = _CommandDict("column", column)
Component = _CommandDict("component", component)
CurtainWall = _CommandDict("curtain_wall", CurtainWall)
Door = _CommandDict("door", door)
Level = _CommandDict("level", _level)
Pipe = _CommandDict("pipe", pipe)
PipeConnector = _CommandDict("pipe_connector", PipeConnector)
Roof = _CommandDict("roof", Roof)
Site = _CommandDict("site", _site)
Slab = _CommandDict("slab", slab)
Space = _CommandDict("space", Space)
Stairs = _CommandDict("stairs", stairs)
ArchStairs = _CommandDict("arch_stairs", stairs)
Wall = _CommandDict("wall", wall)
Window = _CommandDict("window", window)
Beam_Reinforcement = _CommandDict("beam_reinforcement", beam_reinforcement)
Column_Reinforcement = _CommandDict("column_reinforcement", column_reinforcement)
Footing_Reinforcement = _CommandDict("footing_reinforcement", footing_reinforcement)
Slab_Reinforcement = _CommandDict("slab_reinforcement", slab_reinforcement)
External_Reference = _CommandDict("external_reference", external_reference)
Facebinder = _CommandDict("facebinder", facebinder)
Objects_Library = _CommandDict("objects_library", objects_library)
Profile = _CommandDict("profile", profile)
Shape_Builder = _CommandDict("shape_builder", shape_builder)
ArchEquipment = _CommandDict("arch_equipment", ArchEquipment)
ArchFence = _CommandDict("arch_fence", ArchFence)
ArchFrame = _CommandDict("arch_frame", ArchFrame)
ArchPanel = _CommandDict("arch_panel", ArchPanel)
ArchRebar = _CommandDict("arch_rebar", ArchRebar)
ArchRoof = _CommandDict("arch_roof", ArchRoof)
ArchTruss = _CommandDict("arch_truss", ArchTruss)
BentShapeRebar = _CommandDict("bent_shape_rebar", BentShapeRebar)
HelicalRebar = _CommandDict("helical_rebar", HelicalRebar)
LShapeRebar = _CommandDict("l_shape_rebar", LShapeRebar)
StirrupRebar = _CommandDict("stirrup_rebar", StirrupRebar)
StraightRebar = _CommandDict("straight_rebar", StraightRebar)
UShapeRebar = _CommandDict("u_shape_rebar", UShapeRebar)

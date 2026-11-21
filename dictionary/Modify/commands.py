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

"""Comandos FreeCAD de la seccion Modify (consolidado).

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
try:
    from .ayuda import ayuda
except ImportError:  # modulo de ayuda aun no migrado
    ayuda = None


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

def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


# --- AddComponent ---
def AddComponent():
    """Añade objetos basados en formas a un componente BIM, a grupos, sistemas de ejes o planos de sección."""
    Gui.runCommand('Arch_Add', 0)

addcomponent_cmds = {
    'añadir componente': AddComponent,
    'agregar componente': AddComponent,
    'unir objeto a componente': AddComponent,
    'asignar elemento bim': AddComponent,
    'help': ayuda,
}

# --- Array ---
def Array():
    """Crea una matriz u ordenación ortogonal en 3 ejes a partir de un objeto seleccionado."""
    Gui.runCommand('Draft_OrthoArray', 0)

array_cmds = {
    'crear array': Array,
    'generar array': Array,
    'crear matriz ortogonal': Array,
    'duplicar en array': Array,
    'help': ayuda,
}

# --- Clone ---
"""Clone — Menú BIM → Modify → Cloning Tools → Clone.

Crea un clon (copia enlazada) de cada objeto seleccionado: si el original
cambia, el clon también se actualiza.
Comando FreeCAD: BIM_Clone (atajo C, L).
"""

COMMAND_CLONE = "BIM_Clone"

def clone(dx: float = 100.0, dy: float = 0.0, dz: float = 0.0, delta=None):
    """Clona la selección actual.

    Parámetros
    ----------
    dx, dy, dz : float, opcionales
        Desplazamiento del clon respecto del original en mm.
    delta : FreeCAD.Vector | tuple, opcional
        Vector de desplazamiento directo.

    Devuelve
    --------
    Lista de clones creados, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para clonar.")

    if delta is None:
        if dx == 0.0 and dy == 0.0 and dz == 0.0:
            FreeCADGui.runCommand(COMMAND_CLONE)
            return None
        delta = (dx, dy, dz)

    import Draft

    delta = FreeCAD.Vector(delta)
    doc.openTransaction("Clone")
    try:
        clones = [Draft.make_clone(obj, delta=delta) for obj in selection]
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return clones


clone._param_specs = [
    _ParamSpec(1, "dx", float, True),
    _ParamSpec(2, "dy", float, True),
]

# --- Compound ---
"""Compound — Menú BIM → Modify → Compound.

Agrupa las formas seleccionadas en un único objeto Part::Compound.
Comando FreeCAD: BIM_Compound (delega en Part_Compound).
"""

COMMAND_COMPOUND = "BIM_Compound"


def compound(interactive=False):
    """Crea un Part::Compound con los objetos seleccionados.

    Igual que Part_Compound, oculta los objetos originales, que pasan a ser
    hijos del compuesto.

    Parámetros
    ----------
    interactive : bool
        Si es True, abre la herramienta interactiva de FreeCAD en lugar de
        ejecutar la lógica por script.

    Devuelve
    --------
    El objeto Part::Compound creado, o None en modo interactivo.
    """
    doc = _require_document()

    if interactive:
        _require_3d_view()
        FreeCADGui.runCommand(COMMAND_COMPOUND)
        return None

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

# --- Copy ---
"""Copy — Menú BIM → Modify → Copy.

Copia los objetos seleccionados a una nueva ubicación (Move en modo copia).
Comando FreeCAD: BIM_Copy (atajo C, P).
"""

COMMAND_COPY = "BIM_Copy"

def copy(vector=None):
    """Copia la selección actual desplazándola según un vector.

    Parámetros
    ----------
    vector : FreeCAD.Vector | tuple, opcional
        Desplazamiento (X, Y, Z) en mm desde el original hasta la copia.
        Si se omite, se abre la herramienta interactiva para marcar punto
        base y punto destino en la vista 3D.

    Devuelve
    --------
    Las copias creadas, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if vector is None:
        FreeCADGui.runCommand(COMMAND_COPY)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para copiar.")

    import Draft

    doc.openTransaction("Copy")
    try:
        result = Draft.move(selection, FreeCAD.Vector(vector), copy=True)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result

# --- Downgrade ---
def Downgrade():
    """Degrada o reduce de nivel los objetos seleccionados."""
    Gui.runCommand('Draft_Downgrade', 0)

downgrade_cmds = {
    'degradar elemento': Downgrade,
    'bajar nivel': Downgrade,
    'downgrade objeto': Downgrade,
    'descomponer objeto': Downgrade,
    'help': ayuda,
}

# --- DraftToSketch ---
def DraftToSketch():
    """Convierte objetos de Draft a bocetos/croquis de Sketcher y viceversa."""
    Gui.runCommand('Draft_Draft2Sketch', 0)

drafttosketch_cmds = {
    'convertir a croquis': DraftToSketch,
    'draft a croquis': DraftToSketch,
    'convertir a sketch': DraftToSketch,
    'pasar a boceto': DraftToSketch,
    'help': ayuda,
}

# --- Edit ---
def Edit():
    """Pone los objetos seleccionados en modo de edición de Draft, permitiendo editar sus propiedades gráficamente."""
    Gui.runCommand('Draft_Edit', 0)

edit_cmds = {
    'editar elemento': Edit,
    'modo edición': Edit,
    'editar nodos': Edit,
    'modificar gráfico': Edit,
    'help': ayuda,
}

# --- Join ---
def Join():
    """Une líneas (Draft Lines) y alambres (Draft Wires) en un solo alambre continuo (wire)."""
    Gui.runCommand('Draft_Join', 0)

join_cmds = {
    'unir elementos': Join,
    'juntar líneas': Join,
    'unir alambres': Join,
    'generar alambre único': Join,
    'help': ayuda,
}

# --- MakeLink ---
"""Make Link — Menú BIM → Modify → Cloning Tools → Make Link.

Crea un App::Link por cada objeto seleccionado: una referencia liviana que
reutiliza la forma del original sin duplicar datos. Después entra en modo
Mover para reubicar los enlaces.
Comando FreeCAD: BIM_LinkMake (atajo L, K).
"""

MOVE_COMMAND = "Draft_Move"

def make_link(start_move=True):
    """Crea un enlace (App::Link) a cada objeto seleccionado.

    Parámetros
    ----------
    start_move : bool
        Si es True (por defecto, igual que en BIM), deja seleccionados los
        enlaces creados y abre la herramienta Mover para reubicarlos.

    Devuelve
    --------
    Lista de enlaces creados.
    """
    doc = _require_document()

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para enlazar.")

    doc.openTransaction("Make Link")
    try:
        links = []
        for obj in selection:
            link = doc.addObject("App::Link", obj.Name + "_Link")
            link.LinkedObject = obj
            link.Label = obj.Label + "_Link"
            if hasattr(obj, "Placement"):
                link.Placement = obj.Placement
            links.append(link)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()

    if start_move:
        FreeCADGui.Selection.clearSelection()
        for link in links:
            FreeCADGui.Selection.addSelection(link)
        FreeCADGui.runCommand(MOVE_COMMAND)

    return links

# --- Mirror ---
"""Mirror — Menú BIM → Modify → Mirror.

Refleja los objetos seleccionados respecto de una línea definida por dos
puntos (sobre el plano de trabajo actual).
Comando FreeCAD: Draft_Mirror (atajo M, I).
"""

COMMAND_MIRROR = "Draft_Mirror"

def mirror(
    x1: float = 0.0,
    y1: float = 0.0,
    x2: float = 0.0,
    y2: float = 100.0,
    p1=None,
    p2=None,
):
    """Crea la imagen especular de la selección actual.

    Parámetros
    ----------
    x1, y1, x2, y2 : float, opcionales
        Coordenadas de los dos puntos que definen la línea de espejo en mm.
    p1, p2 : FreeCAD.Vector | tuple, opcionales
        Puntos que definen la línea de espejo.

    Devuelve
    --------
    Los objetos Part::Mirroring creados, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if p1 is None and p2 is None:
        p1 = (x1, y1, 0.0)
        p2 = (x2, y2, 0.0)

    p1 = FreeCAD.Vector(p1)
    p2 = FreeCAD.Vector(p2)
    if p1.isEqual(p2, 1e-7):
        raise ValueError("Los dos puntos de la línea de espejo deben ser distintos.")

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para espejar.")

    import Draft

    doc.openTransaction("Mirror")
    try:
        result = Draft.mirror(selection, p1, p2)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result


mirror._param_specs = [
    _ParamSpec(1, "x1", float, True),
    _ParamSpec(2, "y1", float, True),
    _ParamSpec(3, "x2", float, True),
    _ParamSpec(4, "y2", float, True),
]

# --- Move ---
"""Move — Menú BIM → Modify → Move.

Mueve los objetos seleccionados según un vector de desplazamiento.
Comando FreeCAD: Draft_Move (atajo M, V).
"""

COMMAND_MOVE = "Draft_Move"

def move(
    dx: float = 0.0,
    dy: float = 0.0,
    dz: float = 0.0,
    vector=None,
    copy=False,
):
    """Mueve la selección actual.

    Parámetros
    ----------
    dx, dy, dz : float, opcionales
        Desplazamiento en X, Y, Z en mm.
    vector : FreeCAD.Vector | tuple, opcional
        Desplazamiento directo. Si se omite y dx=dy=dz=0, abre la herramienta interactiva.
    copy : bool
        Si es True, crea copias desplazadas en lugar de mover los originales.

    Devuelve
    --------
    Los objetos movidos (o las copias creadas), o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if vector is None:
        if dx == 0.0 and dy == 0.0 and dz == 0.0:
            FreeCADGui.runCommand(COMMAND_MOVE)
            return None
        vector = (dx, dy, dz)

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para mover.")

    import Draft

    doc.openTransaction("Move")
    try:
        result = Draft.move(selection, FreeCAD.Vector(vector), copy=copy)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result


move._param_specs = [
    _ParamSpec(1, "dx", float, True),
    _ParamSpec(2, "dy", float, True),
]

# --- Offset ---
def Offset():
    """Desfasa cada segmento de un objeto seleccionado a una distancia determinada, o crea una copia desfasada del objeto seleccionado."""
    Gui.runCommand('Draft_Offset', 0)

offset_cmds = {
    'offset': Offset,
    'desfase': Offset,
    'crear desfase': Offset,
    'generar offset': Offset,
    'aplicar desfase': Offset,
    'duplicar contorno': Offset,
    'help': ayuda,
}

# --- Offset2D ---
def Offset2D():
    """Construye un alambre paralelo al alambre original a una distancia determinada, o amplía/reduce una cara plana."""
    Gui.runCommand('Part_Offset2D', 0)

offset2d_cmds = {
    'offset2d': Offset2D,
    'desfase2d': Offset2D,
    'help': ayuda,
}

# --- PathArray ---
def PathArray():
    """Crea una matriz o arreglo regular a partir de un objeto seleccionado distribuyendo copias a lo largo de una trayectoria (path)."""
    Gui.runCommand('Draft_PathArray', 0)

patharray_cmds = {
    'path array': PathArray,
    'matriz sobre trayectoria': PathArray,
    'crear path array': PathArray,
    'generar path array': PathArray,
    'crear matriz sobre trayectoria': PathArray,
    'duplicar en curva': PathArray,
    'help': ayuda,
}

# --- RemoveComponent ---
def RemoveComponent():
    """Permite realizar dos tipos de operaciones: quitar un subcomponente de un objeto BIM o sustraer un objeto basado en forma de un componente BIM."""
    Gui.runCommand('Arch_Remove', 0)

removecomponent_cmds = {
    'remove component': RemoveComponent,
    'quitar componente': RemoveComponent,
    'eliminar componente': RemoveComponent,
    'remover componente': RemoveComponent,
    'sustraer objeto': RemoveComponent,
    'desvincular elemento bim': RemoveComponent,
    'help': ayuda,
}

# --- Rotate ---
"""Rotate — Menú BIM → Modify → Rotate.

Rota los objetos seleccionados un ángulo alrededor de un centro y un eje.
Comando FreeCAD: Draft_Rotate (atajo R, O).
"""

COMMAND_ROTATE = "Draft_Rotate"

def rotate(
    angle: float = 90.0,
    center=(0, 0, 0),
    axis=(0, 0, 1),
    copy: bool = False,
    center_x: float = 0.0,
    center_y: float = 0.0,
    center_z: float = 0.0,
):
    """Rota la selección actual.

    Parámetros
    ----------
    angle : float, opcional
        Ángulo en grados. Si se omite, se abre la herramienta interactiva
        para marcar centro y ángulo en la vista 3D.
    center : FreeCAD.Vector | tuple
        Centro de rotación. Por defecto el origen.
    axis : FreeCAD.Vector | tuple
        Eje de rotación. Por defecto Z.
    copy : bool
        Si es True, crea copias rotadas en lugar de rotar los originales.

    Devuelve
    --------
    Los objetos rotados (o las copias creadas), o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if angle is None:
        FreeCADGui.runCommand(COMMAND_ROTATE)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para rotar.")

    import Draft

    if center == (0, 0, 0) and (center_x or center_y or center_z):
        center = (center_x, center_y, center_z)

    doc.openTransaction("Rotate")
    try:
        result = Draft.rotate(
            selection,
            float(angle),
            center=FreeCAD.Vector(center),
            axis=FreeCAD.Vector(axis),
            copy=copy,
        )
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result


rotate._param_specs = [
    _ParamSpec(1, "angle", float, True),
]

# --- Scale ---
"""Scale — Menú BIM → Modify → Scale.

Escala los objetos seleccionados desde un punto base, con factores
independientes en X, Y y Z.
Comando FreeCAD: Draft_Scale (atajo S, C).
"""

COMMAND_SCALE = "Draft_Scale"

def scale(
    factor: float = 2.0,
    center=(0, 0, 0),
    copy: bool = False,
    clone: bool = False,
    center_x: float = 0.0,
    center_y: float = 0.0,
    center_z: float = 0.0,
):
    """Escala la selección actual.

    Parámetros
    ----------
    factor : float | FreeCAD.Vector | tuple, opcional
        Un número escala igual en los tres ejes; un vector (X, Y, Z) escala
        cada eje por separado. Si se omite, se abre la herramienta
        interactiva.
    center : FreeCAD.Vector | tuple
        Punto base de la escala. Por defecto el origen.
    copy : bool
        Si es True, crea una copia escalada y deja el original.
    clone : bool
        Si es True, crea un clon escalado y deja el original.

    Devuelve
    --------
    Los objetos escalados (o las copias/clones), o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if factor is None:
        FreeCADGui.runCommand(COMMAND_SCALE)
        return None

    if copy and clone:
        raise ValueError("Elegí copy o clone, no ambos.")

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para escalar.")

    if center == (0, 0, 0) and (center_x or center_y or center_z):
        center = (center_x, center_y, center_z)

    if isinstance(factor, (int, float)):
        factor = (factor, factor, factor)
    factor = FreeCAD.Vector(factor)
    if 0 in (factor.x, factor.y, factor.z):
        raise ValueError("El factor de escala no puede ser 0 en ningún eje.")

    import Draft

    doc.openTransaction("Scale")
    try:
        result = Draft.scale(
            selection,
            factor,
            center=FreeCAD.Vector(center),
            copy=copy,
            clone=clone,
        )
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result


scale._param_specs = [
    _ParamSpec(1, "factor", float, True),
]

# --- SimpleCopy ---
"""Simple Copy — Menú BIM → Modify → Simple Copy.

Crea una copia no paramétrica ("congelada") de la forma de cada objeto
seleccionado, sin historial ni vínculo con el original.
Comando FreeCAD: BIM_SimpleCopy (delega en Part_SimpleCopy).
"""

COMMAND_SIMPLE_COPY = "BIM_SimpleCopy"


def simple_copy(interactive=False):
    """Crea un Part::Feature con la forma actual de cada objeto seleccionado.

    Parámetros
    ----------
    interactive : bool
        Si es True, abre la herramienta interactiva de FreeCAD en lugar de
        ejecutar la lógica por script.

    Devuelve
    --------
    Lista de copias creadas, o None en modo interactivo.
    """
    doc = _require_document()

    if interactive:
        _require_3d_view()
        FreeCADGui.runCommand(COMMAND_SIMPLE_COPY)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para copiar.")

    import Part

    doc.openTransaction("Simple Copy")
    try:
        copies = []
        for obj in selection:
            shape = Part.getShape(obj, "", needSubElement=False, refine=False)
            if shape.isNull():
                FreeCAD.Console.PrintWarning(
                    "{} no tiene forma, se omite.\n".format(obj.Label)
                )
                continue
            new = doc.addObject("Part::Feature", obj.Name)
            new.Shape = shape
            new.Label = obj.Label + " (copia)"
            copies.append(new)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return copies

# --- Split ---
def Split():
    """Divide una línea (Draft Line) o un alambre (Draft Wire) en un punto o borde especificado."""
    Gui.runCommand('Draft_Split', 0)

split_cmds = {
    'split': Split,
    'dividir': Split,
    'dividir elemento': Split,
    'cortar línea': Split,
    'separar alambre': Split,
    'escindir objeto': Split,
    'help': ayuda,
}

# --- Stretch ---
def Stretch():
    """Estira objetos moviendo los puntos o vértices seleccionados dentro de un área determinada."""
    Gui.runCommand('Draft_Stretch', 0)

stretch_cmds = {
    'stretch': Stretch,
    'estirar': Stretch,
    'estirar elemento': Stretch,
    'aplicar stretch': Stretch,
    'mover vértices': Stretch,
    'deformar objeto': Stretch,
    'help': ayuda,
}

# --- Trimex ---
def Trimex():
    """Recorta o extiende un objeto de Draft seleccionado o un objeto BIM compatible."""
    Gui.runCommand('Draft_Trimex', 0)

trimex_cmds = {
    'trimex': Trimex,
    'recortar o extender': Trimex,
    'ejecutar trimex': Trimex,
    'recortar elemento': Trimex,
    'extender elemento': Trimex,
    'help': ayuda,
}

# --- Upgrade ---
def Upgrade():
    """Promueve o sube de nivel los objetos seleccionados."""
    Gui.runCommand('Draft_Upgrade', 0)

upgrade_cmds = {
    'upgrade': Upgrade,
    'promover': Upgrade,
    'promover elemento': Upgrade,
    'elevar nivel': Upgrade,
    'upgrade objeto': Upgrade,
    'convertir a cara': Upgrade,
    'help': ayuda,
}
# --- Comandos Booleanos, Extrusión y Arreglos ---

def Extrude(length: float = 0.0):
    """Extruye un boceto, cara o forma seleccionada."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Part_Extrude", 0)

Extrude._param_specs = [
    _ParamSpec(1, "length", float, True),
]

def ExtrudeFace():
    """Extruye una sola cara plana seleccionada de un objeto."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Draft_Extrude", 0)

def CutWithPlane():
    """Corta un objeto solido de tipo Arch utilizando un plano o cara plana."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Arch_CutPlane", 0)

def Union():
    """Une dos o mas formas seleccionadas en un unico objeto solido (Fusion)."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Part_Fuse", 0)

def Difference():
    """Corta (resta) una forma de otra realizando una sustraccion booleana."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Part_Cut", 0)

def Intersection():
    """Extrae la parte comun (interseccion) entre objetos seleccionados."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Part_Common", 0)

def PolarArray():
    """Crea una matriz circular distribuyendo copias alrededor de un centro."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Draft_PolarArray", 0)

def PointArray():
    """Crea una matriz colocando copias en los vertices de un objeto base."""
    _require_document()
    _require_3d_view()
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Draft_PointArray", 0)

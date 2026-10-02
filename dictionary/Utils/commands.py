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

"""Comandos FreeCAD de la seccion Utils (consolidado).

Cada funcion conserva su comportamiento original; este modulo
reune lo que antes vivia en una carpeta por funcion.
"""
import FreeCAD
import FreeCADGui
import FreeCADGui as Gui

def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc

def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc

def _replace_references(old, new):
    """Hace que los objetos que apuntaban a `old` apunten a `new`."""
    for parent in old.InList:
        for prop in parent.PropertiesList:
            value = getattr(parent, prop)
            if value == old:
                setattr(parent, prop, new)
            elif isinstance(value, list) and old in value:
                if prop == "Group" and hasattr(parent, "addObject"):
                    parent.addObject(new)
                else:
                    setattr(parent, prop, value + [new])
            else:
                continue
            FreeCAD.Console.PrintMessage(
                "Se actualizó la referencia de {} a este objeto.\n".format(parent.Label)
            )


# --- Unclone ---
"""Unclone — Menú BIM → Utils → Unclone.

Convierte un clon de tipo Arch en un objeto independiente del original:
conserva su forma y propiedades actuales pero deja de actualizarse cuando el
original cambia. Las referencias de otros objetos al clon se actualizan.
Comando FreeCAD: BIM_Unclone.
"""

COMMAND_UNCLONE = "BIM_Unclone"

# Propiedades del original que no se copian al objeto independizado.
SKIPPED_PROPERTIES = (
    "Objects",
    "CloneOf",
    "ExpressionEngine",
    "HorizontalArea",
    "Area",
    "VerticalArea",
    "PerimeterLength",
    "Proxy",
    "Shape",
)

def unclone(interactive=False):
    """Independiza el clon seleccionado de su original.

    Requiere exactamente un objeto seleccionado que sea un clon de tipo Arch
    (con la propiedad CloneOf). Los clones de Draft no están soportados.

    Parámetros
    ----------
    interactive : bool
        Si es True, abre la herramienta interactiva de FreeCAD en lugar de
        ejecutar la lógica por script.

    Devuelve
    --------
    El objeto independiente resultante, o None en modo interactivo.
    """
    doc = _require_document()

    if interactive:
        FreeCADGui.runCommand(COMMAND_UNCLONE)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if len(selection) != 1:
        raise RuntimeError("Seleccioná exactamente un objeto.")
    obj = selection[0]

    import Arch
    import Draft

    if not getattr(obj, "CloneOf", None):
        if Draft.getType(obj) == "Clone":
            raise RuntimeError("Los clones de Draft todavía no están soportados.")
        raise RuntimeError("El objeto seleccionado no es un clon.")

    original = obj.CloneOf
    placement = FreeCAD.Placement(obj.Placement)

    doc.openTransaction("Unclone")
    try:
        if Draft.getType(obj) != Draft.getType(original):
            # El clon es de otro tipo: hay que crear un objeto del tipo original.
            new = getattr(Arch, "make" + Draft.getType(original))()
        else:
            new = obj
            new.CloneOf = None
            if getattr(new, "ViewObject", None):
                new.ViewObject.signalChangeIcon()

        for prop in original.PropertiesList:
            if prop not in SKIPPED_PROPERTIES:
                setattr(new, prop, getattr(original, prop))
        doc.recompute()
        new.Placement = original.Placement.multiply(placement)

        _replace_references(obj, new)

        if new != obj:
            label = obj.Label
            doc.removeObject(obj.Name)
            new.Label = label
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return new

# --- ArchSurvey ---
"""Arch Survey — Menú BIM → Utils → Survey.

Inicia el modo interactivo de inspección del modelo. A medida que se hace clic
en vértices, aristas o caras, la herramienta calcula la medida y la registra en
una lista: longitudes de aristas, áreas de caras y coordenadas de vértices, con
totales acumulados. La lista se puede usar como referencia o exportarla.

El modo se abre y se cierra con la misma llamada: si el survey ya está activo,
la siguiente ejecución lo termina y entrega los totales.
Comando FreeCAD: Arch_Survey.
"""

COMMAND_ARCH_SURVEY = "Arch_Survey"

def ArchSurvey(interactive=False):
    """Abre el modo survey de inspección del modelo.

    Al activarlo, cada clic sobre una arista o una cara acumula su longitud o su
    área en una lista, y un clic en el vacío reinicia los totales. Llamarlo de
    nuevo con el modo ya abierto lo cierra y entrega el resultado.

    Parámetros
    ----------
    interactive : bool
        Si es True, abre la herramienta interactiva de FreeCAD en lugar de
        ejecutar la lógica por script.

    Devuelve
    --------
    None: las medidas se muestran en el panel de tareas.
    """
    _RequireDocument()
    _Require3dView()

    if interactive:
        FreeCADGui.runCommand(COMMAND_ARCH_SURVEY)
        return None

    import Arch

    Arch.survey()

# --- BIMTrash ---
"""BIM Trash — Menú BIM → Utils → Move to Trash.

Mueve los objetos seleccionados a un grupo especial llamado "Trash". Si el grupo
no existe en el documento, lo crea. Los objetos quedan ocultos y fuera de su
grupo original, pero no se eliminan: siguen siendo recuperables desde la papelera.
Comando FreeCAD: BIM_Trash.
"""

COMMAND_BIM_TRASH = "BIM_Trash"

TRASH_NAME = "Trash"

def GetTrash(create=False):
    """Devuelve el grupo Trash del documento, o None si no está y create es False.

    Parámetros
    ----------
    create : bool
        Si es True, crea el grupo Trash cuando todavía no existe.
    """
    doc = _RequireDocument()
    trash = doc.getObject(TRASH_NAME)
    if trash and trash.isDerivedFrom("App::DocumentObjectGroup"):
        return trash
    if not create:
        return None
    trash = doc.addObject("App::DocumentObjectGroup", TRASH_NAME)
    trash.Label = "Trash"
    return trash

def _RemoveFromParents(obj, trash):
    """Saca el objeto de los grupos o contenedores que lo referencian."""
    for parent in obj.InList:
        if parent == trash or not hasattr(parent, "Group"):
            continue
        if obj not in parent.Group:
            continue
        if hasattr(parent, "removeObject"):
            parent.removeObject(obj)
        else:
            group = parent.Group
            group.remove(obj)
            parent.Group = group

def BIMTrash(objects=None):
    """Mueve los objetos indicados a la papelera.

    Parámetros
    ----------
    objects : list, opcional
        Objetos a mover. Si se omite, se abre la herramienta interactiva
        en la vista 3D.

    Devuelve
    --------
    El grupo Trash, o None en modo interactivo o si no había nada seleccionado.
    """
    doc = _RequireDocument()

    if objects is None:
        _Require3dView()
        FreeCADGui.runCommand(COMMAND_BIM_TRASH)
        return None
    objects = list(objects)
    if not objects:
        return None

    doc.openTransaction("Move to Trash")
    try:
        bin_ = GetTrash(create=True)
        for obj in objects:
            bin_.addObject(obj)
            _RemoveFromParents(obj, bin_)
            if getattr(obj, "ViewObject", None):
                obj.ViewObject.hide()
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return bin_

# --- BIMWPView ---
"""BIM WPView — Menú BIM → Utils → Working Plane View.

Alinea la cámara de la vista 3D de forma perpendicular al plano de trabajo
activo, poniendo la cuadrícula de frente. Facilita dibujar, medir y editar
sobre planos inclinados, fachadas o caras concretas del modelo.

Si el panel BIM Views está abierto y tiene un elemento seleccionado, alinea a
ese elemento; si no, alinea al plano de trabajo activo.
Comando FreeCAD: BIM_WPView.
"""

COMMAND_BIMWP_VIEW = "BIM_WPView"

def BIMWPView():
    """Alinea la vista 3D al plano de trabajo activo.

    Devuelve
    --------
    None: la vista 3D queda orientada de frente al plano de trabajo.
    """
    _RequireDocument()
    _Require3dView()
    FreeCADGui.runCommand(COMMAND_BIMWP_VIEW)

# --- DraftSelectGroup ---
"""Draft SelectGroup — Menú BIM → Utils → Select group.

Selecciona de forma recursiva el contenido del grupo o contenedor seleccionado
(Std Group, Draft Block, Arch BuildingPart, etc.) en lugar del contenedor mismo:
la selección del grupo se anula y quedan seleccionados todos sus hijos, tanto
en la vista 3D como en la vista de árbol.

Si lo que está seleccionado no es un grupo, se selecciona el contenido del
grupo que lo contiene.
Comando FreeCAD: Draft_SelectGroup.
"""

COMMAND_DRAFT_SELECT_GROUP = "Draft_SelectGroup"

def _Children(container, recursive):
    """Hijos directos del contenedor, o todo su contenido si recursive."""
    if recursive:
        import Draft

        return Draft.get_group_contents(container)
    return list(getattr(container, "Group", []))

def _Collect(objects, recursive):
    """Arma la lista de hijos de cada objeto, o de su grupo contenedor."""
    from draftutils import groups

    contents = []
    for obj in objects:
        if groups.is_group(obj):
            contents.extend(_Children(obj, recursive))
            continue
        for parent in obj.InList:
            if groups.is_group(parent):
                contents.extend(_Children(parent, recursive))
    return contents

def DraftSelectGroup(objects=None, recursive=True):
    """Selecciona el contenido de los grupos indicados.

    Parámetros
    ----------
    objects : list, opcional
        Grupos o contenedores cuyo contenido hay que seleccionar. Si se omite,
        se abre la herramienta interactiva en la vista 3D.
    recursive : bool
        Si es True, baja también por los subgrupos; si es False, se queda en
        los hijos directos del contenedor.

    Devuelve
    --------
    La lista de objetos que quedaron seleccionados, o None en modo interactivo.
    """
    _RequireDocument()
    _Require3dView()

    if objects is None:
        FreeCADGui.runCommand(COMMAND_DRAFT_SELECT_GROUP)
        return None
    objects = list(objects)
    if not objects:
        raise ValueError("Seleccioná al menos un grupo o contenedor.")

    contents = _Collect(objects, recursive)
    if not contents:
        raise ValueError(
            "No se encontró contenido. Seleccioná grupos con objetos dentro, "
            "u objetos que pertenezcan a un grupo."
        )

    FreeCADGui.Selection.clearSelection()
    for obj in contents:
        FreeCADGui.Selection.addSelection(obj)
    return contents

# --- DraftSlope ---
"""Draft Slope — Menú BIM → Utils → Set slope.

Da pendiente a las Draft Lines y Draft Wires seleccionadas modificando la
coordenada Z de sus vértices, a partir del primero. La pendiente se expresa
como tangente del ángulo horizontal: 0 es horizontal, 1 sube 45 grados, -1 baja
45 grados. En una polilínea la transformación se aplica segmento por segmento.

La pendiente siempre cambia Z, así que la herramienta funciona bien sobre
líneas rectas dibujadas en el plano XY.
Comando FreeCAD: Draft_Slope.
"""

COMMAND_DRAFT_SLOPE = "Draft_Slope"

def DraftSlope(objects=None, value=None):
    """Aplica la pendiente indicada a las Draft Wires seleccionadas.

    Parámetros
    ----------
    objects : list, opcional
        Draft Wires a las que dar pendiente. Si se omite, se usa la selección
        actual.
    value : float, opcional
        Pendiente como tangente del ángulo horizontal: 0 es horizontal, 1 sube
        45 grados, -1 baja 45 grados. Si se omite, se abre el diálogo para
        elegirla.

    Devuelve
    --------
    La lista de Draft Wires modificadas, o None en modo interactivo.
    """
    doc = _RequireDocument()

    if value is None:
        _Require3dView()
        FreeCADGui.runCommand(COMMAND_DRAFT_SLOPE)
        return None

    if objects is None:
        objects = FreeCADGui.Selection.getSelection()
    objects = list(objects)
    if not objects:
        raise ValueError("Seleccioná al menos una línea o polilínea.")

    import Draft

    doc.openTransaction("Set slope")
    try:
        changed = []
        for obj in objects:
            if Draft.getType(obj) != "Wire" or len(obj.Points) < 2:
                continue
            previous = None
            points = []
            for point in obj.Points:
                if previous is None:
                    previous = point
                else:
                    dx, dy = point.x - previous.x, point.y - previous.y
                    rise = value * FreeCAD.Vector(dx, dy, 0).Length
                    previous = FreeCAD.Vector(point.x, point.y, previous.z + rise)
                points.append(previous)
            obj.Points = points
            changed.append(obj)
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return changed

# --- DraftWorkingPlaneProxy ---
"""Draft WorkingPlaneProxy — Menú BIM → Utils → Create working plane proxy.

Guarda el estado actual del plano de trabajo y de la cámara en un objeto
"WorkingPlaneProxy" del documento. Al seleccionarlo después, FreeCAD restaura
esa misma orientación de plano y de vista, lo que permite saltar rápido entre
distintas áreas u orientaciones del proyecto.
Comando FreeCAD: Draft_WorkingPlaneProxy.
"""

COMMAND_DRAFT_WORKING_PLANE_PROXY = "Draft_WorkingPlaneProxy"

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
        FreeCADGui.runCommand(COMMAND_DRAFT_WORKING_PLANE_PROXY)
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

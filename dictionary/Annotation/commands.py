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

"""Comandos FreeCAD de la seccion Annotation (consolidado).

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

def _ProjectionVector(section):
    """Dirección de proyección: la normal del plano de sección, hacia el modelo."""
    return section.Placement.Rotation.multVec(FreeCAD.Vector(0, 0, 1)).negative()


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc

def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


# --- Aligned_Dimension ---
"""Aligned dimension — Menú BIM → Annotation → Aligned dimension.

Crea una cota alineada (objeto Dimension) entre dos puntos o a lo largo de una
arista seleccionada. El formato lo controlan los estilos de anotación del
documento.
Comando FreeCAD: BIM_DimensionAligned (atajo D, I).
"""

COMMAND_ALIGNED_DIMENSION = "BIM_DimensionAligned"

def aligned_dimension():
    """Abre la herramienta de cota alineada.

    Los dos puntos, o la arista de referencia, se marcan en la vista 3D.
    La medida queda alineada a la geometría de referencia.

    Devuelve
    --------
    None. El objeto Dimension lo crea el comando al cerrar.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_ALIGNED_DIMENSION)

# --- Horizontal_Dimension ---
"""Horizontal dimension — Menú BIM → Annotation → Horizontal dimension.

Crea una cota horizontal (objeto Dimension) entre dos puntos o a lo largo de una
arista seleccionada. El formato lo controlan los estilos de anotación del
documento.
Comando FreeCAD: BIM_DimensionHorizontal (atajo D, H).
"""

COMMAND_HORIZONTAL_DIMENSION = "BIM_DimensionHorizontal"

def horizontal_dimension():
    """Abre la herramienta de cota horizontal.

    Los dos puntos, o la arista de referencia, se marcan en la vista 3D.
    Requiere un plano de trabajo horizontal adecuado.

    Devuelve
    --------
    None. El objeto Dimension lo crea el comando al cerrar.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_HORIZONTAL_DIMENSION)

# --- Vertical_Dimension ---
"""Vertical dimension — Menú BIM → Annotation → Vertical dimension.

Crea una cota vertical (objeto Dimension) entre dos puntos o a lo largo de una
arista seleccionada. El formato lo controlan los estilos de anotación del
documento.
Comando FreeCAD: BIM_DimensionVertical (atajo D, V).
"""

COMMAND_VERTICAL_DIMENSION = "BIM_DimensionVertical"

def vertical_dimension():
    """Abre la herramienta de cota vertical.

    Los dos puntos, o la arista de referencia, se marcan en la vista 3D.
    Requiere un plano de trabajo vertical adecuado.

    Devuelve
    --------
    None. El objeto Dimension lo crea el comando al cerrar.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_VERTICAL_DIMENSION)

# --- 2DDrawing ---
"""2D Drawing — Menú BIM → Annotation → Create 2D Views → 2D Drawing.

Crea un contenedor para albergar proyecciones 2D (un BuildingPart modificado
para funcionar como dibujo 2D). Si se indica un plano de sección, se generan
automáticamente la vista de sección ("Viewed lines") y el corte de sección
("Cut lines"), se aplastan sobre el plano XY y se agrupan dentro del objeto
"Drawing", exportable como un único DXF/SVG.
API de FreeCAD: Arch.make2DDrawing(objectslist, baseobj, name).
"""

VIEWED_LINES = "Viewed lines"
CUT_LINES = "Cut lines"
CUT_FACES_2D_DRAWING = "Cutfaces"

def _SectionPlane_2D_DRAWING(base):
    """Devuelve el plano de sección a usar, o None si no hay ninguno."""
    import Draft

    if base is not None:
        return base

    selection = FreeCADGui.Selection.getSelection()
    if len(selection) == 1 and Draft.getType(selection[0]) == "SectionPlane":
        return selection[0]
    return None

def _AddSectionView(drawing, section, mode, label):
    """Agrega al dibujo una proyección del plano de sección."""
    import Draft

    view = Draft.make_shape2dview(section)
    view.Label = label
    view.InPlace = False
    if mode is not None:
        view.ProjectionMode = mode
    drawing.addObject(view)
    return view

def _SectionCutsModel(section):
    """Verifica si el plano de sección realmente corta el modelo."""

    bb = FreeCAD.BoundBox()
    for obj in section.Objects:
        if hasattr(obj, "Shape") and obj.Shape:
            bb.add(obj.Shape.BoundBox)
    return bool(bb.isInside(section.Shape.CenterOfMass))

def CreateTwoDDrawing(base=None, objects=None, name=None):
    """Crea un dibujo 2D, con sus vistas si se pasa un plano de sección.

    Parámetros
    ----------
    base : object, opcional
        Plano de sección del que se extrae la vista. Por defecto, el único plano
        de sección de la selección actual.
    objects : list, opcional
        Contenido inicial del dibujo. Por defecto, vacío.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Drawing".

    Devuelve
    --------
    object: el dibujo creado.
    """
    doc = _RequireDocument()
    _Require3dView()

    import Arch
    import Draft

    section = _SectionPlane_2D_DRAWING(base)
    objectslist = list(objects) if isinstance(objects, (list, tuple)) else objects

    drawing = Arch.make2DDrawing(objectslist, baseobj=section, name=name)
    Draft.autogroup(drawing)

    if section is not None:
        _AddSectionView(drawing, section, None, VIEWED_LINES)
        if _SectionCutsModel(section):
            _AddSectionView(drawing, section, CUT_FACES_2D_DRAWING, CUT_LINES)

    doc.recompute()
    return drawing

TwoDDrawing = {
    "2d drawing": CreateTwoDDrawing,
}

# NOTA: sin comando GUI conocido en el original; solo implementacion por API (equipo: mapear comando).

# --- Axis ---
"""Axis — Menú BIM → Annotation → Axis Tools → Axis.

Coloca una serie de ejes de referencia en el documento. La cantidad, la distancia
y el ángulo entre ejes son configurables, así como el estilo de numeración. Los
ejes sirven sobre todo para ajustar (snap) objetos, pueden combinarse en un
Axis System y se pueden referenciar desde otros objetos Arch para crear arrays
paramétricos.
API de FreeCAD: Arch.makeAxis(num, size, name).
"""

DEFAULT_NUM = 5
DEFAULT_SIZE = 1000.0
DEFAULT_NAME_AXIS = "Axes"

def CreateAxis(num=DEFAULT_NUM, size=DEFAULT_SIZE, name=DEFAULT_NAME_AXIS):
    """Crea un sistema de ejes de referencia.

    Parámetros
    ----------
    num : int, opcional
        Cantidad de ejes a crear. Por defecto 5.
    size : float, opcional
        Distancia entre ejes. Por defecto 1000.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Axes".

    Devuelve
    --------
    object: el sistema de ejes creado.
    """
    _RequireDocument()
    _Require3dView()

    if int(num) < 1:
        raise ValueError("El sistema de ejes necesita al menos un eje.")
    if float(size) <= 0:
        raise ValueError("La distancia entre ejes debe ser mayor que cero.")

    import Arch

    return Arch.makeAxis(num=int(num), size=float(size), name=name)

Axis = {
    "axis": CreateAxis,
}

# NOTA: sin comando GUI conocido en el original; solo implementacion por API (equipo: mapear comando).

# --- AxisSystem ---
"""Axis System — Menú BIM → Annotation → Axis Tools → Axis System.

Combina dos o tres objetos Arch Axis en un único sistema, útil para definir los
puntos de intersección entre los distintos ejes. Los objetos Arch pueden usar
este sistema para duplicar su forma en esos puntos de intersección.
API de FreeCAD: Arch.makeAxisSystem(axes, name).
"""

DEFAULT_NAME_AXIS_SYSTEM = "Axis System"

def _AxesList(axes):
    """Normaliza el argumento a una lista de objetos Arch Axis."""
    import Draft

    if axes is None:
        axes = FreeCADGui.Selection.getSelection()
    axes = list(axes) if isinstance(axes, (list, tuple)) else [axes]

    if not axes:
        raise ValueError("Seleccioná al menos un eje para el sistema de ejes.")

    for axis in axes:
        if Draft.getType(axis) != "Axis":
            raise ValueError("Sólo se pueden combinar objetos Arch Axis.")

    return axes

def CreateAxisSystem(axes=None, name=DEFAULT_NAME_AXIS_SYSTEM):
    """Crea un sistema de ejes combinando los ejes indicados.

    Parámetros
    ----------
    axes : object o list, opcional
        Objeto Arch Axis o lista de ellos. Por defecto, la selección actual.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Axis System".

    Devuelve
    --------
    object: el sistema de ejes creado.
    """
    _RequireDocument()
    _Require3dView()

    import Arch

    return Arch.makeAxisSystem(_AxesList(axes), name=name)

AxisSystem = {
    "axis system": CreateAxisSystem,
}

# NOTA: sin comando GUI conocido en el original; solo implementacion por API (equipo: mapear comando).

# --- Grid ---
"""Grid — Menú BIM → Annotation → Grid.

Coloca un objeto tipo rejilla en el documento. Sirve de base para construir
objetos Arch que necesitan un marco regular pero complejo: ventanas, muros
cortina, rejillas de columnas, barandillas, etc. Es un objeto 2D editable como
una hoja de cálculo (filas, columnas, tamaños y celdas fusionadas) y también
puede comportarse como un Axis System para propagar la ubicación de otros
objetos Arch.
API de FreeCAD: Arch.makeGrid(name).
"""

DEFAULT_NAME_GRID = "Grid"

def CreateGrid(name=DEFAULT_NAME_GRID, rows=None, columns=None, width=None, height=None):
    """Crea una rejilla 2D.

    Parámetros
    ----------
    name : str, opcional
        Nombre del objeto creado. Por defecto "Grid".
    rows : int, opcional
        Cantidad de filas de la rejilla.
    columns : int, opcional
        Cantidad de columnas de la rejilla.
    width : float, opcional
        Ancho total de la rejilla.
    height : float, opcional
        Alto total de la rejilla.

    Devuelve
    --------
    object: la rejilla creada.
    """
    doc = _RequireDocument()
    _Require3dView()

    if rows is not None and int(rows) < 1:
        raise ValueError("La rejilla necesita al menos una fila.")
    if columns is not None and int(columns) < 1:
        raise ValueError("La rejilla necesita al menos una columna.")

    import Arch

    grid = Arch.makeGrid(name=name)

    if rows is not None:
        grid.Rows = int(rows)
    if columns is not None:
        grid.Columns = int(columns)
    if width is not None:
        grid.Width = float(width)
    if height is not None:
        grid.Height = float(height)

    doc.recompute()
    return grid

Grid = {
    "grid": CreateGrid,
}

# NOTA: sin comando GUI conocido en el original; solo implementacion por API (equipo: mapear comando).

# --- Hatch ---
"""Hatch — Menú BIM → Annotation → Hatch.

Crea sombreados sobre las caras planas de los objetos o subelementos indicados.
Solo las caras planas reciben el sombreado. El patrón se define con un archivo
PAT y se pueden indicar su escala y su rotación; sin archivo ni patrón, el
comando de FreeCAD abre su propio diálogo.
Comando FreeCAD: Draft_Hatch.
"""

COMMAND_HATCH = "Draft_Hatch"

def _BaseObject(targets):
    """Devuelve el objeto base del sombreado a partir del argumento recibido."""
    if targets is None:
        targets = FreeCADGui.Selection.getSelection()
    if not isinstance(targets, (list, tuple)):
        return targets
    if not targets:
        raise ValueError("Seleccioná al menos un objeto o cara para el sombreado.")
    first = targets[0]
    if isinstance(first, (list, tuple)) and len(first) == 2:
        # Selection.getSelectionEx() devuelve (objeto, [subelementos])
        return first[0]
    return first

def CreateHatch(targets=None, filename=None, pattern=None, scale=1.0, rotation=0.0):
    """Crea un sombreado con un patrón PAT sobre las caras planas indicadas.

    Parámetros
    ----------
    targets : object o list, opcional
        Objeto (o subobjeto) cuyas caras planas se van a sombrear. Por defecto,
        la selección actual.
    filename : str, opcional
        Ruta del archivo PAT con el patrón. Si se omite se activa el comando
        interactivo.
    pattern : str, opcional
        Nombre del patrón dentro del archivo PAT.
    scale : float, opcional
        Escala del patrón. Por defecto 1.0.
    rotation : float, opcional
        Rotación del patrón en grados. Por defecto 0.0.

    Devuelve
    --------
    object: el sombreado creado, o None si el comando quedó en modo interactivo.
    """
    doc = _RequireDocument()

    if filename is None or pattern is None:
        FreeCADGui.runCommand(COMMAND_HATCH)
        return None

    import Draft

    obj = Draft.make_hatch(_BaseObject(targets), filename, pattern, scale, rotation)
    Draft.autogroup(obj)
    doc.recompute()
    return obj

Hatch = {
    "hatch": CreateHatch,
}

# --- Label ---
"""Label — Menú BIM → Annotation → Label.

Crea un texto multilínea con una línea de líder de dos segmentos y una flecha.
Si se indica un objeto o un subelemento (cara, arista o vértice), la etiqueta
puede mostrar uno o dos de sus atributos (posición, longitud, área, volumen,
material) y queda vinculada a ellos, actualizándose cuando cambian.
Comando FreeCAD: Draft_Label.
"""

COMMAND_LABEL = "Draft_Label"

VALID_DIRECTIONS = {"Horizontal", "Vertical", "Custom"}
VALID_LABEL_TYPES = {
    "Custom", "Name", "Label", "Position", "Length", "Area", "Volume",
    "Tag", "Material", "Label + Position", "Label + Length", "Label + Area",
    "Label + Volume", "Label + Material"
}

def _AsPlacement(value):
    """Normaliza el punto base del texto a Placement, Vector o Rotation."""
    if isinstance(value, (FreeCAD.Placement, FreeCAD.Rotation)):
        return value
    return FreeCAD.Vector(float(value[0]), float(value[1]), float(value[2]))

def _ValidateDirection(value):
    if value not in VALID_DIRECTIONS:
        raise ValueError(
            f"Dirección inválida: {value!r}. Valores permitidos: {sorted(VALID_DIRECTIONS)}"
        )

def _ValidateLabelType(value):
    if value not in VALID_LABEL_TYPES:
        raise ValueError(
            f"Tipo de etiqueta inválido: {value!r}. Valores permitidos: {sorted(VALID_LABEL_TYPES)}"
        )

def _ValidatePoints(points):
    if points is not None:
        if not isinstance(points, (list, tuple)):
            raise ValueError("El parámetro 'points' debe ser una lista de vectores.")
        if len(points) < 2:
            raise ValueError("El parámetro 'points' requiere al menos dos vectores.")

def _SelectedObject():
    selection = FreeCADGui.Selection.getSelection()
    return selection[0] if selection else None

def CreateLabel(
    target_point=None,
    placement=None,
    target_object=None,
    subelements=None,
    label_type="Custom",
    custom_text="Label",
    direction="Horizontal",
    distance=-10,
    points=None,
):
    """Crea una etiqueta con línea de líder de dos segmentos y flecha.

    Parámetros
    ----------
    target_point : tuple, opcional
        Punta de la flecha (x, y, z). Si se omite se activa el comando
        interactivo.
    placement : Placement, Rotation o tuple, opcional
        Punto base del texto. Si se omite se usa el valor de Draft (30, 30, 0).
    target_object : object, opcional
        Objeto cuyos atributos muestra la etiqueta. Por defecto, el primer objeto
        de la selección actual.
    subelements : list, opcional
        Subelementos del objeto (caras, aristas o vértices) a considerar.
    label_type : str, opcional
        Atributo a mostrar: "Custom", "Position", "Length", "Area", "Volume",
        "Material", etc. Por defecto "Custom".
    custom_text : str, opcional
        Texto a mostrar cuando label_type es "Custom".
    direction : str, opcional
        Orientación del texto: "Horizontal", "Vertical", "Aligned", "Auto" o
        "Custom". Por defecto "Horizontal".
    distance : float, opcional
        Distancia del texto respecto del líder.
    points : list, opcional
        Puntos intermedios del líder.

    Devuelve
    --------
    object: la etiqueta creada, o None si el comando quedó en modo interactivo.
    """
    doc = _RequireDocument()

    if target_point is None:
        FreeCADGui.runCommand(COMMAND_LABEL)
        return None

    _ValidateDirection(direction)
    _ValidateLabelType(label_type)
    _ValidatePoints(points)

    import Draft

    if target_object is None:
        target_object = _SelectedObject()

    obj = Draft.make_label(
        target_point=_AsPlacement(target_point),
        placement=None if placement is None else _AsPlacement(placement),
        target_object=target_object,
        subelements=subelements,
        label_type=label_type,
        custom_text=custom_text,
        direction=direction,
        distance=distance,
        points=points,
    )
    if obj is None:
        raise RuntimeError("Draft.make_label rechazó los parámetros (consulte la consola de FreeCAD).")
    Draft.autogroup(obj)
    doc.recompute()
    return obj

Label = {
    "label": CreateLabel,
}

# --- Leader ---
"""Leader — Menú BIM → Annotation → Leader.

Crea una línea de referencia (leader): un objeto Wire con un símbolo de flecha
en el último punto. Se usa junto con la herramienta Text para las anotaciones
BIM. Si se pasan los puntos, el Wire se crea directamente; si no, el comando de
FreeCAD queda a la espera de que el usuario los elija en la vista.
Comando FreeCAD: BIM_Leader.
"""

COMMAND_LEADER = "BIM_Leader"
MIN_POINTS = 2

def _AsVectorList(points):
    return [FreeCAD.Vector(float(p[0]), float(p[1]), float(p[2])) for p in points]

def _CreateLeader(points):
    """Crea el Wire del líder con la flecha final y lo devuelve."""
    import Draft
    from draftutils import params

    doc = _RequireDocument()
    obj = Draft.make_wire(points)
    if FreeCAD.GuiUp and obj.ViewObject:
        obj.ViewObject.LineColor = params.get_param("DefaultTextColor") | 0x000000FF
        obj.ViewObject.ArrowTypeEnd = params.get_param("dimsymbolend")
    Draft.autogroup(obj)
    doc.recompute()
    return obj

def CreateLeader(points=None):
    """Crea una línea de referencia con flecha en el último punto.

    Parámetros
    ----------
    points : list, opcional
        Lista de puntos (x, y, z) que definen el líder; hacen falta al menos
        dos. Si se omite se activa el comando interactivo.

    Devuelve
    --------
    object: el Wire creado, o None si el comando quedó en modo interactivo.
    """
    _RequireDocument()
    _Require3dView()

    if points is None:
        FreeCADGui.runCommand(COMMAND_LEADER)
        return None

    points = _AsVectorList(points)
    if len(points) < MIN_POINTS:
        raise ValueError("El líder necesita al menos dos puntos.")

    return _CreateLeader(points)

Leader = {
    "leader": CreateLeader,
}

# --- NewPage ---
"""New Page — Menú BIM → Annotation → New Page.

Crea una nueva página TechDraw a partir de una plantilla SVG, lista para recibir
vistas (New View) y anotaciones. Sin ruta de plantilla, el comando de FreeCAD
abre su propio diálogo para elegirla y recuerda la última usada.
Comando FreeCAD: BIM_TDPage.
"""

COMMAND_NEW_PAGE = "BIM_TDPage"
PARAM_GROUP = "User parameter:BaseApp/Preferences/Mod/BIM"

def _CreatePage(template):
    """Crea la página TechDraw con su plantilla y devuelve la página."""
    import TechDraw  # noqa: F401  (registra los tipos TechDraw)

    doc = _RequireDocument()
    filename = os.path.abspath(str(template))
    if not os.path.isfile(filename):
        raise ValueError("No se encontró la plantilla SVG indicada.")

    page = doc.addObject("TechDraw::DrawPage", "Page")
    page.Label = os.path.splitext(os.path.basename(filename))[0]
    draw_template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    draw_template.Template = filename
    draw_template.Label = "Template"
    page.Template = draw_template

    FreeCAD.ParamGet(PARAM_GROUP).SetString(
        "TDTemplateDir", filename.replace("\\", "/")
    )
    _ReadEditableScale(page, draw_template)

    doc.recompute()
    return page

def _ReadEditableScale(page, draw_template):
    """Toma la escala del texto editable "scale" de la plantilla, si la tiene."""
    texts = draw_template.EditableTexts
    for key in ["scale", "Scale", "SCALE", "scaling", "Scaling", "SCALING"]:
        value = texts.get(key)
        if not value:
            continue
        value = value.replace(":", "/")
        if "/" in value:
            try:
                numerator, denominator = value.split("/", 1)
                page.Scale = float(numerator) / float(denominator)
            except (ValueError, ZeroDivisionError):
                pass
        else:
            try:
                page.Scale = float(value)
            except ValueError:
                pass
        return

def CreateNewPage(template=None):
    """Crea una página TechDraw nueva a partir de una plantilla SVG.

    Parámetros
    ----------
    template : str, opcional
        Ruta del archivo SVG de la plantilla. Si se omite se activa el comando
        interactivo, que deja elegir la plantilla.

    Devuelve
    --------
    object: la página creada, o None si el comando quedó en modo interactivo.
    """
    _RequireDocument()

    if template is None:
        FreeCADGui.runCommand(COMMAND_NEW_PAGE)
        return None

    return _CreatePage(template)

NewPage = {
    "new page": CreateNewPage,
}

# --- NewView ---
"""New View — Menú BIM → Annotation → New View.

Crea una nueva vista TechDraw a partir de un plano de sección o de objetos 2D y
la inserta en una página. Cada plano de sección genera una vista DrawViewArch y
cada objeto 2D una vista DrawViewDraft, ambas con la escala de la página.
Comando FreeCAD: BIM_TDView.
"""

COMMAND_NEW_VIEW = "BIM_TDView"

def _SplitTargets(targets):
    """Separa los objetivos en planos de sección y objetos 2D."""
    import Draft

    sections = []
    drafts = []
    for obj in targets:
        if obj.isDerivedFrom("TechDraw::DrawPage"):
            # Una página TechDraw seleccionada no debe convertirse en vista
            continue
        if Draft.getType(obj) == "SectionPlane":
            sections.append(obj)
        else:
            drafts.append(obj)
    return sections, drafts

def _ResolvePage(page):
    """Devuelve la página destino: la indicada, la seleccionada o la primera."""
    doc = _RequireDocument()

    if page is None:
        selected = [
            obj
            for obj in FreeCADGui.Selection.getSelection()
            if obj.isDerivedFrom("TechDraw::DrawPage")
        ]
        if selected:
            return selected[0]
        pages = doc.findObjects(Type="TechDraw::DrawPage")
        return pages[0] if pages else None

    if not page.isDerivedFrom("TechDraw::DrawPage"):
        raise ValueError("El destino de la vista tiene que ser una página TechDraw.")

    return page

def _AddArchView(doc, page, section):
    view = doc.addObject("TechDraw::DrawViewArch", "BIM view")
    view.Label = section.Label
    view.Source = section
    page.addView(view)
    if page.Scale:
        view.Scale = page.Scale
    return view

def _AddDraftView(doc, page, draft):
    view = doc.addObject("TechDraw::DrawViewDraft", "DraftView")
    view.Label = draft.Label
    view.Source = draft
    page.addView(view)
    if page.Scale:
        view.Scale = page.Scale
    if "ShapeMode" in draft.PropertiesList:
        draft.ShapeMode = "Shape"
    return view

def CreateNewView(targets=None, page=None):
    """Crea e inserta una vista TechDraw en la página indicada.

    Parámetros
    ----------
    targets : object o list, opcional
        Plano de sección u objetos 2D a representar. Por defecto, la selección
        actual; si está vacía se activa el comando interactivo.
    page : object, opcional
        Página TechDraw destino. Por defecto, la página seleccionada o, si sólo
        hay una, la primera del documento.

    Devuelve
    --------
    list: las vistas creadas, o None si el comando quedó en modo interactivo.
    """
    doc = _RequireDocument()

    if targets is None:
        targets = FreeCADGui.Selection.getSelection()

    if not targets:
        FreeCADGui.runCommand(COMMAND_NEW_VIEW)
        return None

    targets = list(targets) if isinstance(targets, (list, tuple)) else [targets]
    target_page = _ResolvePage(page)
    if target_page is None:
        raise ValueError("No hay ninguna página TechDraw donde insertar la vista.")

    sections, drafts = _SplitTargets(targets)
    views = [_AddArchView(doc, target_page, section) for section in sections]
    views += [_AddDraftView(doc, target_page, draft) for draft in drafts]

    doc.recompute()
    return views

NewView = {
    "new view": CreateNewView,
}

# --- SectionCut ---
"""Section Cut — Menú BIM → Annotation → Create 2D Views → Section Cut.

Produce un objeto Shape2DView en modo "cut lines", que muestra solo las líneas
de corte: la intersección entre el plano de sección y el modelo. La proyección
se crea sobre el plano XY y depende enteramente de la dirección del plano de
sección, ignorando la orientación de la cámara 3D.
Comando FreeCAD: BIM_Shape2DCut.
"""

COMMAND_SECTION_CUT = "BIM_Shape2DCut"
CUT_FACES_SECTION_CUT = "Cutfaces"

def _SectionPlane_SECTION_CUT(target):
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
        FreeCADGui.runCommand(COMMAND_SECTION_CUT)
        return None

    import Draft

    section = _SectionPlane_SECTION_CUT(target)
    view = Draft.make_shape2dview(section, _ProjectionVector(section))
    view.InPlace = False
    view.ProjectionMode = CUT_FACES_SECTION_CUT
    Draft.autogroup(view)
    doc.recompute()
    return view

SectionCut = {
    "section cut": CreateSectionCut,
}

# --- SectionPlane ---
"""Section Plane — Menú BIM → Annotation → Section Plane.

Crea un plano de sección, que define un plano de sección o de vista. Toma su
ubicación según el plano de trabajo de Draft actual y puede reubicarse y
reorientarse moviéndolo y rotándolo, hasta describir la vista 2D deseada. Los
objetos seleccionados al crearlo se añaden automáticamente y otros pueden
añadirse o quitarse después. Por sí solo no genera ninguna vista: es la base
del flujo de producción de dibujos 2D.
API de FreeCAD: Arch.makeSectionPlane(objectslist, name).
"""

DEFAULT_NAME_SECTION_PLANE = "Section"

def CreateSectionPlane(objects=None, name=DEFAULT_NAME_SECTION_PLANE):
    """Crea un plano de sección según el plano de trabajo actual.

    Parámetros
    ----------
    objects : object o list, opcional
        Objetos a incluir en la sección. Si se omite, el plano considera todo
        el documento.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Section".

    Devuelve
    --------
    object: el plano de sección creado.
    """
    _RequireDocument()
    _Require3dView()

    import Arch

    objectslist = None
    if objects is not None:
        objectslist = list(objects) if isinstance(objects, (list, tuple)) else [objects]

    return Arch.makeSectionPlane(objectslist, name=name)

SectionPlane = {
    "section plane": CreateSectionPlane,
}

# NOTA: sin comando GUI conocido en el original; solo implementacion por API (equipo: mapear comando).

# --- SectionView ---
"""Section View — Menú BIM → Annotation → Create 2D Views → Section View.

Produce un objeto Shape2DView en modo "solid" (proyección), que muestra las
líneas proyectadas de lo que ve el plano de sección. La proyección se crea
sobre el plano XY y depende enteramente de la dirección del plano de sección,
ignorando la orientación de la cámara 3D.
Comando FreeCAD: BIM_Shape2DView.
"""

COMMAND_SECTION_VIEW = "BIM_Shape2DView"

def _SectionPlane_SECTION_VIEW(target):
    """Devuelve el plano de sección seleccionado."""
    import Draft

    if target is None:
        selection = FreeCADGui.Selection.getSelection()
        target = selection[0] if len(selection) == 1 else None

    if target is None:
        raise ValueError("Seleccioná un plano de sección para la vista.")

    if Draft.getType(target) != "SectionPlane":
        raise ValueError("La vista necesita un objeto Arch SectionPlane.")

    return target

def CreateSectionView(target=None):
    """Crea la proyección 2D de lo que ve el plano de sección.

    Parámetros
    ----------
    target : object, opcional
        Plano de sección Arch SectionPlane. Por defecto, el único objeto
        seleccionado; si no hay selección se activa el comando interactivo.

    Devuelve
    --------
    object: la vista creada, o None si el comando quedó en modo interactivo.
    """
    doc = _RequireDocument()
    _Require3dView()

    if target is None and not FreeCADGui.Selection.getSelection():
        FreeCADGui.runCommand(COMMAND_SECTION_VIEW)
        return None

    import Draft

    section = _SectionPlane_SECTION_VIEW(target)
    view = Draft.make_shape2dview(section, _ProjectionVector(section))
    view.InPlace = False
    Draft.autogroup(view)
    doc.recompute()
    return view

SectionView = {
    "section view": CreateSectionView,
}

# --- Text ---
"""Text — Menú BIM → Annotation → Text.

Crea un texto, ya sea un objeto Text en la vista 3D actual, o un objeto
Annotation en la página TechDraw activa. El contenido y el punto de inserción
se pueden pasar por parámetro; si no se pasan, el comando de FreeCAD queda a la
espera de que el usuario los indique en la vista.
Comando FreeCAD: BIM_Text.
"""

COMMAND_TEXT = "BIM_Text"

def _RequireView():
    if not FreeCADGui.ActiveDocument:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    view = FreeCADGui.activeView()
    if view is None:
        raise RuntimeError("No hay una vista activa en FreeCAD.")
    return view

def _AsVector(point):
    return FreeCAD.Vector(float(point[0]), float(point[1]), float(point[2]))

def _ActivePage():
    view = FreeCADGui.activeView()
    if hasattr(view, "getPage") and view.getPage():
        return view.getPage()
    return None

def _CreateAnnotation(page, text):
    """Crea un Annotation de TechDraw con el texto indicado."""
    import TechDraw  # noqa: F401  (registra el tipo TechDraw::DrawViewAnnotation)

    doc = _RequireDocument()
    params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
    scale = page.Scale or 1.0
    annotation = doc.addObject("TechDraw::DrawViewAnnotation", "Annotation")
    annotation.Text = text
    annotation.TextSize = params.GetFloat("textheight", 10) * scale
    annotation.Font = params.GetString("textfont", "Sans")
    color = params.GetUnsigned("DefaultTextColor", 255)
    annotation.TextColor = (
        ((color >> 24) & 0xFF) / 255.0,
        ((color >> 16) & 0xFF) / 255.0,
        ((color >> 8) & 0xFF) / 255.0,
    )
    page.addView(annotation)
    doc.recompute()
    return annotation

def _CreateDraftText(text, point):
    """Crea un objeto Draft Text en la vista 3D."""
    import Draft

    doc = _RequireDocument()
    obj = Draft.make_text(
        text, placement=FreeCAD.Vector(0, 0, 0) if point is None else point
    )
    Draft.autogroup(obj)
    doc.recompute()
    return obj

def CreateText(text=None, point=None):
    """Crea un texto en la vista 3D o en la página TechDraw activa.

    Parámetros
    ----------
    text : str, opcional
        Contenido del texto. Si se omite, se activa el comando interactivo.
    point : tuple, opcional
        Punto de inserción (x, y, z) del texto en la vista 3D. Si se omite se
        usa el origen.

    Devuelve
    --------
    object: el texto creado, o None si el comando quedó en modo interactivo.
    """
    _RequireDocument()
    _RequireView()

    if text is not None:
        text = str(text).strip()
        if not text:
            raise ValueError("El contenido del texto no puede estar vacío.")

    page = _ActivePage()
    if page is not None:
        if text is None:
            FreeCADGui.runCommand(COMMAND_TEXT)
            return None
        return _CreateAnnotation(page, text)

    if text is not None:
        return _CreateDraftText(text, None if point is None else _AsVector(point))

    FreeCADGui.runCommand(COMMAND_TEXT)
    return None

Text = {
    "text": CreateText,
}

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

"""Comandos FreeCAD de la seccion Manage (consolidado).

Cada funcion conserva su comportamiento original; este modulo
reune lo que antes vivia en una carpeta por funcion.
"""
import FreeCAD
import FreeCADGui


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc

def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")

# --- ArchSchedule ---
"""Arch Schedule — Menú BIM → Manage → Schedule.

Crea una tabla de planificación (schedule) o lista de materiales a partir de
los objetos BIM/Arch del documento: cuantifica propiedades como cantidades,
longitudes, áreas y volúmenes, y vuelca el resultado en una hoja de cálculo
(Spreadsheet) que se actualiza cuando el modelo cambia.
Comando FreeCAD: Arch_Schedule.

Cada fila de la tabla define una operación con cinco columnas:
"Operation" (título de la fila), "Value" ("Count" o la propiedad a leer,
admite rutas anidadas como "Shape.Volume"), "Unit" (m, m2, m3, deg, ...),
"Objects" (objetos a cuantificar, separados por ";") y "Filter"
(condiciones "PROPIEDAD:valor" unidas por ";").
"""

COMMAND_ARCH_SCHEDULE = "Arch_Schedule"

COLUMN_KEYS = ("Operation", "Value", "Unit", "Objects", "Filter")

def _ObjectsToString(objects):
    """Convierte objetos o nombres de objetos en la cadena de la columna Objects."""
    if isinstance(objects, str):
        return objects
    return ";".join(o if isinstance(o, str) else o.Name for o in objects)

def _NormaliseRows(rows, objects=None):
    """Convierte las filas en las cinco listas de cadenas de las propiedades.

    Cada fila puede ser un diccionario con las claves de COLUMN_KEYS o una
    secuencia de valores en ese mismo orden. Los valores ausentes quedan vacíos
    y `objects`, si se informa, se usa en las filas que no traen columna Objects.
    """
    columns = {key: [] for key in COLUMN_KEYS}
    for row in rows:
        if isinstance(row, dict):
            values = {key: row.get(key, "") for key in COLUMN_KEYS}
        else:
            row = list(row)
            if len(row) > len(COLUMN_KEYS):
                raise ValueError(
                    f"Cada fila admite como máximo {len(COLUMN_KEYS)} valores."
                )
            values = dict(zip(COLUMN_KEYS, row))
        if objects is not None and not values.get("Objects"):
            values["Objects"] = objects
        for key in COLUMN_KEYS:
            value = values.get(key)
            columns[key].append("" if value is None else str(value))
    return columns

def SelectionToObjects():
    """Devuelve los objetos de la selección actual como cadena de columna Objects."""
    return _ObjectsToString(FreeCADGui.Selection.getSelection())

def ArchSchedule(
    rows=None,
    objects=None,
    label="Schedule",
    create_spreadsheet=True,
    detailed_results=False,
    auto_update=True,
):
    """Crea una tabla de planificación a partir de los objetos del modelo.

    Parámetros
    ----------
    rows : list, opcional
        Filas de la tabla, en orden. Cada fila es un diccionario con las claves
        "Operation", "Value", "Unit", "Objects" y "Filter", o una secuencia con
        esos valores en ese orden. Si se omite, se abre el panel interactivo
        donde se configuran las columnas.
    objects : list | str, opcional
        Objetos a cuantificar, como objetos o nombres separados por ";", que se
        aplican a las filas que no traen columna "Objects". Si se omite, cada
        fila sin objetos cuantifica todo el documento.
    label : str
        Etiqueta del objeto Schedule en la vista de árbol.
    create_spreadsheet : bool
        Si es True, se crea o se reutiliza la hoja de cálculo asociada.
    detailed_results : bool
        Si es True, se agrega una línea por objeto y una línea "TOTAL" por
        operación, además del resultado agrupado.
    auto_update : bool
        Si es True, la tabla y la hoja de cálculo se actualizan en cada
        recálculo del documento.

    Devuelve
    --------
    El objeto Schedule creado, o None en modo interactivo.
    """
    doc = _RequireDocument()

    if rows is None:
        FreeCADGui.runCommand(COMMAND_ARCH_SCHEDULE)
        return None

    rows = list(rows)
    if not rows:
        raise ValueError("Definí al menos una fila para la tabla de planificación.")

    columns = _NormaliseRows(rows, _ObjectsToString(objects) if objects else None)

    import Arch

    doc.openTransaction("Schedule")
    try:
        schedule = Arch.makeSchedule()
        for key, values in columns.items():
            setattr(schedule, key, values)
        schedule.Label = label
        schedule.CreateSpreadsheet = create_spreadsheet
        schedule.DetailedResults = detailed_results
        schedule.AutoUpdate = auto_update
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return schedule

# --- BIMClassification ---
"""BIM Classification — Menú BIM → Manage → Classification.

Asigna clasificaciones estandarizadas (Uniclass, OmniClass, MasterFormat, etc.)
a los objetos BIM y a los materiales del modelo. La clasificación queda como
metadato en las propiedades del elemento, para poder filtrarlo y exportarlo a
IFC. Los sistemas de clasificación son archivos .xml que FreeCAD busca en el
directorio de configuración del usuario.
Comando FreeCAD: BIM_Classification.
"""

COMMAND_BIM_CLASSIFICATION = "BIM_Classification"

def BIMClassification(objects=None):
    """Abre el administrador de clasificaciones BIM.

    La asignación de la clasificación (sistema, código y categoría) se hace en
    el diálogo: esta función solo valida que haya documento y, si se pasan
    objetos, que la selección sea utilizable.

    Parámetros
    ----------
    objects : list, opcional
        Objetos que se van a clasificar. Si se omite, se usa la selección actual.

    Devuelve
    --------
    None: la herramienta es un diálogo y no devuelve resultado.
    """
    _RequireDocument()
    _Require3dView()

    if objects is not None and len(objects) == 0:
        raise ValueError("Pasá al menos un objeto para clasificar.")

    if objects:
        FreeCADGui.Selection.clearSelection()
        for obj in objects:
            FreeCADGui.Selection.addSelection(obj)

    FreeCADGui.runCommand(COMMAND_BIM_CLASSIFICATION)

# --- BIMIfcProperties ---
"""BIM IFC Properties — Menú BIM → Manage → IFC Management → Manage IFC Properties.

Gestiona los conjuntos de propiedades IFC (Property Sets o Psets) de los objetos
BIM: asigna los psets predefinidos del estándar y permite crear propiedades
personalizadas. Los psets quedan incrustados en el elemento para exportarlo
correctamente a IFC. Los psets propios se declaran en un `CustomPsets.csv` en
el directorio de datos del usuario.
Comando FreeCAD: BIM_IfcProperties.
"""

COMMAND_BIM_IFC_PROPERTIES = "BIM_IfcProperties"

def BIMIfcProperties(objects=None):
    """Abre el administrador de propiedades IFC.

    La edición de los psets (nombre, tipo y valor de cada propiedad) se hace en
    el diálogo: esta función solo valida que haya documento y, si se pasan
    objetos, que la selección sea utilizable.

    Parámetros
    ----------
    objects : list, opcional
        Objetos cuyas propiedades IFC se van a gestionar. Si se omite, se usa
        la selección actual.

    Devuelve
    --------
    None: la herramienta es un diálogo y no devuelve resultado.
    """
    _RequireDocument()
    _Require3dView()

    if objects is not None and len(objects) == 0:
        raise ValueError("Pasá al menos un objeto para gestionar sus propiedades IFC.")

    if objects:
        FreeCADGui.Selection.clearSelection()
        for obj in objects:
            FreeCADGui.Selection.addSelection(obj)

    FreeCADGui.runCommand(COMMAND_BIM_IFC_PROPERTIES)

# --- BIMLayers ---
"""BIM Layers — Menú BIM → Manage → Manage Layers.

Administra las capas del proyecto. Una capa es un grupo especial que propaga
automáticamente sus propiedades visuales (color de línea, color de forma, grosor
de línea, estilo de dibujo y transparencia) a los objetos que contiene, y es
compatible con la importación y exportación a IFC y DXF/DWG.

Sin argumentos abre el Administrador de Capas; con argumentos crea la capa
directamente.
Comando FreeCAD: BIM_Layers.
"""

COMMAND_BIM_LAYERS = "BIM_Layers"

DEFAULTS = {
    "line_color": (0.0, 0.0, 0.0),
    "shape_color": (0.8, 0.8, 0.8),
    "line_width": 2.0,
    "draw_style": "Solid",
    "transparency": 0,
}

def BIMLayers(
    name,
    line_color=None,
    shape_color=None,
    line_width=None,
    draw_style=None,
    transparency=None,
    objects=None,
    apply=True,
):
    """Crea una capa BIM con las propiedades visuales indicadas.

    Los objetos que se agreguen a la capa adoptan de inmediato sus propiedades
    visuales. Si se omite algún parámetro visual se usa el valor por defecto de
    Draft: negro y 2.0 de grosor para la línea, gris claro y opaco para la forma.

    Parámetros
    ----------
    name : str
        Nombre de la capa. Es el único dato obligatorio.
    line_color : tuple, opcional
        Color de la línea como tripla RGB de 0.0 a 1.0.
    shape_color : tuple, opcional
        Color de la forma como tripla RGB de 0.0 a 1.0.
    line_width : float, opcional
        Grosor de la línea, en píxeles.
    draw_style : str, opcional
        Estilo de dibujo: "Solid", "Dashed", "Dotted" o "Dashdot".
    transparency : int, opcional
        Transparencia de la forma, de 0 (opaco) a 100.
    objects : list, opcional
        Objetos a agregar a la capa al crearla.
    apply : bool
        Si es False, solo crea la capa y deja las propiedades visuales sin
        tocar, tal cual quedarían con la interfaz cerrada.

    Devuelve
    --------
    El objeto Draft Layer creado.
    """
    doc = _RequireDocument()

    if not name:
        raise ValueError("La capa necesita un nombre.")

    if not (
        line_color or shape_color or line_width or draw_style or transparency or objects
    ):
        # Solo el nombre no alcanza para una ruta no interactiva: el nombre va
        # con el resto de las propiedades visuales, que es lo que hace el
        # administrador de capas.
        _Require3dView()
        FreeCADGui.runCommand(COMMAND_BIM_LAYERS)
        return None

    kwargs = {}
    if apply:
        kwargs = {
            "line_color": DEFAULTS["line_color"] if line_color is None else line_color,
            "shape_color": DEFAULTS["shape_color"]
            if shape_color is None
            else shape_color,
            "line_width": DEFAULTS["line_width"] if line_width is None else line_width,
            "draw_style": DEFAULTS["draw_style"] if draw_style is None else draw_style,
            "transparency": DEFAULTS["transparency"]
            if transparency is None
            else transparency,
        }

    import Draft

    doc.openTransaction("Layer")
    try:
        created = Draft.make_layer(name, **kwargs)
        if objects:
            # Los objetos se cuelgan del contenedor de capas, no de la capa.
            from draftmake.make_layer import get_layer_container

            container = get_layer_container()
            for obj in objects:
                container.addObject(obj)
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return created

# --- BIMMaterial ---
"""BIM Material — Menú BIM → Manage → Material.

Administra los materiales del documento. Un material define la apariencia y las
propiedades físicas de los elementos (color, transparencia, densidad, propiedades
mecánicas y térmicas) y se vincula a los objetos BIM a través de su propiedad
`Material`. Los materiales nuevos aparecen en la vista de árbol bajo el grupo
"Materials".

Sin argumentos abre el administrador de materiales; con argumentos crea el
material y lo asigna.
Comando FreeCAD: BIM_Material.
"""

COMMAND_BIM_MATERIAL = "BIM_Material"

def _Assign(material, objects):
    """Vincula el material a cada objeto que admita la propiedad Material."""
    for obj in objects:
        if "Material" not in obj.PropertiesList:
            raise ValueError(
                f"{obj.Label or obj.Name} no admite la propiedad Material."
            )
        obj.Material = material

def BIMMaterial(
    name=None,
    color=None,
    transparency=None,
    multi=False,
    objects=None,
    physical=None,
):
    """Crea un material BIM y opcionalmente lo asigna a objetos.

    Parámetros
    ----------
    name : str, opcional
        Nombre del material. Si se omite, FreeCAD usa "Material".
    color : tuple, opcional
        Color como tripla RGB de 0.0 a 1.0, o cuádrupla con alfa de 0.0 a 1.0.
    transparency : float, opcional
        Transparencia de 0 a 100. Solo tiene efecto si no se pasa `color`.
    multi : bool
        Si es True, crea un multi-material (capas de materiales) en lugar de un
        material simple.
    objects : list, opcional
        Objetos BIM a los que asignar el material creado.
    physical : dict, opcional
        Propiedades físicas del material (densidad, módulo de elasticidad,
        resistencia a la tracción, etc.) que se copian al nuevo material.

    Devuelve
    --------
    El objeto Material o MultiMaterial creado.
    """
    doc = _RequireDocument()

    if not (name or color or transparency or objects or physical):
        _Require3dView()
        FreeCADGui.runCommand(COMMAND_BIM_MATERIAL)
        return None

    if multi and (color or transparency or physical):
        raise ValueError(
            "Un multi-material no lleva color ni propiedades físicas propias."
        )

    import Arch

    doc.openTransaction("Material")
    try:
        created = (
            Arch.makeMultiMaterial(name)
            if multi
            else Arch.makeMaterial(name, color, transparency)
        )

        if physical:
            props = (
                created.PropertiesList if not multi else created.Material.PropertiesList
            )
            target = created if not multi else created.Material
            for key, value in physical.items():
                if key not in props:
                    raise ValueError(f"El material no tiene la propiedad {key}.")
                setattr(target, key, value)

        if objects:
            _Assign(created, objects)
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return created

# --- BIMPreflight ---
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

COMMAND_BIM_PREFLIGHT = "BIM_Preflight"

def BIMPreflight():
    """Abre el informe de comprobaciones del modelo BIM activo.

    No lleva parámetros: la herramienta analiza el documento activo completo.

    Devuelve
    --------
    None: los resultados se muestran en la ventana de preflight.
    """
    _RequireDocument()
    _Require3dView()
    FreeCADGui.runCommand(COMMAND_BIM_PREFLIGHT)

# --- BIMReport ---
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

COMMAND_BIM_REPORT = "Report_Create"

ADDON_NAME = "Reporting"

def IsAvailable():
    """Devuelve True si el addon Reporting está instalado y el comando existe.

    Sin interfaz gráfica no hay registro de comandos, así que en ese caso no
    se puede confirmar nada y se responde False.
    """
    list_commands = getattr(FreeCADGui, "listCommands", None)
    if list_commands is None:
        return False
    return COMMAND_BIM_REPORT in list_commands()

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

    FreeCADGui.runCommand(COMMAND_BIM_REPORT)

# --- DraftAnnotationStyleEditor ---
"""Draft AnnotationStyleEditor — Menú BIM → Manage → Annotation styles.

Administra los estilos de anotación del documento. Un estilo agrupa de forma
centralizada las propiedades visuales que se aplican a los objetos de anotación
—textos, cotas y etiquetas—: fuente, altura de texto, tipo y tamaño de flecha,
colores y multiplicador de escala. Aplicar un estilo a todos los elementos
mantiene el mismo aspecto en el documento y en los planos.
Comando FreeCAD: Draft_AnnotationStyleEditor.
"""

COMMAND_DRAFT_ANNOTATION_STYLE_EDITOR = "Draft_AnnotationStyleEditor"

def DraftAnnotationStyleEditor():
    """Abre el editor de estilos de anotación.

    No lleva parámetros: los estilos se dan de alta y se editan en el diálogo,
    y se guardan en el propio documento para acompañarlo cuando se guarda.

    Devuelve
    --------
    None: la herramienta es un diálogo y no devuelve resultado.
    """
    _RequireDocument()
    _Require3dView()
    FreeCADGui.runCommand(COMMAND_DRAFT_ANNOTATION_STYLE_EDITOR)

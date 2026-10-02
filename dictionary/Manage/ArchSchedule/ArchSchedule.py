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

import FreeCAD
import FreeCADGui

COMMAND = "Arch_Schedule"

COLUMN_KEYS = ("Operation", "Value", "Unit", "Objects", "Filter")


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


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
        FreeCADGui.runCommand(COMMAND)
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

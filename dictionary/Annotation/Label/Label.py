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

"""Label — Menú BIM → Annotation → Label.

Crea un texto multilínea con una línea de líder de dos segmentos y una flecha.
Si se indica un objeto o un subelemento (cara, arista o vértice), la etiqueta
puede mostrar uno o dos de sus atributos (posición, longitud, área, volumen,
material) y queda vinculada a ellos, actualizándose cuando cambian.
Comando FreeCAD: Draft_Label.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Label"

VALID_DIRECTIONS = {"Horizontal", "Vertical", "Custom"}
VALID_LABEL_TYPES = {
    "Custom", "Name", "Label", "Position", "Length", "Area", "Volume",
    "Tag", "Material", "Label + Position", "Label + Length", "Label + Area",
    "Label + Volume", "Label + Material"
}


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


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
        FreeCADGui.runCommand(COMMAND)
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

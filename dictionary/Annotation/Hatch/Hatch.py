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

"""Hatch — Menú BIM → Annotation → Hatch.

Crea sombreados sobre las caras planas de los objetos o subelementos indicados.
Solo las caras planas reciben el sombreado. El patrón se define con un archivo
PAT y se pueden indicar su escala y su rotación; sin archivo ni patrón, el
comando de FreeCAD abre su propio diálogo.
Comando FreeCAD: Draft_Hatch.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Hatch"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


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
        FreeCADGui.runCommand(COMMAND)
        return None

    import Draft

    obj = Draft.make_hatch(_BaseObject(targets), filename, pattern, scale, rotation)
    Draft.autogroup(obj)
    doc.recompute()
    return obj


Hatch = {
    "hatch": CreateHatch,
}

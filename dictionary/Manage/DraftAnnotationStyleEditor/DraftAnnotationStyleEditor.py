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

"""Draft AnnotationStyleEditor — Menú BIM → Manage → Annotation styles.

Administra los estilos de anotación del documento. Un estilo agrupa de forma
centralizada las propiedades visuales que se aplican a los objetos de anotación
—textos, cotas y etiquetas—: fuente, altura de texto, tipo y tamaño de flecha,
colores y multiplicador de escala. Aplicar un estilo a todos los elementos
mantiene el mismo aspecto en el documento y en los planos.
Comando FreeCAD: Draft_AnnotationStyleEditor.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_AnnotationStyleEditor"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


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
    FreeCADGui.runCommand(COMMAND)

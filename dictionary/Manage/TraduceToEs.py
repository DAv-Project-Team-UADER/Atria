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
"""Mapa de voz (ES) para la seccion Manage (consolidado)."""

try:
    from .commands import ArchSchedule
except ImportError:
    ArchSchedule = None
try:
    from .commands import BIMClassification
except ImportError:
    BIMClassification = None
try:
    from .commands import BIMIfcProperties
except ImportError:
    BIMIfcProperties = None
try:
    from .commands import BIMLayers
except ImportError:
    BIMLayers = None
try:
    from .commands import BIMMaterial
except ImportError:
    BIMMaterial = None
try:
    from .commands import BIMPreflight
except ImportError:
    BIMPreflight = None
try:
    from .commands import BIMReport
except ImportError:
    BIMReport = None
BIMSetup = None  # TODO: sin implementacion en commands.py
try:
    from .commands import DraftAnnotationStyleEditor
except ImportError:
    DraftAnnotationStyleEditor = None
ManageDoorsAndWindows = None  # TODO: sin implementacion en commands.py
ManageIFCElements = None  # TODO: sin implementacion en commands.py
ManageIFCQuantities = None  # TODO: sin implementacion en commands.py
SetupProject = None  # TODO: sin implementacion en commands.py

TraduceToEs = {
    # ArchSchedule
    'crear tabla de planificación': ArchSchedule,
    'generar schedule': ArchSchedule,
    'crear lista de materiales': ArchSchedule,
    'cuantificar modelo': ArchSchedule,
    'generar cuadro de superficies': ArchSchedule,
    # BIMClassification
    'clasificar elemento BIM': BIMClassification,
    'asignar clasificación': BIMClassification,
    'clasificar objeto': BIMClassification,
    'gestionar clasificación BIM': BIMClassification,
    # BIMIfcProperties
    'gestionar propiedades IFC': BIMIfcProperties,
    'administrar propiedades IFC': BIMIfcProperties,
    'asignar propiedades BIM': BIMIfcProperties,
    'configurar Psets': BIMIfcProperties,
    # BIMLayers
    'gestionar capas': BIMLayers,
    'administrar capas': BIMLayers,
    'crear capa BIM': BIMLayers,
    'abrir administrador de capas': BIMLayers,
    # BIMMaterial
    'asignar material BIM': BIMMaterial,
    'crear material': BIMMaterial,
    'gestionar materiales': BIMMaterial,
    'administrar materiales': BIMMaterial,
    'editor de materiales': BIMMaterial,
    # BIMPreflight
    'comprobar modelo BIM': BIMPreflight,
    'validar modelo': BIMPreflight,
    'ejecutar preflight': BIMPreflight,
    'diagnóstico del proyecto': BIMPreflight,
    # BIMReport
    'crear informe BIM': BIMReport,
    'generar reporte': BIMReport,
    'consultar modelo': BIMReport,
    'crear tabla de planificación': BIMReport,
    # BIMSetup
    'abrir configuración BIM': BIMSetup,
    'configuración BIM': BIMSetup,
    'preferencias BIM': BIMSetup,
    'ajustes BIM': BIMSetup,
    # DraftAnnotationStyleEditor
    'editar estilos de anotación': DraftAnnotationStyleEditor,
    'gestionar estilos de anotación': DraftAnnotationStyleEditor,
    'configurar estilos de texto': DraftAnnotationStyleEditor,
    'administrar estilos de cotas': DraftAnnotationStyleEditor,
    # ManageDoorsAndWindows
    'gestionar puertas y ventanas': ManageDoorsAndWindows,
    'administrar ventanas': ManageDoorsAndWindows,
    'modificar aberturas': ManageDoorsAndWindows,
    'gestor de puertas': ManageDoorsAndWindows,
    # ManageIFCElements
    'gestionar elementos IFC': ManageIFCElements,
    'administrar tipos IFC': ManageIFCElements,
    'gestor de elementos BIM': ManageIFCElements,
    'asignar materiales IFC': ManageIFCElements,
    # ManageIFCQuantities
    'gestionar cantidades IFC': ManageIFCQuantities,
    'administrar medidas IFC': ManageIFCQuantities,
    'verificar cantidades': ManageIFCQuantities,
    'gestor de cantidades BIM': ManageIFCQuantities,
    # SetupProject
    'configurar proyecto BIM': SetupProject,
    'crear proyecto IFC': SetupProject,
    'nuevo proyecto BIM': SetupProject,
    'iniciar proyecto raíz': SetupProject,
}

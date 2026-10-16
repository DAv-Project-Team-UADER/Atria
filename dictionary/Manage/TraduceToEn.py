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
"""Mapa de voz (EN) para la seccion Manage (consolidado)."""

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

TraduceToEn = {
    # ArchSchedule
    'create schedule': ArchSchedule,
    'generate schedule': ArchSchedule,
    'create material list': ArchSchedule,
    'quantify model': ArchSchedule,
    'generate area schedule': ArchSchedule,
    # BIMClassification
    'classify BIM element': BIMClassification,
    'assign classification': BIMClassification,
    'classify object': BIMClassification,
    'manage BIM classification': BIMClassification,
    # BIMIfcProperties
    'manage IFC properties': BIMIfcProperties,
    'administer IFC properties': BIMIfcProperties,
    'assign BIM properties': BIMIfcProperties,
    'configure Psets': BIMIfcProperties,
    # BIMLayers
    'manage layers': BIMLayers,
    'administer layers': BIMLayers,
    'create BIM layer': BIMLayers,
    'open layers manager': BIMLayers,
    # BIMMaterial
    'assign BIM material': BIMMaterial,
    'create material': BIMMaterial,
    'manage materials': BIMMaterial,
    'administer materials': BIMMaterial,
    'material editor': BIMMaterial,
    # BIMPreflight
    'check BIM model': BIMPreflight,
    'validate model': BIMPreflight,
    'run preflight': BIMPreflight,
    'project diagnosis': BIMPreflight,
    # BIMReport
    'create BIM report': BIMReport,
    'generate report': BIMReport,
    'query model': BIMReport,
    'create schedule table': BIMReport,
    # BIMSetup
    'open BIM setup': BIMSetup,
    'BIM setup': BIMSetup,
    'BIM preferences': BIMSetup,
    'BIM settings': BIMSetup,
    # DraftAnnotationStyleEditor
    'edit annotation styles': DraftAnnotationStyleEditor,
    'manage annotation styles': DraftAnnotationStyleEditor,
    'configure text styles': DraftAnnotationStyleEditor,
    'manage dimension styles': DraftAnnotationStyleEditor,
    # ManageDoorsAndWindows
    'manage doors and windows': ManageDoorsAndWindows,
    'manage windows': ManageDoorsAndWindows,
    'modify openings': ManageDoorsAndWindows,
    'door manager': ManageDoorsAndWindows,
    # ManageIFCElements
    'manage IFC elements': ManageIFCElements,
    'manage IFC types': ManageIFCElements,
    'BIM elements manager': ManageIFCElements,
    'assign IFC materials': ManageIFCElements,
    # ManageIFCQuantities
    'manage IFC quantities': ManageIFCQuantities,
    'manage IFC measurements': ManageIFCQuantities,
    'verify quantities': ManageIFCQuantities,
    'BIM quantities manager': ManageIFCQuantities,
    # SetupProject
    'setup BIM project': SetupProject,
    'create IFC project': SetupProject,
    'new BIM project': SetupProject,
    'start root project': SetupProject,
}

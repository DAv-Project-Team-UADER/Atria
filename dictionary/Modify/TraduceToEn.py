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
"""Mapa de voz (EN) para la seccion Modify (consolidado)."""

try:
    from .commands import AddComponent
except ImportError:
    AddComponent = None
try:
    from .commands import Array
except ImportError:
    Array = None
try:
    from .commands import clone
except ImportError:
    clone = None
try:
    from .commands import compound
except ImportError:
    compound = None
try:
    from .commands import copy
except ImportError:
    copy = None
try:
    from .commands import Downgrade
except ImportError:
    Downgrade = None
try:
    from .commands import DraftToSketch
except ImportError:
    DraftToSketch = None
try:
    from .commands import Edit
except ImportError:
    Edit = None
try:
    from .commands import Join
except ImportError:
    Join = None
try:
    from .commands import make_link
except ImportError:
    make_link = None
try:
    from .commands import mirror
except ImportError:
    mirror = None
try:
    from .commands import move
except ImportError:
    move = None
try:
    from .commands import Offset
except ImportError:
    Offset = None
try:
    from .commands import Offset2D
except ImportError:
    Offset2D = None
try:
    from .commands import PathArray
except ImportError:
    PathArray = None
try:
    from .commands import RemoveComponent
except ImportError:
    RemoveComponent = None
try:
    from .commands import rotate
except ImportError:
    rotate = None
try:
    from .commands import scale
except ImportError:
    scale = None
try:
    from .commands import simple_copy
except ImportError:
    simple_copy = None
try:
    from .commands import Split
except ImportError:
    Split = None
try:
    from .commands import Stretch
except ImportError:
    Stretch = None
try:
    from .commands import Trimex
except ImportError:
    Trimex = None
try:
    from .commands import Upgrade
except ImportError:
    Upgrade = None

TraduceToEn = {
    # AddComponent
    'add component': AddComponent,
    'add bim component': AddComponent,
    'attach component': AddComponent,
    'join object to component': AddComponent,
    'assign bim element': AddComponent,
    # Array
    'array': Array,
    'create array': Array,
    'generate array': Array,
    'create orthogonal array': Array,
    'duplicate in array': Array,
    # Clone
    'clone': clone,
    'create clone': clone,
    'clone object': clone,
    'linked duplicate': clone,
    'create linked copy': clone,
    # Compound
    'compound': compound,
    'create compound': compound,
    'group shapes': compound,
    'combine into compound': compound,
    'make compound': compound,
    # Copy
    'copy': copy,
    'copy object': copy,
    'duplicate and move': copy,
    'copy here': copy,
    'create copy': copy,
    # Downgrade
    'downgrade': Downgrade,
    'downgrade object': Downgrade,
    'lower level': Downgrade,
    'decompose object': Downgrade,
    'break down object': Downgrade,
    # DraftToSketch
    'draft to sketch': DraftToSketch,
    'convert to sketch': DraftToSketch,
    'convert draft to sketch': DraftToSketch,
    'draft to sketcher': DraftToSketch,
    'make sketch': DraftToSketch,
    # Edit
    'edit': Edit,
    'edit element': Edit,
    'edit mode': Edit,
    'edit nodes': Edit,
    'graphical edit': Edit,
    # Join
    'join': Join,
    'join elements': Join,
    'join lines': Join,
    'join wires': Join,
    'create single wire': Join,
    # MakeLink
    'make link': make_link,
    'create link': make_link,
    'link object': make_link,
    'make object link': make_link,
    'create object link': make_link,
    # Mirror
    'mirror': mirror,
    'mirror object': mirror,
    'reflect': mirror,
    'reflect object': mirror,
    'create symmetric object': mirror,
    # Move
    'move': move,
    'move object': move,
    'displace': move,
    'translate': move,
    'move element': move,
    # Offset
    'offset': Offset,
    'create offset': Offset,
    'generate offset': Offset,
    'apply offset': Offset,
    'duplicate contour': Offset,
    # Offset2D
    '2d offset': Offset2D,
    'create 2d offset': Offset2D,
    'generate 2d offset': Offset2D,
    'apply planar offset': Offset2D,
    'offset at distance': Offset2D,
    # PathArray
    'path array': PathArray,
    'create path array': PathArray,
    'generate path array': PathArray,
    'array along path': PathArray,
    'duplicate along curve': PathArray,
    # RemoveComponent
    'remove component': RemoveComponent,
    'delete component': RemoveComponent,
    'subtract object': RemoveComponent,
    'detach bim element': RemoveComponent,
    'remove bim component': RemoveComponent,
    # Rotate
    'rotate': rotate,
    'rotate object': rotate,
    'turn object': rotate,
    'turn': rotate,
    'rotate element': rotate,
    # Scale
    'scale': scale,
    'scale object': scale,
    'resize': scale,
    'resize object': scale,
    'adjust scale': scale,
    # SimpleCopy
    'simple copy': simple_copy,
    'create simple copy': simple_copy,
    'copy shape': simple_copy,
    'non parametric copy': simple_copy,
    'copy without link': simple_copy,
    # Split
    'split': Split,
    'split element': Split,
    'cut line': Split,
    'separate wire': Split,
    'split object': Split,
    # Stretch
    'stretch': Stretch,
    'stretch element': Stretch,
    'move vertices': Stretch,
    'deform object': Stretch,
    'apply stretch': Stretch,
    # Trimex
    'trimex': Trimex,
    'trim or extend': Trimex,
    'trim element': Trimex,
    'extend element': Trimex,
    'execute trimex': Trimex,
    # Upgrade
    'upgrade': Upgrade,
    'upgrade object': Upgrade,
    'promote element': Upgrade,
    'raise level': Upgrade,
    'convert to face': Upgrade,
}

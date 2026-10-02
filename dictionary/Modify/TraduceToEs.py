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
"""Mapa de voz (ES) para la seccion Modify (consolidado)."""

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

TraduceToEs = {
    # AddComponent
    'añadir componente': AddComponent,
    'agregar componente': AddComponent,
    'unir objeto a componente': AddComponent,
    'asignar elemento BIM': AddComponent,
    'incorporar componente': AddComponent,
    # Array
    'crear array': Array,
    'generar array': Array,
    'crear matriz ortogonal': Array,
    'duplicar en array': Array,
    'matriz ortogonal': Array,
    # Clone
    'clonar': clone,
    'crear clon': clone,
    'clonar objeto': clone,
    'duplicar vinculado': clone,
    'crear copia vinculada': clone,
    # Compound
    'crear compuesto': compound,
    'compuesto': compound,
    'agrupar formas': compound,
    'combinar en compuesto': compound,
    'hacer compound': compound,
    # Copy
    'copiar': copy,
    'copiar objeto': copy,
    'duplicar y mover': copy,
    'copiar aquí': copy,
    'copiar aqui': copy,
    'crear copia': copy,
    # Downgrade
    'degradar elemento': Downgrade,
    'degradar': Downgrade,
    'bajar nivel': Downgrade,
    'downgrade objeto': Downgrade,
    'descomponer objeto': Downgrade,
    # DraftToSketch
    'convertir a croquis': DraftToSketch,
    'draft a croquis': DraftToSketch,
    'convertir a sketch': DraftToSketch,
    'pasar a boceto': DraftToSketch,
    'convertir draft a croquis': DraftToSketch,
    # Edit
    'editar elemento': Edit,
    'editar': Edit,
    'modo edición': Edit,
    'modo edicion': Edit,
    'editar nodos': Edit,
    'modificar gráfico': Edit,
    'modificar grafico': Edit,
    # Join
    'unir elementos': Join,
    'unir': Join,
    'juntar líneas': Join,
    'juntar lineas': Join,
    'unir alambres': Join,
    'generar alambre único': Join,
    'generar alambre unico': Join,
    # MakeLink
    'crear enlace': make_link,
    'vincular objeto': make_link,
    'crear link': make_link,
    'hacer enlace': make_link,
    'crear vínculo': make_link,
    'crear vinculo': make_link,
    # Mirror
    'espejar': mirror,
    'reflejar': mirror,
    'espejo': mirror,
    'crear simétrico': mirror,
    'crear simetrico': mirror,
    'reflejar objeto': mirror,
    # Move
    'mover': move,
    'mover objeto': move,
    'desplazar': move,
    'trasladar': move,
    'mover elemento': move,
    # Offset
    'crear desfase': Offset,
    'generar offset': Offset,
    'aplicar desfase': Offset,
    'duplicar contorno': Offset,
    'desfase': Offset,
    # Offset2D
    'crear desfase dos d': Offset2D,
    'generar offset dos d': Offset2D,
    'aplicar desfase plano': Offset2D,
    'duplicar a distancia': Offset2D,
    'desfase 2d': Offset2D,
    'offset 2d': Offset2D,
    # PathArray
    'crear path array': PathArray,
    'generar path array': PathArray,
    'crear matriz sobre trayectoria': PathArray,
    'duplicar en curva': PathArray,
    'matriz sobre trayectoria': PathArray,
    # RemoveComponent
    'quitar componente': RemoveComponent,
    'eliminar componente': RemoveComponent,
    'sustraer objeto': RemoveComponent,
    'desvincular elemento BIM': RemoveComponent,
    'remover componente': RemoveComponent,
    # Rotate
    'rotar': rotate,
    'girar': rotate,
    'rotar objeto': rotate,
    'girar objeto': rotate,
    'rotar elemento': rotate,
    # Scale
    'escalar': scale,
    'escalar objeto': scale,
    'cambiar tamaño': scale,
    'cambiar tamano': scale,
    'ajustar escala': scale,
    # SimpleCopy
    'copia simple': simple_copy,
    'crear copia simple': simple_copy,
    'copiar forma': simple_copy,
    'copia no paramétrica': simple_copy,
    'copia no parametrica': simple_copy,
    'copiar sin vínculo': simple_copy,
    'copiar sin vinculo': simple_copy,
    # Split
    'dividir elemento': Split,
    'dividir': Split,
    'cortar línea': Split,
    'cortar linea': Split,
    'separar alambre': Split,
    'escindir objeto': Split,
    # Stretch
    'estirar elemento': Stretch,
    'estirar': Stretch,
    'aplicar stretch': Stretch,
    'mover vértices': Stretch,
    'mover vertices': Stretch,
    'deformar objeto': Stretch,
    # Trimex
    'recortar o extender': Trimex,
    'ejecutar trimex': Trimex,
    'recortar elemento': Trimex,
    'extender elemento': Trimex,
    'trimex': Trimex,
    # Upgrade
    'promover elemento': Upgrade,
    'promover': Upgrade,
    'elevar nivel': Upgrade,
    'upgrade objeto': Upgrade,
    'convertir a cara': Upgrade,
}

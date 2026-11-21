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
try:
    from .commands import CutWithPlane
except ImportError:
    CutWithPlane = None
try:
    from .commands import Difference
except ImportError:
    Difference = None
try:
    from .commands import ExtrudeFace
except ImportError:
    ExtrudeFace = None
try:
    from .commands import Extrude
except ImportError:
    Extrude = None
try:
    from .commands import Intersection
except ImportError:
    Intersection = None
try:
    from .commands import PointArray
except ImportError:
    PointArray = None
try:
    from .commands import PolarArray
except ImportError:
    PolarArray = None
try:
    from .commands import Union
except ImportError:
    Union = None

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
    'desarmar elemento': Downgrade,
    'descomponer objeto': Downgrade,
    # DraftToSketch
    'convertir a croquis': DraftToSketch,
    'draft a croquis': DraftToSketch,
    'transformar dibujo en croquis': DraftToSketch,
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
    'crear reflejo': mirror,
    'reflejar': mirror,
    'espejo': mirror,
    'crear simétrico': mirror,
    'crear simetrico': mirror,
    'reflejar objeto': mirror,
    # Move
    'cambiar posición': move,
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
    'desplazar contorno plano': Offset2D,
    'separar contorno a distancia': Offset2D,
    'aplicar desfase plano': Offset2D,
    'duplicar a distancia': Offset2D,
    'desfase 2d': Offset2D,
    'offset 2d': Offset2D,
    # PathArray
    'repetir objetos a lo largo de una curva': PathArray,
    'distribuir copias sobre un recorrido': PathArray,
    'crear matriz sobre trayectoria': PathArray,
    'duplicar en curva': PathArray,
    'matriz sobre trayectoria': PathArray,
    # RemoveComponent
    'quitar componente': RemoveComponent,
    'eliminar componente': RemoveComponent,
    'sustraer objeto': RemoveComponent,
    'retirar del componente': RemoveComponent,
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
    'duplicar solo la forma': simple_copy,
    'duplicar sin relación con el original': simple_copy,
    'copiar sin vínculo': simple_copy,
    'copiar sin vinculo': simple_copy,
    # Split
    'dividir elemento': Split,
    'dividir': Split,
    'cortar línea': Split,
    'cortar linea': Split,
    'separar el trazado': Split,
    'partir el elemento': Split,
    # Stretch
    'estirar elemento': Stretch,
    'estirar': Stretch,
    'estirar contorno': Stretch,
    'mover vértices': Stretch,
    'mover vertices': Stretch,
    'cambiar la forma del elemento': Stretch,
    # Trimex
    'recortar o extender': Trimex,
    'ajustar longitud del borde': Trimex,
    'recortar elemento': Trimex,
    'extender elemento': Trimex,
    'ajustar longitud del trazado': Trimex,
    # Upgrade
    'promover elemento': Upgrade,
    'promover': Upgrade,
    'elevar nivel': Upgrade,
    'subir nivel del elemento': Upgrade,
    'convertir a cara': Upgrade,
    # CutWithPlane
    'cortar con plano': CutWithPlane,
    'cortar mediante plano': CutWithPlane,
    'aplicar plano de corte': CutWithPlane,
    'corte plano': CutWithPlane,
    # Difference
    'cortar objetos': Difference,
    'restar objetos': Difference,
    'aplicar diferencia': Difference,
    'quitar un sólido de otro': Difference,
    # ExtrudeFace
    'prolongar la cara': ExtrudeFace,
    'levantar la cara seleccionada': ExtrudeFace,
    'crear volumen desde la cara': ExtrudeFace,
    # Extrude
    'prolongar la pieza': Extrude,
    'dar profundidad a la forma': Extrude,
    'extender el perfil en profundidad': Extrude,
    'dar volumen tridimensional': Extrude,
    # Intersection
    'obtener el volumen común': Intersection,
    'crear intersección': Intersection,
    'extraer parte común': Intersection,
    'volumen compartido': Intersection,
    # PointArray
    'crear matriz por puntos': PointArray,
    'nueva matriz de puntos': PointArray,
    'arreglo por puntos': PointArray,
    'distribuir en puntos': PointArray,
    # PolarArray
    'crear matriz polar': PolarArray,
    'nueva matriz polar': PolarArray,
    'arreglo polar': PolarArray,
    'generar matriz circular': PolarArray,
    # Union
    'unir objetos': Union,
    'fusionar piezas': Union,
    'fusionar sólidos en uno': Union,
    'combinar sólidos': Union,
}
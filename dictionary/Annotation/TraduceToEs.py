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

"""Mapa de voz (ES) para la seccion Annotation (consolidado)."""

TwoDDrawing = None  # TODO: sin implementacion en commands.py
try:
    from .commands import aligned_dimension as Aligned_Dimension
except ImportError:
    Aligned_Dimension = None
Axis = None  # TODO: sin implementacion en commands.py
AxisSystem = None  # TODO: sin implementacion en commands.py
Grid = None  # TODO: sin implementacion en commands.py
Hatch = None  # TODO: sin implementacion en commands.py
try:
    from .commands import horizontal_dimension as Horizontal_Dimension
except ImportError:
    Horizontal_Dimension = None
Label = None  # TODO: sin implementacion en commands.py
Leader = None  # TODO: sin implementacion en commands.py
NewPage = None  # TODO: sin implementacion en commands.py
NewView = None  # TODO: sin implementacion en commands.py
SectionCut = None  # TODO: sin implementacion en commands.py
SectionPlane = None  # TODO: sin implementacion en commands.py
SectionView = None  # TODO: sin implementacion en commands.py
Text = None  # TODO: sin implementacion en commands.py
try:
    from .commands import vertical_dimension as Vertical_Dimension
except ImportError:
    Vertical_Dimension = None

TraduceToEs = {
    # 2DDrawing
    'dibujo 2d': TwoDDrawing,
    'crear dibujo 2d': TwoDDrawing,
    'plano 2d': TwoDDrawing,
    'crear plano 2d': TwoDDrawing,
    'vista 2d': TwoDDrawing,
    'crear vista 2d': TwoDDrawing,
    # Aligned_Dimension
    'cota alineada': Aligned_Dimension,
    'crear cota alineada': Aligned_Dimension,
    'agregar cota alineada': Aligned_Dimension,
    'insertar cota alineada': Aligned_Dimension,
    'acotar alineado': Aligned_Dimension,
    'acotar de forma alineada': Aligned_Dimension,
    'dimension alineada': Aligned_Dimension,
    'dimensión alineada': Aligned_Dimension,
    'crear dimension alineada': Aligned_Dimension,
    'crear dimensión alineada': Aligned_Dimension,
    # Axis
    'eje': Axis,
    'ejes': Axis,
    'crear eje': Axis,
    'crear ejes': Axis,
    'agregar ejes': Axis,
    'ejes de referencia': Axis,
    'retícula de ejes': Axis,
    'reticula de ejes': Axis,
    # AxisSystem
    'sistema de ejes': AxisSystem,
    'crear sistema de ejes': AxisSystem,
    'agregar sistema de ejes': AxisSystem,
    'combinar ejes': AxisSystem,
    'conjunto de ejes': AxisSystem,
    # Grid
    'rejilla': Grid,
    'crear rejilla': Grid,
    'agregar rejilla': Grid,
    'añadir rejilla': Grid,
    'insertar rejilla': Grid,
    'malla': Grid,
    'crear malla': Grid,
    # Hatch
    'sombreado': Hatch,
    'crear sombreado': Hatch,
    'aplicar sombreado': Hatch,
    'trama': Hatch,
    'crear trama': Hatch,
    'relleno': Hatch,
    'aplicar trama': Hatch,
    # Horizontal_Dimension
    'cota horizontal': Horizontal_Dimension,
    'crear cota horizontal': Horizontal_Dimension,
    'agregar cota horizontal': Horizontal_Dimension,
    'insertar cota horizontal': Horizontal_Dimension,
    'acotar horizontal': Horizontal_Dimension,
    'acotar horizontalmente': Horizontal_Dimension,
    'dimension horizontal': Horizontal_Dimension,
    'dimensión horizontal': Horizontal_Dimension,
    'crear dimension horizontal': Horizontal_Dimension,
    'crear dimensión horizontal': Horizontal_Dimension,
    # Label
    'etiqueta': Label,
    'crear etiqueta': Label,
    'agregar etiqueta': Label,
    'añadir etiqueta': Label,
    'insertar etiqueta': Label,
    'nueva etiqueta': Label,
    # Leader
    'líder': Leader,
    'lider': Leader,
    'crear líder': Leader,
    'crear lider': Leader,
    'agregar líder': Leader,
    'línea de referencia': Leader,
    'linea de referencia': Leader,
    'flecha de referencia': Leader,
    'crear línea de referencia': Leader,
    # NewPage
    'nueva página': NewPage,
    'nueva pagina': NewPage,
    'crear página': NewPage,
    'crear pagina': NewPage,
    'hoja nueva': NewPage,
    'nueva hoja': NewPage,
    'nueva lámina': NewPage,
    'nueva lamina': NewPage,
    # NewView
    'vista nueva': NewView,
    'nueva vista': NewView,
    'crear nueva vista': NewView,
    'crear vista': NewView,
    'añadir vista': NewView,
    'agregar vista': NewView,
    'insertar vista': NewView,
    # SectionCut
    'corte de sección': SectionCut,
    'corte de seccion': SectionCut,
    'crear corte de sección': SectionCut,
    'crear corte de seccion': SectionCut,
    'corte': SectionCut,
    'crear corte': SectionCut,
    # SectionPlane
    'plano de sección': SectionPlane,
    'plano de seccion': SectionPlane,
    'crear plano de sección': SectionPlane,
    'crear plano de seccion': SectionPlane,
    'plano de corte': SectionPlane,
    'crear plano de corte': SectionPlane,
    'sección': SectionPlane,
    'seccion': SectionPlane,
    # SectionView
    'vista de sección': SectionView,
    'vista de seccion': SectionView,
    'crear vista de sección': SectionView,
    'crear vista de seccion': SectionView,
    'alzado': SectionView,
    'crear alzado': SectionView,
    # Text
    'texto': Text,
    'crear texto': Text,
    'agregar texto': Text,
    'añadir texto': Text,
    'insertar texto': Text,
    'nuevo texto': Text,
    'escribir texto': Text,
    # Vertical_Dimension
    'cota vertical': Vertical_Dimension,
    'crear cota vertical': Vertical_Dimension,
    'agregar cota vertical': Vertical_Dimension,
    'insertar cota vertical': Vertical_Dimension,
    'acotar vertical': Vertical_Dimension,
    'acotar verticalmente': Vertical_Dimension,
    'dimension vertical': Vertical_Dimension,
    'dimensión vertical': Vertical_Dimension,
    'crear dimension vertical': Vertical_Dimension,
    'crear dimensión vertical': Vertical_Dimension,
}

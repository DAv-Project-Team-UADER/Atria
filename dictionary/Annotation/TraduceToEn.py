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
"""Mapa de voz (EN) para la seccion Annotation (consolidado)."""

try:
    from .commands import TwoDDrawing
except ImportError:
    TwoDDrawing = None
try:
    from .commands import aligned_dimension as Aligned_Dimension
except ImportError:
    Aligned_Dimension = None
try:
    from .commands import Axis
except ImportError:
    Axis = None
try:
    from .commands import AxisSystem
except ImportError:
    AxisSystem = None
try:
    from .commands import Grid
except ImportError:
    Grid = None
try:
    from .commands import Hatch
except ImportError:
    Hatch = None
try:
    from .commands import horizontal_dimension as Horizontal_Dimension
except ImportError:
    Horizontal_Dimension = None
try:
    from .commands import Label
except ImportError:
    Label = None
try:
    from .commands import Leader
except ImportError:
    Leader = None
try:
    from .commands import NewPage
except ImportError:
    NewPage = None
try:
    from .commands import NewView
except ImportError:
    NewView = None
try:
    from .commands import SectionCut
except ImportError:
    SectionCut = None
try:
    from .commands import SectionPlane
except ImportError:
    SectionPlane = None
try:
    from .commands import SectionView
except ImportError:
    SectionView = None
try:
    from .commands import Text
except ImportError:
    Text = None
try:
    from .commands import vertical_dimension as Vertical_Dimension
except ImportError:
    Vertical_Dimension = None

TraduceToEn = {
    # 2DDrawing
    '2d drawing': TwoDDrawing,
    'create 2d drawing': TwoDDrawing,
    'add 2d drawing': TwoDDrawing,
    '2d plan': TwoDDrawing,
    '2d view': TwoDDrawing,
    'create 2d view': TwoDDrawing,
    # Aligned_Dimension
    'aligned dimension': Aligned_Dimension,
    'create aligned dimension': Aligned_Dimension,
    'add aligned dimension': Aligned_Dimension,
    'insert aligned dimension': Aligned_Dimension,
    'aligned measurement': Aligned_Dimension,
    'create aligned measurement': Aligned_Dimension,
    # Axis
    'axis': Axis,
    'axes': Axis,
    'create axis': Axis,
    'create axes': Axis,
    'add axis': Axis,
    'reference axis': Axis,
    'axis grid': Axis,
    # AxisSystem
    'axis system': AxisSystem,
    'create axis system': AxisSystem,
    'add axis system': AxisSystem,
    'combine axes': AxisSystem,
    'axes system': AxisSystem,
    # Grid
    'grid': Grid,
    'create grid': Grid,
    'add grid': Grid,
    'insert grid': Grid,
    'grid object': Grid,
    'make grid': Grid,
    # Hatch
    'hatch': Hatch,
    'create hatch': Hatch,
    'add hatch': Hatch,
    'apply hatch': Hatch,
    'hatching': Hatch,
    'fill pattern': Hatch,
    'apply hatching': Hatch,
    # Horizontal_Dimension
    'horizontal dimension': Horizontal_Dimension,
    'create horizontal dimension': Horizontal_Dimension,
    'add horizontal dimension': Horizontal_Dimension,
    'insert horizontal dimension': Horizontal_Dimension,
    'dimension horizontally': Horizontal_Dimension,
    'horizontal measurement': Horizontal_Dimension,
    'create horizontal measurement': Horizontal_Dimension,
    # Label
    'label': Label,
    'create label': Label,
    'add label': Label,
    'insert label': Label,
    'annotation label': Label,
    'new label': Label,
    # Leader
    'leader': Leader,
    'create leader': Leader,
    'add leader': Leader,
    'insert leader': Leader,
    'reference line': Leader,
    'arrow leader': Leader,
    'create reference line': Leader,
    # NewPage
    'new page': NewPage,
    'create new page': NewPage,
    'create page': NewPage,
    'add page': NewPage,
    'new sheet': NewPage,
    'create new sheet': NewPage,
    # NewView
    'new view': NewView,
    'create new view': NewView,
    'create view': NewView,
    'add view': NewView,
    'insert view': NewView,
    'new techdraw view': NewView,
    # SectionCut
    'section cut': SectionCut,
    'create section cut': SectionCut,
    'add section cut': SectionCut,
    'cut view': SectionCut,
    'create cut': SectionCut,
    # SectionPlane
    'section plane': SectionPlane,
    'create section plane': SectionPlane,
    'add section plane': SectionPlane,
    'cutting plane': SectionPlane,
    'create cutting plane': SectionPlane,
    # SectionView
    'section view': SectionView,
    'create section view': SectionView,
    'add section view': SectionView,
    'projected section view': SectionView,
    'create section projection': SectionView,
    # Text
    'text': Text,
    'create text': Text,
    'add text': Text,
    'insert text': Text,
    'new text': Text,
    'write text': Text,
    # Vertical_Dimension
    'vertical dimension': Vertical_Dimension,
    'create vertical dimension': Vertical_Dimension,
    'add vertical dimension': Vertical_Dimension,
    'insert vertical dimension': Vertical_Dimension,
    'dimension vertically': Vertical_Dimension,
    'vertical measurement': Vertical_Dimension,
    'create vertical measurement': Vertical_Dimension,
}

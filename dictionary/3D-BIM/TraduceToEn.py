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
"""Mapa de voz (EN) para la seccion 3D-BIM (consolidado)."""

try:
    from .commands import Beam
except ImportError:
    Beam = None
try:
    from .commands import beam_reinforcement as Beam_Reinforcement
except ImportError:
    Beam_Reinforcement = None
try:
    from .commands import box as Box
except ImportError:
    Box = None
try:
    from .commands import Building
except ImportError:
    Building = None
try:
    from .commands import Column
except ImportError:
    Column = None
try:
    from .commands import column_reinforcement as Column_Reinforcement
except ImportError:
    Column_Reinforcement = None
try:
    from .commands import component as Component
except ImportError:
    Component = None
try:
    from .commands import CurtainWall
except ImportError:
    CurtainWall = None
try:
    from .commands import Door
except ImportError:
    Door = None
try:
    from .commands import external_reference as External_Reference
except ImportError:
    External_Reference = None
try:
    from .commands import facebinder as Facebinder
except ImportError:
    Facebinder = None
try:
    from .commands import footing_reinforcement as Footing_Reinforcement
except ImportError:
    Footing_Reinforcement = None
try:
    from .commands import Level
except ImportError:
    Level = None
try:
    from .commands import objects_library as Objects_Library
except ImportError:
    Objects_Library = None
try:
    from .commands import Pipe
except ImportError:
    Pipe = None
try:
    from .commands import PipeConnector
except ImportError:
    PipeConnector = None
try:
    from .commands import profile as Profile
except ImportError:
    Profile = None
try:
    from .commands import Roof
except ImportError:
    Roof = None
try:
    from .commands import shape_builder as Shape_Builder
except ImportError:
    Shape_Builder = None
try:
    from .commands import Site
except ImportError:
    Site = None
try:
    from .commands import Slab
except ImportError:
    Slab = None
try:
    from .commands import slab_reinforcement as Slab_Reinforcement
except ImportError:
    Slab_Reinforcement = None
try:
    from .commands import Space
except ImportError:
    Space = None
try:
    from .commands import Wall
except ImportError:
    Wall = None
try:
    from .commands import Window
except ImportError:
    Window = None
ArchEquipment = None  # TODO: sin implementacion en commands.py
ArchFence = None  # TODO: sin implementacion en commands.py
ArchFrame = None  # TODO: sin implementacion en commands.py
ArchPanel = None  # TODO: sin implementacion en commands.py
ArchRebar = None  # TODO: sin implementacion en commands.py
ArchRoof = None  # TODO: sin implementacion en commands.py
ArchStairs = None  # TODO: sin implementacion en commands.py
ArchTruss = None  # TODO: sin implementacion en commands.py
BentShapeRebar = None  # TODO: sin implementacion en commands.py
HelicalRebar = None  # TODO: sin implementacion en commands.py
LShapeRebar = None  # TODO: sin implementacion en commands.py
StirrupRebar = None  # TODO: sin implementacion en commands.py
StraightRebar = None  # TODO: sin implementacion en commands.py
UShapeRebar = None  # TODO: sin implementacion en commands.py

TraduceToEn = {
    # Beam
    'create beam': Beam,
    'new beam': Beam,
    'generate beam': Beam,
    'add beam': Beam,
    # Beam_Reinforcement
    'beam reinforcement': Beam_Reinforcement,
    'add beam reinforcement': Beam_Reinforcement,
    'create beam reinforcement': Beam_Reinforcement,
    'reinforce beam': Beam_Reinforcement,
    'reinforce the beam': Beam_Reinforcement,
    'add reinforcement to beam': Beam_Reinforcement,
    'add reinforcement to the beam': Beam_Reinforcement,
    'add beam rebar': Beam_Reinforcement,
    'create beam rebar': Beam_Reinforcement,
    # Box
    'create ': Box,
    'insert ': Box,
    'add ': Box,
    'create block': Box,
    'insert block': Box,
    'add block': Box,
    ' by dimensions': Box,
    'create  by dimensions': Box,
    'cube': Box,
    'create cube': Box,
    'insert cube': Box,
    # Building
    'create building': Building,
    'new building': Building,
    'generate building': Building,
    'add building': Building,
    # Column
    'create column': Column,
    'new column': Column,
    'generate pillar': Column,
    'add column': Column,
    # Column_Reinforcement
    'column reinforcement': Column_Reinforcement,
    'add column reinforcement': Column_Reinforcement,
    'create column reinforcement': Column_Reinforcement,
    'reinforce column': Column_Reinforcement,
    'reinforce the column': Column_Reinforcement,
    'add reinforcement to column': Column_Reinforcement,
    'add reinforcement to the column': Column_Reinforcement,
    'add column rebar': Column_Reinforcement,
    'create column rebar': Column_Reinforcement,
    # Component
    'convert to component': Component,
    'create component': Component,
    'make component': Component,
    'make Arch component': Component,
    'convert to Arch component': Component,
    'generic component': Component,
    'create generic component': Component,
    # CurtainWall
    'create curtain wall': CurtainWall,
    'new curtain wall': CurtainWall,
    'generate glass facade': CurtainWall,
    'add curtain wall': CurtainWall,
    # Door
    'create door': Door,
    'new door': Door,
    'generate door': Door,
    'add door': Door,
    # External_Reference
    'external reference': External_Reference,
    'insert external reference': External_Reference,
    'create external reference': External_Reference,
    'add external reference': External_Reference,
    'link object from another file': External_Reference,
    'link object from external file': External_Reference,
    'link external object': External_Reference,
    'link document': External_Reference,
    'link external document': External_Reference,
    # Facebinder
    'facebinder': Facebinder,
    'create facebinder': Facebinder,
    'add facebinder': Facebinder,
    'surface from faces': Facebinder,
    'create surface from faces': Facebinder,
    'face covering': Facebinder,
    'create face covering': Facebinder,
    # Footing_Reinforcement
    'footing reinforcement': Footing_Reinforcement,
    'add footing reinforcement': Footing_Reinforcement,
    'create footing reinforcement': Footing_Reinforcement,
    'reinforce footing': Footing_Reinforcement,
    'reinforce the footing': Footing_Reinforcement,
    'add reinforcement to footing': Footing_Reinforcement,
    'add reinforcement to the footing': Footing_Reinforcement,
    'add footing rebar': Footing_Reinforcement,
    'create footing rebar': Footing_Reinforcement,
    # Level
    'create level': Level,
    'new level': Level,
    'generate floor': Level,
    'add level': Level,
    'create floor': Level,
    # Objects_Library
    'objects library': Objects_Library,
    'object library': Objects_Library,
    'open objects library': Objects_Library,
    'open object library': Objects_Library,
    'insert library object': Objects_Library,
    'add library object': Objects_Library,
    'insert object from library': Objects_Library,
    'insert furniture': Objects_Library,
    'add furniture': Objects_Library,
    'insert equipment': Objects_Library,
    'add equipment': Objects_Library,
    # Pipe
    'create pipe': Pipe,
    'new piping': Pipe,
    'generate conduit': Pipe,
    'add pipe': Pipe,
    # PipeConnector
    'create connector': PipeConnector,
    'new connector': PipeConnector,
    'generate pipe joint': PipeConnector,
    'add connection': PipeConnector,
    # Profile
    'create profile': Profile,
    'insert profile': Profile,
    'add profile': Profile,
    'create structural profile': Profile,
    'insert structural profile': Profile,
    'add structural profile': Profile,
    'create parametric profile': Profile,
    'insert parametric profile': Profile,
    'parametric profile': Profile,
    # Roof
    'create roof': Roof,
    'new roof': Roof,
    'generate roof': Roof,
    'add sloped roof': Roof,
    # Shape_Builder
    'shape builder': Shape_Builder,
    'open shape builder': Shape_Builder,
    'create shape': Shape_Builder,
    'build shape': Shape_Builder,
    'create geometric shape': Shape_Builder,
    'build geometric shape': Shape_Builder,
    'build face': Shape_Builder,
    'build shell': Shape_Builder,
    'build solid': Shape_Builder,
    # Site
    'create site': Site,
    'new site': Site,
    'generate terrain': Site,
    'add site': Site,
    # Slab
    'create slab': Slab,
    'new slab': Slab,
    'generate plate': Slab,
    'add slab': Slab,
    # Slab_Reinforcement
    'slab reinforcement': Slab_Reinforcement,
    'add slab reinforcement': Slab_Reinforcement,
    'create slab reinforcement': Slab_Reinforcement,
    'reinforce slab': Slab_Reinforcement,
    'reinforce the slab': Slab_Reinforcement,
    'add reinforcement to slab': Slab_Reinforcement,
    'add reinforcement to the slab': Slab_Reinforcement,
    'add slab rebar': Slab_Reinforcement,
    'create slab rebar': Slab_Reinforcement,
    # Space
    'create space': Space,
    'new ambience': Space,
    'generate room': Space,
    'add space': Space,
    # Wall
    'create wall': Wall,
    'new wall': Wall,
    'generate wall': Wall,
    'add wall': Wall,
    # Window
    'create window': Window,
    'new window': Window,
    'generate window': Window,
    'add window': Window,
    # ArchEquipment
    'create equipment': ArchEquipment,
    'new equipment': ArchEquipment,
    'insert equipment': ArchEquipment,
    'add furniture': ArchEquipment,
    # ArchFence
    'create fence': ArchFence,
    'new fence': ArchFence,
    'generate fence': ArchFence,
    'add fence': ArchFence,
    # ArchFrame
    'create frame': ArchFrame,
    'new frame': ArchFrame,
    'generate frame': ArchFrame,
    'add frame': ArchFrame,
    # ArchPanel
    'create panel': ArchPanel,
    'new panel': ArchPanel,
    'generate panel': ArchPanel,
    'add panel': ArchPanel,
    # ArchRebar
    'create custom rebar': ArchRebar,
    'new reinforcing bar': ArchRebar,
    'generate rebar': ArchRebar,
    'add rebar': ArchRebar,
    'create custom bar': ArchRebar,
    # ArchRoof
    'create roof': ArchRoof,
    'new roof': ArchRoof,
    'generate roof': ArchRoof,
    'add roof': ArchRoof,
    # ArchStairs
    'create stairs': ArchStairs,
    'new stairs': ArchStairs,
    'generate stairs': ArchStairs,
    'add stairs': ArchStairs,
    # ArchTruss
    'create truss': ArchTruss,
    'new truss': ArchTruss,
    'generate truss': ArchTruss,
    'add truss': ArchTruss,
    'create lattice': ArchTruss,
    # BentShapeRebar
    'create bent-shape rebar': BentShapeRebar,
    'new bent bar': BentShapeRebar,
    'generate bent-shape rebar': BentShapeRebar,
    'add bent reinforcing bar': BentShapeRebar,
    'create bent rebar': BentShapeRebar,
    # HelicalRebar
    'create helical rebar': HelicalRebar,
    'new helical bar': HelicalRebar,
    'generate spiral rebar': HelicalRebar,
    'add helical bar': HelicalRebar,
    # LShapeRebar
    'create L-shape rebar': LShapeRebar,
    'new L bar': LShapeRebar,
    'generate L-shape rebar': LShapeRebar,
    'add L reinforcing bar': LShapeRebar,
    'create L rebar': LShapeRebar,
    # StirrupRebar
    'create stirrup': StirrupRebar,
    'new stirrup': StirrupRebar,
    'generate stirrups': StirrupRebar,
    'add stirrup': StirrupRebar,
    'create reinforcing hoop': StirrupRebar,
    # StraightRebar
    'create straight rebar': StraightRebar,
    'new straight bar': StraightRebar,
    'generate straight rebar': StraightRebar,
    'add straight reinforcing bar': StraightRebar,
    # UShapeRebar
    'create U-shape rebar': UShapeRebar,
    'new U bar': UShapeRebar,
    'generate U-shape rebar': UShapeRebar,
    'add U reinforcing bar': UShapeRebar,
    'create U rebar': UShapeRebar,
}

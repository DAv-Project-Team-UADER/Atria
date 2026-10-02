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
"""Mapa de voz (ES) para la seccion 3D-BIM (consolidado)."""

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

TraduceToEs = {
    # Beam
    'crear viga': Beam,
    'nueva viga': Beam,
    'generar haz': Beam,
    'añadir viga': Beam,
    # Beam_Reinforcement
    'reforzar viga': Beam_Reinforcement,
    'agregar refuerzo de viga': Beam_Reinforcement,
    'añadir refuerzo de viga': Beam_Reinforcement,
    'crear refuerzo de viga': Beam_Reinforcement,
    'refuerzo de vigas': Beam_Reinforcement,
    'armar viga': Beam_Reinforcement,
    'agregar armadura de viga': Beam_Reinforcement,
    'añadir armadura de viga': Beam_Reinforcement,
    # Box
    'crear caja': Box,
    'insertar caja': Box,
    'agregar caja': Box,
    'crear bloque': Box,
    'insertar bloque': Box,
    'agregar bloque': Box,
    'caja por dimensiones': Box,
    'crear caja por dimensiones': Box,
    'cubo': Box,
    'crear cubo': Box,
    'insertar cubo': Box,
    # Building
    'crear edificio': Building,
    'nuevo edificio': Building,
    'generar edificio': Building,
    'añadir edificio': Building,
    # Column
    'crear columna': Column,
    'nueva columna': Column,
    'generar pilar': Column,
    'añadir columna': Column,
    # Column_Reinforcement
    'reforzar columna': Column_Reinforcement,
    'agregar refuerzo de columna': Column_Reinforcement,
    'añadir refuerzo de columna': Column_Reinforcement,
    'añadir refuerzo de columnas': Column_Reinforcement,
    'crear refuerzo de columna': Column_Reinforcement,
    'armar columna': Column_Reinforcement,
    'agregar armadura de columna': Column_Reinforcement,
    'añadir armadura de columna': Column_Reinforcement,
    # Component
    'convertir en componente': Component,
    'crear componente': Component,
    'hacer componente': Component,
    'hacer componente Arch': Component,
    'convertir en componente Arch': Component,
    'componente generico': Component,
    'componente genérico': Component,
    'crear componente generico': Component,
    'crear componente genérico': Component,
    # CurtainWall
    'crear muro cortina': CurtainWall,
    'nuevo muro cortina': CurtainWall,
    'generar fachada de cristal': CurtainWall,
    'añadir curtain wall': CurtainWall,
    # Door
    'crear puerta': Door,
    'nueva puerta': Door,
    'generar puerta': Door,
    'añadir puerta': Door,
    # External_Reference
    'referencia externa': External_Reference,
    'insertar referencia externa': External_Reference,
    'crear referencia externa': External_Reference,
    'agregar referencia externa': External_Reference,
    'vincular objeto de otro archivo': External_Reference,
    'enlazar objeto de otro archivo': External_Reference,
    'vincular objeto externo': External_Reference,
    'enlazar objeto externo': External_Reference,
    'enlazar documento': External_Reference,
    'vincular documento': External_Reference,
    # Facebinder
    'crear atrapacaras': Facebinder,
    'atrapacaras': Facebinder,
    'facebinder': Facebinder,
    'crear facebinder': Facebinder,
    'superficie desde caras': Facebinder,
    'crear superficie desde caras': Facebinder,
    'revestimiento de caras': Facebinder,
    'crear revestimiento de caras': Facebinder,
    # Footing_Reinforcement
    'reforzar zapata': Footing_Reinforcement,
    'agregar refuerzo de zapata': Footing_Reinforcement,
    'añadir refuerzo de zapata': Footing_Reinforcement,
    'crear refuerzo de zapata': Footing_Reinforcement,
    'refuerzo de zapatas': Footing_Reinforcement,
    'armar zapata': Footing_Reinforcement,
    'agregar armadura de zapata': Footing_Reinforcement,
    'añadir armadura de zapata': Footing_Reinforcement,
    # Level
    'crear nivel': Level,
    'nuevo nivel': Level,
    'generar piso': Level,
    'añadir nivel': Level,
    'crear planta': Level,
    # Objects_Library
    'biblioteca de objetos': Objects_Library,
    'abrir biblioteca de objetos': Objects_Library,
    'insertar objeto de biblioteca': Objects_Library,
    'agregar objeto de biblioteca': Objects_Library,
    'insertar objeto desde biblioteca': Objects_Library,
    'insertar mobiliario': Objects_Library,
    'agregar mobiliario': Objects_Library,
    'insertar equipo': Objects_Library,
    'agregar equipo': Objects_Library,
    # Pipe
    'crear tubo': Pipe,
    'nueva tubería': Pipe,
    'generar caño': Pipe,
    'añadir tubo': Pipe,
    # PipeConnector
    'crear conector': PipeConnector,
    'nuevo conector': PipeConnector,
    'generar unión de tubos': PipeConnector,
    'añadir conexión': PipeConnector,
    # Profile
    'crear perfil': Profile,
    'insertar perfil': Profile,
    'agregar perfil': Profile,
    'crear perfil estructural': Profile,
    'insertar perfil estructural': Profile,
    'agregar perfil estructural': Profile,
    'crear perfil parametrico': Profile,
    'insertar perfil parametrico': Profile,
    'perfil parametrico': Profile,
    # Roof
    'crear cubierta': Roof,
    'nuevo techo': Roof,
    'generar cubierta': Roof,
    'añadir techo inclinado': Roof,
    # Shape_Builder
    'constructor de formas': Shape_Builder,
    'abrir constructor de formas': Shape_Builder,
    'crear forma': Shape_Builder,
    'construir forma': Shape_Builder,
    'crear forma geométrica': Shape_Builder,
    'construir forma geométrica': Shape_Builder,
    'construir cara': Shape_Builder,
    'construir cascara': Shape_Builder,
    'construir cáscara': Shape_Builder,
    'construir solido': Shape_Builder,
    'construir sólido': Shape_Builder,
    # Site
    'crear sitio': Site,
    'nuevo sitio': Site,
    'generar terreno': Site,
    'añadir emplazamiento': Site,
    # Slab
    'crear losa': Slab,
    'nueva losa': Slab,
    'generar placa': Slab,
    'añadir losa': Slab,
    # Slab_Reinforcement
    'reforzar losa': Slab_Reinforcement,
    'agregar refuerzo de losa': Slab_Reinforcement,
    'añadir refuerzo de losa': Slab_Reinforcement,
    'crear refuerzo de losa': Slab_Reinforcement,
    'refuerzo de losas': Slab_Reinforcement,
    'armar losa': Slab_Reinforcement,
    'agregar armadura de losa': Slab_Reinforcement,
    'añadir armadura de losa': Slab_Reinforcement,
    # Space
    'crear espacio': Space,
    'nuevo ambiente': Space,
    'generar habitación': Space,
    'añadir espacio': Space,
    # Wall
    'crear muro': Wall,
    'nuevo muro': Wall,
    'generar pared': Wall,
    'añadir muro': Wall,
    # Window
    'crear ventana': Window,
    'nueva ventana': Window,
    'generar ventana': Window,
    'añadir ventana': Window,
}

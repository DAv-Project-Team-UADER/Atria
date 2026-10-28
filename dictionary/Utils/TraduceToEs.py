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
"""Mapa de voz (ES) para la seccion Utils (consolidado)."""

try:
    from .commands import unclone
except ImportError:
    unclone = None
add_to_construction_group = None  # TODO: sin implementacion en commands.py
check = None  # TODO: sin implementacion en commands.py
close_holes = None  # TODO: sin implementacion en commands.py
convert_to_ifc_project = None  # TODO: sin implementacion en commands.py
ifc_diff = None  # TODO: sin implementacion en commands.py
structure = None  # TODO: sin implementacion en commands.py
multiple_structures = None  # TODO: sin implementacion en commands.py
panel_sheet = None  # TODO: sin implementacion en commands.py
ifc_expand = None  # TODO: sin implementacion en commands.py
ifc_explorer = None  # TODO: sin implementacion en commands.py
ifc_openshell_update = None  # TODO: sin implementacion en commands.py
ifc_shape_diff = None  # TODO: sin implementacion en commands.py
image_plane = None  # TODO: sin implementacion en commands.py
lock_ifc = None  # TODO: sin implementacion en commands.py
merge_walls = None  # TODO: sin implementacion en commands.py
mesh_to_shape = None  # TODO: sin implementacion en commands.py
new_ifc_spreadsheet = None  # TODO: sin implementacion en commands.py
nest = None  # TODO: sin implementacion en commands.py
nudge_down = None  # TODO: sin implementacion en commands.py
nudge_extend = None  # TODO: sin implementacion en commands.py
nudge_left = None  # TODO: sin implementacion en commands.py
nudge_right = None  # TODO: sin implementacion en commands.py
nudge_rotate_left = None  # TODO: sin implementacion en commands.py
nudge_rotate_right = None  # TODO: sin implementacion en commands.py
nudge_shrink = None  # TODO: sin implementacion en commands.py
nudge_switch = None  # TODO: sin implementacion en commands.py
nudge_up = None  # TODO: sin implementacion en commands.py
panel = None  # TODO: sin implementacion en commands.py
glue = None  # TODO: sin implementacion en commands.py
preferences = None  # TODO: sin implementacion en commands.py
ifc_project = None  # TODO: sin implementacion en commands.py
panel_cut = None  # TODO: sin implementacion en commands.py
reextrude = None  # TODO: sin implementacion en commands.py
remove_shape_from_bim = None  # TODO: sin implementacion en commands.py
rename_wire = None  # TODO: sin implementacion en commands.py
select_non_manifold_meshes = None  # TODO: sin implementacion en commands.py
structural_system = None  # TODO: sin implementacion en commands.py
split_mesh = None  # TODO: sin implementacion en commands.py
toggle_3d_view_background = None  # TODO: sin implementacion en commands.py
toggle_bim_views = None  # TODO: sin implementacion en commands.py
toggle_ifc_brep_flag = None  # TODO: sin implementacion en commands.py
toggle_subcomponents = None  # TODO: sin implementacion en commands.py
try:
    from .commands import ArchSurvey
except ImportError:
    ArchSurvey = None
try:
    from .commands import BIMTrash
except ImportError:
    BIMTrash = None
try:
    from .commands import BIMWPView
except ImportError:
    BIMWPView = None
try:
    from .commands import DraftSelectGroup
except ImportError:
    DraftSelectGroup = None
try:
    from .commands import DraftSlope
except ImportError:
    DraftSlope = None
try:
    from .commands import DraftWorkingPlaneProxy
except ImportError:
    DraftWorkingPlaneProxy = None

TraduceToEs = {
    # Unclone
    'desclonar': unclone,
    'desclonar objeto': unclone,
    'independizar clon': unclone,
    'separar del original': unclone,
    'romper vínculo de clon': unclone,
    'romper vinculo de clon': unclone,
    # Add to construction group
    'agregar al grupo de construcción': add_to_construction_group,
    'agregar a construcción': add_to_construction_group,
    'mover al grupo de construcción': add_to_construction_group,
    # Check
    'comprobar modelo': check,
    'comprobar sólidos': check,
    'verificar geometría': check,
    'revisar objeto': check,
    # Close Holes
    'cerrar agujeros': close_holes,
    'reparar agujeros': close_holes,
    'cerrar holes': close_holes,
    'cerrar huecos': close_holes,
    # Convertir a proyecto IFC
    'convertir a proyecto IFC': convert_to_ifc_project,
    'convertir en IFC': convert_to_ifc_project,
    'pasar a proyecto IFC': convert_to_ifc_project,
    'transformar a proyecto ifc': convert_to_ifc_project,
    # Diferencia archivos IFC
    'mostrar diferencia de IFC': ifc_diff,
    'Ver cambios IFC': ifc_diff,
    'Comparar archivos IFC': ifc_diff,
    'Diff de IFC': ifc_diff,
    # Estructura
    'nueva estructura': structure,
    'crear estructura': structure,
    'generar estructura': structure,
    'crear elemento estructural': structure,
    # Estructuras múltiples
    'crear varias estructuras': multiple_structures,
    'generar estructuras multiples': multiple_structures,
    'crear estructuras múltiples': multiple_structures,
    'estructuras desde bordes': multiple_structures,
    # Hoja de panel
    'crear hoja de panel': panel_sheet,
    'nueva hoja de panel': panel_sheet,
    'generar hoja de panel': panel_sheet,
    'crear lamina de panel': panel_sheet,
    # IFC Expand
    'desplegar IFC': ifc_expand,
    'expandir IFC': ifc_expand,
    'expandir elementos IFC': ifc_expand,
    'mostrar hijos IFC': ifc_expand,
    # IFC Explorer
    'explorador IFC': ifc_explorer,
    'abrir explorador IFC': ifc_explorer,
    'ver contenido IFC': ifc_explorer,
    'inspeccionar archivo IFC': ifc_explorer,
    # IFC OpenShell Update
    'actualizar IFC OpenShell': ifc_openshell_update,
    'chequear versión IFC OpenShell': ifc_openshell_update,
    'actualizar librería IFC': ifc_openshell_update,
    'actualizar IFCOpenShell': ifc_openshell_update,
    # IFC Shape Diff
    'comparar formas IFC': ifc_shape_diff,
    'comparar IFC': ifc_shape_diff,
    'comparar geometría IFC': ifc_shape_diff,
    'diferencias entre archivos IFC': ifc_shape_diff,
    # Image Plane
    'crear plano de imagen': image_plane,
    'insertar plano de imagen': image_plane,
    'insertar imagen': image_plane,
    'agregar imagen de referencia': image_plane,
    # Lock IFC
    'bloquear IFC': lock_ifc,
    'alternar modo IFC estricto': lock_ifc,
    'activar modo IFC': lock_ifc,
    'bloquear modo IFC': lock_ifc,
    # Merge Walls
    'unir muros': merge_walls,
    'fusionar muros': merge_walls,
    'combinar muros': merge_walls,
    'unir paredes': merge_walls,
    # Mesh to Shape
    'convertir malla en forma': mesh_to_shape,
    'convertir mesh a shape': mesh_to_shape,
    'transformar malla en forma': mesh_to_shape,
    'convertir malla': mesh_to_shape,
    # New IFC Spreadsheet
    'nueva hoja de cálculo IFC': new_ifc_spreadsheet,
    'generar hoja IFC': new_ifc_spreadsheet,
    # Nido
    'crear nido': nest,
    'nestear piezas': nest,
    'organizar piezas': nest,
    'anidar piezas': nest,
    # Nudge Down
    'desplazar abajo': nudge_down,
    'empujar hacia abajo': nudge_down,
    'mover abajo': nudge_down,
    'mover hacia abajo': nudge_down,
    # Nudge Extend
    'extender altura': nudge_extend,
    'extender objeto': nudge_extend,
    'aumentar altura': nudge_extend,
    'incrementar altura': nudge_extend,
    # Nudge Left
    'desplazar izquierda': nudge_left,
    'empujar hacia la izquierda': nudge_left,
    'mover izquierda': nudge_left,
    'mover a la izquierda': nudge_left,
    # Nudge Right
    'desplazar derecha': nudge_right,
    'empujar hacia la derecha': nudge_right,
    'mover derecha': nudge_right,
    'mover a la derecha': nudge_right,
    # Nudge Rotate Left
    'rotar a la izquierda': nudge_rotate_left,
    'girar a la izquierda': nudge_rotate_left,
    'girar antihorario': nudge_rotate_left,
    'rotar antihorario': nudge_rotate_left,
    # Nudge Rotate Right
    'rotar a la derecha': nudge_rotate_right,
    'girar a la derecha': nudge_rotate_right,
    'girar horario': nudge_rotate_right,
    'rotar horario': nudge_rotate_right,
    # Nudge Shrink
    'reducir altura': nudge_shrink,
    'disminuir altura': nudge_shrink,
    'achicar altura': nudge_shrink,
    'contraer objeto': nudge_shrink,
    # Nudge Switch
    'cambiar modo empuje': nudge_switch,
    'alternar modo empuje': nudge_switch,
    'cambiar distancia de empuje': nudge_switch,
    'alternar nudge': nudge_switch,
    # Nudge Up
    'desplazar arriba': nudge_up,
    'empujar hacia arriba': nudge_up,
    'mover arriba': nudge_up,
    'mover hacia arriba': nudge_up,
    # Panel
    'nuevo panel': panel,
    'crear panel': panel,
    'generar panel': panel,
    'añadir panel': panel,
    # Pegamento
    'pegamento': glue,
    'pegar formas': glue,
    'unir formas': glue,
    'agrupar formas': glue,
    # Preferences
    'abrir preferencias BIM': preferences,
    'abrir opciones BIM': preferences,
    'configuración BIM': preferences,
    'preferencias BIM': preferences,
    # Proyecto IFC
    'nuevo proyecto IFC': ifc_project,
    'crear proyecto IFC': ifc_project,
    'generar proyecto IFC': ifc_project,
    'crear proyecto BIM': ifc_project,
    # Recorte de panel
    'crear recorte de panel': panel_cut,
    'recortar panel': panel_cut,
    'visto de corte de panel': panel_cut,
    'generar recorte de panel': panel_cut,
    # Reextruir
    'reextruir': reextrude,
    're-extruir': reextrude,
    'recrear extrusión': reextrude,
    'volver a extruir': reextrude,
    # Remove Shape from BIM
    'eliminar forma de BIM': remove_shape_from_bim,
    'hacer paramétrico': remove_shape_from_bim,
    'quitar shape de BIM': remove_shape_from_bim,
    # Renombrar alambrado
    'renombrar alambrado': rename_wire,
    'recrear alambrado': rename_wire,
    'reconstruir entorno': rename_wire,
    # Select Non-Manifold Meshes
    'seleccionar mallas no manifold': select_non_manifold_meshes,
    'seleccionar meshes no manifold': select_non_manifold_meshes,
    'buscar mallas no manifold': select_non_manifold_meshes,
    'detectar mallas problemáticas': select_non_manifold_meshes,
    # Sistema estructural
    'sistema de estructura': structural_system,
    'crear sistema estructural': structural_system,
    'distribuir estructura': structural_system,
    'generar sistema estructural': structural_system,
    # Split Mesh
    'separar malla': split_mesh,
    'dividir malla': split_mesh,
    'dividir el mesh': split_mesh,
    'separar componentes de la malla': split_mesh,
    # Toggle 3D View Background
    'alternar fondo 3D': toggle_3d_view_background,
    'cambiar fondo a blanco': toggle_3d_view_background,
    'cambiar fondo de vista 3D': toggle_3d_view_background,
    'cambiar estilo de fondo': toggle_3d_view_background,
    # Toggle BIM Views
    'alternar vistas BIM': toggle_bim_views,
    'mostrar vistas BIM': toggle_bim_views,
    'ocultar panel BIM': toggle_bim_views,
    'panel de vistas BIM': toggle_bim_views,
    # Toggle IFC B-Rep Flag
    'alternar indicador B-Rep de IFC': toggle_ifc_brep_flag,
    'alternar bandera IFC B-Rep': toggle_ifc_brep_flag,
    'activar B-Rep IFC': toggle_ifc_brep_flag,
    'desactivar B-Rep IFC': toggle_ifc_brep_flag,
    # Toggle Subcomponents
    'alternar subcomponentes': toggle_subcomponents,
    'mostrar subcomponentes': toggle_subcomponents,
    'ocultar subcomponentes': toggle_subcomponents,
    'mostrar componentes internos': toggle_subcomponents,
    # ArchSurvey
    'inspeccionar modelo': ArchSurvey,
    'tomar medidas': ArchSurvey,
    'medir modelo': ArchSurvey,
    'iniciar modo de inspección': ArchSurvey,
    'extraer medidas': ArchSurvey,
    # BIMTrash
    'mover a la papelera': BIMTrash,
    'enviar a la papelera': BIMTrash,
    'ocultar en papelera': BIMTrash,
    'descartar objetos': BIMTrash,
    # BIMWPView
    'alinear vista a plano de trabajo': BIMWPView,
    'vista de plano de trabajo': BIMWPView,
    'mirar al plano activo': BIMWPView,
    'centrar cámara en cuadrícula': BIMWPView,
    # DraftSelectGroup
    'seleccionar contenido de grupo': DraftSelectGroup,
    'seleccionar elementos del grupo': DraftSelectGroup,
    'seleccionar hijos': DraftSelectGroup,
    'seleccionar interior del grupo': DraftSelectGroup,
    # DraftSlope
    'establecer pendiente': DraftSlope,
    'aplicar pendiente': DraftSlope,
    'inclinar línea': DraftSlope,
    'configurar inclinación': DraftSlope,
    # DraftWorkingPlaneProxy
    'crear proxy de plano de trabajo': DraftWorkingPlaneProxy,
    'guardar plano de trabajo': DraftWorkingPlaneProxy,
    'guardar vista de trabajo': DraftWorkingPlaneProxy,
    'crear estado de plano': DraftWorkingPlaneProxy,
}

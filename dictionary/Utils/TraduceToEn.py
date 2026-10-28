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
"""Mapa de voz (EN) para la seccion Utils (consolidado)."""

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

TraduceToEn = {
    # Unclone
    'unclone': unclone,
    'unclone object': unclone,
    'make clone independent': unclone,
    'detach clone': unclone,
    'break clone link': unclone,
    # Add to construction group
    'add to construction group': add_to_construction_group,
    'add to construction': add_to_construction_group,
    'move to construction group': add_to_construction_group,
    # Check
    'check model': check,
    'check solids': check,
    'check geometry': check,
    'check object': check,
    # Close Holes
    'close holes': close_holes,
    'repair holes': close_holes,
    'fill holes': close_holes,
    'close gaps': close_holes,
    # Convertir a proyecto IFC
    'convert to IFC project': convert_to_ifc_project,
    'convert to IFC': convert_to_ifc_project,
    'move to IFC project': convert_to_ifc_project,
    'transform to IFC project': convert_to_ifc_project,
    # Diferencia archivos IFC
    'show IFC difference': ifc_diff,
    'view IFC changes': ifc_diff,
    'compare IFC files': ifc_diff,
    'IFC diff': ifc_diff,
    # Estructura
    'new structure': structure,
    'create structure': structure,
    'generate structure': structure,
    'create structural element': structure,
    # Estructuras múltiples
    'create multiple structures': multiple_structures,
    'generate multiple structures': multiple_structures,
    'create multiple elements': multiple_structures,
    'structures from edges': multiple_structures,
    # Hoja de panel
    'create panel sheet': panel_sheet,
    'new panel sheet': panel_sheet,
    'generate panel sheet': panel_sheet,
    'create panel drawing sheet': panel_sheet,
    # IFC Expand
    'unfold IFC': ifc_expand,
    'expand IFC': ifc_expand,
    'expand IFC elements': ifc_expand,
    'show IFC children': ifc_expand,
    # IFC Explorer
    'IFC explorer': ifc_explorer,
    'open IFC explorer': ifc_explorer,
    'view IFC contents': ifc_explorer,
    'inspect IFC file': ifc_explorer,
    # IFC OpenShell Update
    'update IFC OpenShell': ifc_openshell_update,
    'check IFC OpenShell version': ifc_openshell_update,
    'update IFC library': ifc_openshell_update,
    'update IFCOpenShell': ifc_openshell_update,
    # IFC Shape Diff
    'compare IFC shapes': ifc_shape_diff,
    'compare IFC': ifc_shape_diff,
    'compare IFC geometry': ifc_shape_diff,
    'IFC file differences': ifc_shape_diff,
    # Image Plane
    'create image plane': image_plane,
    'insert image plane': image_plane,
    'insert image': image_plane,
    'add reference image': image_plane,
    # Lock IFC
    'lock IFC': lock_ifc,
    'toggle strict IFC mode': lock_ifc,
    'enable IFC mode': lock_ifc,
    'lock IFC mode': lock_ifc,
    # Merge Walls
    'merge walls': merge_walls,
    'fuse walls': merge_walls,
    'combine walls': merge_walls,
    'join walls': merge_walls,
    # Mesh to Shape
    'convert mesh to shape': mesh_to_shape,
    'convert mesh into shape': mesh_to_shape,
    'transform mesh to shape': mesh_to_shape,
    'convert mesh': mesh_to_shape,
    # New IFC Spreadsheet
    'new IFC spreadsheet': new_ifc_spreadsheet,
    'generate IFC spreadsheet': new_ifc_spreadsheet,
    # Nido
    'create nest': nest,
    'nest parts': nest,
    'organize parts': nest,
    'nest components': nest,
    # Nudge Down
    'nudge down': nudge_down,
    'push down': nudge_down,
    'move down': nudge_down,
    'shift down': nudge_down,
    # Nudge Extend
    'extend height': nudge_extend,
    'extend object': nudge_extend,
    'increase height': nudge_extend,
    'increment height': nudge_extend,
    # Nudge Left
    'nudge left': nudge_left,
    'push left': nudge_left,
    'move left': nudge_left,
    'shift left': nudge_left,
    # Nudge Right
    'nudge right': nudge_right,
    'push right': nudge_right,
    'move right': nudge_right,
    'shift right': nudge_right,
    # Nudge Rotate Left
    'rotate left': nudge_rotate_left,
    'turn left': nudge_rotate_left,
    'rotate counterclockwise': nudge_rotate_left,
    'turn counterclockwise': nudge_rotate_left,
    # Nudge Rotate Right
    'rotate right': nudge_rotate_right,
    'turn right': nudge_rotate_right,
    'turn clockwise': nudge_rotate_right,
    'rotate clockwise': nudge_rotate_right,
    # Nudge Shrink
    'shrink height': nudge_shrink,
    'decrease height': nudge_shrink,
    'reduce height': nudge_shrink,
    'shrink object': nudge_shrink,
    # Nudge Switch
    'switch nudge mode': nudge_switch,
    'toggle nudge mode': nudge_switch,
    'change nudge distance': nudge_switch,
    'toggle nudge': nudge_switch,
    # Nudge Up
    'nudge up': nudge_up,
    'push up': nudge_up,
    'move up': nudge_up,
    'shift up': nudge_up,
    # Panel
    'new panel': panel,
    'create panel': panel,
    'generate panel': panel,
    'add panel': panel,
    # Pegamento
    'glue shapes': glue,
    'fuse shapes': glue,
    'join shapes': glue,
    'group shapes': glue,
    # Preferences
    'open BIM preferences': preferences,
    'open BIM options': preferences,
    'BIM configuration': preferences,
    'BIM preferences': preferences,
    # Proyecto IFC
    'new IFC project': ifc_project,
    'create IFC project': ifc_project,
    'generate IFC project': ifc_project,
    'create BIM project': ifc_project,
    # Recorte de panel
    'create panel cut': panel_cut,
    'cut panel': panel_cut,
    'panel cut view': panel_cut,
    'generate panel cut': panel_cut,
    # Reextruir
    'reextrude': reextrude,
    're-extrude': reextrude,
    'recreate extrusion': reextrude,
    'extrude again': reextrude,
    # Remove Shape from BIM
    'remove shape from BIM': remove_shape_from_bim,
    'make parametric': remove_shape_from_bim,
    'remove BIM shape': remove_shape_from_bim,
    # Renombrar alambrado
    'rename wire': rename_wire,
    'recreate wire': rename_wire,
    'rebuild wire': rename_wire,
    # Select Non-Manifold Meshes
    'select non-manifold meshes': select_non_manifold_meshes,
    'select non-manifold mesh': select_non_manifold_meshes,
    'find non-manifold meshes': select_non_manifold_meshes,
    'detect problematic meshes': select_non_manifold_meshes,
    # Sistema estructural
    'structural system': structural_system,
    'create structural system': structural_system,
    'distribute structure': structural_system,
    'generate structural system': structural_system,
    # Split Mesh
    'split mesh': split_mesh,
    'divide mesh': split_mesh,
    'split the mesh': split_mesh,
    'separate mesh components': split_mesh,
    # Toggle 3D View Background
    'toggle 3D background': toggle_3d_view_background,
    'change background to white': toggle_3d_view_background,
    'change 3D view background': toggle_3d_view_background,
    'change background style': toggle_3d_view_background,
    # Toggle BIM Views
    'toggle BIM views': toggle_bim_views,
    'show BIM views': toggle_bim_views,
    'hide BIM panel': toggle_bim_views,
    'BIM views panel': toggle_bim_views,
    # Toggle IFC B-Rep Flag
    'toggle IFC B-Rep flag': toggle_ifc_brep_flag,
    'toggle IFC B-Rep indicator': toggle_ifc_brep_flag,
    'enable IFC B-Rep': toggle_ifc_brep_flag,
    'disable IFC B-Rep': toggle_ifc_brep_flag,
    # Toggle Subcomponents
    'toggle subcomponents': toggle_subcomponents,
    'show subcomponents': toggle_subcomponents,
    'hide subcomponents': toggle_subcomponents,
    'show internal components': toggle_subcomponents,
    # ArchSurvey
    'inspect model': ArchSurvey,
    'take measurements': ArchSurvey,
    'measure model': ArchSurvey,
    'start inspection mode': ArchSurvey,
    'extract measurements': ArchSurvey,
    # BIMTrash
    'move to trash': BIMTrash,
    'send to trash': BIMTrash,
    'hide in trash': BIMTrash,
    'discard objects': BIMTrash,
    # BIMWPView
    'align view to working plane': BIMWPView,
    'working plane view': BIMWPView,
    'look at active plane': BIMWPView,
    'center camera on grid': BIMWPView,
    # DraftSelectGroup
    'select group contents': DraftSelectGroup,
    'select group elements': DraftSelectGroup,
    'select children': DraftSelectGroup,
    'select group interior': DraftSelectGroup,
    # DraftSlope
    'set slope': DraftSlope,
    'apply slope': DraftSlope,
    'incline line': DraftSlope,
    'configure inclination': DraftSlope,
    # DraftWorkingPlaneProxy
    'create working plane proxy': DraftWorkingPlaneProxy,
    'save working plane': DraftWorkingPlaneProxy,
    'save working view': DraftWorkingPlaneProxy,
    'create plane state': DraftWorkingPlaneProxy,
}

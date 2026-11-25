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
"""Mapa de voz (ES) para la seccion Snapping (consolidado)."""

try:
    from .commands import WorkingPlaneFront
except ImportError:
    WorkingPlaneFront = None
try:
    from .commands import working_plane
except ImportError:
    working_plane = None
try:
    from .commands import working_plane_side
except ImportError:
    working_plane_side = None
try:
    from .commands import working_plane_top
except ImportError:
    working_plane_top = None

TraduceToEs = {
    # WorkingPlaneFront
    'plano frontal': WorkingPlaneFront,
    'plano de trabajo frontal': WorkingPlaneFront,
    'vista frontal': WorkingPlaneFront,
    'establecer plano frontal': WorkingPlaneFront,
    'fijar plano frontal': WorkingPlaneFront,
    'poner plano frontal': WorkingPlaneFront,
    # WorkingPlane
    'plano de trabajo': working_plane,
    'definir plano de trabajo': working_plane,
    'seleccionar plano': working_plane,
    'configurar plano de trabajo': working_plane,
    'fijar plano de trabajo': working_plane,
    # WorkingPlaneSide
    'plano de trabajo lateral': working_plane_side,
    'vista de plano lateral': working_plane_side,
    'plano lateral': working_plane_side,
    'plano de trabajo al costado': working_plane_side,
    'fijar plano lateral': working_plane_side,
    # WorkingPlaneTop
    'plano de trabajo superior': working_plane_top,
    'vista de plano superior': working_plane_top,
    'fijar plano arriba': working_plane_top,
    'fijar plano de arriba': working_plane_top,
    'plano de arriba': working_plane_top,
    'plano superior': working_plane_top,
}
try:
    from .commands import toggle_snap, snap_grid, snap_endpoint, snap_midpoint, snap_center, snap_ortho, snap_lock
except ImportError:
    toggle_snap = None
    snap_grid = None
    snap_endpoint = None
    snap_midpoint = None
    snap_center = None
    snap_ortho = None
    snap_lock = None

TraduceToEs.update({
    'alternar enganche': toggle_snap,
    'activar enganche': toggle_snap,
    'desactivar enganche': toggle_snap,
    'enganche a rejilla': snap_grid,
    'enganche a grilla': snap_grid,
    'enganche a extremo': snap_endpoint,
    'punto final': snap_endpoint,
    'enganche a punto medio': snap_midpoint,
    'punto medio': snap_midpoint,
    'enganche a centro': snap_center,
    'centro': snap_center,
    'modo ortogonal': snap_ortho,
    'ortogonal': snap_ortho,
    'bloquear enganche': snap_lock,
})

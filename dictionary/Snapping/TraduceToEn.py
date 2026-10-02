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
"""Mapa de voz (EN) para la seccion Snapping (consolidado)."""

WorkingPlaneFront = None  # TODO: sin implementacion en commands.py
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

TraduceToEn = {
    # WorkingPlaneFront
    'front plane': WorkingPlaneFront,
    'working plane front': WorkingPlaneFront,
    'front working plane': WorkingPlaneFront,
    'set front plane': WorkingPlaneFront,
    'set working plane front': WorkingPlaneFront,
    'front view plane': WorkingPlaneFront,
    # WorkingPlane
    'working plane': working_plane,
    'define working plane': working_plane,
    'select plane': working_plane,
    'configure working plane': working_plane,
    'set working plane': working_plane,
    # WorkingPlaneSide
    'working plane side': working_plane_side,
    'side working plane': working_plane_side,
    'side plane': working_plane_side,
    'set side plane': working_plane_side,
    'set working plane side': working_plane_side,
    # WorkingPlaneTop
    'working plane top': working_plane_top,
    'top working plane': working_plane_top,
    'top plane': working_plane_top,
    'set top plane': working_plane_top,
    'set working plane top': working_plane_top,
}

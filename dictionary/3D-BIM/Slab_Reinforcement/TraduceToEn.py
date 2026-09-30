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

try:
    from .Slab_Reinforcement import Slab_Reinforcement
except ImportError:
    Slab_Reinforcement = None   

TraduceToEn = {
    # Slab Reinforcement
    'slab reinforcement':             Slab_Reinforcement,
    'add slab reinforcement':         Slab_Reinforcement,
    'create slab reinforcement':      Slab_Reinforcement,
    'reinforce slab':                 Slab_Reinforcement,
    'reinforce the slab':             Slab_Reinforcement,
    'add reinforcement to slab':      Slab_Reinforcement,
    'add reinforcement to the slab':  Slab_Reinforcement,
    'add slab rebar':                 Slab_Reinforcement,
    'create slab rebar':              Slab_Reinforcement,
}
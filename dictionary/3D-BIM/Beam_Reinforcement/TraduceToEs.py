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
    from .Beam_Reinforcement import Beam_Reinforcement
except ImportError:
    Beam_Reinforcement = None

TraduceToEs = {
    # Refuerzo de viga
    'reforzar viga':              Beam_Reinforcement,
    'agregar refuerzo de viga':   Beam_Reinforcement,
    'añadir refuerzo de viga':    Beam_Reinforcement,
    'crear refuerzo de viga':     Beam_Reinforcement,
    'refuerzo de vigas':          Beam_Reinforcement,
    'armar viga':                 Beam_Reinforcement,
    'agregar armadura de viga':   Beam_Reinforcement,
    'añadir armadura de viga':    Beam_Reinforcement,
}
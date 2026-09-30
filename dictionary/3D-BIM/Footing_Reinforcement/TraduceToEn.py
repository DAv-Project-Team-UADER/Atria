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
    from .Footing_Reinforcement import Footing_Reinforcement
except ImportError:
    Footing_Reinforcement = None    

TraduceToEn = {
    # Footing Reinforcement
    'footing reinforcement':             Footing_Reinforcement,
    'add footing reinforcement':         Footing_Reinforcement,
    'create footing reinforcement':      Footing_Reinforcement,
    'reinforce footing':                 Footing_Reinforcement,
    'reinforce the footing':             Footing_Reinforcement,
    'add reinforcement to footing':      Footing_Reinforcement,
    'add reinforcement to the footing':  Footing_Reinforcement,
    'add footing rebar':                 Footing_Reinforcement,
    'create footing rebar':              Footing_Reinforcement,
}
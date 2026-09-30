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
    from .Column_Reinforcement import Column_Reinforcement
except ImportError:
    Column_Reinforcement = None

TraduceToEn = {
    # Column Reinforcement
    'column reinforcement':          Column_Reinforcement,
    'add column reinforcement':      Column_Reinforcement,
    'create column reinforcement':   Column_Reinforcement,
    'reinforce column':              Column_Reinforcement,
    'reinforce the column':          Column_Reinforcement,
    'add reinforcement to column':   Column_Reinforcement,
    'add reinforcement to the column': Column_Reinforcement,
    'add column rebar':              Column_Reinforcement,
    'create column rebar':           Column_Reinforcement,
}
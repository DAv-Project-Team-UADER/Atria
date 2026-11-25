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

import FreeCADGui as Gui
from ayuda import ayuda


def BIMClassification():
    """
    Permite asignar clasificaciones estandarizadas (como Uniclass, OmniClass, 
    MasterFormat, etc.) a los objetos y materiales del modelo BIM. Esto 
    añade metadatos estructurados a los elementos, lo cual es fundamental para el 
    intercambio de información y la correcta exportación a formatos como IFC.
    """
    Gui.runCommand('BIM_Classification', 0)


comandos = {
    'clasificar elemento bim': BIMClassification,
    'asignar clasificación': BIMClassification,
    'clasificar objeto': BIMClassification,
    'gestionar clasificación bim': BIMClassification,
    'help': ayuda
}

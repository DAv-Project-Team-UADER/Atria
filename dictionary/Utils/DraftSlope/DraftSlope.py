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


def DraftSlope():
    """
    Permite inclinar o dar pendiente a líneas (Draft Lines) o polilíneas (Draft Wires) 
    seleccionadas. La herramienta modifica la coordenada Z de todos los puntos 
    (a partir del primero) para alcanzar la inclinación especificada mediante un valor 
    de pendiente (porcentaje o ratio) o un ángulo.
    """
    Gui.runCommand('Draft_Slope', 0)


comandos = {
    'establecer pendiente': DraftSlope,
    'aplicar pendiente': DraftSlope,
    'inclinar línea': DraftSlope,
    'configurar inclinación': DraftSlope,
    'help': ayuda
}

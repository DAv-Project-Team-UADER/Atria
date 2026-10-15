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


def Union():
    """
    Fusiona (une) dos o más formas u objetos de FreeCAD seleccionados para convertirlos 
    en uno solo. Esta operación es completamente paramétrica, por lo que los 
    componentes pueden modificarse y el resultado se recalculará automáticamente.
    """
    Gui.runCommand('Part_Fuse', 0)


comandos = {
    'unir objetos': Union,
    'fusionar piezas': Union,
    'unión booleana': Union,
    'combinar sólidos': Union,
    'help': ayuda
}

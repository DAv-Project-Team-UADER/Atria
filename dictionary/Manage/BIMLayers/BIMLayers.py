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


def BIMLayers():
    """
    Permite crear y gestionar las capas dentro de un proyecto BIM. Las capas 
    actúan como un grupo especial que controla y propaga automáticamente propiedades 
    visuales (como grosor de línea, color de línea, color de la forma y transparencia) 
    a los objetos que se encuentran en su interior. Además, son totalmente 
    compatibles con la importación y exportación de formatos como IFC y DXF/DWG, y 
    cuentan con soporte para NativeIFC.
    """
    Gui.runCommand('BIM_Layers', 0)


comandos = {
    'gestionar capas': BIMLayers,
    'administrar capas': BIMLayers,
    'crear capa bim': BIMLayers,
    'abrir administrador de capas': BIMLayers,
    'help': ayuda
}

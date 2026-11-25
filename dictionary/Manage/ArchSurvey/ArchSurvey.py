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


def ArchSurvey():
    """
    Habilita un modo interactivo de inspección que permite extraer medidas, 
    cantidades, coordenadas y áreas de un modelo 3D o dibujo 2D de forma rápida. 
    Al seleccionar diferentes elementos geométricos (vértices, aristas o caras), 
    la herramienta calcula la información y permite recopilar estos datos en una 
    lista para su posterior uso o exportación.
    """
    Gui.runCommand('Arch_Survey', 0)


comandos = {
    'inspeccionar modelo': ArchSurvey,
    'tomar medidas': ArchSurvey,
    'medir modelo': ArchSurvey,
    'iniciar modo de inspección': ArchSurvey,
    'extraer medidas': ArchSurvey,
    'help': ayuda
}

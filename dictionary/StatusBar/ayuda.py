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

from ._help_gui import show_help_dialog

def ayuda():
    content = """Comandos directos de la barra de estado:
  bloquear ifc                - Activa o desactiva el modo IFC estricto (Lock IFC)
  alternar vistas bim         - Muestra u oculta el panel lateral de vistas BIM
  cambiar fondo de vista 3d   - Alterna el fondo de la vista 3D entre gradiente
                                vertical, gradiente radial y color plano

Sinónimos reconocidos:
  bloquear ifc:
    - alternar modo ifc estricto
    - activar modo ifc
    - bloquear modo ifc
  alternar vistas bim:
    - mostrar vistas bim
    - ocultar panel bim
    - panel de vistas bim
  cambiar fondo de vista 3d:
    - alternar fondo 3d
    - cambiar fondo a blanco
    - cambiar estilo de fondo"""
    show_help_dialog("Barra de estado", content)

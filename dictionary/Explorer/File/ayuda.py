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
from .._help_gui import show_help_dialog

def ayuda():
    content = """Comandos disponibles en Archivo:
  nuevo       - Crea un nuevo documento
  abrir       - Abre un archivo existente
  guardar     - Guarda el documento activo
  guardar como - Guarda con un nuevo nombre
  guardar copia - Guarda una copia del documento
  revertir    - Revierte al último guardado
  combinar    - Combina proyectos
  importar    - Importa un archivo externo
  exportar    - Exporta el documento
  recientes   - Abre la lista de archivos recientes
  cargar imagen - Carga una imagen en la vista 3D"""
    show_help_dialog("Archivo", content)


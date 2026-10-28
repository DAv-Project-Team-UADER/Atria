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

def ayuda():
    print('Comandos disponibles en Manage:')
    print('  planificación       - Crea una tabla de planificación o lista de materiales del modelo')
    print('  clasificación       - Asigna clasificaciones BIM estandarizadas a los objetos')
    print('  propiedades ifc     - Gestiona los conjuntos de propiedades IFC (Psets) de los objetos')
    print('  capas               - Administra las capas del proyecto con sus propiedades visuales')
    print('  material            - Crea y asigna materiales a los objetos BIM del documento')
    print('  preflight           - Ejecuta comprobaciones de calidad del modelo antes de exportar a IFC')
    print('  informe             - Genera informes con consultas BIM SQL sobre el modelo')
    print('  estilos de anotación- Administra los estilos de anotación (textos, cotas y etiquetas)')

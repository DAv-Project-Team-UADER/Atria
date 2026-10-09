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

"""Ayuda de Utils — Menú BIM → Utils.

Explica en lenguaje sencillo qué permite hacer cada herramienta de la carpeta
Utils y con qué frase de voz se la invoca.
"""

def ayuda():
    content = """Medir y revisar:
  tomar medidas              - Mide aristas, caras y puntos con clics y suma los totales
  comprobar modelo           - Revisa los objetos seleccionados en busca de problemas
  buscar mallas no manifold  - Selecciona las mallas que no están bien cerradas

Seleccionar y organizar:
  seleccionar hijos          - Selecciona todo lo que hay dentro del grupo elegido
  agregar a construcción     - Pasa los objetos al grupo de geometría de construcción
  mover a la papelera        - Oculta los objetos en una papelera sin borrarlos

Vista y plano de trabajo:
  mirar al plano activo      - Pone la vista de frente al plano de trabajo
  guardar plano de trabajo   - Guarda el plano y la vista actuales para volver a ellos
  alternar fondo 3D          - Cambia el fondo de la vista 3D entre liso y degradado
  alternar vistas BIM        - Muestra u oculta el panel de vistas BIM
  alternar subcomponentes    - Muestra u oculta las partes internas de un objeto BIM

Mover de a pasos (empuje):
  mover arriba / abajo       - Desplaza la selección un paso hacia arriba o abajo
  mover izquierda / derecha  - Desplaza la selección un paso hacia los costados
  girar a la izquierda       - Gira la selección 45 grados en sentido antihorario
  girar a la derecha         - Gira la selección 45 grados en sentido horario
  extender altura            - Hace más alto el objeto seleccionado en un paso
  reducir altura             - Hace más bajo el objeto seleccionado en un paso
  cambiar modo empuje        - Alterna el tamaño del paso entre automático y fijo

Editar objetos:
  desclonar                  - Convierte un clon en un objeto independiente
  aplicar pendiente          - Inclina líneas y polilíneas con la pendiente indicada
  unir muros                 - Une los muros seleccionados en uno solo
  reextruir                  - Rehace una estructura extruida desde una cara elegida
  pegar formas               - Junta varias formas en una sola forma fija
  recrear alambrado          - Vuelve a armar las líneas de los objetos elegidos
  eliminar forma de BIM      - Quita la forma cúbica fija de un objeto BIM

Estructuras y paneles:
  crear estructura           - Crea una viga o columna
  crear varias estructuras   - Crea una estructura por cada línea seleccionada
  crear sistema estructural  - Reparte estructuras a lo largo de ejes
  crear panel                - Crea un panel (placa) de espesor fijo
  crear recorte de panel     - Dibuja en 2D el recorte de un panel para fabricarlo
  crear hoja de panel        - Crea una hoja para ubicar los recortes de paneles
  organizar piezas           - Acomoda las piezas en la hoja para aprovechar material

Mallas:
  convertir malla en forma   - Transforma una malla en un objeto sólido editable
  separar malla              - Divide una malla en partes independientes
  cerrar agujeros            - Tapa los agujeros de una forma abierta y la vuelve sólida

Imágenes y planillas:
  insertar imagen            - Crea un plano con una imagen para usar de referencia
  nueva hoja de cálculo IFC  - Crea una planilla con las propiedades IFC del objeto

Archivos IFC:
  nuevo proyecto IFC         - Crea un proyecto IFC nuevo
  convertir a proyecto IFC   - Convierte la selección en un proyecto IFC
  explorador IFC             - Abre un archivo IFC para ver su contenido
  expandir IFC               - Despliega los elementos internos de un objeto IFC
  bloquear IFC               - Activa o desactiva el modo de trabajo IFC estricto
  ver cambios IFC            - Muestra los cambios sin guardar del archivo IFC
  comparar formas IFC        - Compara la geometría de los objetos IFC
  activar B-Rep IFC          - Decide si el objeto se exporta como B-Rep o no
  actualizar librería IFC    - Busca e instala la última versión de IfcOpenShell

Configuración:
  abrir preferencias BIM     - Abre las preferencias del entorno BIM"""
    print("=== Ayuda: Utils ===")
    print(content)

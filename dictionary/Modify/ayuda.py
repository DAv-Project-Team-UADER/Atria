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
    content = """Edición y conversión:
  editar elemento           - Pone el objeto en modo de edición gráfica (nodos)
                              También: modo edición, editar nodos, modificar gráfico
  estirar elemento          - Estira el objeto moviendo vértices seleccionados
                              También: aplicar stretch, mover vértices, deformar objeto
  recortar o extender       - Recorta o extiende un objeto hasta otro borde
                              También: ejecutar trimex, recortar elemento, extender elemento
  promover elemento         - Sube de nivel el objeto (fusiona, crea caras)
                              También: elevar nivel, upgrade objeto, convertir a cara
  degradar elemento         - Baja de nivel (sólido a caras, wire a aristas)
                              También: bajar nivel, downgrade objeto, descomponer objeto
  convertir a croquis       - Convierte objetos Draft a croquis (y viceversa)
                              También: draft a croquis, convertir a sketch, pasar a boceto

Líneas y alambres:
  unir elementos            - Une líneas y alambres en un solo alambre
                              También: juntar líneas, unir alambres, generar alambre único
  dividir elemento          - Divide una línea o alambre en un punto
                              También: cortar línea, separar alambre, escindir objeto

Desfases:
  crear desfase             - Desfasa un objeto o crea una copia desfasada
                              También: generar offset, aplicar desfase, duplicar contorno
  crear desfase dos d       - Alambre o cara paralela a una distancia (2D Offset)
                              También: generar offset dos d, aplicar desfase plano, duplicar a distancia

Matrices:
  crear array               - Matriz ortogonal en los ejes X, Y y Z
                              También: generar array, crear matriz ortogonal, duplicar en array
  crear matriz polar        - Copias distribuidas alrededor de un centro
                              También: nueva matriz polar, arreglo polar, generar matriz circular
  crear path array          - Copias distribuidas a lo largo de una trayectoria
                              También: generar path array, crear matriz sobre trayectoria, duplicar en curva
  crear matriz por puntos   - Copias ubicadas en los puntos de otro objeto
                              También: nueva matriz de puntos, arreglo por puntos, distribuir en puntos

Operaciones booleanas:
  unir objetos              - Fusiona dos o más objetos en uno (Part Fuse)
                              También: fusionar piezas, unión booleana, combinar sólidos
  cortar objetos            - Resta la herramienta de la forma base (Part Cut)
                              También: restar objetos, aplicar diferencia, corte booleano
  intersecar objetos        - Conserva solo el volumen común (Part Common)
                              También: crear intersección, extraer parte común, volumen compartido

Extrusión y corte:
  extruir pieza             - Extruye una forma a lo largo de una distancia
                              También: extruir forma, generar extrusión, dar volumen tridimensional
  extruir cara              - Extruye una sola cara plana seleccionada
                              También: dar volumen a la cara, extrusión de cara
  cortar con plano          - Corta un objeto Arch con un plano de referencia
                              También: cortar mediante plano, aplicar plano de corte, corte plano

Componentes BIM:
  añadir componente         - Añade objetos a un muro, estructura, nivel, eje o plano
                              También: agregar componente, unir objeto a componente, asignar elemento bim
  quitar componente         - Quita o sustrae un componente de un objeto BIM
                              También: eliminar componente, sustraer objeto, desvincular elemento bim"""
    show_help_dialog("Modificar", content)

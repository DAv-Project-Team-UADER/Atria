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

"""Repositorio de contenido de ayuda y explicaciones para cada categoría de ATRIA.

Proporciona explicaciones claras y detalladas de cada botón y comando disponible
en cada una de las secciones, para mostrarlas en la ventana emergente de ayuda.
"""

from __future__ import annotations

from typing import Any

from GUIFreeCad.ui.Textos import format_section_title


HELP_BY_CATEGORY: dict[str, list[tuple[str, str]]] = {
    "Base": [
        ("explorador", "Abre el explorador de archivos, proyectos, edición, ventanas y herramientas generales."),
        ("2d-drafting", "Herramientas de dibujo 2D (líneas, rectángulos, círculos, cotas, textos, arcos y curvas)."),
        ("3d-bim", "Modelado arquitectónico y estructural 3D (muros, puertas, ventanas, columnas, vigas, losas, etc.)."),
        ("anotacion", "Acotación de planos, ejes, secciones 2D, capas y láminas de dibujo técnico."),
        ("administracion", "Gestión de proyectos, clasificación IFC, materiales, tablas de cantidades y vistas."),
        ("modificar", "Operaciones de modificación y transformación (mover, rotar, copiar, recortar, booleanas, etc.)."),
        ("preferencias", "Configuración y preferencias del entorno de trabajo, unidades, idioma y herramientas."),
        ("enganche", "Modos de referencia a objetos (Snapping), rejilla y selección del plano de trabajo."),
        ("barra de estado", "Alternar modo IFC, visibilidad de vistas BIM y estilo de fondo de vista 3D."),
        ("utilidades", "Herramientas auxiliares de medición, verificación del modelo y utilidades geométricas."),
        ("vistas", "Control de vistas estándar, rotación, encuadre y cambio de perspectiva o cámara ortogonal."),
        ("seleccionar", "Navega y selecciona objetos 3D del modelo con avanzar, retroceder, marcar y deseleccionar."),
    ],
    "3D-BIM": [
        ("crear sitio", "Crea el emplazamiento o terreno del proyecto y agrupa los edificios."),
        ("crear edificio", "Crea el grupo Edificio que organiza los niveles del modelo."),
        ("crear nivel", "Crea un nivel o planta que agrupa objetos y comparte su altura de piso."),
        ("crear espacio", "Define el volumen de un ambiente y calcula su área de piso."),
        ("crear muro", "Construye un muro arquitectónico desde cero o sobre una línea, cara o boceto base."),
        ("crear muro cortina", "Subdivide una cara base en montantes, travesaños y paneles acristalados."),
        ("crear columna", "Crea un elemento estructural vertical (columna o pilar)."),
        ("crear viga", "Crea un elemento estructural horizontal entre dos puntos."),
        ("crear losa", "Crea una losa horizontal extruida desde una forma plana."),
        ("crear cubierta", "Crea un techo inclinado paramétrico desde un contorno cerrado."),
        ("crear techo", "Crea un techo inclinado con pendiente y voladizo por borde."),
        ("crear escalera", "Crea escaleras rectas, con descansillo o con largueros."),
        ("crear marco", "Extruye un perfil a lo largo de un trazado (barandillas, entramados)."),
        ("crear armadura", "Crea una celosía (truss) paramétrica desde una línea o desde cero."),
        ("crear cerca", "Repite un poste y un tramo de cerca a lo largo de una trayectoria."),
        ("crear panel", "Crea un panel paramétrico desde un contorno 2D, liso o corrugado."),
        ("crear equipamiento", "Inserta muebles, equipos o electrodomésticos no estructurales."),
        ("crear armadura personalizada", "Coloca barras de refuerzo desde un boceto sobre la estructura."),
        ("crear ventana", "Inserta una ventana sobre un muro y genera la abertura correspondiente."),
        ("crear puerta", "Inserta una puerta sobre un muro y genera la abertura correspondiente."),
        ("crear tubo", "Crea una tubería recta o a partir de un contorno base."),
        ("crear conector", "Une dos o tres tubos en esquina o en T con radio de curvatura."),
        ("crear caja", "Crea una caja de Part definiendo sus dimensiones."),
        ("convertir en componente", "Convierte un objeto de Part en un componente Arch."),
        ("insertar referencia externa", "Enlaza un objeto que vive en otro archivo de FreeCAD."),
        ("crear atrapacaras", "Crea una superficie paramétrica a partir de las caras seleccionadas."),
        ("insertar objeto de biblioteca", "Abre la biblioteca de objetos (mobiliario y equipamiento)."),
        ("crear perfil", "Crea un perfil paramétrico 2D para extruir (C, H, R, U, L, T)."),
        ("constructor de formas", "Arma aristas, alambres, caras, cáscaras y sólidos desde primitivas."),
        ("agregar refuerzo de viga", "Arma la viga: estribos y armaduras superior, inferior y de corte."),
        ("agregar refuerzo de columna", "Arma la columna: estribos y armaduras principales y secundarias."),
        ("agregar refuerzo de zapata", "Arma la zapata: malla de barras y columnas sobre ella."),
        ("agregar refuerzo de losa", "Arma la losa: mallado de barras en ambas direcciones."),
        ("crear armadura doblada", "Crea barras de refuerzo dobladas dentro de una estructura."),
        ("crear armadura helicoidal", "Crea una barra de refuerzo helicoidal dentro de una estructura."),
        ("crear armadura en l", "Crea barras de refuerzo con forma de L dentro de una estructura."),
        ("crear armadura recta", "Crea barras de refuerzo rectas dentro de una estructura."),
        ("crear estribo", "Crea estribos (lazos cerrados) dentro de una estructura."),
        ("crear armadura en u", "Crea barras de refuerzo con forma de U dentro de una estructura."),
    ],
    "2D-Drafting": [
        ("punto", "Crea un punto simple en el plano de trabajo."),
        ("línea", "Crea una línea recta a partir de dos puntos."),
        ("rectángulo", "Crea un rectángulo a partir de dos puntos opuestos."),
        ("polígono", "Crea un polígono regular a partir de un centro y un radio."),
        ("polilínea", "Crea una secuencia de líneas rectas continuas que une varios puntos."),
        ("círculo", "Crea un círculo a partir de su centro y radio."),
        ("arco", "Crea un arco a partir de su centro, radio y ángulos inicial y final."),
        ("arco 3 puntos", "Crea un arco pasando exactamente por tres puntos del perímetro."),
        ("elipse", "Crea una elipse a partir de su centro y sus radios mayor y menor."),
        ("fillet", "Crea un redondeo o chaflán entre dos líneas seleccionadas."),
        ("curva bspline", "Crea una curva B-Spline suave a partir de una serie de puntos."),
        ("curva bezier", "Crea una curva Bézier a partir de sus puntos de control."),
        ("texto", "Crea una anotación de texto plano o multilínea en el dibujo."),
        ("cota", "Inserta una cota para medir distancias o ángulos entre puntos."),
        ("rotular", "Añade un rótulo o etiqueta de texto vinculada a un elemento."),
    ],
    "Annotation": [
        ("cota alineada", "Crea una cota alineada entre dos puntos o a lo largo de una arista inclinada."),
        ("cota horizontal", "Crea una cota restringida horizontalmente entre dos puntos."),
        ("cota vertical", "Crea una cota restringida verticalmente entre dos puntos."),
        ("dibujo 2d", "Crea un dibujo 2D proyectando las vistas y secciones del modelo."),
        ("ejes", "Coloca un sistema de ejes de referencia estructural en el documento."),
        ("sistema de ejes", "Combina varios ejes de referencia en un único sistema coordinado."),
        ("rotular", "Añade un rótulo o etiqueta de texto asociada a un elemento constructivo."),
        ("plano de trabajo", "Configura la posición y orientación del plano de trabajo activo."),
        ("vista de seccion", "Crea un plano de corte para seccionar y visualizar el modelo."),
        ("pagina de dibujo", "Crea una nueva lámina o página para generar planos técnicos."),
        ("vista de dibujo", "Inserta una vista proyectada del modelo en la lámina técnica activa."),
        ("capa", "Crea una capa para organizar elementos y controlar color y visibilidad."),
        ("administrador de capas", "Abre el panel para gestionar, ocultar o bloquear capas."),
        ("clonar", "Crea un clon paramétrico enlazado que replica la geometría del objeto."),
    ],
    "Manage": [
        ("configurar proyecto", "Asistente guiado para configurar los parámetros iniciales del proyecto BIM."),
        ("administrador ifc", "Abre el gestor integral de entidades, tipos y atributos IFC."),
        ("exportar ifc", "Exporta el modelo arquitectónico al formato estándar abierto IFC."),
        ("administrador bim", "Abre el panel central de gestión y organización del modelo BIM."),
        ("revisar clasificaciones", "Verifica que todos los objetos tengan asignada su clasificación."),
        ("revisar ifc", "Inspecciona y valida la coherencia de las propiedades y tipos IFC."),
        ("materiales", "Abre el catálogo y gestor de materiales de construcción."),
        ("tabla de cantidades", "Genera una planilla con el cómputo métrico de materiales y áreas."),
        ("actualizar cantidades", "Recalcula automáticamente los cómputos métricos tras modificaciones."),
        ("vistas de dibujo", "Inserta vistas y detalles técnicos en las láminas del proyecto."),
        ("plano de corte", "Define un plano de corte interactivo sobre la vista 3D del modelo."),
        ("cuadricula", "Genera una cuadrícula modular de líneas guía para el diseño."),
        ("gestor de vistas", "Administra cámaras guardadas, perspectivas y orientaciones."),
    ],
    "Modify": [
        ("mover", "Desplaza uno o más objetos seleccionados desde un punto origen a un destino."),
        ("copiar", "Duplica los objetos seleccionados colocándolos en nuevas coordenadas."),
        ("rotar", "Gira los objetos seleccionados alrededor de un centro y un ángulo definido."),
        ("clonar", "Crea una copia vinculada paramétricamente al objeto original."),
        ("desplazar", "Desplaza la geometría de un objeto a lo largo de un vector."),
        ("espejo", "Crea una copia simétrica reflejada respecto a un plano o línea eje."),
        ("escalar", "Modifica el tamaño de los objetos aplicando un factor de escala."),
        ("recortar", "Recorta aristas o líneas que se intersecan con otros elementos."),
        ("estirar", "Estira aristas o vértices seleccionados deformando el objeto suavemente."),
        ("alinear", "Alinea caras, aristas o centros entre dos o más objetos."),
        ("editar objeto", "Entra en el modo de edición de vértices y parámetros de la pieza."),
        ("convertir a croquis", "Convierte elementos de dibujo 2D (Draft) a un croquis (Sketcher)."),
        ("unir elementos", "Fusiona líneas y aristas contiguas en un único alambre (Wire)."),
        ("dividir elemento", "Corta o separa una línea o alambre en el punto indicado."),
        ("crear desfase", "Crea una curva o contorno desfasado a una distancia paralela constante."),
        ("crear desfase dos d", "Genera un contorno 2D paralelo desfasado a una distancia específica."),
        ("crear array", "Genera una matriz ortogonal de copias distribuidas en X, Y y Z."),
        ("crear matriz polar", "Distribuye copias del objeto en forma circular alrededor de un centro."),
        ("crear path array", "Distribuye copias del objeto a lo largo de una trayectoria o curva."),
        ("crear matriz por puntos", "Ubica copias del objeto exactamente en los puntos de otra geometría."),
        ("unir objetos", "Realiza la unión booleana de dos o más sólidos combinándolos en uno."),
        ("cortar objetos", "Realiza la diferencia booleana restando un sólido de otro."),
        ("intersecar objetos", "Conserva únicamente el volumen compartido por la intersección de sólidos."),
        ("extruir pieza", "Extruye una forma plana a lo largo de una distancia dándole volumen 3D."),
        ("extruir cara", "Extruye perpendicularmente una cara plana seleccionada de un sólido."),
        ("cortar con plano", "Corta un objeto BIM o sólido utilizando un plano de referencia."),
        ("añadir componente", "Agrega objetos a un muro, estructura, nivel o elemento anfitrión."),
        ("quitar componente", "Sustrae o desvincula un objeto componente de su elemento anfitrión."),
    ],
    "Preferences": [
        ("preferencias generales", "Configura las opciones globales de la interfaz, idioma y rendimiento."),
        ("preferencias 2d", "Ajustes del entorno de dibujo 2D (colores de línea, snaps, precisión)."),
        ("preferencias 3d", "Configuración del entorno 3D y parámetros de visualización y render."),
        ("preferencias anotacion", "Estilos por defecto de cotas, fuentes tipográficas y flechas."),
        ("preferencias administracion", "Ajustes de esquema IFC, metadatos y opciones de proyecto BIM."),
        ("preferencias modificar", "Tolerancias y comportamientos por defecto de las herramientas de edición."),
        ("preferencias enganche", "Sensibilidad del cursor, radio de captura y rejilla de trabajo."),
        ("preferencias vistas", "Configuración gráfica de los modos de cámara y navegación 3D."),
        ("preferencias herramientas", "Personalización de barras de herramientas, accesos y atajos."),
        ("preferencias importar exportar", "Parámetros y filtros para importación y exportación de archivos (IFC, DXF, SVG, STEP)."),
    ],
    "Snapping": [
        ("plano de trabajo", "Abre el panel para definir el plano de trabajo a partir de vértices, caras o vistas rápidas."),
        ("plano superior", "Fija el plano de trabajo en vista superior (plano XY horizontal)."),
        ("plano frontal", "Fija el plano de trabajo en vista frontal (plano XZ vertical)."),
        ("plano lateral", "Fija el plano de trabajo en vista lateral (plano YZ vertical)."),
        ("alternar enganche", "Activa o desactiva de forma global los modos de enganche magnético (Snap)."),
        ("enganche a rejilla", "Activa o desactiva el enganche a las intersecciones de la cuadrícula."),
        ("enganche a extremo", "Engancha el cursor a los vértices y extremos de aristas y líneas."),
        ("enganche a punto medio", "Engancha el cursor al punto medio de aristas y segmentos."),
        ("enganche a centro", "Engancha el cursor al punto central de círculos, arcos y polígonos."),
        ("modo ortogonal", "Restringe el movimiento del cursor a ángulos estrictamente ortogonales."),
        ("bloquear enganche", "Bloquea o congela la coordenada de referencia de enganche actual."),
    ],
    "StatusBar": [
        ("bloquear ifc", "Activa o desactiva el modo estricto IFC para validar geometría según el estándar."),
        ("alternar vistas bim", "Muestra u oculta el panel lateral acoplable de vistas y niveles BIM."),
        ("cambiar fondo de vista 3d", "Alterna el fondo de la ventana 3D entre gradiente vertical, radial y color plano."),
    ],
    "Utils": [
        ("tomar medidas", "Mide distancias, aristas, caras y ángulos mediante clics interactivos."),
        ("comprobar modelo", "Revisa la geometría de los objetos seleccionados detectando fallos o caras abiertas."),
        ("cerrar huecos", "Repara y sella agujeros abiertos en mallas y caras no planas."),
        ("crear componente", "Convierte formas geométricas estándar en componentes arquitectónicos BIM."),
        ("revisar ifc", "Audita y valida las propiedades y tipos IFC del modelo contra el estándar."),
    ],
    "Explorer": [
        ("archivo", "Submenú de gestión de archivos: nuevo, abrir, guardar, importar y exportar."),
        ("proyecto", "Submenú para abrir, guardar y exportar por voz sin cuadros de diálogo nativos."),
        ("editar", "Submenú de operaciones de edición: deshacer, rehacer, cortar, copiar y pegar."),
        ("imprimir", "Submenú para configurar impresión en papel y exportación directa a formato PDF."),
        ("ventanas", "Submenú de control de ventanas: cerrar documento, cerrar todo y salir."),
        ("expresiones", "Submenú para copiar, pegar y administrar fórmulas y expresiones paramétricas."),
        ("herramientas", "Submenú de herramientas auxiliares: medir distancias, personalizar y parámetros."),
        ("estructura", "Submenú para crear piezas, grupos organizadores y enlaces (links)."),
        ("ejemplos", "Submenú con manual de usuario y ejemplos guiados interactivos paso a paso."),
        ("refrescar", "Recarga y actualiza inmediatamente la vista 3D y el árbol de objetos."),
        ("foto", "Captura una imagen de la vista 3D activa y la guarda en disco."),
        ("texto", "Crea un nuevo documento de texto dentro del proyecto."),
        ("desvincular", "Quita el enlace o dependencia del objeto seleccionado."),
        ("congelar", "Bloquea y congela la geometría del objeto seleccionado para evitar cambios."),
        ("instancias", "Selecciona automáticamente todas las instancias asociadas al objeto."),
        ("variables", "Crea un conjunto de variables de diseño paramétricas (VarSet)."),
    ],
    "Views": [
        ("perspectiva", "Activa la cámara con perspectiva cónica 3D (profundidad realista con punto de fuga)."),
        ("ortogonal", "Activa la cámara ortogonal/paralela sin distorsión de perspectiva (para planos técnicos)."),
        ("isometrica", "Orienta la vista en perspectiva isométrica 3D clásica."),
        ("frontal", "Orienta la cámara de frente (vista de alzado frontal, plano XZ)."),
        ("superior", "Orienta la cámara desde arriba (vista de planta, plano XY)."),
        ("derecha", "Orienta la cámara en vista lateral derecha (plano YZ)."),
        ("izquierda", "Orienta la cámara en vista lateral izquierda."),
        ("posterior", "Orienta la cámara en vista posterior (trasera)."),
        ("inferior", "Orienta la cámara en vista inferior (desde abajo)."),
        ("centrar vista", "Encuadra y ajusta todo el modelo visible en la pantalla (Fit All)."),
        ("enfocar seleccion", "Centra y acerca la vista al objeto actualmente seleccionado."),
        ("acercar", "Acerca la cámara aumentando el zoom sobre el modelo (Zoom In)."),
        ("alejar", "Aleja la cámara disminuyendo el zoom sobre el modelo (Zoom Out)."),
        ("girar izquierda", "Rota la cámara 15° hacia la izquierda alrededor del modelo."),
        ("girar derecha", "Rota la cámara 15° hacia la derecha alrededor del modelo."),
        ("girar arriba", "Inclina la cámara 15° hacia arriba."),
        ("girar abajo", "Inclina la cámara 15° hacia abajo."),
        ("mover camara", "Centra la cámara en unas coordenadas específicas dictadas por voz (X, Y, Z)."),
    ],
    "Select": [
        ("avanzar", "Navega al siguiente objeto del modelo 3D y lo enfoca en la vista y en el árbol."),
        ("retroceder", "Navega al objeto anterior del modelo 3D y lo enfoca en la vista y en el árbol."),
        ("seleccionar", "Selecciona y marca el objeto actual para editarlo o modificarlo."),
        ("deseleccionar", "Quita la selección del objeto actual sin afectar los demás."),
        ("seleccionar todos", "Selecciona todos los objetos del documento activo de FreeCAD."),
        ("deseleccionar todos", "Limpia y anula la selección de todos los objetos en el documento."),
        ("editar", "Pone el objeto seleccionado en modo de edición interactiva."),
        ("borrar", "Elimina del documento el objeto actualmente seleccionado."),
    ],
}

# Alias de carpetas espejo
HELP_BY_CATEGORY["BIM3D"] = HELP_BY_CATEGORY["3D-BIM"]
HELP_BY_CATEGORY["Drafting2D"] = HELP_BY_CATEGORY["2D-Drafting"]
HELP_BY_CATEGORY["Vistas"] = HELP_BY_CATEGORY["Views"]
HELP_BY_CATEGORY["Seleccionar"] = HELP_BY_CATEGORY["Select"]
HELP_BY_CATEGORY["Selection"] = HELP_BY_CATEGORY["Select"]


def get_help_for_category(
    category_name: str,
    context_path: str = "",
    current_entries: list[Any] | None = None,
) -> tuple[str, list[tuple[str, str]], str]:
    """Retorna el título, la lista de pares (comando, descripción) y el texto plano formateado.

    Args:
        category_name: Nombre interno de la categoría (p. ej. "3D-BIM", "Modify", "Base").
        context_path: Ruta de navegación (p. ej. "Base > 3D-BIM").
        current_entries: Lista opcional de ContextEntry actuales para fallback dinámico.

    Returns:
        tuple (title, items, formatted_text)
    """
    clean_cat = (category_name or "Base").strip()
    path = context_path or clean_cat
    title = format_section_title(path)

    items: list[tuple[str, str]] = []

    # 1. Búsqueda exacta en el diccionario estructurado
    if clean_cat in HELP_BY_CATEGORY:
        items = list(HELP_BY_CATEGORY[clean_cat])
    else:
        # Búsqueda por subsegmento de context_path si es un submenú (ej. Explorer > file)
        segments = [s.strip() for s in path.split(">") if s.strip()]
        last_seg = segments[-1] if segments else clean_cat
        if last_seg in HELP_BY_CATEGORY:
            items = list(HELP_BY_CATEGORY[last_seg])

    # 2. Si no se encontró o se proporcionaron entradas del navegador, complementar
    if not items and current_entries:
        seen = set()
        for entry in current_entries:
            spoken = getattr(entry, "Spoken", "").strip()
            if not spoken or spoken in seen:
                continue
            seen.add(spoken)
            is_sub = getattr(entry, "IsSubContext", lambda: False)() if callable(getattr(entry, "IsSubContext", None)) else getattr(entry, "IsSubContext", False)
            if is_sub:
                desc = f"Submenú para ingresar y ver herramientas de {spoken}."
            else:
                desc = f"Ejecuta la herramienta de {spoken}."
            items.append((spoken, desc))

    # Fallback genérico si sigue vacío
    if not items:
        items = [("ayuda", "Muestra esta ventana con las instrucciones de uso.")]

    # Generar texto plano amigable
    lines = [f"=== {title} ===", ""]
    for cmd, desc in items:
        lines.append(f"  {cmd.ljust(26)} - {desc}")
    lines.append("")
    lines.append("Para cerrar esta ventana di: «cerrar ayuda» o «cerrar»")
    formatted_text = "\n".join(lines)

    return title, items, formatted_text

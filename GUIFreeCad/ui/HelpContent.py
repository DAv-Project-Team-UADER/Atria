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

HELP_BY_CATEGORY_EN: dict[str, list[tuple[str, str]]] = {
    "Base": [
        ("explorer", "Browse files, projects, editing commands, windows, and general tools."),
        ("two d", "Open 2D drawing tools such as lines, circles, dimensions, text, and curves."),
        ("three d", "Open 3D architectural and structural modeling tools, including walls, doors, columns, and slabs."),
        ("annotation", "Create drawing dimensions, axes, sections, layers, and technical sheets."),
        ("manage", "Manage projects, IFC classification, materials, quantity schedules, and views."),
        ("modify", "Modify and transform objects with move, rotate, copy, trim, and boolean tools."),
        ("preferences", "Configure the workspace, units, language, and tool preferences."),
        ("snapping", "Configure object snapping, the grid, and the working plane."),
        ("status bar", "Toggle IFC mode, BIM views, and the 3D viewport background style."),
        ("utils", "Open measurement, model-checking, and geometry utility tools."),
        ("views", "Control standard views, camera rotation, framing, and projection mode."),
    ],
    "3D-BIM": [
        ("create site", "Create the project site or terrain and organize its buildings."),
        ("create building", "Create a building group to organize the model's levels."),
        ("create level", "Create a story or floor that groups objects at a shared elevation."),
        ("create space", "Define a room volume and calculate its floor area."),
        ("create wall", "Create an architectural wall from scratch or from a line, face, or sketch."),
        ("create curtain wall", "Divide a base face into mullions, transoms, and glazed panels."),
        ("create column", "Create a vertical structural element."),
        ("create beam", "Create a horizontal structural element between two points."),
        ("create slab", "Create a horizontal slab by extruding a planar shape."),
        ("create roof", "Create a parametric sloped roof from a closed outline."),
        ("create sloped roof", "Create a sloped roof with a pitch and an overhang on each edge."),
        ("create stairs", "Create straight stairs, stairs with a landing, or stairs with stringers."),
        ("create frame", "Extrude a profile along a path to create railings or frames."),
        ("create truss", "Create a parametric truss from a line or from scratch."),
        ("create fence", "Repeat fence posts and sections along a path."),
        ("create panel", "Create a parametric panel from a flat or corrugated 2D outline."),
        ("create equipment", "Insert non-structural furniture, equipment, or appliances."),
        ("create custom rebar", "Place reinforcing bars from a sketch onto a structure."),
        ("create window", "Insert a window into a wall and create the corresponding opening."),
        ("create door", "Insert a door into a wall and create the corresponding opening."),
        ("create pipe", "Create a straight pipe or a pipe from a base outline."),
        ("create connector", "Connect two or three pipes at an elbow or T-junction."),
        ("create box", "Create a Part box by specifying its dimensions."),
        ("convert to component", "Convert a Part object into an Arch component."),
        ("insert external reference", "Link an object stored in another FreeCAD file."),
        ("create facebinder", "Create a parametric surface from selected faces."),
        ("insert library object", "Open the object library to insert furniture and equipment."),
        ("create profile", "Create a parametric 2D profile for extrusion, such as C, H, R, U, L, or T."),
        ("shape builder", "Build edges, wires, faces, shells, and solids from primitives."),
        ("add beam reinforcement", "Reinforce a beam with stirrups and upper, lower, and shear bars."),
        ("add column reinforcement", "Reinforce a column with stirrups and main and secondary bars."),
        ("add footing reinforcement", "Reinforce a footing with a bar mesh and columns."),
        ("add slab reinforcement", "Reinforce a slab with bar meshes in both directions."),
        ("create bent-shape rebar", "Create bent reinforcing bars inside a structure."),
        ("create helical rebar", "Create a helical reinforcing bar inside a structure."),
        ("create L-shape rebar", "Create L-shaped reinforcing bars inside a structure."),
        ("create straight rebar", "Create straight reinforcing bars inside a structure."),
        ("create stirrup", "Create closed-loop reinforcing bars inside a structure."),
        ("create U-shape rebar", "Create U-shaped reinforcing bars inside a structure."),
    ],
    "2D-Drafting": [
        ("point", "Create a point on the working plane."),
        ("line", "Create a straight line between two points."),
        ("rectangle", "Create a rectangle from two opposite corners."),
        ("polygon", "Create a regular polygon from a center point and radius."),
        ("polyline", "Create a continuous sequence of straight segments through several points."),
        ("circle", "Create a circle from its center and radius."),
        ("arc", "Create an arc from its center, radius, and start and end angles."),
        ("arc from 3 points", "Create an arc that passes through three points on its perimeter."),
        ("ellipse", "Create an ellipse from its center and major and minor radii."),
        ("fillet", "Create a fillet or chamfer between selected lines."),
        ("B-spline curve", "Create a smooth B-spline curve through a series of points."),
        ("Bezier curve", "Create a Bezier curve from its control points."),
        ("text", "Create a single-line or multiline text annotation in the drawing."),
        ("dimension", "Add a dimension to measure distances or angles between points."),
        ("label", "Add a text label linked to an element."),
    ],
    "Annotation": [
        ("aligned dimension", "Create a dimension between two points or along a sloped edge."),
        ("horizontal dimension", "Create a horizontally constrained dimension between two points."),
        ("vertical dimension", "Create a vertically constrained dimension between two points."),
        ("2D drawing", "Create a 2D drawing by projecting model views and sections."),
        ("axes", "Place a structural reference axis system in the document."),
        ("axis system", "Combine multiple reference axes into one coordinated system."),
        ("label", "Add a text label associated with a building element."),
        ("working plane", "Set the position and orientation of the active working plane."),
        ("section view", "Create a cutting plane to section and display the model."),
        ("new page", "Create a sheet for technical drawings."),
        ("new view", "Insert a projected model view into the active drawing sheet."),
        ("layer", "Create a layer to organize elements and control their color and visibility."),
        ("layer manager", "Open the panel for managing, hiding, or locking layers."),
        ("clone", "Create a linked parametric clone of an object's geometry."),
    ],
    "Manage": [
        ("setup BIM project", "Guided setup for the initial parameters of a BIM project."),
        ("manage IFC properties", "Open the manager for IFC entities, types, and attributes."),
        ("export IFC", "Export the architectural model to the open IFC standard."),
        ("BIM manager", "Open the central panel for organizing and managing the BIM model."),
        ("review classifications", "Check that every object has an assigned classification."),
        ("review IFC", "Inspect and validate IFC properties and types."),
        ("manage materials", "Open the catalog and manager for construction materials."),
        ("create schedule", "Generate a schedule of material quantities and areas."),
        ("update quantities", "Recalculate quantities after model changes."),
        ("drawing views", "Insert technical views and details into project sheets."),
        ("section plane", "Define an interactive cutting plane in the 3D model view."),
        ("grid", "Generate a modular grid of guide lines for design."),
        ("view manager", "Manage saved cameras, perspectives, and orientations."),
    ],
    "Modify": [
        ("move", "Move selected objects from a source point to a destination."),
        ("copy", "Duplicate selected objects at new coordinates."),
        ("rotate", "Rotate selected objects around a center by a specified angle."),
        ("clone", "Create a parametric linked copy of the original object."),
        ("offset", "Move an object's geometry along a vector."),
        ("mirror", "Create a mirrored copy across a plane or axis."),
        ("scale", "Resize objects by applying a scale factor."),
        ("trim or extend", "Trim edges or lines that intersect other elements."),
        ("stretch", "Stretch selected edges or vertices to deform an object."),
        ("align", "Align faces, edges, or centers across multiple objects."),
        ("edit", "Edit the part's vertices and parameters."),
        ("convert to sketch", "Convert 2D Draft elements into a Sketcher sketch."),
        ("join elements", "Join contiguous lines and edges into a single wire."),
        ("split element", "Cut or split a line or wire at a selected point."),
        ("create offset", "Create a parallel offset curve or outline at a constant distance."),
        ("create 2D offset", "Create a parallel 2D outline at a specified distance."),
        ("create array", "Create an orthogonal array of copies along the X, Y, and Z axes."),
        ("create polar array", "Arrange copies in a circle around a center."),
        ("create path array", "Distribute copies along a path or curve."),
        ("array by points", "Place copies at points on another piece of geometry."),
        ("union objects", "Combine two or more solids into one using a boolean union."),
        ("cut objects", "Subtract one solid from another using a boolean difference."),
        ("intersect objects", "Keep only the volume shared by intersecting solids."),
        ("extrude piece", "Extrude a planar shape to give it 3D volume."),
        ("extrude face", "Extrude a selected planar face perpendicularly."),
        ("cut with plane", "Cut a BIM object or solid using a reference plane."),
        ("add component", "Add objects to a wall, structure, level, or host element."),
        ("remove component", "Remove or detach a component from its host element."),
    ],
    "Preferences": [
        ("general preferences", "Configure global interface, language, and performance options."),
        ("2D preferences", "Configure 2D drawing colors, snapping, and precision."),
        ("3D preferences", "Configure the 3D workspace, display, and rendering options."),
        ("annotation preferences", "Set default dimension styles, fonts, and arrows."),
        ("management preferences", "Configure IFC schemes, metadata, and BIM project options."),
        ("modify preferences", "Set default tolerances and editing tool behavior."),
        ("snapping preferences", "Configure cursor sensitivity, snap radius, and the working grid."),
        ("view preferences", "Configure camera display modes and 3D navigation."),
        ("tool preferences", "Customize toolbars, access, and keyboard shortcuts."),
        ("import export preferences", "Configure import and export settings and filters for IFC, DXF, SVG, and STEP."),
    ],
    "Snapping": [
        ("working plane", "Set the working plane using vertices, faces, or a quick view."),
        ("top plane", "Set the working plane to the top XY plane."),
        ("front plane", "Set the working plane to the front XZ plane."),
        ("side plane", "Set the working plane to the side YZ plane."),
        ("toggle snap", "Turn object snapping modes on or off globally."),
        ("snap grid", "Toggle snapping to grid intersections."),
        ("snap endpoint", "Snap the cursor to vertices and line or edge endpoints."),
        ("snap midpoint", "Snap the cursor to the midpoint of edges and segments."),
        ("snap center", "Snap the cursor to the center of circles, arcs, and polygons."),
        ("snap ortho", "Constrain cursor movement to orthogonal angles."),
        ("lock snap", "Lock the current snapping reference coordinate."),
    ],
    "StatusBar": [
        ("lock IFC", "Toggle strict IFC mode to validate geometry against the standard."),
        ("toggle BIM views", "Show or hide the dockable BIM views and levels panel."),
        ("toggle 3D background", "Cycle the 3D view background between vertical gradient, radial gradient, and solid color."),
    ],
    "Utils": [
        ("take measurements", "Measure distances, edges, faces, and angles interactively."),
        ("check model", "Check selected object geometry for faults and open faces."),
        ("close holes", "Repair and seal open holes in meshes and non-planar faces."),
        ("create component", "Convert standard geometric shapes into BIM architectural components."),
        ("review IFC", "Audit the model's IFC properties and types against the standard."),
    ],
    "Explorer": [
        ("file", "Open file tools for creating, opening, saving, importing, and exporting."),
        ("project", "Open project tools for voice-based file operations."),
        ("edit", "Open editing tools such as undo, redo, cut, copy, and paste."),
        ("print", "Configure printing or export directly to PDF."),
        ("windows", "Manage document windows, close documents, or exit the application."),
        ("expressions", "Copy, paste, and manage formulas and parametric expressions."),
        ("tools", "Open utility tools for measurements, customization, and parameters."),
        ("structure", "Create parts, groups, and links."),
        ("refresh", "Refresh the 3D view and object tree."),
        ("screenshot", "Capture the active 3D view and save it to disk."),
        ("text document", "Create a text document in the project."),
        ("unlink", "Remove the link or dependency from the selected object."),
        ("freeze", "Lock the selected object's geometry to prevent changes."),
        ("all instances", "Select every instance associated with the object."),
        ("variables", "Create a parametric design variable set."),
    ],
    "Views": [
        ("perspective", "Enable the 3D perspective camera with realistic depth and a vanishing point."),
        ("orthographic", "Enable a parallel camera without perspective distortion for technical drawings."),
        ("isometric", "Set the view to the classic 3D isometric orientation."),
        ("front", "Set the camera to the front elevation in the XZ plane."),
        ("top", "Set the camera to the top or plan view in the XY plane."),
        ("right", "Set the camera to the right-side view in the YZ plane."),
        ("left", "Set the camera to the left-side view."),
        ("rear", "Set the camera to the rear view."),
        ("bottom", "Set the camera to the bottom view."),
        ("fit all", "Frame the entire visible model in the viewport."),
        ("fit selection", "Center and zoom in on the selected object."),
        ("zoom in", "Zoom in on the model."),
        ("zoom out", "Zoom out from the model."),
        ("rotate left", "Rotate the camera 15 degrees to the left around the model."),
        ("rotate right", "Rotate the camera 15 degrees to the right around the model."),
        ("rotate up", "Tilt the camera 15 degrees upward."),
        ("rotate down", "Tilt the camera 15 degrees downward."),
        ("move camera", "Center the camera on coordinates specified by voice (X, Y, Z)."),
    ],
}

# Keep the translated aliases aligned with the Spanish catalog aliases.
HELP_BY_CATEGORY_EN["BIM3D"] = HELP_BY_CATEGORY_EN["3D-BIM"]
HELP_BY_CATEGORY_EN["Drafting2D"] = HELP_BY_CATEGORY_EN["2D-Drafting"]
HELP_BY_CATEGORY_EN["Vistas"] = HELP_BY_CATEGORY_EN["Views"]


def get_help_for_category(
    category_name: str,
    context_path: str = "",
    current_entries: list[Any] | None = None,
    language: str = "es",
) -> tuple[str, list[tuple[str, str]], str]:
    """Retorna el título, la lista de pares (comando, descripción) y el texto plano formateado.

    Args:
        category_name: Nombre interno de la categoría (p. ej. "3D-BIM", "Modify", "Base").
        context_path: Ruta de navegación (p. ej. "Base > 3D-BIM").
        current_entries: Lista opcional de ContextEntry actuales para fallback dinámico.
        language: Idioma de las etiquetas y explicaciones ("es" o "en").

    Returns:
        tuple (title, items, formatted_text)
    """
    clean_cat = (category_name or "Base").strip()
    path = context_path or clean_cat
    lang = "en" if str(language).lower().startswith("en") else "es"
    help_by_category = HELP_BY_CATEGORY_EN if lang == "en" else HELP_BY_CATEGORY
    title = format_section_title(path, lang)

    items: list[tuple[str, str]] = []

    # 1. Búsqueda exacta en el diccionario estructurado
    if clean_cat in help_by_category:
        items = list(help_by_category[clean_cat])
    else:
        # Búsqueda por subsegmento de context_path si es un submenú (ej. Explorer > file)
        segments = [s.strip() for s in path.split(">") if s.strip()]
        last_seg = segments[-1] if segments else clean_cat
        if last_seg in help_by_category:
            items = list(help_by_category[last_seg])

    # 2. Si no se encontró o se proporcionaron entradas del navegador, complementar
    if not items and current_entries:
        seen = set()
        for entry in current_entries:
            spoken = getattr(entry, "Spoken", "").strip()
            if not spoken or spoken in seen:
                continue
            seen.add(spoken)
            is_sub = getattr(entry, "IsSubContext", lambda: False)() if callable(getattr(entry, "IsSubContext", None)) else getattr(entry, "IsSubContext", False)
            if lang == "en" and is_sub:
                desc = f"Open this submenu to browse the {spoken} tools."
            elif lang == "en":
                desc = f"Run the {spoken} tool."
            elif is_sub:
                desc = f"Submenú para ingresar y ver herramientas de {spoken}."
            else:
                desc = f"Ejecuta la herramienta de {spoken}."
            items.append((spoken, desc))

    # Fallback genérico si sigue vacío
    if not items:
        items = (
            [("help", "Open this window to view usage instructions.")]
            if lang == "en"
            else [("ayuda", "Muestra esta ventana con las instrucciones de uso.")]
        )

    # Generar texto plano amigable
    lines = [f"=== {title} ===", ""]
    for cmd, desc in items:
        lines.append(f"  {cmd.ljust(26)} - {desc}")
    lines.append("")
    lines.append(
        "To close this window, say: «close help» or «close»"
        if lang == "en"
        else "Para cerrar esta ventana di: «cerrar ayuda» o «cerrar»"
    )
    formatted_text = "\n".join(lines)

    return title, items, formatted_text

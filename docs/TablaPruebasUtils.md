# Tabla de pruebas — Utils

Preparación común a todas las pruebas: FreeCAD 1.1 abierto con el banco de trabajo BIM activo. En cada fila se indica solo lo que hay que preparar además de eso.

La columna **Resultado obtenido** se completa durante la ejecución de las pruebas.

| Nombre de la función | Preparación previa | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| Add to construction group (`add_to_construction_group`) | Crear un documento en blanco, dibujar una línea y seleccionarla. | La línea pasa al grupo "Construction" (se crea si no existe) y toma el estilo de construcción. | |
| ArchSurvey (`ArchSurvey`) | Crear un documento en blanco con una pieza (por ejemplo, un cubo) y tener la vista 3D activa. | Se abre el modo survey: al hacer clic en aristas o caras se listan sus longitudes y áreas con los totales. Al ejecutar la función otra vez, el modo se cierra. | |
| BIMTrash (`BIMTrash`) | Crear un documento en blanco, crear una pieza y seleccionarla. | La pieza pasa al grupo "Trash" (se crea si no existe) y queda oculta, sin eliminarse del documento. | |
| BIMWPView (`BIMWPView`) | Crear un documento en blanco, definir un plano de trabajo (por ejemplo, frontal) y rotar la vista 3D. | La cámara de la vista 3D queda perpendicular al plano de trabajo activo, con la cuadrícula de frente. | |
| Check (`check`) | Crear un documento en blanco, crear un muro y seleccionarlo. | Se revisan los objetos seleccionados y se informa en la vista de informe si tienen problemas o si no se encontró ninguno. | |
| Close Holes (`close_holes`) | Crear un documento en blanco con una forma abierta (por ejemplo, un cubo al que se le quitó una cara) y seleccionarla. | Los agujeros de la forma se cierran y el objeto pasa a ser un sólido. | |
| Convertir a proyecto IFC (`convert_to_ifc_project`) | Crear un documento en blanco, crear un muro y seleccionarlo. | La selección se convierte en un proyecto IFC, que aparece en el árbol con el objeto dentro. | |
| Diferencia archivos IFC (`ifc_diff`) | Abrir un archivo IFC como proyecto IFC nativo y modificar uno de sus objetos sin guardar. | Se abre un diálogo que muestra los cambios todavía no guardados en el archivo IFC. | |
| DraftSelectGroup (`DraftSelectGroup`) | Crear un documento en blanco, crear un grupo con dos piezas adentro y seleccionar el grupo. | El grupo se deselecciona y quedan seleccionadas todas las piezas que contiene, en la vista 3D y en el árbol. | |
| DraftSlope (`DraftSlope`) | Crear un documento en blanco, dibujar una línea sobre el plano XY y seleccionarla. | Sin parámetros se abre el panel para ingresar la pendiente. Con un valor (por ejemplo, 1), cambia la coordenada Z de los vértices y la línea queda inclinada 45 grados. | |
| DraftWorkingPlaneProxy (`DraftWorkingPlaneProxy`) | Crear un documento en blanco y tener la vista 3D activa. | Se crea un objeto WorkingPlaneProxy que guarda el plano de trabajo y la posición de cámara actuales. | |
| Estructura (`structure`) | Crear un documento en blanco. | Se abre el panel de tareas para colocar una estructura; al indicar un punto en la vista 3D se crea el objeto Structure. | |
| Estructuras múltiples (`multiple_structures`) | Crear un documento en blanco, dibujar un perfil cerrado (base) y un objeto con varias aristas, y seleccionar ambos, primero la base. | Se crea una estructura por cada arista seleccionada, usando la arista como recorrido de extrusión de la base. | |
| Hoja de panel (`panel_sheet`) | Crear un documento en blanco. | Se crea un objeto PanelSheet (hoja 2D) que puede contener cortes de panel. | |
| IFC Expand (`ifc_expand`) | Abrir un archivo IFC como proyecto IFC nativo y seleccionar el proyecto en el árbol. | Los hijos del objeto seleccionado se cargan y aparecen desplegados en el árbol. | |
| IFC Explorer (`ifc_explorer`) | Tener a mano un archivo IFC. | Se abre la ventana del explorador IFC, que permite abrir el archivo y recorrer su estructura y atributos. | |
| IFC OpenShell Update (`ifc_openshell_update`) | Tener conexión a internet. | Se abre un diálogo que informa si IfcOpenShell está actualizado o que ofrece instalar la última versión. | |
| IFC Shape Diff (`ifc_shape_diff`) | Abrir dos documentos basados en el mismo archivo IFC, uno de ellos con un objeto modificado. | Se abre un diálogo que muestra las diferencias entre los dos documentos. | |
| Image Plane (`image_plane`) | Crear un documento en blanco y tener a mano un archivo de imagen. | Se abre el selector de archivos; tras elegir la imagen e indicar los puntos en la vista 3D se crea un plano con la imagen como textura. | |
| Lock IFC (`lock_ifc`) | Crear un documento en blanco con un muro. | Se alterna el modo IFC estricto del documento: el botón de la barra de estado cambia de estado y, al activarlo, el documento se convierte en documento IFC. | |
| Merge Walls (`merge_walls`) | Crear un documento en blanco, crear dos muros contiguos del mismo ancho y alto, y seleccionarlos. | Los dos muros se unen en un único muro. | |
| Mesh to Shape (`mesh_to_shape`) | Crear un documento en blanco, crear una malla (por ejemplo, un cubo del banco Mesh) y seleccionarla. | Se crea un objeto Part con la forma de la malla. | |
| New IFC Spreadsheet (`new_ifc_spreadsheet`) | Crear un documento en blanco, crear un muro y seleccionarlo. | Se crea una hoja de cálculo para guardar las propiedades IFC del muro. | |
| Nido (`nest`) | Crear un documento en blanco con un rectángulo (contenedor) y varias formas planas. | Se abre el panel de tareas de anidado, donde se eligen el contenedor y las formas a acomodar dentro. | |
| Nudge Down (`nudge_down`) | Crear un documento en blanco, crear una pieza y seleccionarla. | La pieza se desplaza hacia abajo en el plano de trabajo, la distancia indicada en el valor de empuje de la barra de estado. | |
| Nudge Extend (`nudge_extend`) | Crear un documento en blanco, crear un muro y seleccionarlo. | La altura (Height) del muro aumenta en el valor de empuje de la barra de estado. | |
| Nudge Left (`nudge_left`) | Crear un documento en blanco, crear una pieza y seleccionarla. | La pieza se desplaza hacia la izquierda en el plano de trabajo, la distancia indicada en el valor de empuje. | |
| Nudge Right (`nudge_right`) | Crear un documento en blanco, crear una pieza y seleccionarla. | La pieza se desplaza hacia la derecha en el plano de trabajo, la distancia indicada en el valor de empuje. | |
| Nudge Rotate Left (`nudge_rotate_left`) | Crear un documento en blanco, crear una pieza y seleccionarla. | La pieza rota 45 grados en sentido antihorario alrededor de su centro, sobre el eje del plano de trabajo. | |
| Nudge Rotate Right (`nudge_rotate_right`) | Crear un documento en blanco, crear una pieza y seleccionarla. | La pieza rota 45 grados en sentido horario alrededor de su centro, sobre el eje del plano de trabajo. | |
| Nudge Shrink (`nudge_shrink`) | Crear un documento en blanco, crear un muro y seleccionarlo. | La altura (Height) del muro disminuye en el valor de empuje de la barra de estado. | |
| Nudge Switch (`nudge_switch`) | Crear un documento en blanco y tener visible la barra de estado BIM. | El valor de empuje de la barra de estado alterna entre "Auto" y una distancia fija. | |
| Nudge Up (`nudge_up`) | Crear un documento en blanco, crear una pieza y seleccionarla. | La pieza se desplaza hacia arriba en el plano de trabajo, la distancia indicada en el valor de empuje. | |
| Panel (`panel`) | Crear un documento en blanco. | Se abre el panel de tareas para colocar un panel; al indicar un punto en la vista 3D se crea el objeto Panel. | |
| Pegamento (`glue`) | Crear un documento en blanco, crear dos piezas que se toquen y seleccionarlas. | Las piezas se unen en una única forma no paramétrica. | |
| Preferences (`preferences`) | Ninguna. | Se abre el diálogo de preferencias de FreeCAD en la sección BIM. | |
| Proyecto IFC (`ifc_project`) | Crear un documento en blanco. | Se crea un proyecto IFC nativo vacío, que aparece en el árbol. | |
| Recorte de panel (`panel_cut`) | Crear un documento en blanco, crear un panel y seleccionarlo. | Se crea un objeto PanelCut con la vista 2D del panel seleccionado. | |
| Reextruir (`reextrude`) | Crear un documento en blanco, crear una pieza extruida y seleccionar una de sus caras. | Se crea una estructura extruida nueva a partir de la cara seleccionada. | |
| Remove Shape from BIM (`remove_shape_from_bim`) | Crear un documento en blanco, crear una estructura a partir de un cubo y seleccionarla. | La estructura deja de depender del cubo base y conserva sus dimensiones como propiedades propias. | |
| Renombrar alambrado (`rename_wire`) | Crear un documento en blanco, dibujar varias líneas conectadas entre sí y seleccionarlas. | Las líneas se recrean como un único alambre (wire). | |
| Select Non-Manifold Meshes (`select_non_manifold_meshes`) | Crear un documento en blanco con una malla cerrada y una malla abierta (non-manifold). | Queda seleccionada solo la malla abierta. | |
| Sistema estructural (`structural_system`) | Crear un documento en blanco, crear una estructura y un sistema de ejes, y seleccionar ambos. | Se crea un sistema estructural que repite la estructura a lo largo de los ejes. | |
| Split Mesh (`split_mesh`) | Crear un documento en blanco con una malla formada por dos componentes separados y seleccionarla. | La malla se divide en una malla independiente por cada componente. | |
| Toggle 3D View Background (`toggle_3d_view_background`) | Crear un documento en blanco y tener la vista 3D activa. | El fondo de la vista 3D alterna entre color liso y degradado. | |
| Toggle BIM Views (`toggle_bim_views`) | Crear un documento en blanco. | El panel del gestor de vistas BIM (BIM Views) se muestra si estaba oculto y se oculta si estaba visible. | |
| Toggle IFC B-Rep Flag (`toggle_ifc_brep_flag`) | Crear un documento en blanco, crear un muro y seleccionarlo. | Se alterna la marca que fuerza a exportar el muro a IFC como B-rep. | |
| Toggle Subcomponents (`toggle_subcomponents`) | Crear un documento en blanco, crear un muro con una ventana y seleccionar el muro. | Los subcomponentes del muro (adiciones y sustracciones) se muestran si estaban ocultos y se ocultan si estaban visibles. | |
| Unclone (`unclone`) | Crear un documento en blanco, crear un muro, clonarlo y seleccionar solo el clon. | El clon pasa a ser un objeto independiente: conserva su forma y propiedades, y ya no cambia cuando se modifica el original. | |
| Ayuda de Utils (`ayuda`) | Ninguna. | Se imprime en la consola Python la ayuda de Utils, con la descripción de cada herramienta y su frase de voz. | |

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

TEXTS = {
    "es": {
        "mic_active":      "Microfono activo - Escuchando...",
        "mic_error":       "Error de micrófono",
        "section_listen":  "Voz reconocida:",
        "section_model":   "Modelo 3D:",
        "section_history": "Historial:",
        "mic_inactive":    "Microfono inactivo",
        "empty_context":   "Sin comandos en este contexto",
        "help_btn":        "Ayuda",
        "status_idle":     "Microfono inactivo",
        "no_document":    "(sin documento abierto)",
        "document_name":  "Documento",
        "hidden":         "(oculto)",
        "dock_floating":  "⧈ Volver a unir a la ventana de FreeCAD",
        "dock_attached":  "⧉ Separar de la ventana de FreeCAD",
        "dock_tooltip":   "⧉ Desacoplar / Acoplar panel ATRIA\n(Permite flotar o fijar el panel en FreeCAD)",
        "preferences_tooltip": (
            "⚙ Preferencias y configuración de voz\n"
            "Di: «preferencias»\n"
            "Haz clic para abrir las opciones"
        ),
        "help_tooltip": (
            "? Ayuda y manual de la sección\n"
            "Di: «ayuda» o «manual»\n"
            "Abre una ventana con la explicación de cada botón\n"
            "Para cerrar, di: «cerrar ayuda» o «cerrar»"
        ),
        "submenu_tooltip": (
            "Submenú: {name}\n"
            "Di: «{spoken}»\n"
            "Haz clic para explorar las herramientas"
        ),
        "tool_tooltip": (
            "Herramienta: {name}\n"
            "Di: «{spoken}»\n"
            "Haz clic para ejecutar"
        ),
        "back_tooltip": (
            "Volver al nivel anterior\n"
            "Di: «volver» o «subir»\n"
            "Haz clic para regresar"
        ),
        "context_help_tooltip": (
            "Ayuda y manual de la sección\n"
            "Di: «ayuda» o «manual»\n"
            "Haz clic para abrir la ayuda de esta sección\n"
            "Di: «cerrar ayuda» o «cerrar» para cerrarla"
        ),
        "help_window_title": "ATRIA - Manual y ayuda: {title}",
        "help_intro": "Di el comando o haz clic en su botón en la pantalla:",
        "help_close_hint": "Di: «cerrar ayuda» o «cerrar» para cerrar esta ventana",
        "close": "Cerrar",
        "help_shown": "Mostrando ayuda de {title}",
        "help_failed": "No se pudo mostrar la ayuda: {error}",
        "help_closed": "Ventana de ayuda cerrada",
        "help_not_open": "No hay una ventana de ayuda abierta",
        "help_close_failed": "Error al cerrar la ayuda: {error}",
    },
    "en": {
        "mic_active":      "Microphone active - Listening...",
        "mic_error":       "Microphone error",
        "section_listen":  "Recognized voice:",
        "section_model":   "3D Model:",
        "section_history": "History:",
        "mic_inactive":    "Microphone inactive",
        "empty_context":   "No commands in this context",
        "help_btn":        "Help",
        "status_idle":     "Microphone inactive",
        "no_document":    "(no open document)",
        "document_name":  "Document",
        "hidden":         "(hidden)",
        "dock_floating":  "⧈ Dock panel in the FreeCAD window",
        "dock_attached":  "⧉ Detach from the FreeCAD window",
        "dock_tooltip":   "⧉ Dock / undock the ATRIA panel\n(Floats or docks the panel in FreeCAD)",
        "preferences_tooltip": (
            "Preferences and voice settings\n"
            "Say: «preferences»\n"
            "Click to open the options"
        ),
        "help_tooltip": (
            "Section help and manual\n"
            "Say: «help» or «manual»\n"
            "Opens a window explaining each button\n"
            "To close it, say: «close help» or «close»"
        ),
        "submenu_tooltip": (
            "Submenu: {name}\n"
            "Say: «{spoken}»\n"
            "Click to browse tools"
        ),
        "tool_tooltip": (
            "Tool: {name}\n"
            "Say: «{spoken}»\n"
            "Click to run"
        ),
        "back_tooltip": (
            "Return to the previous level\n"
            "Say: «up» or «back»\n"
            "Click to go back"
        ),
        "context_help_tooltip": (
            "Section help and manual\n"
            "Say: «help» or «manual»\n"
            "Click to open help for this section\n"
            "Say: «close help» or «close» to close it"
        ),
        "help_window_title": "ATRIA - Help and Manual: {title}",
        "help_intro": "Say the command or click its button on the screen:",
        "help_close_hint": "Say: «close help» or «close» to close this window",
        "close": "Close",
        "help_shown": "Showing help for {title}",
        "help_failed": "Could not show help: {error}",
        "help_closed": "Help window closed",
        "help_not_open": "No help window is open",
        "help_close_failed": "Could not close help: {error}",
    },
}

SECTION_NAMES = {
    "es": {
        "Base": "Categorías Principales",
        "3D-BIM": "3D - Modelado BIM",
        "BIM3D": "3D - Modelado BIM",
        "2D-Drafting": "2D - Dibujo y Boceto",
        "Drafting2D": "2D - Dibujo y Boceto",
        "Annotation": "Anotación y Cotas",
        "Manage": "Administración y Gestión BIM",
        "Modify": "Modificar y Transformar",
        "Preferences": "Preferencias y Ajustes",
        "Snapping": "Enganche (Snapping)",
        "StatusBar": "Barra de Estado y Vistas",
        "Utils": "Utilidades y Herramientas",
        "Explorer": "Explorador de Archivos",
        "Views": "Vistas y Cámara",
        "file": "Archivo",
        "edit": "Edición",
        "print": "Imprimir / Exportar PDF",
        "windows": "Ventanas",
        "expressions": "Expresiones",
        "tools": "Herramientas",
        "structure": "Estructura",
        "examples": "Ejemplos y Tutoriales",
    },
    "en": {
        "Base": "Main Categories",
        "3D-BIM": "3D - BIM Modeling",
        "BIM3D": "3D - BIM Modeling",
        "2D-Drafting": "2D - Drafting & Sketch",
        "Drafting2D": "2D - Drafting & Sketch",
        "Annotation": "Annotation & Dimensions",
        "Manage": "Management & BIM Data",
        "Modify": "Modify & Transform",
        "Preferences": "Preferences & Settings",
        "Snapping": "Snapping",
        "StatusBar": "Status Bar & Views",
        "Utils": "Utilities & Tools",
        "Explorer": "File Explorer",
        "Views": "Views & Camera",
        "file": "File",
        "edit": "Edit",
        "print": "Print / Export PDF",
        "windows": "Windows",
        "expressions": "Expressions",
        "tools": "Tools",
        "structure": "Structure",
        "examples": "Examples & Tutorials",
    },
}


def format_section_title(context_path: str, lang: str = "es") -> str:
    """Genera el título legible y descriptivo para la sección activa de comandos."""
    lang_key = "en" if str(lang).lower().startswith("en") else "es"
    names = SECTION_NAMES.get(lang_key, SECTION_NAMES["es"])
    prefix = "Section:" if lang_key == "en" else "Sección:"

    path = (context_path or "Base").strip()
    if not path or path == "Base":
        base_name = names.get("Base", "Categorías Principales")
        return f"{prefix} {base_name}"

    segments = [p.strip() for p in path.split(">") if p.strip()]
    content = [s for s in segments if s != "Base"]
    if not content:
        return f"{prefix} {names.get('Base', 'Categorías Principales')}"

    translated = [names.get(s, s) for s in content]
    return f"{prefix} " + " > ".join(translated)

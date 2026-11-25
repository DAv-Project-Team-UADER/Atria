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
        "title":           "ASISTENTE DE VOZ PARA TECNICOS",
        "mic_active":      "Microfono activo - Escuchando...",
        "mic_error":       "Esperando microfono",
        "section_listen":  "Voz reconocida:",
        "detected":        "Detectado:",
        "section_model":   "Modelo 3D:",
        "section_history": "Historial:",
        "mic_inactive":    "Microfono inactivo",
        "empty_context":   "Sin comandos en este contexto",
        "section_cmds":    "Comandos sugeridos",
        "help_btn":        "Ayuda",
        "help_title":      "AYUDA PARA ASISTENTE DE VOZ",
        "help_text": (
            "COMANDOS DE VOZ DISPONIBLES:\n\n"
            "CONTROL DE LA APP:\n"
            "   'ayuda'           - abre esta ventana\n"
            "   'cerrar ayuda'    - cierra esta ventana\n"
            "   'minimizar'       - minimiza el programa\n"
            "   'maximizar'       - maximiza el programa\n"
            "   'cerrar programa' - cierra la aplicacion\n\n"
            "COMANDOS TECNICOS:\n"
            "   'dibujar linea'\n"
            "   'dibujar circulo'\n"
            "   'acercar'\n"
            "   'guardar archivo'\n"
            "   'limpiar pantalla'\n\n"
            "NAVEGACION EN HISTORIAL:\n"
            "   'subir' - sube 5 comandos en el historial\n"
            "   'bajar' - baja 5 comandos en el historial\n\n"
            "NAVEGACION EN MODELO:\n"
            "   'ir a [nombre]'  - resalta la parte del modelo\n\n"
            "TIP: Habla CLARO. Tambien podes hacer CLICK."
        ),
        "help_close":  "CERRAR AYUDA",
        "unknown":     "No entendi",
        "go_to":       "ir a",
        "not_found":   "no encontrado en modelo",
    },
    "en": {
        "title":           "VOICE ASSISTANT FOR TECHNICIANS",
        "mic_active":      "Microphone active - Listening...",
        "mic_error":       "Microphone error",
        "section_listen":  "Recognized voice:",
        "detected":        "Detected:",
        "section_model":   "3D Model:",
        "section_history": "History:",
        "mic_inactive":    "Microphone inactive",
        "empty_context":   "No commands in this context",
        "section_cmds":    "Suggested commands",
        "help_btn":        "Help",
        "help_title":      "HELP FOR VOICE ASSISTANT",
        "help_text": (
            "AVAILABLE VOICE COMMANDS:\n\n"
            "APP CONTROL:\n"
            "   'ayuda'           - opens this window\n"
            "   'cerrar ayuda'    - closes this window\n"
            "   'minimizar'       - minimizes the program\n"
            "   'maximizar'       - maximizes the program\n"
            "   'cerrar programa' - closes the application\n\n"
            "TECHNICAL COMMANDS:\n"
            "   'dibujar linea'\n"
            "   'dibujar circulo'\n"
            "   'acercar'\n"
            "   'guardar archivo'\n"
            "   'limpiar pantalla'\n\n"
            "HISTORY NAVIGATION:\n"
            "   'subir' - scrolls history up 5 entries\n"
            "   'bajar' - scrolls history down 5 entries\n\n"
            "MODEL NAVIGATION:\n"
            "   'ir a [name]'  - highlights model part\n\n"
            "TIP: Speak CLEARLY. You can also CLICK."
        ),
        "help_close":  "CLOSE HELP",
        "unknown":     "Not understood",
        "go_to":       "ir a",
        "not_found":   "not found in model",
    },
    "pt": {
        "title":           "ASSISTENTE DE VOZ PARA TECNICOS",
        "mic_active":      "Microfone ativo - Escutando...",
        "mic_error":       "Erro de microfone",
        "section_listen":  "Voz reconhecida:",
        "detected":        "Detectado:",
        "section_model":   "Modelo 3D:",
        "section_history": "Histórico:",
        "mic_inactive":    "Microfone inativo",
        "empty_context":   "Sem comandos neste contexto",
        "section_cmds":    "Comandos sugeridos",
        "help_btn":        "Ajuda",
        "help_title":      "AJUDA PARA ASSISTENTE DE VOZ",
        "help_text": (
            "COMANDOS DE VOZ DISPONIVEIS:\n\n"
            "CONTROLE DO APP:\n"
            "   'ayuda'           - abre esta janela\n"
            "   'cerrar ayuda'    - fecha esta janela\n"
            "   'minimizar'       - minimiza o programa\n"
            "   'maximizar'       - maximiza o programa\n"
            "   'cerrar programa' - fecha o aplicativo\n\n"
            "COMANDOS TECNICOS:\n"
            "   'dibujar linea'\n"
            "   'dibujar circulo'\n"
            "   'acercar'\n"
            "   'guardar archivo'\n"
            "   'limpiar pantalla'\n\n"
            "NAVEGACAO NO HISTORICO:\n"
            "   'subir' - sobe 5 entradas no historico\n"
            "   'bajar' - desce 5 entradas no historico\n\n"
            "NAVEGACAO NO MODELO:\n"
            "   'ir a [nome]'  - destaca a parte do modelo\n\n"
            "DICA: Fale CLARAMENTE. Voce tambem pode CLICAR."
        ),
        "help_close":  "FECHAR AJUDA",
        "unknown":     "Nao entendido",
        "go_to":       "ir a",
        "not_found":   "nao encontrado no modelo",
    },
}

MODEL_PARTS = ["Documento 1"]

MODEL_PARTS_ALIASES = {
    "documento uno": "Documento 1",
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
        "Select": "Selección de Objetos",
        "Seleccionar": "Selección de Objetos",
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
        "Select": "Object Selection",
        "Selection": "Object Selection",
        "file": "File",
        "edit": "Edit",
        "print": "Print / Export PDF",
        "windows": "Windows",
        "expressions": "Expressions",
        "tools": "Tools",
        "structure": "Structure",
        "examples": "Examples & Tutorials",
    },
    "pt": {
        "Base": "Categorias Principais",
        "3D-BIM": "3D - Modelagem BIM",
        "BIM3D": "3D - Modelagem BIM",
        "2D-Drafting": "2D - Desenho e Esboço",
        "Drafting2D": "2D - Desenho e Esboço",
        "Annotation": "Anotação e Cotas",
        "Manage": "Administração e Gestão BIM",
        "Modify": "Modificar e Transformar",
        "Preferences": "Preferências e Configurações",
        "Snapping": "Encaixe (Snapping)",
        "StatusBar": "Barra de Estado e Vistas",
        "Utils": "Utilidades e Ferramentas",
        "Explorer": "Explorador de Arquivos",
        "file": "Arquivo",
        "edit": "Edição",
        "print": "Imprimir / Exportar PDF",
        "windows": "Janelas",
        "expressions": "Expressões",
        "tools": "Ferramentas",
        "structure": "Estrutura",
        "examples": "Exemplos e Tutoriais",
    },
}


def format_section_title(context_path: str, lang: str = "es") -> str:
    """Genera el título legible y descriptivo para la sección activa de comandos."""
    lang_key = "en" if str(lang).lower().startswith("en") else ("pt" if str(lang).lower().startswith("pt") else "es")
    names = SECTION_NAMES.get(lang_key, SECTION_NAMES["es"])
    prefix = "Section:" if lang_key == "en" else ("Seção:" if lang_key == "pt" else "Sección:")

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

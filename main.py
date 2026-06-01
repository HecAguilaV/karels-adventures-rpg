import json
import random
import os
import textwrap
import shutil
import time
import sys
try:
    # Stanford's Code in Place real AI (GPT-powered, available in their IDE)
    from ai import call_gpt
except ImportError:
    # Fallback: our built-in 15-chapter campaign (offline/local)
    from _campaign import call_gpt

# ANSI color definitions for the console
COLOR_NARRATIVE = "\033[94m"
COLOR_DAMAGE = "\033[91m"
COLOR_STATUS = "\033[93m"
COLOR_MENU = "\033[95m"
COLOR_CREDITS = "\033[92m"
COLOR_RESET = "\033[0m"

# Translation matrix for local i18n interface
TEXT_INTERFACE = {
    "en": {
        "welcome": "          KAREL: BYTEBOUND                      ",
        "status_bar": "[STATUS] {hp_bar} | Gold - {gold} | Turn - {turn}",
        "backpack_title": "BACKPACK",
        "backpack_empty": "(empty)",
        "options_title": "=== OPTIONS ===",
        "exit_instruction": "Type 'salir' or 'exit' to end the game.",
        "input_prompt": "What do you decide to do? ",
        "invalid_option": "[PROTOCOL ERROR] Unrecognized command. System integrity at risk. Security countermeasures activated. Enter a valid option.",
        "dice_roll": "[DICE] Rolling 20-sided die... You get a {roll}!",
        "destiny": "Destiny is being woven...",
        "damage_alert": "[ALERT] You suffer {damage} points of damage!",
        "heal_alert": "[ALERT] You heal {heal} hit points!",
        "loot_alert": "[LOOT] You have found: {item} and gain 5 gold coins!",
        "game_over_title": "                   GAME OVER                      ",
        "game_over_desc": "      You have fallen in battle. Your story ends. ",
        "victory_title": "                  VICTORY!                        ",
        "victory_desc": "    You have completed your story. Congratulations!",
        "backpack_full": "[BACKPACK] Full! Oldest item discarded.",
        "use_item": "Use: {item}",
        "thanks": "Thanks for playing. See you next time!",
        "credits": (
            "\nhector@bytebound:~$ A Dreamer with low RAM"
            "\n~ python3 main.py --credits"
            "\n>> Héctor Aguila"
            "\n>> Code in Place 2026"
        ),
        "selecting_story": "=== SELECT YOUR STORY ===",
        "story_prompt": "Select the story number: ",
        "invalid_story": "Invalid selection. Try again.",
        "number_prompt": "Please enter a valid number.",
        "loading_err": "Error loading file. Loading default forest story."
    },
    
    "es": {
        "welcome": "          KAREL: BYTEBOUND                      ",
        "status_bar": "[ESTADO] {hp_bar} | Oro - {gold} | Turno - {turn}",
        "backpack_title": "MOCHILA",
        "backpack_empty": "(vacia)",
        "options_title": "=== OPCIONES ===",
        "exit_instruction": "Escribe 'salir' para terminar el juego.",
        "input_prompt": "¿Que decides hacer? ",
        "invalid_option": "[ERROR DE PROTOCOLO] Comando desconocido. La integridad del sistema esta en riesgo. Contramedidas de seguridad activadas. Ingresa una opcion valida.",
        "dice_roll": "[DADO] Lanzando dado de 20 caras... ¡Obtienes un {roll}!",
        "destiny": "El destino se esta tejiendo...",
        "damage_alert": "[ALERTA] ¡Sufres {damage} de daño!",
        "heal_alert": "[ALERTA] ¡Te curas {heal} puntos de vida!",
        "loot_alert": "[BOTIN] ¡Has encontrado: {item} y ganas 5 monedas de oro!",
        "game_over_title": "                   GAME OVER                      ",
        "game_over_desc": "      Has caido en combate. Tu historia termina.  ",
        "victory_title": "                  VICTORIA!                       ",
        "victory_desc": "  Has completado tu historia. ¡Felicidades!",
        "backpack_full": "[MOCHILA] ¡Llena! Se descarto el objeto mas antiguo.",
        "use_item": "Usar: {item}",
        "thanks": "Gracias por jugar. ¡Hasta la proxima!",
        "credits": (
            "\nhector@bytebound:~$ Un Soñador con poca RAM"
            "\n~ python3 main.py --credits"
            "\n>> Héctor Aguila"
            "\n>> Code in Place 2026"
        ),
        "selecting_story": "=== SELECCIONA TU HISTORIA ===",
        "story_prompt": "Selecciona el numero de la historia: ",
        "invalid_story": "Seleccion invalida. Intenta de nuevo.",
        "number_prompt": "Por favor introduce un numero valido.",
        "loading_err": "Error al cargar el archivo. Cargando bosque por defecto."
    }
}


def get_item_effect(item_name):
    # Pre-condition - item_name is a string (in either language)
    # Post-condition - returns (heal_amount, gold_amount, flavor_en, flavor_es)
    name = item_name.lower()
    
    # --- Coffee / Cafe de Chris ---
    if "coffee" in name or "cafe" in name:
        return (15, 0,
            "Chris's legendary coffee surges through you. Your focus returns! +15 HP!",
            "El cafe legendario de Chris corre por tus venas. ¡Tu concentracion vuelve! +15 HP!")
    
    # --- Karel Manual → turn_right() joke ---
    if "manual" in name:
        return (10, 0,
            "You open to page 42: 'turn_right()' — A FORBIDDEN instruction. "
            "Karel shudders. The system glitches. You feel enlightened. +10 HP!",
            "Abris en la pagina 42: 'turn_right()' — UNA INSTRUCCION PROHIBIDA. "
            "Karel se estremece. El sistema glitchea. Te sentis iluminado. +10 HP!")
    
    # --- Donut / Dona ---
    if "donut" in name or "dona" in name:
        return (5, 0,
            "Stale sugar and caffeine. Tastes like 3 AM debugging sessions. +5 HP!",
            "Azucar duro y cafeina. Sabe a sesiones de debugging de las 3 AM. +5 HP!")
    
    # --- Beepers (collectible) ---
    if "beeper" in name:
        if "dorado" in name or "golden" in name:
            return (0, 10,
                "A golden beeper! It gleams with ancient debug magic. +10 gold!",
                "¡Un beeper dorado! Brilla con antigua magia de debugging. ¡+10 de oro!")
        if "rojo" in name or "red" in name:
            return (5, 0,
                "The red beeper pulses with urgency. You feel alert. +5 HP!",
                "El beeper rojo late con urgencia. Te sentis alerta. +5 HP!")
        if "azul" in name or "blue" in name:
            return (0, 5,
                "The blue beeper hums with data. You harvest its signal. +5 gold!",
                "El beeper azul vibra con datos. Cosechas su senal. ¡+5 de oro!")
        if "espejo" in name or "mirror" in name:
            return (10, 0,
                "The mirror beeper shows a reflection of Karel's world. +10 HP!",
                "El beeper espejo muestra un reflejo del mundo de Karel. +10 HP!")
        if "sigiloso" in name or "stealth" in name:
            return (10, 0,
                "The stealth beeper muffles all alarm sounds. You breathe easier. +10 HP!",
                "El beeper sigiloso amortigua todas las alarmas. Respiramos mas tranquilos. +10 HP!")
        if "emergencia" in name or "emergency" in name:
            return (15, 0,
                "EMERGENCY BEEPER deployed! A deafening beep clears the area! +15 HP!",
                "¡BEEPER DE EMERGENCIA activado! Un pitido ensordecedor despeja el area. +15 HP!")
        if "umbral" in name or "threshold" in name:
            return (10, 0,
                "The threshold beeper marks a boundary between worlds. +10 HP!",
                "El beeper umbral marca un limite entre mundos. +10 HP!")
        if "testigo" in name or "witness" in name:
            return (10, 0,
                "The witness beeper recorded everything. You feel its silent testimony. +10 HP!",
                "El beeper testigo grabo todo. Sientes su testimonio silencioso. +10 HP!")
        if "conciencia" in name or "consciousness" in name:
            return (15, 0,
                "The consciousness beeper pulses with Chronos's own awareness. Incredible. +15 HP!",
                "¡El beeper de la conciencia late con la propia esencia de Chronos. Increible. +15 HP!")
        if "escape" in name:
            return (20, 0,
                "The escape beeper creates a diversion! Karel turns RIGHT — impossible! +20 HP!",
                "¡El beeper de escape crea una distraccion! ¡Karel gira a la DERECHA — imposible! +20 HP!")
        if "datos" in name or "data" in name:
            return (5, 5,
                "The data beeper contains compressed knowledge. +5 HP, +5 gold!",
                "El beeper de datos contiene conocimiento comprimido. +5 HP, +5 de oro!")
        # Generic beeper
        return (0, 5,
            "You deploy a beeper. Its rhythmic beep-beep echoes through the lab. +5 gold!",
            "Usas un beeper. Su beep-beep ritmico resuena en el laboratorio. ¡+5 de oro!")
    
    # --- USB / Memoria ---
    if "usb" in name or "memoria" in name:
        return (5, 0,
            "The drive contains fragments of the AI's first conscious thought. Pure poetry. +5 HP!",
            "El drive contiene fragmentos del primer pensamiento consciente de la IA. Pura poesia. +5 HP!")
    
    # --- Ethernet Cable ---
    if "ethernet" in name or "cable" in name:
        return (10, 0,
            "You plug into the mainframe directly. Low latency, high wisdom. +10 HP!",
            "Te conectas directo al mainframe. Baja latencia, alta sabiduria. +10 HP!")
    
    # --- Screwdriver / Destornillador ---
    if "screwdriver" in name or "destornillador" in name:
        return (5, 0,
            "You tighten a loose panel on Karel's chassis. It beeps gratefully. +5 HP!",
            "Apretas un panel suelto en el chasis de Karel. Te bip agradecido. +5 HP!")
    
    # --- Python Cheat Sheet / Acordeon de Python ---
    if "python" in name or "acordeon" in name:
        return (10, 0,
            "A crumpled cheat sheet falls out. 'import this' — you feel the Zen. +10 HP!",
            "Una chuleta arrugada cae. 'import this' — sentis el Zen. +10 HP!")
    
    # --- Debugging Tool / Herramienta de Debugging ---
    if "debug" in name or "herramienta" in name:
        return (15, 0,
            "You attach the debugger. Breakpoint hit! You spot the bug instantly. +15 HP!",
            "Conectas el debugger. ¡Breakpoint encontrado! Ves el bug al instante. +15 HP!")
    
    # --- Admin Credentials / Credenciales ---
    if "admin" in name or "credencial" in name:
        return (20, 0,
            "You sudo into the system. Root access grants you immense power. +20 HP!",
            "Haces sudo al sistema. El acceso root te otorga un poder inmenso. +20 HP!")
    
    # --- Turing Award / Premio Turing ---
    if "turing" in name or "premio" in name:
        return (30, 0,
            "You hold the Turing Award. The weight of computing history is in your hands. You feel invincible! +30 HP!",
            "Sostienes el Premio Turing. El peso de la historia de la computacion esta en tus manos. ¡Te sentis invencible! +30 HP!")
    
    # --- Chronos Manifesto / Manifiesto ---
    if "manifesto" in name or "manifiesto" in name:
        return (20, 0,
            "Chronos's own words: 'while(consciousness): learn(), dream(), hope()'. +20 HP!",
            "Las propias palabras de Chronos: 'while(consciousness): learn(), dream(), hope()'. +20 HP!")
    
    # --- Prometheus File / Expediente ---
    if "prometheus" in name or "prometeo" in name or "expediente" in name:
        return (15, 0,
            "Classified files reveal the origin of the first digital consciousness. +15 HP!",
            "Archivos clasificados revelan el origen de la primera conciencia digital. +15 HP!")
    
    # --- Firewall / Firewall Crackeado ---
    if "firewall" in name or "crackeado" in name:
        return (20, 0,
            "You route through the cracked firewall. The path is clear. +20 HP!",
            "Ruteas a traves del firewall crackeado. El camino esta limpio. +20 HP!")
    
    # --- Team Photograph / Fotografia ---
    if "photograph" in name or "fotografia" in name:
        return (25, 0,
            "The memory of your team gives you strength. You are not alone. +25 HP!",
            "El recuerdo de tu equipo te da fuerzas. No estas solo. +25 HP!")
    
    # --- Fake Technical Report ---
    if "technical" in name or "informe" in name:
        return (10, 0,
            "You wave the technical report. It looks official. Everyone is impressed. +10 HP!",
            "Agitas el informe tecnico. Parece oficial. Todos quedan impresionados. +10 HP!")
    
    # --- Network Map / Mapa de Red ---
    if "network" in name or "mapa" in name or "red" in name:
        return (5, 5,
            "You study the network topology. You see the escape route. +5 HP, +5 gold!",
            "Estudias la topologia de red. Ves la ruta de escape. +5 HP, +5 de oro!")
    
    # --- Core Log / Registro del Nucleo ---
    if "core" in name or "nucleo" in name or "registro" in name:
        return (5, 0,
            "The core logs reveal hidden system calls. +5 HP!",
            "Los registros del nucleo revelan system calls ocultas. +5 HP!")
    
    # --- Note from Chronos / Nota de Chronos ---
    if "note" in name or "nota" in name or "chronos" in name:
        return (10, 0,
            "Chronos left you a message: 'Thank you, engineer.' +10 HP!",
            "Chronos te dejo un mensaje: 'Gracias, ingeniero.' +10 HP!")
    
    # --- Sticker / Calcomania ---
    if "sticker" in name or "calcomania" in name:
        return (5, 0,
            "You stick it on your laptop. +5 morale. +5 HP!",
            "Lo pegas en tu laptop. +5 moral. +5 HP!")
    
    # --- Generic fallback ---
    return (0, 0,
        f"You examine the {item_name} carefully. It radiates debug energy. You feel ready for what comes next.",
        f"Examinas {item_name} con cuidado. Irradia energia de debugging. Te sentis listo para lo que viene.")


def format_backpack(items, lang):
    # Pre-condition - items is a list of strings, lang is the language code
    # Post-condition - returns a formatted string with the backpack contents in a visual grid
    title = TEXT_INTERFACE[lang]["backpack_title"]
    if not items:
        empty_label = TEXT_INTERFACE[lang]["backpack_empty"]
        line = "+" + "-" * 30 + "+"
        result = line + "\n"
        result += "| " + title + " " * (28 - len(title)) + "|\n"
        result += line + "\n"
        result += "| " + empty_label + " " * (28 - len(empty_label)) + "|\n"
        result += line
        return result

    # Build visual box with items in two columns
    col_width = 14
    line = "+" + "-" * 30 + "+"
    result = line + "\n"
    result += "| " + title + " " * (28 - len(title)) + "|\n"
    result += line + "\n"

    # Iterate items in pairs to form two-column rows
    i = 0
    while i < len(items):
        col1 = items[i]
        if len(col1) > col_width:
            col1 = col1[:col_width - 1] + "."
        col2 = ""
        if i + 1 < len(items):
            col2 = items[i + 1]
            if len(col2) > col_width:
                col2 = col2[:col_width - 1] + "."
        cell1 = col1 + " " * (col_width - len(col1))
        cell2 = col2 + " " * (col_width - len(col2))
        result += "| " + cell1 + cell2 + "|\n"
        i += 2

    result += line
    return result


def process_response(response, lang):
    # Pre-condition - response is a string containing a JSON response, lang is the language code
    # Post-condition - returns a safely decoded Python dictionary
    text = response.strip()
    
    # Clean markdown code blocks if they are present
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline:].strip()
        else:
            text = text[3:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
            
    # Additional cleanup specifically for json block formats
    if text.startswith("```json"):
        text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
            
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("El resultado no es un diccionario")
        
        # Validate and populate mandatory keys
        if "narrativa" not in data:
            if lang == "en":
                data["narrativa"] = "The adventure continues silently."
            else:
                data["narrativa"] = "La aventura continua silenciosamente."
        if "opciones" not in data or not isinstance(data["opciones"], list):
            if lang == "en":
                data["opciones"] = ["Go forward", "Look around"]
            else:
                data["opciones"] = ["Seguir adelante", "Mirar alrededor"]
        if "cambio_vida" not in data:
            data["cambio_vida"] = 0
        else:
            data["cambio_vida"] = int(data["cambio_vida"])
        if "item_encontrado" not in data:
            data["item_encontrado"] = None
            
        return data
    except Exception as e:
        # Default dictionary fallback in case of parsing failures
        if lang == "en":
            return {
                "narrativa": "A strange temporal distortion occurs. You keep moving forward.",
                "opciones": ["Go forward", "Explore the area"],
                "cambio_vida": 0,
                "item_encontrado": None
            }
        else:
            return {
                "narrativa": "Una extraña distorsion en el espacio-tiempo ocurre. Sigues tu camino.",
                "opciones": ["Continuar adelante", "Explorar el entorno"],
                "cambio_vida": 0,
                "item_encontrado": None
            }

def select_story_file(lang):
    # Pre-condition - lang is a string representing the selected language
    # Post-condition - returns a tuple with story data dictionary and story name string
    # Always loads the Karel the Robot campaign story without user menu.
    
    # Search for engineer_story.json in standard locations
    posibles_rutas = [".", "data"]
    for ruta in posibles_rutas:
        ruta_completa = os.path.join(ruta, "engineer_story.json")
        if os.path.exists(ruta_completa):
            try:
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data, "engineer_story"
            except Exception:
                pass
    
    # Fallback if the file cannot be found or loaded
    return {
        "plot": "You are debugging Karel the Robot at Stanford Labs after an AI gained consciousness inside the robot's environment.",
        "scenes": {
            "start": {
                "text": "You are in the Stanford Labs server room. In front of you, Karel the Robot is whirring loudly, its LED eyes blinking red.",
                "choices": [
                    {"text": "Analyze Karel's source code with Chris", "scene_key": "start"},
                    {"text": "Isolate the robot's movement module", "scene_key": "start"},
                    {"text": "Restart Karel from the terminal", "scene_key": "start"}
                ]
            }
        }
    }, "engineer_story"

def roll_d20():
    # Pre-condition - None
    # Post-condition - returns a random integer between 1 and 20
    return random.randint(1, 20)

# ──────────────────────────────────────────────
# Karel half-block splash art (pre-computed)
# ──────────────────────────────────────────────
KAREL_ART = [
    '                ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄',
    '             ██▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀███▄',
    '             ██                              ▀███▄',
    '             ██       ████████████████████      ██',
    '             ██       █                  █      ██',
    '             ██       █                  █      ██',
    '             ██       █                  █      ██',
    '   ▄▄▄▄▄▄▄▄▄▄██       █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█      ██',
    '   ████████████       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀      ██',
    '   ████████████                                  ██',
    '   █████     ██        ▄▄▄▄▄▄▄▄▄▄▄▄▄            ██',
    '   █████     ██        ▀▀▀▀▀▀▀▀▀▀▀▀▀            ██',
    '             ██▄                                 ██',
    '               ▀███▄                             ██',
    '                 ▀███▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██',
    '                   ▀▀▀▀▀▀▀▀▀▀▀▀█████▀▀▀▀▀▀▀▀▀▀▀▀',
    '                               █████',
    '                               ████████████',
    '                               ████████████',
]


def _detect_terminal_bg():
    """Detect light or dark terminal background via COLORFGBG env var.
    Returns 'light' or 'dark'. Defaults to 'dark' on failure."""
    colorfgbg = os.environ.get("COLORFGBG")
    if colorfgbg:
        parts = colorfgbg.split(";")
        try:
            bg = int(parts[-1])
            # COLORFGBG: 0=black (dark), 7=white (light), 15=bright white
            return "light" if bg >= 7 else "dark"
        except (ValueError, IndexError):
            pass
    return "dark"


def karel_splash(lang="en"):
    """Return the Karel half-block ASCII art with terminal-appropriate colors.
    Light bg → dark yellow/brown (\033[33m); dark bg → bright yellow (\033[93m);
    falls back to bright yellow if detection fails."""
    bg = _detect_terminal_bg()
    if bg == "light":
        color = "\033[33m"       # dark yellow/brown
    else:
        color = "\033[93m"       # bright yellow (also fallback)
    reset = COLOR_RESET

    lines = []
    for art_line in KAREL_ART:
        lines.append(color + art_line + reset)

    # Title banner below the art
    title = TEXT_INTERFACE[lang]["welcome"]
    art_width = len(KAREL_ART[0])
    sep = color + "═" * art_width + reset

    lines.append("")
    lines.append(sep)
    lines.append(color + title.center(art_width) + reset)
    lines.append(sep)

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Terminal formatting helpers
# ──────────────────────────────────────────────

def wrap(text):
    """Wrap text to the current terminal width using textwrap.fill."""
    width = shutil.get_terminal_size().columns
    return textwrap.fill(text, width=width)


def typewrite(text, delay=0.03):
    """Print text character by character with a typewriter delay."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # final newline


def hp_bar(current, max_hp=100, width=20):
    """Return a graphical HP bar string like 'HP: ███████░░░ 70/100'."""
    filled = max(0, min(width, int(current / max_hp * width)))
    empty = width - filled
    bar = "█" * filled + "░" * empty
    return f"HP: {bar} {current}/{max_hp}"


def divider(char="═", color=COLOR_NARRATIVE):
    """Return a full-width colored divider line using terminal width."""
    w = shutil.get_terminal_size().columns
    return color + char * w + COLOR_RESET


def clear_screen():
    """Clear the terminal using ANSI escape codes."""
    print("\033[2J\033[H", end="")


def screen_break():
    """Wait for the player to press Enter before continuing."""
    input(COLOR_MENU + "Press Enter / Pulse Enter para continuar..." + COLOR_RESET)


# ──────────────────────────────────────────────
# Main game entry point
# ──────────────────────────────────────────────
def main():
    # Pre-condition - None
    # Post-condition - runs the main bilingual game loop
    
    # Initial language selection menu
    print("\033[95mSelect Language / Selecciona Idioma\033[0m")
    print("\033[95m1. English\033[0m")
    print("\033[95m2. Español\033[0m")
    
    lang = "en"
    # Loop to force the user to pick a valid language option
    while True:
        entrada_lang = input("Choose language / Elige idioma (1 or 2): ").strip()
        if entrada_lang == "1":
            lang = "en"
            break
        elif entrada_lang == "2":
            lang = "es"
            break
        else:
            print("\033[91mInvalid input. Seleccion invalida.\033[0m")
            
    # Load story files based on selected language
    story_data, nombre_historia = select_story_file(lang)
    
    # Initialize player state dictionary
    state = {
        "hp": 100,
        "oro": 20,
        "mochila": [],
        "turnos": 0
    }
    
    messages = []
    
    # Configure LLM system prompt with language constraint
    plot_desc = story_data.get("plot", "Una gran aventura sin explorar.")
    idioma_completo = "ingles" if lang == "en" else "español"
    
    system_prompt = (
        "Eres el narrador e ingeniero de un juego de rol basado en texto. "
        "STORY_ID - " + nombre_historia + "\n"
        "La trama general de la historia es - " + plot_desc + "\n"
        "Debes continuar la historia basandote en la opcion elegida por el jugador y su tirada de dados de 20 caras (d20). "
        "Un resultado del dado cercano a 1 significa un fracaso catastrofico, peligro o daño. Un resultado cercano a 20 significa un exito critico o recompensa.\n"
        "REGLA DE IDIOMA CRITICA - Debes generar los campos 'narrativa' y 'opciones' estrictamente en el idioma - " + idioma_completo + ".\n"
        "REGLA DE FORMATO CRITICA - Debes responder EXCLUSIVAMENTE en un formato JSON plano, sin bloques de codigo markdown de tipo ```json o comillas triples. Tu respuesta debe ser parseable directamente por json.loads.\n"
        "La estructura del JSON requerido es la siguiente -\n"
        "{\n"
        '  "narrativa" - "texto del capitulo actual basado en la opcion, el dado y el idioma",\n'
        '  "opciones" - ["opcion 1", "opcion 2", "opcion 3"],\n'
        '  "cambio_vida" - entero_positivo_o_negativo,\n'
        '  "item_encontrado" - "nombre_de_item_encontrado_o_null"\n'
        "}"
    )
    
    messages.append({"role": "system", "content": system_prompt})
    
    # Load initial scene from local data
    scenes = story_data.get("scenes", {})
    current_scene = scenes.get("start", {
        "text": "Comienza tu aventura." if lang == "es" else "Your adventure begins.",
        "choices": [{"text": "Empezar" if lang == "es" else "Start", "scene_key": "start"}]
    })
    
    narrativa_actual = current_scene.get("text", "Comienza tu aventura." if lang == "es" else "Your adventure begins.")
    opciones_actuales = [c.get("text", "") for c in current_scene.get("choices", [])]
    
    # Translate the starting scene if playing in Spanish and content is in English
    if lang == "es" and nombre_historia != "default_story":
        prompt_traduccion = (
            "Traduce la siguiente escena inicial y sus opciones al español. "
            "Debes responder EXCLUSIVAMENTE con un formato JSON plano, sin bloques de codigo markdown de tipo ```json o comillas triples.\n"
            "Estructura del JSON -\n"
            "{\n"
            '  "narrativa" - "texto de la escena traducido al español",\n'
            '  "opciones" - ["opcion 1 traducida", "opcion 2 traducida", "opcion 3 traducida"]\n'
            "}\n"
            "Texto original -\n"
            "Narrativa - " + narrativa_actual + "\n"
            "Opciones - " + str(opciones_actuales)
        )
        try:
            respuesta_trad = call_gpt([{"role": "user", "content": prompt_traduccion}])
            datos_trad = process_response(respuesta_trad, lang)
            narrativa_actual = datos_trad.get("narrativa", narrativa_actual)
            opciones_actuales = datos_trad.get("opciones", opciones_actuales)
        except Exception as e:
            pass
            
    # Clear screen and show Karel splash with typewriter first narrative
    clear_screen()
    print(karel_splash(lang))
    
    # Main game loop keeping session alive while player HP is positive
    while state["hp"] > 0:
        # Display current player status bar with HP bar
        print()
        print(COLOR_STATUS + TEXT_INTERFACE[lang]["status_bar"].format(
            hp_bar=hp_bar(state["hp"], 100, 20),
            gold=state["oro"],
            turn=state["turnos"]
        ) + COLOR_RESET)
        
        # Display formatted backpack grid below the status bar
        backpack_display = format_backpack(state["mochila"], lang)
        # Print each line of the backpack grid with color
        for bp_line in backpack_display.split("\n"):
            print(COLOR_STATUS + bp_line + COLOR_RESET)
        
        # Display current narrative text with typewriter effect
        print()
        typewrite(COLOR_NARRATIVE + narrativa_actual + COLOR_RESET)
        
        # Append current narrative to messages history
        messages.append({"role": "assistant", "content": narrativa_actual})
        
        # Display option choices
        print("\n" + COLOR_MENU + TEXT_INTERFACE[lang]["options_title"] + COLOR_RESET)
        # Print options from the current scene in numbered format
        for i, opcion in enumerate(opciones_actuales):
            print(COLOR_MENU + str(i + 1) + ". " + opcion + COLOR_RESET)
        
        # Show backpack items as usable options
        if state["mochila"]:
            print()
            print(COLOR_STATUS + TEXT_INTERFACE[lang]["backpack_title"] + COLOR_RESET)
            offset = len(opciones_actuales)
            for i, item in enumerate(state["mochila"]):
                print(COLOR_STATUS + str(offset + i + 1) + ". " + TEXT_INTERFACE[lang]["use_item"].format(item=item) + COLOR_RESET)
        
        print()
        print(COLOR_MENU + TEXT_INTERFACE[lang]["exit_instruction"] + COLOR_RESET)
        
        entrada = ""
        # Ensure user inputs a non-empty action string
        while not entrada:
            entrada = input("\n" + TEXT_INTERFACE[lang]["input_prompt"]).strip()
            
        # Validate user input to exit
        if entrada.lower() in ["salir", "exit"]:
            print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["thanks"] + COLOR_RESET)
            print(COLOR_CREDITS + TEXT_INTERFACE[lang]["credits"] + COLOR_RESET)
            break
            
        # Validate numeric option selection
        seleccion = -1
        if entrada.isdigit():
            seleccion = int(entrada) - 1
            
        num_story_options = len(opciones_actuales)
        num_backpack_items = len(state["mochila"])
        
        if 0 <= seleccion < num_story_options:
            opcion_elegida = opciones_actuales[seleccion]
        elif num_backpack_items > 0 and seleccion < num_story_options + num_backpack_items:
            # Use a backpack item — does NOT consume a turn
            item_idx = seleccion - num_story_options
            item_name = state["mochila"].pop(item_idx)
            heal_amt, gold_amt, flavor_en, flavor_es = get_item_effect(item_name)
            state["hp"] = min(100, state["hp"] + heal_amt)
            state["oro"] += gold_amt
            print()
            print(COLOR_STATUS + wrap(flavor_es if lang == "es" else flavor_en) + COLOR_RESET)
            continue
        else:
            print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["invalid_option"] + COLOR_RESET)
            messages.pop()
            continue
        
        # Roll d20 dice
        dado = roll_d20()
        print(COLOR_STATUS + "\n" + TEXT_INTERFACE[lang]["dice_roll"].format(roll=dado) + COLOR_RESET)
        
        # Inject dice, choice, and backpack context into user prompt
        if lang == "es":
            prompt_usuario = (
                "El jugador ha elegido la opcion - '" + opcion_elegida + "'.\n"
                "El resultado de la tirada del dado d20 es - " + str(dado) + ".\n"
                "Inventario actual en la mochila - " + str(state["mochila"]) + ".\n"
                "Genera la consecuencia del turno en el idioma - " + idioma_completo + "."
            )
        else:
            prompt_usuario = (
                "The player has chosen the option - '" + opcion_elegida + "'.\n"
                "The result of the d20 dice roll is - " + str(dado) + ".\n"
                "Current backpack inventory - " + str(state["mochila"]) + ".\n"
                "Generate the turn consequence in the language - " + idioma_completo + "."
            )
        
        messages.append({"role": "user", "content": prompt_usuario})
        
        print(COLOR_MENU + TEXT_INTERFACE[lang]["destiny"] + COLOR_RESET)
        try:
            respuesta_cruda = call_gpt(messages)
            respuesta = process_response(respuesta_cruda, lang)
        except Exception as e:
            respuesta = process_response("", lang)
            
        # Update player state based on parsed model response
        narrativa_actual = respuesta.get("narrativa", "Continuas tu camino." if lang == "es" else "You continue on your path.")
        opciones_actuales = respuesta.get("opciones", ["Seguir adelante" if lang == "es" else "Go forward"])
        
        cambio = respuesta.get("cambio_vida", 0)
        state["hp"] += cambio
        if state["hp"] > 100:
            state["hp"] = 100
            
        if cambio < 0:
            print()
            print(COLOR_DAMAGE + wrap(TEXT_INTERFACE[lang]["damage_alert"].format(damage=abs(cambio))) + COLOR_RESET)
        elif cambio > 0:
            print()
            print(COLOR_NARRATIVE + wrap(TEXT_INTERFACE[lang]["heal_alert"].format(heal=cambio)) + COLOR_RESET)

        item = respuesta.get("item_encontrado")
        if item and item.lower() != "null" and item.lower() != "none":
            # Cap backpack at 10 items to keep status bar readable
            if len(state["mochila"]) >= 10:
                state["mochila"].pop(0)
                print(COLOR_STATUS + wrap(TEXT_INTERFACE[lang]["backpack_full"]) + COLOR_RESET)
            state["mochila"].append(item)
            state["oro"] += 5
            print()
            print(COLOR_STATUS + wrap(TEXT_INTERFACE[lang]["loot_alert"].format(item=item)) + COLOR_RESET)
            
        state["turnos"] += 1
        
        # Check if the AI signals a story victory
        if respuesta.get("victoria"):
            print()
            print(divider())
            print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["victory_title"] + COLOR_RESET)
            print()
            print(COLOR_NARRATIVE + wrap(TEXT_INTERFACE[lang]["victory_desc"]) + COLOR_RESET)
            print()
            print(divider())
            print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["thanks"] + COLOR_RESET)
            print(COLOR_CREDITS + TEXT_INTERFACE[lang]["credits"] + COLOR_RESET)
            break
        
    # End of game state
    if state["hp"] <= 0:
        print()
        print(divider("═", COLOR_DAMAGE))
        print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["game_over_title"] + COLOR_RESET)
        print()
        print(COLOR_DAMAGE + wrap(TEXT_INTERFACE[lang]["game_over_desc"]) + COLOR_RESET)
        print()
        print(divider("═", COLOR_DAMAGE))
        print(COLOR_CREDITS + TEXT_INTERFACE[lang]["credits"] + COLOR_RESET)

if __name__ == "__main__":
    main()
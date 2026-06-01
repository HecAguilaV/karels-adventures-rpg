import json
import random
import os
from ai import call_gpt

# ANSI color definitions for the console
COLOR_NARRATIVE = "\033[94m"
COLOR_DAMAGE = "\033[91m"
COLOR_STATUS = "\033[93m"
COLOR_MENU = "\033[95m"
COLOR_RESET = "\033[0m"

# Translation matrix for local i18n interface
TEXT_INTERFACE = {
    "en": {
        "welcome": "             INFINITE STORY RPG                   ",
        "status_bar": "[STATUS] HP - {hp} | Gold - {gold} | Turn - {turn}",
        "backpack_title": "BACKPACK",
        "backpack_empty": "(empty)",
        "options_title": "=== OPTIONS ===",
        "exit_instruction": "Type 'salir' or 'exit' to end the game.",
        "input_prompt": "What do you decide to do? ",
        "invalid_option": "Invalid option. Try again.",
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
        "thanks": "Thanks for playing. See you next time!",
        "selecting_story": "=== SELECT YOUR STORY ===",
        "story_prompt": "Select the story number: ",
        "invalid_story": "Invalid selection. Try again.",
        "number_prompt": "Please enter a valid number.",
        "loading_err": "Error loading file. Loading default forest story."
    },
    
    "es": {
        "welcome": "             INFINITE STORY RPG                   ",
        "status_bar": "[ESTADO] HP - {hp} | Oro - {gold} | Turno - {turn}",
        "backpack_title": "MOCHILA",
        "backpack_empty": "(vacia)",
        "options_title": "=== OPCIONES ===",
        "exit_instruction": "Escribe 'salir' para terminar el juego.",
        "input_prompt": "¿Que decides hacer? ",
        "invalid_option": "Opcion no valida. Intenta de nuevo.",
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
        "thanks": "Gracias por jugar. ¡Hasta la proxima!",
        "selecting_story": "=== SELECCIONA TU HISTORIA ===",
        "story_prompt": "Selecciona el numero de la historia: ",
        "invalid_story": "Seleccion invalida. Intenta de nuevo.",
        "number_prompt": "Por favor introduce un numero valido.",
        "loading_err": "Error al cargar el archivo. Cargando bosque por defecto."
    }
}

# Friendly display names mapping for story json files
STORY_DISPLAY_NAMES = {
    "original_small": {
        "en": "Original Adventure (Short)",
        "es": "Aventura Original (Corta)"
    },
    "original_big": {
        "en": "Original Adventure (Full Campaign)",
        "es": "Aventura Original (Campaña Completa)"
    },
    "engineer_story": {
        "en": "Karel the Robot - Debug Mission",
        "es": "Karel el Robot - Mision de Depuracion"
    }
}

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
    posibles_rutas = [".", "data", "Infinite Story", "Infinite Story/data"]
    archivos_json = []
    
    # Traverse suggested directories to locate valid folders
    for ruta in posibles_rutas:
        if os.path.exists(ruta) and os.path.isdir(ruta):
            # Iterate over files in each folder to collect JSON files
            for archivo in os.listdir(ruta):
                if archivo.endswith(".json"):
                    ruta_completa = os.path.join(ruta, archivo)
                    if ruta_completa not in archivos_json:
                        archivos_json.append(ruta_completa)
                        
    # Deduplicate files based on their base filename
    archivos_unicos = {}
    # Iterate over found JSON files to process base names
    for ruta in archivos_json:
        nombre_base = os.path.basename(ruta)
        # Prioritize paths in data directory or root over subfolders
        if nombre_base not in archivos_unicos:
            archivos_unicos[nombre_base] = ruta
        else:
            if "data" in ruta or "./" in ruta:
                archivos_unicos[nombre_base] = ruta
                
    lista_final = sorted(list(archivos_unicos.values()), key=lambda r: os.path.basename(r))
    
    if not lista_final:
        # Fallback in case no story JSON files are found
        default_data = {
            "plot": "Exploras un bosque misterioso.",
            "scenes": {
                "start": {
                    "text": "Estás al borde de un bosque oscuro.",
                    "choices": [
                        {"text": "Entrar al bosque", "scene_key": "bosque"},
                        {"text": "Volver a la aldea", "scene_key": "aldea"}
                    ]
                }
            }
        }
        return default_data, "default_story"
        
    print(COLOR_MENU + TEXT_INTERFACE[lang]["selecting_story"] + COLOR_RESET)
    # Display the list of available story files to the user
    for i, ruta in enumerate(lista_final):
        nombre_sin_ext = os.path.splitext(os.path.basename(ruta))[0]
        # Get the translated friendly name or format original filename
        if nombre_sin_ext in STORY_DISPLAY_NAMES:
            nombre_mostrar = STORY_DISPLAY_NAMES[nombre_sin_ext][lang]
        else:
            nombre_mostrar = nombre_sin_ext.replace("_", " ").title()
        print(COLOR_MENU + str(i + 1) + ". " + nombre_mostrar + COLOR_RESET)
        
    seleccion = -1
    # Loop to ensure user selects a valid story index number
    while seleccion < 0 or seleccion >= len(lista_final):
        entrada = input(COLOR_MENU + TEXT_INTERFACE[lang]["story_prompt"] + COLOR_RESET).strip()
        if entrada.isdigit():
            seleccion = int(entrada) - 1
            if seleccion < 0 or seleccion >= len(lista_final):
                print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["invalid_story"] + COLOR_RESET)
        else:
            if entrada.lower() in ["salir", "exit"]:
                print("Saliendo...")
                exit()
            print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["number_prompt"] + COLOR_RESET)
            
    ruta_seleccionada = lista_final[seleccion]
    try:
        with open(ruta_seleccionada, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data, os.path.splitext(os.path.basename(ruta_seleccionada))[0]
    except Exception as e:
        # Fallback if file reading fails
        print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["loading_err"] + COLOR_RESET)
        return {
            "plot": "Exploras un bosque misterioso.",
            "scenes": {
                "start": {
                    "text": "Estás al borde de un bosque oscuro.",
                    "choices": [
                        {"text": "Entrar al bosque", "scene_key": "bosque"},
                        {"text": "Volver a la aldea", "scene_key": "aldea"}
                    ]
                }
            }
        }, "default_story"

def roll_d20():
    # Pre-condition - None
    # Post-condition - returns a random integer between 1 and 20
    return random.randint(1, 20)

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
            
    # Welcome screen banner
    print(COLOR_NARRATIVE + "==================================================" + COLOR_RESET)
    print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["welcome"] + COLOR_RESET)
    print(COLOR_NARRATIVE + "==================================================" + COLOR_RESET)
    
    # Main game loop keeping session alive while player HP is positive
    while state["hp"] > 0:
        # Display current player status bar
        status_bar = (
            "\n" + COLOR_STATUS +
            TEXT_INTERFACE[lang]["status_bar"].format(
                hp=state["hp"],
                gold=state["oro"],
                turn=state["turnos"]
            ) + COLOR_RESET
        )
        print(status_bar)
        
        # Display formatted backpack grid below the status bar
        backpack_display = format_backpack(state["mochila"], lang)
        # Print each line of the backpack grid with color
        for bp_line in backpack_display.split("\n"):
            print(COLOR_STATUS + bp_line + COLOR_RESET)
        
        # Display current narrative text
        print("\n" + COLOR_NARRATIVE + narrativa_actual + COLOR_RESET)
        
        # Append current narrative to messages history
        messages.append({"role": "assistant", "content": narrativa_actual})
        
        # Display option choices
        print("\n" + COLOR_MENU + TEXT_INTERFACE[lang]["options_title"] + COLOR_RESET)
        # Print options from the current scene in numbered format
        for i, opcion in enumerate(opciones_actuales):
            print(COLOR_MENU + str(i + 1) + ". " + opcion + COLOR_RESET)
        print(COLOR_MENU + TEXT_INTERFACE[lang]["exit_instruction"] + COLOR_RESET)
        
        entrada = ""
        # Ensure user inputs a non-empty action string
        while not entrada:
            entrada = input("\n" + TEXT_INTERFACE[lang]["input_prompt"]).strip()
            
        # Validate user input to exit
        if entrada.lower() in ["salir", "exit"]:
            print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["thanks"] + COLOR_RESET)
            break
            
        # Validate numeric option selection
        seleccion = -1
        if entrada.isdigit():
            seleccion = int(entrada) - 1
            
        if seleccion < 0 or seleccion >= len(opciones_actuales):
            print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["invalid_option"] + COLOR_RESET)
            messages.pop()
            continue
            
        opcion_elegida = opciones_actuales[seleccion]
        
        # Roll d20 dice
        dado = roll_d20()
        print(COLOR_STATUS + "\n" + TEXT_INTERFACE[lang]["dice_roll"].format(roll=dado) + COLOR_RESET)
        
        # Inject dice, choice, and backpack context into user prompt
        prompt_usuario = (
            "El jugador ha elegido la opcion - '" + opcion_elegida + "'.\n"
            "El resultado de la tirada del dado d20 es - " + str(dado) + ".\n"
            "Inventario actual en la mochila - " + str(state["mochila"]) + ".\n"
            "Genera la consecuencia del turno en el idioma - " + idioma_completo + "."
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
            print(COLOR_DAMAGE + "\n" + TEXT_INTERFACE[lang]["damage_alert"].format(damage=abs(cambio)) + COLOR_RESET)
        elif cambio > 0:
            print(COLOR_NARRATIVE + "\n" + TEXT_INTERFACE[lang]["heal_alert"].format(heal=cambio) + COLOR_RESET)
            
        item = respuesta.get("item_encontrado")
        if item and item.lower() != "null" and item.lower() != "none":
            # Cap backpack at 10 items to keep status bar readable
            if len(state["mochila"]) >= 10:
                state["mochila"].pop(0)
                print(COLOR_STATUS + TEXT_INTERFACE[lang]["backpack_full"] + COLOR_RESET)
            state["mochila"].append(item)
            state["oro"] += 5
            print(COLOR_STATUS + "\n" + TEXT_INTERFACE[lang]["loot_alert"].format(item=item) + COLOR_RESET)
            
        state["turnos"] += 1
        
        # Check if the AI signals a story victory
        if respuesta.get("victoria"):
            print("\n" + COLOR_NARRATIVE + "==================================================" + COLOR_RESET)
            print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["victory_title"] + COLOR_RESET)
            print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["victory_desc"] + COLOR_RESET)
            print(COLOR_NARRATIVE + "==================================================" + COLOR_RESET)
            print(COLOR_NARRATIVE + TEXT_INTERFACE[lang]["thanks"] + COLOR_RESET)
            break
        
    # End of game state
    if state["hp"] <= 0:
        print("\n" + COLOR_DAMAGE + "==================================================" + COLOR_RESET)
        print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["game_over_title"] + COLOR_RESET)
        print(COLOR_DAMAGE + TEXT_INTERFACE[lang]["game_over_desc"] + COLOR_RESET)
        print(COLOR_DAMAGE + "==================================================" + COLOR_RESET)

if __name__ == "__main__":
    main()
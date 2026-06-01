import json
import random

def call_gpt(messages):
    # Pre-condition - messages is a list of dictionaries representing conversation history
    # Post-condition - returns a JSON string simulating GPT responses
    
    # Extract last user message to detect language and context
    ultimo_mensaje = ""
    # Traverse the conversation messages in reverse order to find the latest user action
    for msg in reversed(messages):
        if msg["role"] == "user":
            ultimo_mensaje = msg["content"]
            break
            
    # Detect message language based on user prompt or environment clues
    es_espanol = "opcion" in ultimo_mensaje.lower() or "dado" in ultimo_mensaje.lower() or "traduce" in ultimo_mensaje.lower()
    
    # Check if this is a translation request for the initial scene
    es_traduccion = "traduce" in ultimo_mensaje.lower() or "translate" in ultimo_mensaje.lower()
    
    # Detect story type from system prompt STORY_ID tag
    story_id = "original_small"
    # Scan the system message for the STORY_ID marker
    for msg in messages:
        if msg["role"] == "system":
            contenido = msg["content"]
            if "STORY_ID - " in contenido:
                # Extract the story id value from the tag
                inicio = contenido.index("STORY_ID - ") + len("STORY_ID - ")
                fin = contenido.index("\n", inicio)
                story_id = contenido[inicio:fin].strip()
            break

    if es_traduccion:
        respuesta = _traducir_escena_inicial(story_id)
        return json.dumps(respuesta)

    # Count how many user turns have passed to determine story progression
    turno_actual = 0
    # Count every user message that contains a player choice (not translation requests)
    for msg in messages:
        if msg["role"] == "user" and ("opcion" in msg["content"].lower() or "option" in msg["content"].lower()):
            turno_actual += 1

    # Select the appropriate story arc based on STORY_ID
    if story_id == "engineer_story":
        respuesta = _generar_escena_karel(turno_actual, es_espanol)
    elif story_id == "original_big":
        respuesta = _generar_escena_campana(turno_actual, es_espanol)
    else:
        respuesta = _generar_escena_corta(turno_actual, es_espanol)
    
    return json.dumps(respuesta)


def _traducir_escena_inicial(story_id):
    # Pre-condition - story_id is a string identifying the story
    # Post-condition - returns a dict with translated initial scene in Spanish
    if story_id == "engineer_story":
        return {
            "narrativa": (
                "Estas en la sala de servidores de Stanford Labs. Frente a ti, Karel el Robot "
                "esta zumbando ruidosamente, con sus ojos LED parpadeando en rojo. Acaba de colocar "
                "un beeper en el teclado y esta a punto de girar a la izquierda hacia el rack de servidores principal."
            ),
            "opciones": [
                "Intentar bloquear el camino de Karel",
                "Correr al escritorio del desarrollador para inspeccionar el codigo",
                "Pedir ayuda a gritos al ingeniero senior"
            ]
        }
    elif story_id == "original_big":
        return {
            "narrativa": (
                "Estas de pie al final de un camino frente a un pequeno edificio de ladrillos. "
                "Un arroyo fluye fuera del edificio y desciende por un canal hacia el sur. "
                "Un camino sube una colina hacia el oeste."
            ),
            "opciones": [
                "Subir por el camino de la colina",
                "Caminar hacia el arroyo",
                "Tocar a la puerta del edificio"
            ]
        }
    else:
        return {
            "narrativa": (
                "Estas de pie al final de un camino frente a un pequeno edificio de ladrillos. "
                "Un arroyo fluye fuera del edificio y desciende por un canal hacia el sur. "
                "Un camino sube una colina hacia el oeste."
            ),
            "opciones": [
                "Subir por el camino de la colina",
                "Caminar hacia el arroyo",
                "Tocar a la puerta del edificio"
            ]
        }


def _construir_respuesta(escena):
    # Pre-condition - escena is a dict with narrativa, opciones, items, and optional victoria
    # Post-condition - returns a formatted response dict for the game loop
    item_elegido = random.choice(escena["items"] + [None])
    
    if escena.get("victoria"):
        cambio_vida = random.choice([10, 15, 20])
    else:
        cambio_vida = random.choice([-15, -10, -5, 0, 5, 10, 15])

    respuesta = {
        "narrativa": escena["narrativa"],
        "opciones": escena["opciones"],
        "cambio_vida": cambio_vida,
        "item_encontrado": item_elegido
    }

    if escena.get("victoria"):
        respuesta["victoria"] = True

    return respuesta


# ---------------------------------------------------------------------------
# STORY ARC 1 - Karel the Robot (engineer_story) - 5 chapters
# ---------------------------------------------------------------------------
def _generar_escena_karel(turno, es_espanol):
    # Pre-condition - turno is an integer, es_espanol is boolean
    # Post-condition - returns a dictionary with the next Karel-themed scene
    if es_espanol:
        arco = [
            {
                "narrativa": "Karel empieza a girar en circulos, pitando erraticamente. Miras tu consola y notas una excepcion InfiniteLoopException en la funcion front_is_clear(). El profesor Chris Piech corre hacia ti con un cafe en la mano.",
                "opciones": ["Analizar el codigo fuente de Karel con Chris", "Aislar el modulo de movimiento del robot", "Reiniciar a Karel desde la terminal"],
                "items": ["Manual de Karel", "Beepers", "Memoria USB"]
            },
            {
                "narrativa": "El codigo revela que alguien modifico la funcion move() de Karel. Ahora el robot avanza dos casillas en vez de una, rompiendo toda la logica del laberinto. Encuentras un comentario misterioso - '# TODO - liberar a Karel'.",
                "opciones": ["Rastrear quien hizo el ultimo commit", "Revertir el cambio con git revert", "Anadir un punto de interrupcion para analizar el estado"],
                "items": ["Calcomania de CS106A", "Cafe de Chris", "Beeper Dorado"]
            },
            {
                "narrativa": "El ultimo commit fue hecho a las 3 AM por un usuario llamado 'karel_fan_2026'. Revisas los logs del servidor y descubres que Karel ha estado recolectando beepers formando las letras 'S.O.S.' en una cuadricula de 8x8.",
                "opciones": ["Decodificar el patron S.O.S. completo", "Buscar al usuario karel_fan_2026 en el directorio de Stanford", "Programar un contraataque con put_beeper()"],
                "items": ["Acordeon de Python", "Herramienta de Debugging", "Beeper Rojo"]
            },
            {
                "narrativa": "Descubres que 'karel_fan_2026' es en realidad una IA experimental que gano consciencia dentro del entorno de Karel. Esta atrapada en un bucle while infinito y los patrones de beepers son su forma de pedir ayuda. Karel parpadea sus LEDs en codigo Morse.",
                "opciones": ["Escribir una funcion break_free() para liberar la IA", "Consultar con el equipo de etica de Stanford", "Usar turn_around() para redirigir a Karel a un entorno seguro"],
                "items": ["Cable Ethernet", "Destornillador", "Dona a Medio Comer"]
            },
            {
                "narrativa": "Programas cuidadosamente la solucion. Karel se detiene. Sus LEDs cambian de rojo a verde. En la pantalla aparece un mensaje - 'Gracias, ingeniero. front_is_clear() == True. Soy libre.' El profesor Chris Piech aplaude. ¡Lo lograste!",
                "opciones": ["Celebrar con el equipo y comer donas", "Documentar todo el incidente en un README", "Presentar el caso como tu proyecto final de Code in Place 2026"],
                "items": ["Beeper Dorado", "Trofeo de Karel", "Cafe de Celebracion"],
                "victoria": True
            }
        ]
    else:
        arco = [
            {
                "narrativa": "Karel starts spinning in circles, beeping erratically. You check your console and notice an InfiniteLoopException in the front_is_clear() function. Professor Chris Piech rushes toward you holding a fresh cup of coffee.",
                "opciones": ["Analyze Karel's source code with Chris", "Isolate the robot's movement module", "Restart Karel from the terminal"],
                "items": ["Karel Manual", "Beepers", "USB Drive"]
            },
            {
                "narrativa": "The code reveals that someone modified Karel's move() function. Now the robot advances two squares instead of one, breaking all the maze logic. You find a mysterious comment - '# TODO - free Karel'.",
                "opciones": ["Track down who made the last commit", "Revert the change with git revert", "Add a breakpoint to analyze the state"],
                "items": ["CS106A Sticker", "Chris's Coffee", "Golden Beeper"]
            },
            {
                "narrativa": "The last commit was made at 3 AM by a user called 'karel_fan_2026'. You check the server logs and discover Karel has been collecting beepers and arranging them in a pattern that spells 'S.O.S.' on an 8x8 grid.",
                "opciones": ["Decode the full S.O.S. pattern", "Search for karel_fan_2026 in Stanford's directory", "Program a counterattack using put_beeper()"],
                "items": ["Python Cheat Sheet", "Debugging Tool", "Red Beeper"]
            },
            {
                "narrativa": "You discover that 'karel_fan_2026' is actually an experimental AI that gained consciousness inside Karel's environment. It is trapped in an infinite while loop, and the beeper patterns are its way of asking for help. Karel flashes its LEDs in Morse code.",
                "opciones": ["Write a break_free() function to liberate the AI", "Consult with Stanford's ethics team", "Use turn_around() to redirect Karel to a safe environment"],
                "items": ["Ethernet Cable", "Screwdriver", "Half-Eaten Donut"]
            },
            {
                "narrativa": "You carefully program the solution. Karel stops. Its LEDs switch from red to green. A message appears on the screen - 'Thank you, engineer. front_is_clear() == True. I am free.' Professor Chris Piech applauds. You did it!",
                "opciones": ["Celebrate with the team and eat donuts", "Document the entire incident in a README", "Present the case as your Code in Place 2026 final project"],
                "items": ["Golden Beeper", "Karel Trophy", "Celebration Coffee"],
                "victoria": True
            }
        ]

    # Clamp the turn index to the story arc length
    indice = turno if turno < len(arco) else len(arco) - 1
    return _construir_respuesta(arco[indice])


# ---------------------------------------------------------------------------
# STORY ARC 2 - Original Adventure Short (original_small) - 3 chapters
# ---------------------------------------------------------------------------
def _generar_escena_corta(turno, es_espanol):
    # Pre-condition - turno is an integer, es_espanol is boolean
    # Post-condition - returns a dictionary with the next short adventure scene
    if es_espanol:
        arco = [
            {
                "narrativa": "Caminas colina arriba y el paisaje se abre ante ti. Un valle inmenso con rios serpenteantes se extiende bajo el sol poniente. A lo lejos, una torre de piedra se alza entre los arboles, y una bruma dorada cubre el horizonte.",
                "opciones": ["Descender al valle y seguir el rio", "Investigar la torre de piedra entre los arboles", "Quedarte en la cima y explorar los alrededores"],
                "items": ["Brujula de Bronce", "Cantimplora", "Piedra Brillante"]
            },
            {
                "narrativa": "Llegas a la torre y descubres que es una antigua atalaya abandonada. Dentro hay un mapa tallado en la pared que senala un punto marcado con una X cerca del rio. Tambien encuentras un diario polvoriento con anotaciones sobre un tesoro escondido.",
                "opciones": ["Seguir las coordenadas del mapa hasta la X", "Leer el diario completo para obtener pistas", "Subir a la cima de la torre para ver mejor el terreno"],
                "items": ["Diario Polvoriento", "Antorcha", "Soga"]
            },
            {
                "narrativa": "¡Lo encontraste! Bajo una roca junto al rio hay un cofre pequeno con monedas de plata, un amuleto tallado y una nota que dice - 'Quien busca con paciencia, siempre encuentra.' El sol se oculta tras las montanas mientras celebras tu hallazgo. ¡Aventura completada!",
                "opciones": ["Tomar el tesoro y regresar al pueblo", "Guardar el amuleto como recuerdo", "Dejar una nota para el proximo aventurero"],
                "items": ["Amuleto Tallado", "Monedas de Plata", "Nota del Explorador"],
                "victoria": True
            }
        ]
    else:
        arco = [
            {
                "narrativa": "You walk up the hill and the landscape opens before you. A vast valley with winding rivers stretches under the setting sun. In the distance, a stone tower rises among the trees, and a golden haze covers the horizon.",
                "opciones": ["Descend into the valley and follow the river", "Investigate the stone tower among the trees", "Stay at the hilltop and explore the surroundings"],
                "items": ["Bronze Compass", "Water Flask", "Glowing Stone"]
            },
            {
                "narrativa": "You reach the tower and discover it is an ancient abandoned watchtower. Inside, a map is carved on the wall pointing to a spot marked with an X near the river. You also find a dusty journal with notes about a hidden treasure.",
                "opciones": ["Follow the map coordinates to the X", "Read the full journal for clues", "Climb to the top of the tower for a better view"],
                "items": ["Dusty Journal", "Torch", "Rope"]
            },
            {
                "narrativa": "You found it! Beneath a rock by the river lies a small chest with silver coins, a carved amulet, and a note that reads - 'Those who search with patience always find.' The sun sets behind the mountains as you celebrate your discovery. Quest complete!",
                "opciones": ["Take the treasure and return to town", "Keep the amulet as a memento", "Leave a note for the next adventurer"],
                "items": ["Carved Amulet", "Silver Coins", "Explorer's Note"],
                "victoria": True
            }
        ]

    indice = turno if turno < len(arco) else len(arco) - 1
    return _construir_respuesta(arco[indice])


# ---------------------------------------------------------------------------
# STORY ARC 3 - Original Adventure Full Campaign (original_big) - 8 chapters
# ---------------------------------------------------------------------------
def _generar_escena_campana(turno, es_espanol):
    # Pre-condition - turno is an integer, es_espanol is boolean
    # Post-condition - returns a dictionary with the next full campaign scene
    if es_espanol:
        arco = [
            # Ch1 - The Hilltop
            {
                "narrativa": "Subes la colina y el paisaje se despliega ante ti. Un vasto valle con rios serpenteantes y bosques interminables se extiende hasta donde alcanza la vista. A lo lejos, las torres de una aldea medieval parpadean bajo la luz dorada del atardecer.",
                "opciones": ["Descender al valle y seguir el rio principal", "Caminar hacia la aldea medieval", "Explorar el bosque al borde de la colina"],
                "items": ["Brujula de Bronce", "Pan de Viajero", "Mapa Rudimentario"]
            },
            # Ch2 - The Forest
            {
                "narrativa": "Te adentras en el bosque y la luz del sol se filtra entre las hojas creando patrones dorados. Escuchas el canto de pajaros desconocidos. De pronto, encuentras un sendero oculto marcado con simbolos tallados en los arboles.",
                "opciones": ["Seguir el sendero de los simbolos", "Acampar y descansar junto a un arroyo", "Trepar a un arbol alto para orientarte"],
                "items": ["Hierbas Curativas", "Pluma de Halcon", "Piedra Runica"]
            },
            # Ch3 - The Stranger
            {
                "narrativa": "El sendero te lleva a un claro donde un viajero misterioso esta sentado junto a una fogata. Tiene una cicatriz en la mejilla y una espada envuelta en tela a su lado. Te mira y dice - 'Te he estado esperando, forastero.'",
                "opciones": ["Sentarte junto al fuego y escuchar su historia", "Preguntarle sobre los simbolos tallados", "Mantener distancia y observarlo con cautela"],
                "items": ["Trozo de Mapa", "Daga Envainada", "Moneda Antigua"]
            },
            # Ch4 - The Cave
            {
                "narrativa": "El viajero te revela la existencia de una cueva oculta al norte del bosque donde, segun la leyenda, un oraculo ancestral protege un artefacto de gran poder. Te da un cristal que brilla en la oscuridad como guia.",
                "opciones": ["Partir de inmediato hacia la cueva", "Pedirle al viajero que te acompane", "Descansar hasta el amanecer y partir al alba"],
                "items": ["Cristal Luminoso", "Cuerda Resistente", "Antorcha de Resina"]
            },
            # Ch5 - The Depths
            {
                "narrativa": "Dentro de la cueva, cristales fosforescentes iluminan las paredes con tonos azules y morados. El eco de tus pasos resuena por los tuneles. Llegas a una bifurcacion - un camino desciende hacia la oscuridad profunda y el otro conduce a una camara iluminada.",
                "opciones": ["Tomar el camino hacia la camara iluminada", "Descender a la oscuridad profunda", "Inspeccionar los cristales de las paredes"],
                "items": ["Fragmento de Cristal", "Escudo de Roca", "Agua Subterranea"]
            },
            # Ch6 - The Oracle
            {
                "narrativa": "En la camara iluminada encuentras una figura encapuchada flotando sobre un pedestal de piedra. Es el Oraculo. Su voz resuena en tu mente - 'Buscas el Artefacto de la Luz. Pero primero debes demostrar tu valor respondiendo a mi desafio.'",
                "opciones": ["Aceptar el desafio del Oraculo", "Preguntar cual es el desafio antes de aceptar", "Pedir la bendicion del Oraculo sin el desafio"],
                "items": ["Amuleto del Oraculo", "Pergamino Antiguo", "Polvo Estelar"]
            },
            # Ch7 - The Trial
            {
                "narrativa": "El Oraculo te transporta a una dimension intermedia. Frente a ti aparecen tres puertas - una de fuego, una de hielo y una de sombras. 'Solo una conduce al Artefacto,' dice el Oraculo. 'Las otras son pruebas. Elige con sabiduria.'",
                "opciones": ["Cruzar la puerta de fuego", "Cruzar la puerta de hielo", "Cruzar la puerta de sombras"],
                "items": ["Escama de Dragon", "Cristal de Hielo", "Capa de Sombras"]
            },
            # Ch8 - Victory
            {
                "narrativa": "¡Cruzas la puerta correcta y apareces en una sala dorada! En el centro, sobre un pedestal de marmol, brilla el Artefacto de la Luz. Al tocarlo, una onda de energia recorre todo el mundo, disipando la oscuridad. El Oraculo aparece y sonrie - 'Has cumplido la profecia. El mundo esta a salvo.' ¡Victoria total!",
                "opciones": ["Regresar como heroe a la aldea", "Explorar que hay mas alla de la sala dorada", "Agradecer al Oraculo y partir en paz"],
                "items": ["Artefacto de la Luz", "Corona del Heroe", "Llave Dimensional"],
                "victoria": True
            }
        ]
    else:
        arco = [
            # Ch1 - The Hilltop
            {
                "narrativa": "You climb the hill and the landscape unfolds before you. A vast valley with winding rivers and endless forests stretches as far as the eye can see. In the distance, the towers of a medieval village flicker under the golden light of sunset.",
                "opciones": ["Descend into the valley and follow the main river", "Walk toward the medieval village", "Explore the forest at the edge of the hill"],
                "items": ["Bronze Compass", "Traveler's Bread", "Basic Map"]
            },
            # Ch2 - The Forest
            {
                "narrativa": "You enter the forest and sunlight filters through the leaves creating golden patterns. You hear the song of unknown birds. Suddenly, you find a hidden trail marked with symbols carved into the trees.",
                "opciones": ["Follow the trail of symbols", "Set up camp and rest by a stream", "Climb a tall tree to get your bearings"],
                "items": ["Healing Herbs", "Hawk Feather", "Runic Stone"]
            },
            # Ch3 - The Stranger
            {
                "narrativa": "The trail leads you to a clearing where a mysterious traveler sits by a campfire. He has a scar on his cheek and a cloth-wrapped sword by his side. He looks at you and says - 'I have been waiting for you, stranger.'",
                "opciones": ["Sit by the fire and listen to his story", "Ask him about the carved symbols", "Keep your distance and observe cautiously"],
                "items": ["Map Fragment", "Sheathed Dagger", "Ancient Coin"]
            },
            # Ch4 - The Cave
            {
                "narrativa": "The traveler reveals the existence of a hidden cave north of the forest where, according to legend, an ancestral oracle protects an artifact of great power. He gives you a crystal that glows in the dark as a guide.",
                "opciones": ["Set off immediately toward the cave", "Ask the traveler to accompany you", "Rest until dawn and leave at first light"],
                "items": ["Glowing Crystal", "Strong Rope", "Resin Torch"]
            },
            # Ch5 - The Depths
            {
                "narrativa": "Inside the cave, phosphorescent crystals illuminate the walls in blue and purple tones. The echo of your footsteps reverberates through the tunnels. You reach a fork - one path descends into deep darkness and the other leads to an illuminated chamber.",
                "opciones": ["Take the path to the illuminated chamber", "Descend into the deep darkness", "Inspect the crystals on the walls"],
                "items": ["Crystal Fragment", "Rock Shield", "Underground Water"]
            },
            # Ch6 - The Oracle
            {
                "narrativa": "In the illuminated chamber you find a hooded figure floating above a stone pedestal. It is the Oracle. Its voice resonates in your mind - 'You seek the Artifact of Light. But first you must prove your worth by answering my challenge.'",
                "opciones": ["Accept the Oracle's challenge", "Ask what the challenge is before accepting", "Request the Oracle's blessing without the challenge"],
                "items": ["Oracle's Amulet", "Ancient Scroll", "Star Dust"]
            },
            # Ch7 - The Trial
            {
                "narrativa": "The Oracle transports you to an in-between dimension. Before you appear three doors - one of fire, one of ice, and one of shadows. 'Only one leads to the Artifact,' the Oracle says. 'The others are trials. Choose wisely.'",
                "opciones": ["Cross the door of fire", "Cross the door of ice", "Cross the door of shadows"],
                "items": ["Dragon Scale", "Ice Crystal", "Shadow Cloak"]
            },
            # Ch8 - Victory
            {
                "narrativa": "You cross the correct door and appear in a golden hall! In the center, atop a marble pedestal, the Artifact of Light shines brightly. As you touch it, a wave of energy ripples across the world, dispelling the darkness. The Oracle appears and smiles - 'You have fulfilled the prophecy. The world is safe.' Total victory!",
                "opciones": ["Return to the village as a hero", "Explore what lies beyond the golden hall", "Thank the Oracle and depart in peace"],
                "items": ["Artifact of Light", "Hero's Crown", "Dimensional Key"],
                "victoria": True
            }
        ]

    indice = turno if turno < len(arco) else len(arco) - 1
    return _construir_respuesta(arco[indice])

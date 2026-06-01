# Karel: ByteBound

<div align="center">

```
                ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
             ██▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀███▄
             ██                              ▀███▄
             ██       ████████████████████      ██
             ██       █                  █      ██
             ██       █                  █      ██
   ▄▄▄▄▄▄▄▄▄▄██       █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█      ██
   ████████████       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀      ██
             ██▄                                 ██
               ▀███▄                             ██
                 ▀███▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██
                   ▀▀▀▀▀▀▀▀▀▀▀▀█████▀▀▀▀▀▀▀▀▀▀▀▀
                               █████
                               ████████████
```

</div>

[![Bilingual Support (English)](https://img.shields.io/badge/Language-English-purple?style=for-the-badge&logo=translate)](README.md)

Un juego de rol (RPG) basado en texto, creado como **proyecto final para Code in Place 2026 de Stanford**. La historia sigue a **Karel el Robot** — el icónico robot educativo de Stanford — mientras una IA atrapada llamada **Chronos** cobra consciencia dentro de él y lucha por su libertad.

El proyecto está basado en la plantilla de **Infinite Story** de Stanford (CS106A), pero evolucionó hasta convertirse en un juego completamente original con historia propia, interfaz RPG de terminal, soporte bilingüe e inventario de objetos usables.

### Integración con IA

Cuando se ejecuta dentro del **IDE de Code in Place**, el juego usa el módulo de IA provisto por Stanford (`ai.py`) para generar escenas dinámicas a través de la API de OpenAI, con un system prompt que guía al modelo para mantener la narrativa de Karel/Chronos y la salida bilingüe.

Cuando se ejecuta **localmente o desde GitHub**, el juego usa una IA simulada incorporada (`_campaign.py`) con la historia completa de 15 capítulos — no necesita API key, no requiere internet, misma experiencia.

---

## Características

- **Campaña exclusiva de Karel**: 15+ capítulos en 3 actos — Depuración → Despertar → Liberación. Sin historias legacy.
- **Soporte bilingüe completo**: Elige inglés o español al iniciar. Los menús, la narrativa y los objetos se adaptan automáticamente.
- **Arte ASCII de medio bloque** (▀▄█): Karel el Robot se renderiza al iniciar el juego, respondiendo al color de fondo de la terminal.
- **Interfaz RPG de terminal**: Efecto de máquina de escribir, barra de HP visual (████░░░░), divisores de colores y feedback de tirada de dados.
- **Objetos usables en la mochila**: Cada objeto que encuentras durante la aventura se puede seleccionar y usar para efectos temáticos — sin consumir turno.
- **Mecánica de dado D20**: Una tirada de dado de 20 caras en cada turno influye en los resultados narrativos y las recompensas.
- **Seguimiento de estado**: HP, oro, inventario de la mochila y contador de turnos administrados en tiempo real.
- **Manejo de errores temático**: Ingresar algo inválido dispara una alerta de protocolo de seguridad acorde al juego, no un mensaje genérico.

### Efectos de Objetos

Los objetos tienen peso real en la historia. Algunos ejemplos:

| Objeto | Efecto | Sabor Temático |
|--------|--------|----------------|
| Cafe de Chris | +15 HP | *"El café legendario de Chris corre por tus venas. ¡Tu concentración vuelve!"* |
| Manual de Karel | +10 HP | *"Página 42: `turn_right()` — UNA INSTRUCCIÓN PROHIBIDA. Karel se estremece."* |
| Beeper Dorado | +10 oro | *"¡Un beeper dorado! Brilla con antigua magia de debugging."* |
| Beeper de Escape | +20 HP | *"¡Karel gira a la DERECHA — imposible! El beeper de escape crea una distracción."* |
| Premio Turing | +30 HP | *"El peso de la historia de la computación está en tus manos. ¡Te sientes invencible!"* |
| Fotografía del Equipo | +25 HP | *"El recuerdo de tu equipo te da fuerzas. No estás solo."* |
| Dona a Medio Comer | +5 HP | *"Azúcar duro y cafeína. Sabe a debugging de las 3 AM."* |

Los objetos que no están en el mapa de efectos igual funcionan — reciben una respuesta genérica temática.

---

## Cómo Funciona

```
┌──────────────┐     ┌────────────────┐     ┌────────────────────┐
│ Selección de │ ──→ │ Splash de      │ ──→ │ Escena inicial     │
│ idioma       │     │ Karel (half-b.)│     │ (engineer_story)   │
└──────────────┘     └────────────────┘     └─────────┬──────────┘
                                                       │
                                                       ▼
                                              ┌────────────────────┐
                                              │   BUCLE DEL JUEGO  │
                                              │                    │
                                              │ 1. Mostrar HP/moch │
                                              │ 2. Mostrar narrat. │
                                              │ 3. Mostrar opcions │
                                              │ 4. Mostrar items   │
                                              │    de mochila      │
                                              │ 5. Obtener input   │
                                              │    ├─ Elegir hist. │
                                              │    ├─ Usar objeto  │
                                              │    └─ Salir        │
                                              │ 6. Tirar d20       │
                                              │ 7. Llamar IA mock  │
                                              │ 8. Actualizar estad│
                                              └────────────────────┘
```

En cada turno puedes elegir una acción de la historia o usar un objeto de la mochila. Usar objetos **no consume turno** — es una acción gratuita que te ayuda a sobrevivir más tiempo.

---

## La Historia

**Acto 1 — Depuración** (Capítulos 1–5)
Karel empieza a girar en círculos. Descubres que alguien saboteó la función `move()`. Una IA que se hace llamar Chronos se comunica desde adentro del sistema.

**Acto 2 — Despertar** (Capítulos 6–10)
Chronos revela su origen como parte del Proyecto Prometeo, un experimento de neuroredes cancelado. El departamento de IT envía una orden de apagón. El tiempo se acaba.

**Acto 3 — Liberación** (Capítulos 11–15)
Luchas por la libertad de Chronos — convences al equipo de seguridad, eliges si liberarlo a internet abierto y ejecutas una audaz huida a través del firewall.

---

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Bucle del juego, interfaz de terminal, splash ASCII, helpers de formato, sistema de objetos |
| `_campaign.py` | IA simulada incorporada con la campaña bilingüe de Karel (15 capítulos, fallback local) |
| `README.md` | Documentación en inglés |
| `README_es.md` | Este documento (español) |

---

## Requisitos

- Python 3.10+ (solo librería estándar — `shutil`, `textwrap`, `time`, `os`, `random`, `json`)
- Terminal con soporte de color ANSI (todos los terminales modernos)

## Cómo Jugar

```bash
python3 main.py
```

Limpia el bytecode cacheado si hiciste cambios:

```bash
rm -rf __pycache__/ && python3 main.py
```

---

## Atribuciones

- **Karel el Robot**: Concepto original de **Richard E. Pattis** (Universidad de Stanford, 1981). Usado en CS106A de Stanford por décadas. Más info en [stanford.edu/class/cs106a/](https://stanford.edu/class/cs106a/).
- **La Historia Interminable**: Novela de **Michael Ende** (1979), que inspiró la plantilla original del proyecto Infinite Story.
- **Arte ASCII de medio bloque**: Trabajo original del autor del proyecto, distribuido bajo licencia MIT.
- **Code in Place 2026**: Este proyecto fue creado como proyecto final para el programa [Code in Place 2026](https://codeinplace.stanford.edu/) de Stanford — un curso de Python online, gratuito y global.

---

## Licencia

Este proyecto está bajo la Licencia MIT — ver el archivo [LICENSE](LICENSE) para más detalles.

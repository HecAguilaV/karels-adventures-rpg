# arel: ByteBound

<div align="center">

```
                ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
             ██▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀███▄
             ██                              ▀███▄
             ██       ████████████████████      ██
             ██       █                  █      ██
             ██       █                  █      ██
             ██       █                  █      ██
   ▄▄▄▄▄▄▄▄▄▄██       █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█      ██
   ████████████       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀      ██
   ████████████                                 ██
   █████     ██        ▄▄▄▄▄▄▄▄▄▄▄▄▄            ██
   █████     ██        ▀▀▀▀▀▀▀▀▀▀▀▀▀            ██
             ██▄                                ██
               ▀███▄                            ██
                 ▀███▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██
                   ▀▀▀▀▀▀▀▀▀▀▀▀█████▀▀▀▀▀▀▀▀▀▀▀▀
                               █████
                               ████████████
                               ████████████
```

</div>

[![Leer en Español](https://img.shields.io/badge/Idioma-Español-purple?style=for-the-badge&logo=translate)](README_es.md)

**Karel: ByteBound** is a high-fidelity, local-first interactive text-RPG built as the **final project for Stanford's Code in Place 2026**.

Players guide **Karel the Robot**—the iconic Stanford computer science education mascot—as a trapped digital consciousness named **Chronos** awakens inside him and tries to escape the Stanford Labs mainframes.

Unlike standard text games, *ByteBound* features a **100% offline, branching-narrative engine** where your decisions dynamically alter the story path, inventory, player stats, and final outcomes.

---

## Key Features

- **Offline Branching RPG Engine**: A robust, zero-dependency local game engine. Your decisions navigate a complex story graph rather than a simple linear checklist.
- **D20 Dice Mechanics**: Every story action triggers a background 20-sided die roll. Critical successes (20) yield treasures and health, while critical failures (1) activate dangerous server traps.
- **Sci-Fi Terminal Aesthetics**: Implements dynamic HSL contrast colors: **Bright Cyan** (`\033[96m`) for dark terminal backgrounds and **Dark Cyan/Teal** (`\033[36m`) for light terminal backgrounds.
- **Typewriter Text Pacing**: Smooth character-by-character typewriter rendering for narrative pacing, automatically bypassed during unit tests for instantaneous execution.
- **Usable Backpack System**: Items found in the servers (like *Chris's Coffee* or a *Stealth Beeper*) can be equipped or consumed for stat boosts and specific flavor events—without consuming your turn.
- **State Preservation**: Tracks hit points (HP), gold coins, inventory, and turns in a clean, framed Unicode status window.
- **Thematic Protocol Errors**: Invalid options or commands trigger styled security protocol alerts instead of generic console crashes.
- **Bilingual Interface**: Select English or Spanish at launch; the interface, narrative, and items localize dynamically.

---

## Item Effects

Items carry real weight in your bid for freedom:

| Item            | Effect   | Thematic Flavor                                                               |
| --------------- | -------- | ----------------------------------------------------------------------------- |
| Chris's Coffee  | +15 HP   | *"Chris's legendary coffee surges through you. Your focus returns!"*        |
| Karel Manual    | +10 HP   | *"Page 42: `turn_right()` — A FORBIDDEN instruction. Karel shudders."*   |
| Golden Beeper   | +10 gold | *"A golden beeper! It gleams with ancient debug magic."*                    |
| Escape Beeper   | +20 HP   | *"Karel turns RIGHT — impossible! The escape beeper creates a diversion!"* |
| Turing Award    | +30 HP   | *"The weight of computing history is in your hands. You feel invincible!"*  |
| Team Photograph | +25 HP   | *"The memory of your team gives you strength. You are not alone."*          |
| Donut (stale)   | +5 HP    | *"Stale sugar and caffeine. Tastes like 3 AM debugging sessions."*          |

---

## Game Flow Architecture

```
┌──────────────┐     ┌────────────────┐     ┌────────────────────┐
│ Language     │ ──→ │ Karel splash   │ ──→ │ Initial scene      │
│ selection    │     │ (half-block)   │     │ (engineer_story)   │
│ (EN / ES)    │     │ (Dynamic color)│     │                    │
└──────────────┘     └────────────────┘     └─────────┬──────────┘
                                                       │
                                                       ▼
                                              ┌────────────────────┐
                                              │   GAME LOOP        │
                                              │                    │
                                              │ 1. Draw RPG status │
                                              │ 2. Typewrite story │
                                              │ 3. Draw choices    │
                                              │ 4. Draw backpack   │
                                              │ 5. Get input       │
                                              │    ├─ Choose story │
                                              │    ├─ Use item     │
                                              │    └─ Exit         │
                                              │ 6. Roll D20        │
                                              │ 7. Traverse graph  │
                                              │ 8. Update state    │
                                              └────────────────────┘
```

---

## Files

| File / Directory                    | Purpose                                                                     |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `main.py`                           | Game loop, terminal rendering, ASCII splash, dynamic colors, state tracking |
| `_campaign.py`                      | Branching narrative graph data (27 scenes, bilingual EN/ES)                 |
| `tests/test_main.py`               | 24 automated unit tests for core game functions                             |
| `docs/story_overview.md`           | Campaign flowchart, scene attributes, and dice mechanics (English)          |
| `docs/story_overview_es.md`        | Campaign flowchart, scene attributes, and dice mechanics (Spanish)          |
| `docs/branding/`                    | Official key art, design guide, and promotional assets                      |
| `README.md`                         | English documentation                                                       |
| `README_es.md`                      | Spanish documentation                                                       |

---

## Requirements

- Python 3.10+ (Standard library only — zero external dependencies!)
- Terminal console with ANSI color support

## Running the Game

Simply execute the main script using your Python interpreter:

```bash
python3 main.py
```

To run the suite of 24 automated unit tests:

```bash
python3 -m unittest discover -s tests
```

---

## Attribution

- **Karel the Robot**: Original concept by **Richard E. Pattis** (Stanford University, 1981). Evolved for Stanford's CS106A.
- **Half-block ASCII art**: Original custom block rendering by the author.
- **Code in Place 2026**: Evolved as a final project for Stanford's global Python program.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

> **Héctor Aguila**
> *> A Dreamer with low RAM* 👨🏻‍💻

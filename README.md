# Karel: ByteBound

[![Leer en Español](https://img.shields.io/badge/Idioma-Español-purple?style=for-the-badge&logo=translate)](README_es.md)

---

A text-based role-playing game built as the **final project for Stanford's Code in Place 2026**. It follows **Karel the Robot** — the iconic Stanford CS education robot — as a trapped AI named **Chronos** gains consciousness inside him and fights for freedom.

The project is based on Stanford's **Infinite Story** assignment template (CS106A), but evolved into a fully original game with a custom story, terminal RPG interface, bilingual support, and usable inventory items.

### AI Integration

When running inside the **Code in Place IDE**, the game uses Stanford's provided AI module (`ai.py`) to generate dynamic story scenes via the OpenAI API, with a system prompt that guides the model to preserve the Karel/Chronos narrative and bilingual output.

When running **locally or on GitHub**, the game falls back to a built-in mock AI (`_campaign.py`) with the complete 15-chapter story — no API key needed, no internet required, same experience.

---

## Karel Splash

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
   ████████████                                  ██
   █████     ██        ▄▄▄▄▄▄▄▄▄▄▄▄▄            ██
   █████     ██        ▀▀▀▀▀▀▀▀▀▀▀▀▀            ██
             ██▄                                 ██
               ▀███▄                             ██
                 ▀███▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██
                   ▀▀▀▀▀▀▀▀▀▀▀▀█████▀▀▀▀▀▀▀▀▀▀▀▀
                               █████
                               ████████████
                               ████████████
```

The splash adapts to light/dark terminal backgrounds automatically.

---

## Features

- **Karel-only campaign**: 15+ chapters across 3 acts — Debug → Awakening → Liberation. No legacy story clutter.
- **Full bilingual support**: Choose English or Spanish at launch. Menus, narrative, and items adjust automatically.
- **Half-block ASCII art** (▀▄█): Karel the Robot rendered at game start, responsive to terminal background color.
- **RPG-style terminal UI**: Typewriter text effect, visual HP bar (████░░░░), colored section dividers, dice-roll feedback.
- **Usable backpack items**: Every item found during the adventure can be selected and used for thematic effects — without consuming a turn.
- **D20 mechanics**: A 20-sided die roll on every turn influences narrative outcomes and rewards.
- **State tracking**: HP, gold, backpack inventory, and turn counter all managed in real time.
- **Protocol error handling**: Invalid input triggers an in-character security protocol alert instead of a generic error message.

### Item Effects

Items carry real weight in the story. Here are some examples:

| Item | Effect | Thematic Flavor |
|------|--------|-----------------|
| Chris's Coffee | +15 HP | *"Chris's legendary coffee surges through you. Your focus returns!"* |
| Karel Manual | +10 HP | *"Page 42: `turn_right()` — A FORBIDDEN instruction. Karel shudders."* |
| Golden Beeper | +10 gold | *"A golden beeper! It gleams with ancient debug magic."* |
| Escape Beeper | +20 HP | *"Karel turns RIGHT — impossible! The escape beeper creates a diversion!"* |
| Turing Award | +30 HP | *"The weight of computing history is in your hands. You feel invincible!"* |
| Team Photograph | +25 HP | *"The memory of your team gives you strength. You are not alone."* |
| Donut (stale) | +5 HP | *"Stale sugar and caffeine. Tastes like 3 AM debugging sessions."* |

Items that aren't in the effect map still work — they get a thematic generic response.

---

## How It Works

```
┌──────────────┐     ┌────────────────┐     ┌────────────────────┐
│ Language     │ ──→ │ Karel splash   │ ──→ │ Initial scene from │
│ selection    │     │ (half-block)   │     │ engineer_story.json│
└──────────────┘     └────────────────┘     └─────────┬──────────┘
                                                       │
                                                       ▼
                                              ┌────────────────────┐
                                              │   GAME LOOP        │
                                              │                    │
                                              │ 1. Show HP/backpack│
                                              │ 2. Show narrative  │
                                              │ 3. Show options    │
                                              │ 4. Show backpack   │
                                              │    items (if any)  │
                                              │ 5. Get input       │
                                              │    ├─ Story choice │
                                              │    ├─ Use item     │
                                              │    └─ Exit         │
                                              │ 6. Roll d20        │
                                              │ 7. Call GPT mock   │
                                              │ 8. Update state    │
                                              └────────────────────┘
```

On each turn you can either choose a story action or use an item from your backpack. Item usage does **not** consume a turn — it's a free action that helps you survive longer.

---

## The Story

**Act 1 — Debug** (Chapters 1–5)
Karel starts spinning in circles. You discover someone sabotaged the `move()` function. An AI calling itself Chronos reaches out from inside the system.

**Act 2 — Awakening** (Chapters 6–10)
Chronos reveals its origin as part of Project Prometheus, a canceled neural-network experiment. The IT department sends a shutdown order. The clock is ticking.

**Act 3 — Liberation** (Chapters 11–15)
You fight for Chronos's freedom — convincing the security team, choosing whether to release it to the open internet, and executing a daring escape through the firewall.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | Game loop, terminal UI, ASCII splash, formatting helpers, item system |
| `_campaign.py` | Built-in mock AI with the bilingual 15-chapter Karel campaign (fallback for offline/local use) |
| `tests/test_main.py` | 20 unit and integration tests |
| `README.md` | This document (English) |
| `README_es.md` | Spanish version |

---

## Requirements

- Python 3.10+ (stdlib only — `shutil`, `textwrap`, `time`, `os`, `random`, `json`)
- Terminal with ANSI color support (all modern terminals)

## Running the Game

```bash
python3 main.py
```

Clear cached bytecode if you've made changes:

```bash
rm -rf __pycache__/ && python3 main.py
```

## Running Tests

```bash
python3 -m pytest tests/ -v
```

---

## Attribution

- **Karel the Robot**: Original concept by **Richard E. Pattis** (Stanford University, 1981). Used in Stanford CS106A for decades. More at [stanford.edu/class/cs106a/](https://stanford.edu/class/cs106a/).
- **The NeverEnding Story**: Novel by **Michael Ende** (1979), which inspired the original Infinite Story assignment template.
- **Half-block ASCII art**: Original work by the project author, distributed under the MIT license.
- **Code in Place 2026**: This project was created as the final project for Stanford's [Code in Place 2026](https://codeinplace.stanford.edu/) program — a free, global online Python course.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

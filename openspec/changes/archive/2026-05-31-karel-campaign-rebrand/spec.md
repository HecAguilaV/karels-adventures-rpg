# Delta Specs: Karel Campaign Rebrand

> **STATUS: IMPLEMENTED ✅** — All 3 capabilities are **new** (no existing `openspec/specs/` found). Full specs below.
> Archive date: 2026-05-31

---

## 1. karel-campaign — Expanded Karel Story Arc

### Purpose

Replace all non-Karel story options (original_small, original_big) with a single expanded Karel campaign: 15+ chapters across 3 acts (Debug → Awakening → Liberation), fully bilingual (EN/ES).

### Requirements

| ID | Requirement | RFC 2119 |
|----|------------|----------|
| KC-1 | The game MUST offer **only** the Karel campaign as a playable story. No original_small/original_big options. | MUST |
| KC-2 | The Karel campaign MUST contain **15+ distinct chapters** across 3 acts: Debug (chapters 1–5), Awakening (6–10), Liberation (11–15+). | MUST |
| KC-3 | Each chapter MUST have unique narrative text in both English and Spanish, stored in side-by-side arrays. | MUST |
| KC-4 | The mock AI (`ai.py`) MUST serve Karel campaign scenes from static arrays — no GPT calls. | SHALL |
| KC-5 | The campaign SHOULD include a victory arc after Liberation for player satisfaction. | SHOULD |
| KC-6 | Legacy `_generar_escena_corta()` and `_generar_escena_campana()` functions MUST be removed from `ai.py`. | MUST |
| KC-7 | `data/original_small.json` and `data/original_big.json` MUST be deleted. | MUST |

#### Scenario: EN — Full campaign plays without legacy stories

- GIVEN the player launches the game and selects "Karel's Adventures RPG"
- WHEN they play through all 15+ chapters
- THEN each chapter displays unique narrative text in English
- AND no original_small/original_big story options appear in any menu

#### Scenario: ES — Campaña completa sin historias heredadas

- GIVEN el jugador inicia el juego y selecciona "Karel's Adventures RPG"
- WHEN juega los 15+ capítulos
- THEN cada capítulo muestra texto narrativo único en español
- AND ninguna opción de historia original_small/original_big aparece en ningún menú

#### Scenario: Legacy arcs removed from ai.py

- GIVEN the codebase after the change
- WHEN inspecting `ai.py` for `_generar_escena_corta` or `_generar_escena_campana`
- THEN those functions MUST NOT exist
- AND `call_gpt()` MUST NOT reference them

---

## 2. ascii-splash — Half-Block Karel ASCII Art

### Purpose

Display a Karel the dog ASCII art rendered with half-block characters (▀▄█) at game launch, adapting to light/dark terminal background.

### Requirements

| ID | Requirement | RFC 2119 |
|----|------------|----------|
| AS-1 | The game MUST display Karel ASCII art using half-block Unicode characters (▀▄█) before the welcome banner. | MUST |
| AS-2 | The art MUST detect terminal background via `COLORFGBG` or ANSI query and render a light-background variant (█→▄ swap) or dark-background variant accordingly. | MUST |
| AS-3 | If background detection fails, the art SHOULD default to dark-background variant. | SHOULD |
| AS-4 | If the terminal cannot render Unicode half-blocks, the art MUST degrade gracefully (e.g. skip to text-only launch). | MUST |

#### Scenario: EN — Dark terminal displays solid Karel

- GIVEN the terminal has a dark background (no `COLORFGBG` or bg=0)
- WHEN the game starts
- THEN half-block Karel art renders with ▀█ for filled areas and spaces for empty areas

#### Scenario: ES — Terminal claro muestra Karel invertido

- GIVEN el terminal tiene fondo claro (`COLORFGBG` indica bg=7 o similar)
- WHEN el juego inicia
- THEN el arte de Karel se renderiza con ▄█ intercambiados para adaptarse al fondo claro

#### Scenario: Terminal cannot render Unicode

- GIVEN a terminal that does not support half-block Unicode characters
- WHEN the game starts
- THEN no art is shown and gameplay proceeds normally to the welcome banner

---

## 3. terminal-formatting — Dynamic Layout & RPG UI

### Purpose

Adapt all narrative text output to terminal width and enhance the UI with RPG-style elements: HP bars, typewriter text, colored dividers.

### Requirements

| ID | Requirement | RFC 2119 |
|----|------------|----------|
| TF-1 | All narrative text MUST wrap to the terminal width via `shutil.get_terminal_size().columns` + `textwrap.fill()`. | MUST |
| TF-2 | The HP bar MUST render visually as characters (e.g. `████░░░░`) representing player health. | MUST |
| TF-3 | Narrative text SHOULD appear with a typewriter effect (`time.sleep()` between characters) for pacing. | SHOULD |
| TF-4 | Section dividers and borders MUST use ANSI color codes for visual separation. | MUST |
| TF-5 | All formatting MUST degrade gracefully on terminals without ANSI color support (plain text fallback). | MUST |

#### Scenario: EN — Text wraps at 40 columns

- GIVEN the terminal is resized to 40 columns wide
- WHEN narrative text is displayed
- THEN no line exceeds 40 characters (wrapped by `textwrap.fill`)

#### Scenario: EN — HP bar shows current health

- GIVEN the player has 60% health
- WHEN the HP bar renders
- THEN it displays `████░░░░` (5 filled, 3 empty blocks)

#### Scenario: ES — Escritura tipo máquina de escribir

- GIVEN el jugador avanza a un nuevo capítulo
- WHEN el texto narrativo se muestra
- THEN los caracteres aparecen uno por uno con una pausa breve entre ellos

#### Scenario: Terminal without ANSI color

- GIVEN a terminal that does not support ANSI escape codes
- WHEN the game displays dividers or borders
- THEN plain ASCII characters (e.g. `===`, `---`) are shown instead of colored output

---

## Acceptance Criteria

- [x] Game starts, shows Karel ASCII art, then Karel story as the only option
- [x] `original_small` / `original_big` absent from file picker and `ai.py`
- [x] Karel campaign has 15+ distinct chapters without repetition
- [x] Text wraps cleanly at 40, 80, and 120 column widths
- [x] HP bar renders as visual indicator (████░░░░)
- [x] All 6 legacy files deleted; `main.py` and `ai.py` run cleanly
- [x] Bilingual gameplay works in both EN and ES

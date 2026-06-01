# Design: Karel Campaign Rebrand

## Technical Approach

Single-file surgical refactor of `main.py` and `ai.py`. Add three new utility functions to `main.py` (ASCII splash, text wrapper, visual helpers). Rewrite `_generar_escena_karel()` with 15+ chapters across 3 acts, remove two legacy story arcs. Delete 4 legacy files and 2 JSON files. No new Python modules — everything stays in the existing two files to minimize churn.

## Architecture Decisions

| Decision | Choice | Alternatives | Rationale |
|----------|--------|-------------|-----------|
| Story storage | Bilingual arrays in `ai.py` | JSON files, single file per lang | Follows existing `_construir_respuesta()` pattern; no file I/O, atomic in memory |
| Splash art | Function + constant in `main.py` | Separate module | Only 40 lines, one call site; avoids new file overhead |
| Text wrapping | `wrap()` helper called per `print()` | Override `print()` globally | Explicit wrapping is testable and visible; monkey-patching print() is fragile |
| bg color detection | `COLORFGBG` env var parse, fallback to `curses` light-check | Always assume dark | Dark-bg-only breaks on light terminals; env var is zero-dependency |
| Screen clear | ANSI `\033[2J\033[H` | `os.system('clear')` | ANSI is portable, no subprocess, works in all modern terminals |
| Turn clamping | `min(turno, len(arco) - 1)` | Modulo wrap, explicit end | Modulo creates narrative loops; clamping freezes on victory screen — existing pattern, correct |

## Data Flow

```
main.py                          ai.py
───────                          ─────
main()
  │ select_story_file()
  │   └─→ removed (always Karel)     ┌──────────────────────────────┐
  │ game_loop                        │ _generar_escena_karel(turno) │
  │   │                              │   ├── Act 1: Debug (ch 1-5)  │
  │   │  wrap(text)  ←─── text ────→│   ├── Act 2: Awakening(6-10) │
  │   │  typewrite(text)             │   └── Act 3: Liberation(11+) │
  │   │  hp_bar(hp)                  │       → _construir_respuesta()│
  │   │  divider(symbol)             └──────────────────────────────┘
  │   │  clear_screen()
  │   │
  │   karel_splash()  ←─── on startup before welcome
  │
  exit / game_over / victory
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `main.py` | Modify | Rebrand TEXT_INTERFACE; add `karel_splash()`, `wrap()`, `typewrite()`, `hp_bar()`, `divider()`, `clear_screen()`; hardcode Karel as only story; wrap all narrative prints |
| `ai.py` | Modify | Remove `_generar_escena_corta()` + `_generar_escena_campana()`; rewrite `_generar_escena_karel()` → 15 chapters; simplify `call_gpt()` and `_traducir_escena_inicial()` to only Karel path |
| `data/original_small.json` | Delete | Legacy Stanford arc |
| `data/original_big.json` | Delete | Legacy Stanford arc |
| `README.md` | Modify | Rebrand title, remove arc references |
| `README_es.md` | Modify | Rebrand title, remove arc references |
| `infinite_story.py` | Delete | Legacy skeleton |
| `warmup.py` | Delete | Legacy stub |
| `instruccionesoriginales.md` | Delete | Legacy handout |
| `notopenai.py` | Delete | Legacy mock |

## Interfaces / Contracts

```python
# ── New functions in main.py ──

def karel_splash() -> None:
    """Detect terminal bg, render half-block Karel in yellow/dark-yellow.
    Falls back silently on unsupported terminals."""

def wrap(text: str) -> str:
    """textwrap.fill(text, width=shutil.get_terminal_size().columns)"""

def typewrite(text: str, delay: float = 0.03) -> None:
    """Print text char-by-char with time.sleep(delay)."""

def hp_bar(current: int, max_hp: int = 100, width: int = 20) -> str:
    """Return '██████░░░░░░░░' bar colored by percentage."""

def divider(char: str = "═", color: str = COLOR_NARRATIVE) -> None:
    """Print a full-width colored divider line."""

def clear_screen() -> None:
    """ANSI escape \033[2J\033[H to clear terminal."""

# ── Rewritten in ai.py ──

def _generar_escena_karel(turno: int, es_espanol: bool) -> dict:
    """15+ scenes in 3 acts. Same signature, clamped indexing, bilingual.
    Returns dict with keys: narrativa, opciones, items, victoria (optional)."""
```

## Act Structure (15 scenes)

| Act | #Ch | Theme | Narrative Beat |
|-----|-----|-------|---------------|
| 1: Debug | 1-5 | Karel malfunctions at Stanford, SOS beeper pattern discovered | Same as current 5 chapters |
| 2: Awakening | 6-10 | Karel's consciousness grows, explores Stanford network, meets other AI | Mid-campaign conflict, no victory flag |
| 3: Liberation | 11-15+ | Karel faces shutdown order, player must choose: free or contain Karel | Fork → victory or bittersweet ending |

Each act maintains bilingual EN/ES arrays. Victory flag set only in act 3 final scene. `_construir_respuesta()` unchanged.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `karel_splash()` on light/dark terminal | Mock `os.environ` for COLORFGBG; assert ANSI output |
| Unit | `wrap()` at various widths | Monkey-patch `shutil.get_terminal_size()`; assert output length ≤ width |
| Unit | `hp_bar()` at 0, 50, 100 HP | Assert bar length matches `width` parameter, correct fill/empty ratio |
| Unit | `_generar_escena_karel()` at turn 0, 7, 14 | Assert returned keys, bilingual correctness, no None crashes |
| Integration | Full game loop with mocked input | Feed "1\n1\n1\n..." sequence; assert no crashes through victory |
| Integration | Spanish path | Same input sequence in lang=es; assert Spanish narrative returned |

## Migration / Rollout

No migration needed — no persistent state on disk. All changes are code-only.
- **Branch**: Feature branch from `main`
- **Commit 1**: Remove legacy files (JSON + 4 files), clean imports
- **Commit 2**: Rebrand strings, hardcode Karel story in `main.py`, simplify `select_story_file`
- **Commit 3**: Rewrite `_generar_escena_karel()` with 15 chapters, remove old arcs from `ai.py`
- **Commit 4**: Add ASCII splash + visual enhancements to `main.py`
- **Commit 5**: Update READMEs

## Open Questions

- [ ] Confirm terminal background color detection order: `COLORFGBG` → `os.environ.get("COLORFGBG")` parsed as `bg:fg` → last value wins. On macOS Terminal.app this is not set; fallback to `curses` or assume dark?

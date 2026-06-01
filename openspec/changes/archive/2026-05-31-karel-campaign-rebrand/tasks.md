# Tasks: Karel Campaign Rebrand

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~490 (non-trivial) + ~1737 (file deletions) |
| 400-line budget risk | Medium — 490 non-trivial lines exceeds budget; file deletions are trivially reviewable |
| Chained PRs recommended | Yes |
| Suggested split | PR 1: Foundation + Campaign (ai.py + deletions) → PR 2: Rebrand + UI (main.py) → PR 3: Docs + Tests |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: pending
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Delete 6 legacy files + rewrite `_generar_escena_karel()` + remove old arcs | PR 1 | base=main; bulk is file deletions + bilingual arrays, low cognitive load |
| 2 | Rebrand strings, hardcode Karel story, add 6 UI functions, wrap prints | PR 2 | base=main; independent of PR 1, small and focused |
| 3 | Update READMEs + write unit/integration tests | PR 3 | base=main; docs/tests, depends on both PR 1 & 2 being stable |

## Phase 1: Foundation & Cleanup

- [x] 1.1 Delete 6 files: `data/original_small.json`, `data/original_big.json`, `infinite_story.py`, `warmup.py`, `instruccionesoriginales.md`, `notopenai.py`
- [x] 1.2 Remove `_generar_escena_corta()` and `_generar_escena_campana()` from `ai.py`
- [x] 1.3 Simplify `call_gpt()` and `_traducir_escena_inicial()` to Karel-only path

## Phase 2: Campaign Expansion

- [x] 2.1 Write 15+ bilingual chapter arrays in `_generar_escena_karel()` across 3 acts: Debug (1-5), Awakening (6-10), Liberation (11-15+)
- [x] 2.2 Add victory fork logic in Liberation act final chapter with `victoria` flag

## Phase 3: Rebrand & UI Enhancements

- [x] 3.1 Rebrand `TEXT_INTERFACE` welcome, title banner, and `STORY_DISPLAY_NAMES` in `main.py`
- [x] 3.2 Hardcode Karel as only story option; remove story selector branching from `select_story_file()`
- [x] 3.3 Add `karel_splash()` with half-block ASCII art + `COLORFGBG` terminal bg detection
- [x] 3.4 Add `wrap()`, `typewrite()`, `hp_bar()`, `divider()`, `clear_screen()` helpers to `main.py`
- [x] 3.5 Wrap all narrative `print()` calls with `wrap()` + `typewrite()`; add dividers and HP bar

## Phase 4: Documentation

- [x] 4.1 Update `README.md`: rebrand title, remove legacy arc references
- [x] 4.2 Update `README_es.md`: rebrand title, remove legacy arc references

## Phase 5: Testing

- [x] 5.1 Unit test `karel_splash()` with mocked dark/light `COLORFGBG`
- [x] 5.2 Unit test `wrap()` at 40, 80, 120 column widths
- [x] 5.3 Unit test `hp_bar()` at 0%, 50%, 100% health
- [x] 5.4 Unit test additional core functions (`roll_d20()`, `format_backpack()`)
- [x] 5.5 Integration test: full game loop with mocked `"1\n"` input through victory
- [x] 5.6 Integration test: game over by HP, exit immediately, and Spanish locale

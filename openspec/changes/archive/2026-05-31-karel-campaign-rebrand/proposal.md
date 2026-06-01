# Proposal: Karel Campaign Rebrand

## Intent

Rebrand "Infinite Story RPG" to "Karel's Adventures RPG", consolidate on the Karel narrative, expand it into a deeper campaign, and polish the terminal UX with dynamic layout, ASCII art, and visual immersion — while removing legacy code from the Stanford CS106A skeleton.

## Scope

### In Scope
- Rebrand title, welcome text, READMEs, and all user-facing strings
- Delete `original_small` and `original_big` JSON files + their ai.py story arcs
- Expand Karel campaign from 5 to 15+ chapters with richer narrative arc
- Half-block Karel ASCII art (▀▄█) at game start, responsive to terminal background
- Dynamic text wrapping via `shutil.get_terminal_size()`
- Enhanced RPG-style terminal UI (colors, formatting, pacing)
- Delete legacy files: `infinite_story.py`, `warmup.py`, `instruccionesoriginales.md`, `notopenai.py`

### Out of Scope
- Real GPT integration (mock `ai.py` stays as-is)
- Audio, GUI, web interface
- Save/load game state to disk
- Multiplayer or leaderboards

## Capabilities

> No existing `openspec/specs/` found — all capabilities are new.

### New Capabilities
- `karel-campaign`: Expanded Karel story arc (15+ chapters, bilingual, with victory arcs)
- `ascii-splash`: Half-block Karel ASCII art launch screen
- `terminal-formatting`: Dynamic terminal width detection + enhanced RPG UI layout

### Modified Capabilities
- None (no existing specs to modify)

## Approach

1. **Rebrand**: Replace `TEXT_INTERFACE` welcome, `STORY_DISPLAY_NAMES`, READMEs, and title banner — single pass on `main.py`.
2. **Story cleanup**: Delete `data/original_small.json`, `data/original_big.json`. Remove `_generar_escena_corta()` and `_generar_escena_campana()` from `ai.py`. Remove their branches in `call_gpt()` and `_traducir_escena_inicial()`.
3. **Campaign expansion**: Rewrite `_generar_escena_karel()` with 15+ chapters in 3 acts (Debug → Awakening → Liberation), bilingual side-by-side arrays.
4. **Karel ASCII art**: Detect terminal background (`COLORFGBG` or ANSI query), render light/dark half-block variant, display before welcome.
5. **Text wrapping**: `shutil.get_terminal_size().columns` + `textwrap.fill()` on all narrative output.
6. **UI polish**: Typewriter-style `time.sleep()` pauses, HP bar (████░░), section dividers, colored borders.
7. **Legacy cleanup**: Delete 4 files, verify imports in `main.py`.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `main.py` | Modified | Rebrand, text wrap, ASCII splash, UI polish |
| `ai.py` | Modified | Remove 2 arcs, expand Karel to 15+ chapters |
| `data/original_small.json` | Removed | Legacy story |
| `data/original_big.json` | Removed | Legacy story |
| `README.md` | Modified | Rebrand |
| `README_es.md` | Modified | Rebrand |
| `infinite_story.py` | Removed | Legacy Stanford skeleton |
| `warmup.py` | Removed | Legacy stub |
| `instruccionesoriginales.md` | Removed | Legacy assignment handout |
| `notopenai.py` | Removed | Legacy mock (replaced by `ai.py`) |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| ASCII art breaks on unusual terminals | Low | Graceful fallback to no art |
| Spanish/English narrative drift | Low | Side-by-side arrays, same structure |
| Campaign length overwhelms mock AI | Low | Mock uses static arrays, no issue |

## Rollback Plan

`git revert` the feature branch. Restore 4 legacy files from git. Swap back original JSON files and story arcs.

## Dependencies

- Python 3.10+ stdlib only (`shutil`, `textwrap`, `time`, `os`, `random`, `json`)
- Terminal with ANSI color support (all modern terminals)

## Success Criteria

- [ ] Game starts, shows Karel ASCII art, then Karel story as the only option
- [ ] `original_small` / `original_big` absent from file picker and `ai.py`
- [ ] Karel campaign has 15+ distinct chapters without repetition
- [ ] Text wraps cleanly at 40, 80, 120 column widths
- [ ] HP bar renders as visual indicator (████░░░░)
- [ ] All 4 legacy files deleted; `main.py` and `ai.py` run cleanly
- [ ] Bilingual gameplay works in both EN and ES

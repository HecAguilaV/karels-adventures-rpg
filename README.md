# Infinite Story RPG

[![Bilingual Support (Español)](https://img.shields.io/badge/Language-Español-purple?style=for-the-badge&logo=translate)](README_es.md)

---

A text based RPG engine built as a final project for Stanford's Code in Place 2026. The game uses an LLM to generate narrative chapters and choices dynamically, incorporating a player's choices and a 20-sided die roll.

## Features

- **English and Spanish support**: Players pick their language at the start. Both the console menus and the generated story adjust automatically. This was built to help native Spanish speakers navigate the game more naturally.
- **State manager**: A Python dictionary tracks HP, gold, backpack inventory, and turns by parsing the LLM's JSON outputs.
- **D20 mechanics**: The game rolls a 20-sided die on every turn. The result goes into the prompt to influence the LLM's narrative direction.

## Files

- `main.py` runs the game loop.
- `data/` stores the starting configurations for the stories.
- `README.md` is this document.
- `README_es.md` is the Spanish version.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

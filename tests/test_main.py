"""Tests for main.py — Karel's Adventures RPG.

Phase 5: Unit and integration tests for core game functions.
"""

import json
import os
import sys
import unittest
from unittest.mock import patch

# Add project root so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import (
    COLOR_RESET,
    KAREL_ART,
    TEXT_INTERFACE,
    format_backpack,
    hp_bar,
    karel_splash,
    roll_d20,
    wrap,
)


# ── 5.1 Unit test: wrap() ────────────────────────────────────────────────


class TestWrapFunction(unittest.TestCase):
    """Verify wrap() uses terminal width."""

    @patch("main.shutil.get_terminal_size")
    def test_wrap_at_40_columns(self, mock_term_size):
        mock_term_size.return_value.columns = 40
        text = "word " * 30  # ~150 chars
        result = wrap(text)
        for line in result.split("\n"):
            self.assertLessEqual(
                len(line), 40, f"Line exceeds 40 columns: {len(line)} chars"
            )

    @patch("main.shutil.get_terminal_size")
    def test_wrap_at_80_columns(self, mock_term_size):
        mock_term_size.return_value.columns = 80
        text = "word " * 30
        result = wrap(text)
        for line in result.split("\n"):
            self.assertLessEqual(
                len(line), 80, f"Line exceeds 80 columns: {len(line)} chars"
            )


# ── 5.2 Unit test: hp_bar() ──────────────────────────────────────────────


class TestHpBar(unittest.TestCase):
    """Verify hp_bar() renders correct ratio."""

    def test_hp_bar_zero(self):
        result = hp_bar(0, 100, 20)
        self.assertIn("0/100", result)
        self.assertEqual(result.count("█"), 0)
        self.assertEqual(result.count("░"), 20)

    def test_hp_bar_half(self):
        result = hp_bar(50, 100, 20)
        self.assertIn("50/100", result)
        self.assertEqual(result.count("█"), 10)
        self.assertEqual(result.count("░"), 10)

    def test_hp_bar_full(self):
        result = hp_bar(100, 100, 20)
        self.assertIn("100/100", result)
        self.assertEqual(result.count("█"), 20)
        self.assertEqual(result.count("░"), 0)


# ── 5.3 Unit test: karel_splash() ────────────────────────────────────────


class TestKarelSplash(unittest.TestCase):
    """Verify karel_splash() returns correct type and contains expected chars."""

    @patch.dict(os.environ, {"COLORFGBG": ";0"}, clear=True)
    def test_returns_string(self):
        result = karel_splash("en")
        self.assertIsInstance(result, str)

    @patch.dict(os.environ, {"COLORFGBG": ";0"}, clear=True)
    def test_contains_expected_chars(self):
        result = karel_splash("en")
        # Half-block characters from the art
        self.assertIn("▄", result)
        self.assertIn("▀", result)
        self.assertIn("█", result)
        # Title banner
        self.assertIn(TEXT_INTERFACE["en"]["welcome"].strip(), result)

    @patch.dict(os.environ, {"COLORFGBG": ";0"}, clear=True)
    def test_dark_bg_uses_bright_yellow(self):
        result = karel_splash("en")
        self.assertIn("\033[93m", result)  # bright yellow
        self.assertIn(COLOR_RESET, result)

    @patch.dict(os.environ, {"COLORFGBG": ";7"}, clear=True)
    def test_light_bg_uses_dark_yellow(self):
        result = karel_splash("en")
        self.assertIn("\033[33m", result)  # dark yellow/brown
        self.assertIn(COLOR_RESET, result)

    @patch.dict(os.environ, {}, clear=True)
    def test_fallback_to_dark(self):
        """When COLORFGBG is unset, defaults to bright yellow."""
        result = karel_splash("en")
        self.assertIn("\033[93m", result)
        self.assertIn(COLOR_RESET, result)


# ── 5.4 Unit test: roll_d20() ────────────────────────────────────────────


class TestRollD20(unittest.TestCase):
    """Verify roll is always 1-20."""

    def test_roll_range(self):
        for _ in range(1000):
            roll = roll_d20()
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 20)

    def test_roll_is_integer(self):
        roll = roll_d20()
        self.assertIsInstance(roll, int)


# ── 5.5 Unit test: format_backpack() ─────────────────────────────────────


class TestBackpackFormat(unittest.TestCase):
    """Verify format_backpack() renders correctly."""

    def test_empty_backpack(self):
        result = format_backpack([], "en")
        self.assertIn(TEXT_INTERFACE["en"]["backpack_title"], result)
        self.assertIn(TEXT_INTERFACE["en"]["backpack_empty"], result)
        self.assertTrue(result.startswith("+"))

    def test_single_item(self):
        result = format_backpack(["Sword"], "en")
        self.assertIn("Sword", result)
        self.assertTrue(result.startswith("+"))

    def test_multiple_items(self):
        items = ["Sword", "Shield", "Potion"]
        result = format_backpack(items, "en")
        for item in items:
            self.assertIn(item, result)
        self.assertTrue(result.startswith("+"))

    def test_spanish_backpack(self):
        result = format_backpack(["Espada", "Escudo"], "es")
        self.assertIn(TEXT_INTERFACE["es"]["backpack_title"], result)
        self.assertIn("Espada", result)
        self.assertIn("Escudo", result)

    def test_long_item_truncated(self):
        """Items longer than 14 chars should be truncated with '.'"""
        result = format_backpack(["VeryLongItemNameHere"], "en")
        self.assertIn("VeryLongItemN.", result)


# ── 5.6 Integration test: game loop ──────────────────────────────────────


class TestGameLoopNoCrash(unittest.TestCase):
    """Verify main.py runs with mock input without crashing."""

    @patch("main.call_gpt")
    @patch("time.sleep", return_value=None)  # speed up typewriter
    @patch("builtins.input")
    def test_game_loop_exit_immediately(self, mock_input, mock_sleep, mock_gpt):
        """Type 'exit' after language selection — no crash."""
        mock_input.side_effect = ["1", "exit"]
        mock_gpt.return_value = json.dumps({
            "narrativa": "not used",
            "opciones": ["Go", "Wait"],
            "cambio_vida": 0,
            "item_encontrado": None,
        })
        from main import main
        main()  # should return without exception

    @patch("main.call_gpt")
    @patch("time.sleep", return_value=None)
    @patch("builtins.input")
    def test_game_loop_one_turn_victory(self, mock_input, mock_sleep, mock_gpt):
        """Play one turn triggering victory — no crash."""
        mock_input.side_effect = ["1", "1"]
        mock_gpt.return_value = json.dumps({
            "narrativa": "You debugged Karel successfully.",
            "opciones": ["Celebrate"],
            "cambio_vida": 10,
            "item_encontrado": "Golden Beeper",
            "victoria": True,
        })
        from main import main
        main()  # should return without exception

    @patch("main.call_gpt")
    @patch("time.sleep", return_value=None)
    @patch("builtins.input")
    def test_game_over_by_hp(self, mock_input, mock_sleep, mock_gpt):
        """HP drops to 0 — game over screen should show."""
        mock_input.side_effect = ["1", "1"]
        mock_gpt.return_value = json.dumps({
            "narrativa": "You took fatal damage.",
            "opciones": ["Give up"],
            "cambio_vida": -999,  # guaranteed KO
            "item_encontrado": None,
        })
        from main import main
        main()  # should reach game over without exception


if __name__ == "__main__":
    unittest.main()

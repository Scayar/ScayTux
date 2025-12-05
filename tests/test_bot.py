"""
TUX Droid AI Control - Bot Tests
================================

Basic tests for the Telegram bot components.
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.keyboards import (
    CallbackData,
    get_main_menu_keyboard,
    get_eyes_keyboard,
    get_mouth_keyboard,
    get_wings_keyboard,
    get_spin_keyboard,
    get_leds_keyboard,
    get_sound_keyboard,
    get_sleep_keyboard,
)
from bot.api_client import TuxAPIClient


class TestKeyboards:
    """Tests for keyboard layouts."""
    
    def test_main_menu_keyboard(self):
        """Test main menu keyboard has all categories."""
        keyboard = get_main_menu_keyboard()
        assert keyboard is not None
        assert len(keyboard.inline_keyboard) >= 4
    
    def test_eyes_keyboard(self):
        """Test eyes keyboard has expected buttons."""
        keyboard = get_eyes_keyboard()
        assert keyboard is not None
        # Flatten keyboard to get all buttons
        buttons = [btn for row in keyboard.inline_keyboard for btn in row]
        callback_data = [btn.callback_data for btn in buttons]
        assert CallbackData.EYES_OPEN in callback_data
        assert CallbackData.EYES_CLOSE in callback_data
        assert CallbackData.MENU_MAIN in callback_data
    
    def test_mouth_keyboard(self):
        """Test mouth keyboard has expected buttons."""
        keyboard = get_mouth_keyboard()
        assert keyboard is not None
        buttons = [btn for row in keyboard.inline_keyboard for btn in row]
        callback_data = [btn.callback_data for btn in buttons]
        assert CallbackData.MOUTH_OPEN in callback_data
        assert CallbackData.MOUTH_CLOSE in callback_data
    
    def test_wings_keyboard(self):
        """Test wings keyboard has expected buttons."""
        keyboard = get_wings_keyboard()
        assert keyboard is not None
        buttons = [btn for row in keyboard.inline_keyboard for btn in row]
        callback_data = [btn.callback_data for btn in buttons]
        assert CallbackData.WINGS_RAISE in callback_data
        assert CallbackData.WINGS_LOWER in callback_data
    
    def test_spin_keyboard(self):
        """Test spin keyboard has expected buttons."""
        keyboard = get_spin_keyboard()
        assert keyboard is not None
        buttons = [btn for row in keyboard.inline_keyboard for btn in row]
        callback_data = [btn.callback_data for btn in buttons]
        assert CallbackData.SPIN_LEFT_90 in callback_data
        assert CallbackData.SPIN_RIGHT_90 in callback_data
    
    def test_leds_keyboard(self):
        """Test LEDs keyboard has expected buttons."""
        keyboard = get_leds_keyboard()
        assert keyboard is not None
        buttons = [btn for row in keyboard.inline_keyboard for btn in row]
        callback_data = [btn.callback_data for btn in buttons]
        assert CallbackData.LEDS_ON_BOTH in callback_data
        assert CallbackData.LEDS_OFF in callback_data
    
    def test_sound_keyboard(self):
        """Test sound keyboard has expected buttons."""
        keyboard = get_sound_keyboard()
        assert keyboard is not None
        buttons = [btn for row in keyboard.inline_keyboard for btn in row]
        callback_data = [btn.callback_data for btn in buttons]
        assert CallbackData.SOUND_MUTE in callback_data
        assert CallbackData.SOUND_UNMUTE in callback_data
    
    def test_sleep_keyboard(self):
        """Test sleep keyboard has expected buttons."""
        keyboard = get_sleep_keyboard()
        assert keyboard is not None
        buttons = [btn for row in keyboard.inline_keyboard for btn in row]
        callback_data = [btn.callback_data for btn in buttons]
        assert CallbackData.SLEEP_NORMAL in callback_data
        assert CallbackData.WAKE_UP in callback_data


class TestCallbackData:
    """Tests for callback data constants."""
    
    def test_menu_callbacks(self):
        """Test menu callback data."""
        assert CallbackData.MENU_MAIN == "menu:main"
        assert CallbackData.MENU_EYES == "menu:eyes"
        assert CallbackData.MENU_MOUTH == "menu:mouth"
    
    def test_action_callbacks(self):
        """Test action callback data format."""
        assert ":" in CallbackData.EYES_BLINK_1
        assert ":" in CallbackData.WINGS_WAVE_3
        assert ":" in CallbackData.SPIN_LEFT_90


class TestAPIClient:
    """Tests for the API client."""
    
    def test_client_initialization(self):
        """Test API client initializes correctly."""
        client = TuxAPIClient("http://localhost:8000")
        assert client.base_url == "http://localhost:8000"
        assert client.timeout == 10.0
    
    def test_client_base_url_trailing_slash(self):
        """Test API client removes trailing slash from base URL."""
        client = TuxAPIClient("http://localhost:8000/")
        assert client.base_url == "http://localhost:8000"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


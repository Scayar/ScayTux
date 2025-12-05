"""
TUX Droid AI Control - Mock Driver
==================================

Mock driver implementation for development and testing without
actual TUX Droid hardware connected.
"""

import logging
import time
from typing import Dict, Any, List
from datetime import datetime

# Import from parent package
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tux.driver import TuxDriverInterface
from tux.actions import TuxAction, ActionType, FIRMWARE_COMMANDS

logger = logging.getLogger(__name__)


class MockTuxDriver(TuxDriverInterface):
    """
    Mock TUX Droid driver for development without hardware.
    
    This driver simulates TUX Droid behavior by logging all commands
    and maintaining a simulated state. Useful for:
    - Development on machines without TUX connected
    - Testing the API and bot without hardware
    - Demonstrating the system
    
    Example:
        driver = MockTuxDriver()
        driver.connect()
        driver.execute_action(TuxAction.blink_eyes(3))
        print(driver.get_action_history())
    """
    
    def __init__(self, simulate_delay: bool = True, delay_ms: int = 100):
        """
        Initialize the mock driver.
        
        Args:
            simulate_delay: Whether to add realistic delays
            delay_ms: Simulated delay in milliseconds
        """
        self._connected = False
        self._simulate_delay = simulate_delay
        self._delay_ms = delay_ms
        
        # Track simulated state
        self._state = {
            "eyes": "open",
            "mouth": "closed",
            "wings": "lowered",
            "leds_left": "off",
            "leds_right": "off",
            "sleeping": False,
            "rotation": 0,
        }
        
        # Action history for debugging
        self._action_history: List[Dict[str, Any]] = []
        
        logger.info("MockTuxDriver initialized (simulation mode)")
    
    def connect(self) -> bool:
        """Simulate connection to TUX Droid."""
        logger.info("🐧 [MOCK] Connecting to virtual TUX Droid...")
        self._simulate_action_delay()
        self._connected = True
        self._log_action("CONNECT", {}, "Connected to virtual TUX Droid")
        logger.info("🐧 [MOCK] Successfully connected to virtual TUX Droid!")
        return True
    
    def disconnect(self) -> bool:
        """Simulate disconnection from TUX Droid."""
        logger.info("🐧 [MOCK] Disconnecting from virtual TUX Droid...")
        self._connected = False
        self._log_action("DISCONNECT", {}, "Disconnected from virtual TUX Droid")
        logger.info("🐧 [MOCK] Disconnected from virtual TUX Droid")
        return True
    
    def is_connected(self) -> bool:
        """Check if connected to virtual TUX Droid."""
        return self._connected
    
    def send_command(self, command: bytes) -> bool:
        """Simulate sending raw command bytes."""
        if not self._connected:
            logger.warning("🐧 [MOCK] Cannot send command: Not connected")
            return False
        
        self._simulate_action_delay()
        logger.debug(f"🐧 [MOCK] Sent raw command: {command.hex()}")
        return True
    
    def execute_action(self, action: TuxAction) -> bool:
        """
        Simulate executing a TUX action.
        
        This method logs the action and updates the simulated state.
        """
        if not self._connected:
            logger.warning("🐧 [MOCK] Cannot execute action: Not connected")
            return False
        
        self._simulate_action_delay()
        
        # Get action details
        action_type = action.action_type
        params = action.params
        
        # Update simulated state based on action
        state_message = self._update_state(action_type, params)
        
        # Log the action
        self._log_action(action_type.value, params, state_message)
        
        # Print visual feedback
        self._print_visual_feedback(action_type, params)
        
        logger.info(f"🐧 [MOCK] Executed: {action_type.value} | {state_message}")
        return True
    
    def _update_state(self, action_type: ActionType, params: Dict[str, Any]) -> str:
        """Update simulated TUX state based on action."""
        
        # Eye actions
        if action_type == ActionType.BLINK_EYES:
            count = params.get("count", 1)
            return f"Eyes blinked {count} time(s)"
        elif action_type == ActionType.OPEN_EYES:
            self._state["eyes"] = "open"
            return "Eyes are now open"
        elif action_type == ActionType.CLOSE_EYES:
            self._state["eyes"] = "closed"
            return "Eyes are now closed"
        elif action_type == ActionType.STOP_EYES:
            return "Eye movement stopped"
        
        # Mouth actions
        elif action_type == ActionType.MOVE_MOUTH:
            count = params.get("count", 1)
            return f"Mouth moved {count} time(s)"
        elif action_type == ActionType.OPEN_MOUTH:
            self._state["mouth"] = "open"
            return "Mouth is now open"
        elif action_type == ActionType.CLOSE_MOUTH:
            self._state["mouth"] = "closed"
            return "Mouth is now closed"
        elif action_type == ActionType.STOP_MOUTH:
            return "Mouth movement stopped"
        
        # Wing actions
        elif action_type == ActionType.WAVE_WINGS:
            count = params.get("count", 1)
            speed = params.get("speed", 3)
            return f"Wings waved {count} time(s) at speed {speed}"
        elif action_type == ActionType.RAISE_WINGS:
            self._state["wings"] = "raised"
            return "Wings are now raised"
        elif action_type == ActionType.LOWER_WINGS:
            self._state["wings"] = "lowered"
            return "Wings are now lowered"
        elif action_type == ActionType.STOP_WINGS:
            return "Wing movement stopped"
        elif action_type == ActionType.RESET_WINGS:
            self._state["wings"] = "lowered"
            return "Wings reset to default position"
        
        # Spin actions
        elif action_type == ActionType.SPIN_LEFT:
            angle = params.get("angle", 4)
            speed = params.get("speed", 3)
            self._state["rotation"] = (self._state["rotation"] - angle * 45) % 360
            return f"Spun left {angle} units at speed {speed}"
        elif action_type == ActionType.SPIN_RIGHT:
            angle = params.get("angle", 4)
            speed = params.get("speed", 3)
            self._state["rotation"] = (self._state["rotation"] + angle * 45) % 360
            return f"Spun right {angle} units at speed {speed}"
        elif action_type == ActionType.STOP_SPIN:
            return "Spinning stopped"
        
        # LED actions
        elif action_type == ActionType.LED_ON:
            target = params.get("target", "both")
            if target in ["both", "left"]:
                self._state["leds_left"] = "on"
            if target in ["both", "right"]:
                self._state["leds_right"] = "on"
            return f"LED(s) {target} turned on"
        elif action_type == ActionType.LED_OFF:
            target = params.get("target", "both")
            if target in ["both", "left"]:
                self._state["leds_left"] = "off"
            if target in ["both", "right"]:
                self._state["leds_right"] = "off"
            return f"LED(s) {target} turned off"
        elif action_type == ActionType.LED_TOGGLE:
            count = params.get("count", 1)
            return f"LEDs toggled {count} time(s)"
        elif action_type == ActionType.LED_PULSE:
            count = params.get("count", 5)
            return f"LEDs pulsed {count} time(s)"
        
        # Sound actions
        elif action_type == ActionType.PLAY_SOUND:
            sound_num = params.get("sound_number", 0)
            volume = params.get("volume", 100)
            return f"Playing sound #{sound_num} at volume {volume}"
        elif action_type == ActionType.MUTE:
            return "Audio muted"
        elif action_type == ActionType.UNMUTE:
            return "Audio unmuted"
        
        # Sleep actions
        elif action_type == ActionType.SLEEP:
            mode = params.get("mode", "normal")
            self._state["sleeping"] = True
            return f"TUX is now sleeping (mode: {mode})"
        elif action_type == ActionType.WAKE_UP:
            self._state["sleeping"] = False
            return "TUX is now awake"
        
        return f"Action {action_type.value} executed"
    
    def _print_visual_feedback(self, action_type: ActionType, params: Dict[str, Any]):
        """Print ASCII art feedback for actions."""
        
        visuals = {
            ActionType.BLINK_EYES: "👀 *blink blink*",
            ActionType.OPEN_EYES: "👁️👁️ Eyes wide open!",
            ActionType.CLOSE_EYES: "😌 Eyes closed...",
            ActionType.OPEN_MOUTH: "😮 Mouth open!",
            ActionType.CLOSE_MOUTH: "😶 Mouth closed",
            ActionType.MOVE_MOUTH: "🗣️ *chomp chomp*",
            ActionType.WAVE_WINGS: "🐧 *flap flap flap*",
            ActionType.RAISE_WINGS: "🙌 Wings up!",
            ActionType.LOWER_WINGS: "🐧 Wings down",
            ActionType.SPIN_LEFT: "↩️ Spinning left...",
            ActionType.SPIN_RIGHT: "↪️ Spinning right...",
            ActionType.LED_ON: "💡 LEDs ON",
            ActionType.LED_OFF: "🔌 LEDs OFF",
            ActionType.LED_TOGGLE: "✨ *blink blink*",
            ActionType.LED_PULSE: "🌟 *pulse pulse*",
            ActionType.PLAY_SOUND: "🔊 Playing sound...",
            ActionType.SLEEP: "😴 Zzz...",
            ActionType.WAKE_UP: "⏰ Good morning!",
        }
        
        visual = visuals.get(action_type, "🐧 TUX is doing something!")
        print(f"\n    {visual}\n")
    
    def _log_action(self, action: str, params: Dict[str, Any], message: str):
        """Log an action to history."""
        self._action_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "params": params,
            "message": message,
            "state_snapshot": self._state.copy()
        })
    
    def _simulate_action_delay(self):
        """Add simulated delay for realism."""
        if self._simulate_delay:
            time.sleep(self._delay_ms / 1000.0)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current virtual TUX status."""
        return {
            "connected": self._connected,
            "driver_type": "mock",
            "simulated_state": self._state.copy(),
            "actions_executed": len(self._action_history)
        }
    
    def get_action_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of all executed actions.
        
        Returns:
            list: List of action records with timestamps
        """
        return self._action_history.copy()
    
    def clear_history(self):
        """Clear the action history."""
        self._action_history.clear()
        logger.info("🐧 [MOCK] Action history cleared")
    
    def get_simulated_state(self) -> Dict[str, Any]:
        """
        Get the current simulated state of TUX.
        
        Returns:
            dict: Current state (eyes, mouth, wings, LEDs, etc.)
        """
        return self._state.copy()
    
    def reset_state(self):
        """Reset simulated state to defaults."""
        self._state = {
            "eyes": "open",
            "mouth": "closed",
            "wings": "lowered",
            "leds_left": "off",
            "leds_right": "off",
            "sleeping": False,
            "rotation": 0,
        }
        logger.info("🐧 [MOCK] State reset to defaults")


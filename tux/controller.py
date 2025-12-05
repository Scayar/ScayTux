"""
TUX Droid AI Control - High-Level Controller
============================================

This module provides a high-level interface for controlling TUX Droid.
It wraps the driver layer and provides easy-to-use methods.
"""

import logging
from typing import Optional, Dict, Any

from .actions import TuxAction, ActionType, LEDTarget, SleepMode
from .driver import TuxDriverInterface, TuxDriver

logger = logging.getLogger(__name__)


class TuxController:
    """
    High-level controller for TUX Droid.
    
    This class provides a clean, easy-to-use interface for controlling
    TUX Droid. It handles driver initialization, connection management,
    and provides high-level methods for all TUX actions.
    
    Example:
        controller = TuxController(driver)
        controller.connect()
        controller.wave_wings(count=3, speed=4)
        controller.blink_eyes(count=2)
        controller.disconnect()
    """
    
    def __init__(self, driver: TuxDriverInterface):
        """
        Initialize the TUX controller.
        
        Args:
            driver: The driver implementation to use
        """
        self.driver = driver
        self._last_action: Optional[TuxAction] = None
        logger.info("TuxController initialized")
    
    def connect(self) -> bool:
        """
        Connect to TUX Droid.
        
        Returns:
            bool: True if connection successful
        """
        result = self.driver.connect()
        if result:
            logger.info("TuxController: Connected to TUX Droid")
        return result
    
    def disconnect(self) -> bool:
        """
        Disconnect from TUX Droid.
        
        Returns:
            bool: True if disconnection successful
        """
        result = self.driver.disconnect()
        if result:
            logger.info("TuxController: Disconnected from TUX Droid")
        return result
    
    def is_connected(self) -> bool:
        """Check if connected to TUX Droid."""
        return self.driver.is_connected()
    
    def _execute(self, action: TuxAction) -> Dict[str, Any]:
        """
        Execute an action and return result.
        
        Args:
            action: The action to execute
            
        Returns:
            dict: Result with success status and details
        """
        self._last_action = action
        
        try:
            success = self.driver.execute_action(action)
            return {
                "success": success,
                "action": action.action_type.value,
                "params": action.params,
                "message": f"Action '{action.action_type.value}' executed successfully" if success else "Action failed"
            }
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return {
                "success": False,
                "action": action.action_type.value,
                "params": action.params,
                "message": str(e)
            }
    
    # ==========================================
    # Eye Controls
    # ==========================================
    
    def blink_eyes(self, count: int = 1) -> Dict[str, Any]:
        """
        Blink TUX's eyes.
        
        Args:
            count: Number of blinks
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Blinking eyes {count} time(s)")
        return self._execute(TuxAction.blink_eyes(count))
    
    def open_eyes(self) -> Dict[str, Any]:
        """Open TUX's eyes."""
        logger.info("Opening eyes")
        return self._execute(TuxAction.open_eyes())
    
    def close_eyes(self) -> Dict[str, Any]:
        """Close TUX's eyes."""
        logger.info("Closing eyes")
        return self._execute(TuxAction.close_eyes())
    
    def stop_eyes(self) -> Dict[str, Any]:
        """Stop eye movement."""
        logger.info("Stopping eyes")
        return self._execute(TuxAction(ActionType.STOP_EYES, {}))
    
    # ==========================================
    # Mouth Controls
    # ==========================================
    
    def move_mouth(self, count: int = 1) -> Dict[str, Any]:
        """
        Move TUX's mouth.
        
        Args:
            count: Number of movements
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Moving mouth {count} time(s)")
        return self._execute(TuxAction.move_mouth(count))
    
    def open_mouth(self) -> Dict[str, Any]:
        """Open TUX's mouth."""
        logger.info("Opening mouth")
        return self._execute(TuxAction.open_mouth())
    
    def close_mouth(self) -> Dict[str, Any]:
        """Close TUX's mouth."""
        logger.info("Closing mouth")
        return self._execute(TuxAction.close_mouth())
    
    def stop_mouth(self) -> Dict[str, Any]:
        """Stop mouth movement."""
        logger.info("Stopping mouth")
        return self._execute(TuxAction(ActionType.STOP_MOUTH, {}))
    
    # ==========================================
    # Wing/Flipper Controls
    # ==========================================
    
    def wave_wings(self, count: int = 1, speed: int = 3) -> Dict[str, Any]:
        """
        Wave TUX's wings/flippers.
        
        Args:
            count: Number of waves
            speed: Speed of movement (1-5, slow to fast)
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Waving wings {count} time(s) at speed {speed}")
        return self._execute(TuxAction.wave_wings(count, speed))
    
    def raise_wings(self) -> Dict[str, Any]:
        """Raise TUX's wings to upper position."""
        logger.info("Raising wings")
        return self._execute(TuxAction.raise_wings())
    
    def lower_wings(self) -> Dict[str, Any]:
        """Lower TUX's wings to lower position."""
        logger.info("Lowering wings")
        return self._execute(TuxAction.lower_wings())
    
    def stop_wings(self) -> Dict[str, Any]:
        """Stop wing movement."""
        logger.info("Stopping wings")
        return self._execute(TuxAction(ActionType.STOP_WINGS, {}))
    
    def reset_wings(self) -> Dict[str, Any]:
        """Reset wings to default position."""
        logger.info("Resetting wings")
        return self._execute(TuxAction(ActionType.RESET_WINGS, {}))
    
    # ==========================================
    # Spin/Rotation Controls
    # ==========================================
    
    def spin_left(self, angle: int = 4, speed: int = 3) -> Dict[str, Any]:
        """
        Spin TUX to the left.
        
        Args:
            angle: Angle to turn (unit is ~1/8th of full turn)
            speed: Speed of rotation (1-5)
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Spinning left: angle={angle}, speed={speed}")
        return self._execute(TuxAction.spin_left(angle, speed))
    
    def spin_right(self, angle: int = 4, speed: int = 3) -> Dict[str, Any]:
        """
        Spin TUX to the right.
        
        Args:
            angle: Angle to turn (unit is ~1/8th of full turn)
            speed: Speed of rotation (1-5)
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Spinning right: angle={angle}, speed={speed}")
        return self._execute(TuxAction.spin_right(angle, speed))
    
    def stop_spin(self) -> Dict[str, Any]:
        """Stop spinning."""
        logger.info("Stopping spin")
        return self._execute(TuxAction(ActionType.STOP_SPIN, {}))
    
    # ==========================================
    # LED Controls
    # ==========================================
    
    def led_on(self, target: str = "both") -> Dict[str, Any]:
        """
        Turn on LEDs.
        
        Args:
            target: Which LEDs ("both", "left", "right")
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Turning on LEDs: {target}")
        led_target = LEDTarget(target)
        return self._execute(TuxAction.led_on(led_target))
    
    def led_off(self, target: str = "both") -> Dict[str, Any]:
        """
        Turn off LEDs.
        
        Args:
            target: Which LEDs ("both", "left", "right")
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Turning off LEDs: {target}")
        led_target = LEDTarget(target)
        return self._execute(TuxAction.led_off(led_target))
    
    def led_toggle(self, count: int = 1, delay: int = 25) -> Dict[str, Any]:
        """
        Toggle LEDs.
        
        Args:
            count: Number of toggles
            delay: Delay between toggles (in 4ms units)
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Toggling LEDs {count} time(s)")
        return self._execute(TuxAction.led_toggle(count, delay))
    
    def led_pulse(self, target: str = "both", count: int = 5, 
                  pulse_width: int = 10) -> Dict[str, Any]:
        """
        Pulse LEDs with fading effect.
        
        Args:
            target: Which LEDs ("both", "left", "right")
            count: Number of pulses
            pulse_width: Width of pulse
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Pulsing LEDs: target={target}, count={count}")
        led_target = LEDTarget(target)
        return self._execute(TuxAction.led_pulse(led_target, count, pulse_width))
    
    # ==========================================
    # Sound Controls
    # ==========================================
    
    def play_sound(self, sound_number: int = 0, volume: int = 100) -> Dict[str, Any]:
        """
        Play a sound from TUX's flash memory.
        
        Args:
            sound_number: Index of sound to play
            volume: Volume level (0-100)
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Playing sound {sound_number} at volume {volume}")
        return self._execute(TuxAction.play_sound(sound_number, volume))
    
    def mute(self) -> Dict[str, Any]:
        """Mute TUX's audio."""
        logger.info("Muting audio")
        return self._execute(TuxAction(ActionType.MUTE, {"state": 1}))
    
    def unmute(self) -> Dict[str, Any]:
        """Unmute TUX's audio."""
        logger.info("Unmuting audio")
        return self._execute(TuxAction(ActionType.UNMUTE, {"state": 0}))
    
    # ==========================================
    # Sleep/Power Controls
    # ==========================================
    
    def sleep(self, mode: str = "normal") -> Dict[str, Any]:
        """
        Put TUX to sleep.
        
        Args:
            mode: Sleep mode ("awake", "quick", "normal", "deep")
            
        Returns:
            dict: Result of the action
        """
        logger.info(f"Putting TUX to sleep: mode={mode}")
        sleep_mode = SleepMode(mode)
        return self._execute(TuxAction.sleep(sleep_mode))
    
    def wake_up(self) -> Dict[str, Any]:
        """Wake TUX up from sleep."""
        logger.info("Waking up TUX")
        return self._execute(TuxAction.wake_up())
    
    # ==========================================
    # Status
    # ==========================================
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get TUX Droid status.
        
        Returns:
            dict: Current status information
        """
        driver_status = self.driver.get_status()
        return {
            **driver_status,
            "last_action": self._last_action.action_type.value if self._last_action else None
        }


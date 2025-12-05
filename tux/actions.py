"""
TUX Droid AI Control - Action Types and Mapping
===============================================

This module defines all TUX Droid actions and their parameters.
Based on the firmware commands from tuxcore/common/commands.h
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, Dict


class ActionType(str, Enum):
    """Enumeration of all available TUX Droid action types."""
    
    # Eye actions
    BLINK_EYES = "blink_eyes"
    OPEN_EYES = "open_eyes"
    CLOSE_EYES = "close_eyes"
    STOP_EYES = "stop_eyes"
    
    # Mouth actions
    MOVE_MOUTH = "move_mouth"
    OPEN_MOUTH = "open_mouth"
    CLOSE_MOUTH = "close_mouth"
    STOP_MOUTH = "stop_mouth"
    
    # Wing/Flipper actions
    WAVE_WINGS = "wave_wings"
    RAISE_WINGS = "raise_wings"
    LOWER_WINGS = "lower_wings"
    STOP_WINGS = "stop_wings"
    RESET_WINGS = "reset_wings"
    
    # Spin/Rotation actions
    SPIN_LEFT = "spin_left"
    SPIN_RIGHT = "spin_right"
    STOP_SPIN = "stop_spin"
    
    # LED actions
    LED_ON = "led_on"
    LED_OFF = "led_off"
    LED_TOGGLE = "led_toggle"
    LED_PULSE = "led_pulse"
    LED_SET_INTENSITY = "led_set_intensity"
    
    # Sound actions
    PLAY_SOUND = "play_sound"
    MUTE = "mute"
    UNMUTE = "unmute"
    
    # Sleep/Power actions
    SLEEP = "sleep"
    WAKE_UP = "wake_up"
    
    # IR actions
    IR_ON = "ir_on"
    IR_OFF = "ir_off"
    IR_SEND = "ir_send"


class LEDTarget(str, Enum):
    """LED target selection."""
    BOTH = "both"
    LEFT = "left"
    RIGHT = "right"


class SleepMode(str, Enum):
    """Sleep mode types from firmware."""
    AWAKE = "awake"
    QUICK = "quick"
    NORMAL = "normal"
    DEEP = "deep"


@dataclass
class TuxAction:
    """
    Represents a TUX Droid action with its parameters.
    
    Attributes:
        action_type: The type of action to perform
        params: Dictionary of action-specific parameters
    """
    action_type: ActionType
    params: Dict[str, Any]
    
    def __post_init__(self):
        """Validate action parameters."""
        if self.params is None:
            self.params = {}
    
    @classmethod
    def blink_eyes(cls, count: int = 1) -> "TuxAction":
        """Create a blink eyes action."""
        return cls(ActionType.BLINK_EYES, {"count": count})
    
    @classmethod
    def open_eyes(cls) -> "TuxAction":
        """Create an open eyes action."""
        return cls(ActionType.OPEN_EYES, {})
    
    @classmethod
    def close_eyes(cls) -> "TuxAction":
        """Create a close eyes action."""
        return cls(ActionType.CLOSE_EYES, {})
    
    @classmethod
    def move_mouth(cls, count: int = 1) -> "TuxAction":
        """Create a move mouth action."""
        return cls(ActionType.MOVE_MOUTH, {"count": count})
    
    @classmethod
    def open_mouth(cls) -> "TuxAction":
        """Create an open mouth action."""
        return cls(ActionType.OPEN_MOUTH, {})
    
    @classmethod
    def close_mouth(cls) -> "TuxAction":
        """Create a close mouth action."""
        return cls(ActionType.CLOSE_MOUTH, {})
    
    @classmethod
    def wave_wings(cls, count: int = 1, speed: int = 3) -> "TuxAction":
        """
        Create a wave wings action.
        
        Args:
            count: Number of wing movements
            speed: PWM speed value (1-5, where 1=slow, 5=fast)
        """
        return cls(ActionType.WAVE_WINGS, {"count": count, "speed": speed})
    
    @classmethod
    def raise_wings(cls) -> "TuxAction":
        """Create a raise wings action."""
        return cls(ActionType.RAISE_WINGS, {})
    
    @classmethod
    def lower_wings(cls) -> "TuxAction":
        """Create a lower wings action."""
        return cls(ActionType.LOWER_WINGS, {})
    
    @classmethod
    def spin_left(cls, angle: int = 4, speed: int = 3) -> "TuxAction":
        """
        Create a spin left action.
        
        Args:
            angle: Angle to turn (unit is ~1/8th of a full turn)
            speed: PWM speed value (1-5)
        """
        return cls(ActionType.SPIN_LEFT, {"angle": angle, "speed": speed})
    
    @classmethod
    def spin_right(cls, angle: int = 4, speed: int = 3) -> "TuxAction":
        """
        Create a spin right action.
        
        Args:
            angle: Angle to turn (unit is ~1/8th of a full turn)
            speed: PWM speed value (1-5)
        """
        return cls(ActionType.SPIN_RIGHT, {"angle": angle, "speed": speed})
    
    @classmethod
    def led_on(cls, target: LEDTarget = LEDTarget.BOTH) -> "TuxAction":
        """Create an LED on action."""
        return cls(ActionType.LED_ON, {"target": target.value})
    
    @classmethod
    def led_off(cls, target: LEDTarget = LEDTarget.BOTH) -> "TuxAction":
        """Create an LED off action."""
        return cls(ActionType.LED_OFF, {"target": target.value})
    
    @classmethod
    def led_toggle(cls, count: int = 1, delay: int = 25) -> "TuxAction":
        """
        Create an LED toggle action.
        
        Args:
            count: Number of toggles
            delay: Delay between toggles (in 4ms units)
        """
        return cls(ActionType.LED_TOGGLE, {"count": count, "delay": delay})
    
    @classmethod
    def led_pulse(cls, target: LEDTarget = LEDTarget.BOTH, 
                  count: int = 5, pulse_width: int = 10) -> "TuxAction":
        """Create an LED pulse action."""
        return cls(ActionType.LED_PULSE, {
            "target": target.value,
            "count": count,
            "pulse_width": pulse_width
        })
    
    @classmethod
    def play_sound(cls, sound_number: int = 0, volume: int = 100) -> "TuxAction":
        """
        Create a play sound action.
        
        Args:
            sound_number: Index of sound in flash memory
            volume: Volume level (0-100)
        """
        return cls(ActionType.PLAY_SOUND, {
            "sound_number": sound_number,
            "volume": volume
        })
    
    @classmethod
    def sleep(cls, mode: SleepMode = SleepMode.NORMAL) -> "TuxAction":
        """Create a sleep action."""
        return cls(ActionType.SLEEP, {"mode": mode.value})
    
    @classmethod
    def wake_up(cls) -> "TuxAction":
        """Create a wake up action."""
        return cls(ActionType.WAKE_UP, {})


# Firmware command codes (from commands.h)
# These map action types to raw command bytes
FIRMWARE_COMMANDS = {
    ActionType.BLINK_EYES: 0x40,
    ActionType.STOP_EYES: 0x32,
    ActionType.OPEN_EYES: 0x33,
    ActionType.CLOSE_EYES: 0x38,
    
    ActionType.MOVE_MOUTH: 0x41,
    ActionType.OPEN_MOUTH: 0x34,
    ActionType.CLOSE_MOUTH: 0x35,
    ActionType.STOP_MOUTH: 0x36,
    
    ActionType.WAVE_WINGS: 0x80,
    ActionType.STOP_WINGS: 0x30,
    ActionType.RESET_WINGS: 0x31,
    ActionType.RAISE_WINGS: 0x39,
    ActionType.LOWER_WINGS: 0x3A,
    
    ActionType.SPIN_LEFT: 0x82,
    ActionType.SPIN_RIGHT: 0x83,
    ActionType.STOP_SPIN: 0x37,
    
    ActionType.LED_ON: 0x1A,
    ActionType.LED_OFF: 0x1B,
    ActionType.LED_TOGGLE: 0x9A,
    
    ActionType.PLAY_SOUND: 0x90,
    ActionType.MUTE: 0x92,
    
    ActionType.SLEEP: 0xB7,
    ActionType.WAKE_UP: 0xB7,  # Same command, different params
    
    ActionType.IR_ON: 0x17,
    ActionType.IR_OFF: 0x18,
    ActionType.IR_SEND: 0x91,
}


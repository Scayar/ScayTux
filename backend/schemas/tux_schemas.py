"""
TUX Droid AI Control - Pydantic Schemas
=======================================

Request and response models for the TUX Droid API.
"""

from enum import Enum
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


# ==========================================
# Action Enums
# ==========================================

class EyesAction(str, Enum):
    """Available eye actions."""
    BLINK = "blink"
    OPEN = "open"
    CLOSE = "close"
    STOP = "stop"


class MouthAction(str, Enum):
    """Available mouth actions."""
    MOVE = "move"
    OPEN = "open"
    CLOSE = "close"
    STOP = "stop"


class WingsAction(str, Enum):
    """Available wing actions."""
    WAVE = "wave"
    RAISE = "raise"
    LOWER = "lower"
    STOP = "stop"
    RESET = "reset"


class SpinAction(str, Enum):
    """Available spin actions."""
    LEFT = "left"
    RIGHT = "right"
    STOP = "stop"


class LEDAction(str, Enum):
    """Available LED actions."""
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"
    PULSE = "pulse"


class LEDTarget(str, Enum):
    """LED target selection."""
    BOTH = "both"
    LEFT = "left"
    RIGHT = "right"


class SoundAction(str, Enum):
    """Available sound actions."""
    PLAY = "play"
    MUTE = "mute"
    UNMUTE = "unmute"


class SleepAction(str, Enum):
    """Available sleep actions."""
    SLEEP = "sleep"
    WAKE = "wake"


class SleepMode(str, Enum):
    """Sleep mode types."""
    AWAKE = "awake"
    QUICK = "quick"
    NORMAL = "normal"
    DEEP = "deep"


# ==========================================
# Request Models
# ==========================================

class EyesRequest(BaseModel):
    """Request model for eye actions."""
    action: EyesAction = Field(..., description="The eye action to perform")
    count: int = Field(default=1, ge=1, le=100, description="Number of repetitions (for blink)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "blink", "count": 3},
                {"action": "open"},
                {"action": "close"}
            ]
        }
    }


class MouthRequest(BaseModel):
    """Request model for mouth actions."""
    action: MouthAction = Field(..., description="The mouth action to perform")
    count: int = Field(default=1, ge=1, le=100, description="Number of movements (for move)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "move", "count": 5},
                {"action": "open"},
                {"action": "close"}
            ]
        }
    }


class WingsRequest(BaseModel):
    """Request model for wing actions."""
    action: WingsAction = Field(..., description="The wing action to perform")
    count: int = Field(default=1, ge=1, le=100, description="Number of waves (for wave)")
    speed: int = Field(default=3, ge=1, le=5, description="Speed of movement (1=slow, 5=fast)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "wave", "count": 3, "speed": 4},
                {"action": "raise"},
                {"action": "lower"}
            ]
        }
    }


class SpinRequest(BaseModel):
    """Request model for spin/rotation actions."""
    action: SpinAction = Field(..., description="The spin action to perform")
    angle: int = Field(default=4, ge=1, le=16, description="Angle to turn (~1/8th of full turn per unit)")
    speed: int = Field(default=3, ge=1, le=5, description="Speed of rotation (1=slow, 5=fast)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "left", "angle": 4, "speed": 3},
                {"action": "right", "angle": 8, "speed": 5}
            ]
        }
    }


class LEDRequest(BaseModel):
    """Request model for LED actions."""
    action: LEDAction = Field(..., description="The LED action to perform")
    target: LEDTarget = Field(default=LEDTarget.BOTH, description="Which LED(s) to control")
    count: int = Field(default=1, ge=1, le=100, description="Number of toggles/pulses")
    delay: int = Field(default=25, ge=1, le=255, description="Delay between toggles (4ms units)")
    pulse_width: int = Field(default=10, ge=1, le=255, description="Pulse width for pulse action")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "on", "target": "both"},
                {"action": "toggle", "count": 5, "delay": 50},
                {"action": "pulse", "target": "left", "count": 10}
            ]
        }
    }


class SoundRequest(BaseModel):
    """Request model for sound actions."""
    action: SoundAction = Field(..., description="The sound action to perform")
    sound_number: int = Field(default=0, ge=0, le=255, description="Sound index in flash memory")
    volume: int = Field(default=100, ge=0, le=100, description="Volume level (0-100)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "play", "sound_number": 1, "volume": 80},
                {"action": "mute"},
                {"action": "unmute"}
            ]
        }
    }


class SleepRequest(BaseModel):
    """Request model for sleep/wake actions."""
    action: SleepAction = Field(..., description="The sleep action to perform")
    mode: SleepMode = Field(default=SleepMode.NORMAL, description="Sleep mode type")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action": "sleep", "mode": "normal"},
                {"action": "wake"}
            ]
        }
    }


class SpeakRequest(BaseModel):
    """Request model for text-to-speech (future feature)."""
    text: str = Field(..., min_length=1, max_length=500, description="Text to speak")
    language: str = Field(default="en", description="Language code (e.g., 'en', 'fr', 'ar')")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed multiplier")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"text": "Hello, I am TUX!", "language": "en", "speed": 1.0}
            ]
        }
    }


class CustomActionRequest(BaseModel):
    """Request model for custom/raw actions."""
    action_type: str = Field(..., description="Action type identifier")
    params: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"action_type": "blink_eyes", "params": {"count": 5}}
            ]
        }
    }


# ==========================================
# Response Models
# ==========================================

class TuxResponse(BaseModel):
    """Standard response model for TUX actions."""
    success: bool = Field(..., description="Whether the action was successful")
    action: str = Field(..., description="The action that was performed")
    message: str = Field(..., description="Human-readable result message")
    params: Dict[str, Any] = Field(default_factory=dict, description="Action parameters used")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "action": "blink_eyes",
                    "message": "Action 'blink_eyes' executed successfully",
                    "params": {"count": 3}
                }
            ]
        }
    }


class TuxStatus(BaseModel):
    """TUX Droid status response model."""
    connected: bool = Field(..., description="Whether TUX is connected")
    driver_type: str = Field(..., description="Type of driver in use (mock/hardware)")
    device_path: Optional[str] = Field(None, description="USB device path (if applicable)")
    simulated_state: Optional[Dict[str, Any]] = Field(None, description="Simulated state (mock mode only)")
    last_action: Optional[str] = Field(None, description="Last executed action")
    actions_executed: Optional[int] = Field(None, description="Total actions executed (mock mode)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "connected": True,
                    "driver_type": "mock",
                    "simulated_state": {
                        "eyes": "open",
                        "mouth": "closed",
                        "wings": "lowered"
                    },
                    "last_action": "blink_eyes",
                    "actions_executed": 10
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="API health status")
    version: str = Field(..., description="API version")
    tux_connected: bool = Field(..., description="TUX connection status")
    mode: str = Field(..., description="Operating mode (DEV/PROD)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "version": "1.0.0",
                    "tux_connected": True,
                    "mode": "DEV"
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error type/code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


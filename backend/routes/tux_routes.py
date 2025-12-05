"""
TUX Droid AI Control - TUX Control Routes
=========================================

API endpoints for controlling TUX Droid.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from ..schemas.tux_schemas import (
    EyesRequest, EyesAction,
    MouthRequest, MouthAction,
    WingsRequest, WingsAction,
    SpinRequest, SpinAction,
    LEDRequest, LEDAction,
    SoundRequest, SoundAction,
    SleepRequest, SleepAction,
    SpeakRequest,
    CustomActionRequest,
    TuxResponse,
    ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tux", tags=["TUX Control"])


def get_tux_controller():
    """Dependency to get the TUX controller instance."""
    from ..main import tux_controller
    return tux_controller


def ensure_connected(controller) -> None:
    """Ensure TUX is connected, raise error if not."""
    if controller is None:
        raise HTTPException(
            status_code=503,
            detail="TUX controller not initialized"
        )
    if not controller.is_connected():
        raise HTTPException(
            status_code=503,
            detail="TUX Droid is not connected"
        )


def create_response(result: Dict[str, Any]) -> TuxResponse:
    """Create a TuxResponse from controller result."""
    return TuxResponse(
        success=result.get("success", False),
        action=result.get("action", "unknown"),
        message=result.get("message", ""),
        params=result.get("params", {})
    )


# ==========================================
# Eye Control Endpoints
# ==========================================

@router.post(
    "/eyes",
    response_model=TuxResponse,
    summary="Control Eyes",
    description="Control TUX's eyes: blink, open, close, or stop"
)
async def control_eyes(
    request: EyesRequest,
    controller=Depends(get_tux_controller)
):
    """
    Control TUX Droid's eyes.
    
    Actions:
    - **blink**: Blink eyes a specified number of times
    - **open**: Open eyes
    - **close**: Close eyes
    - **stop**: Stop eye movement
    """
    ensure_connected(controller)
    
    logger.info(f"Eyes request: {request.action.value}, count={request.count}")
    
    if request.action == EyesAction.BLINK:
        result = controller.blink_eyes(count=request.count)
    elif request.action == EyesAction.OPEN:
        result = controller.open_eyes()
    elif request.action == EyesAction.CLOSE:
        result = controller.close_eyes()
    elif request.action == EyesAction.STOP:
        result = controller.stop_eyes()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown eye action: {request.action}")
    
    return create_response(result)


# ==========================================
# Mouth Control Endpoints
# ==========================================

@router.post(
    "/mouth",
    response_model=TuxResponse,
    summary="Control Mouth",
    description="Control TUX's mouth: move, open, close, or stop"
)
async def control_mouth(
    request: MouthRequest,
    controller=Depends(get_tux_controller)
):
    """
    Control TUX Droid's mouth.
    
    Actions:
    - **move**: Move mouth a specified number of times
    - **open**: Open mouth
    - **close**: Close mouth
    - **stop**: Stop mouth movement
    """
    ensure_connected(controller)
    
    logger.info(f"Mouth request: {request.action.value}, count={request.count}")
    
    if request.action == MouthAction.MOVE:
        result = controller.move_mouth(count=request.count)
    elif request.action == MouthAction.OPEN:
        result = controller.open_mouth()
    elif request.action == MouthAction.CLOSE:
        result = controller.close_mouth()
    elif request.action == MouthAction.STOP:
        result = controller.stop_mouth()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown mouth action: {request.action}")
    
    return create_response(result)


# ==========================================
# Wing Control Endpoints
# ==========================================

@router.post(
    "/wings",
    response_model=TuxResponse,
    summary="Control Wings",
    description="Control TUX's wings/flippers: wave, raise, lower, stop, or reset"
)
async def control_wings(
    request: WingsRequest,
    controller=Depends(get_tux_controller)
):
    """
    Control TUX Droid's wings (flippers).
    
    Actions:
    - **wave**: Wave wings a specified number of times at given speed
    - **raise**: Raise wings to upper position
    - **lower**: Lower wings to lower position
    - **stop**: Stop wing movement
    - **reset**: Reset wings to default position
    """
    ensure_connected(controller)
    
    logger.info(f"Wings request: {request.action.value}, count={request.count}, speed={request.speed}")
    
    if request.action == WingsAction.WAVE:
        result = controller.wave_wings(count=request.count, speed=request.speed)
    elif request.action == WingsAction.RAISE:
        result = controller.raise_wings()
    elif request.action == WingsAction.LOWER:
        result = controller.lower_wings()
    elif request.action == WingsAction.STOP:
        result = controller.stop_wings()
    elif request.action == WingsAction.RESET:
        result = controller.reset_wings()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown wing action: {request.action}")
    
    return create_response(result)


# ==========================================
# Spin Control Endpoints
# ==========================================

@router.post(
    "/spin",
    response_model=TuxResponse,
    summary="Control Spin",
    description="Control TUX's rotation: spin left, right, or stop"
)
async def control_spin(
    request: SpinRequest,
    controller=Depends(get_tux_controller)
):
    """
    Control TUX Droid's spinning/rotation.
    
    Actions:
    - **left**: Spin left by specified angle at given speed
    - **right**: Spin right by specified angle at given speed
    - **stop**: Stop spinning
    
    Angle unit is approximately 1/8th of a full turn.
    """
    ensure_connected(controller)
    
    logger.info(f"Spin request: {request.action.value}, angle={request.angle}, speed={request.speed}")
    
    if request.action == SpinAction.LEFT:
        result = controller.spin_left(angle=request.angle, speed=request.speed)
    elif request.action == SpinAction.RIGHT:
        result = controller.spin_right(angle=request.angle, speed=request.speed)
    elif request.action == SpinAction.STOP:
        result = controller.stop_spin()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown spin action: {request.action}")
    
    return create_response(result)


# ==========================================
# LED Control Endpoints
# ==========================================

@router.post(
    "/leds",
    response_model=TuxResponse,
    summary="Control LEDs",
    description="Control TUX's eye LEDs: on, off, toggle, or pulse"
)
async def control_leds(
    request: LEDRequest,
    controller=Depends(get_tux_controller)
):
    """
    Control TUX Droid's eye LEDs.
    
    Actions:
    - **on**: Turn LED(s) on
    - **off**: Turn LED(s) off
    - **toggle**: Toggle LED(s) on/off
    - **pulse**: Pulse LED(s) with fading effect
    
    Target can be: both, left, or right
    """
    ensure_connected(controller)
    
    logger.info(f"LED request: {request.action.value}, target={request.target.value}")
    
    if request.action == LEDAction.ON:
        result = controller.led_on(target=request.target.value)
    elif request.action == LEDAction.OFF:
        result = controller.led_off(target=request.target.value)
    elif request.action == LEDAction.TOGGLE:
        result = controller.led_toggle(count=request.count, delay=request.delay)
    elif request.action == LEDAction.PULSE:
        result = controller.led_pulse(
            target=request.target.value,
            count=request.count,
            pulse_width=request.pulse_width
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unknown LED action: {request.action}")
    
    return create_response(result)


# ==========================================
# Sound Control Endpoints
# ==========================================

@router.post(
    "/sound",
    response_model=TuxResponse,
    summary="Control Sound",
    description="Control TUX's sound: play, mute, or unmute"
)
async def control_sound(
    request: SoundRequest,
    controller=Depends(get_tux_controller)
):
    """
    Control TUX Droid's sound.
    
    Actions:
    - **play**: Play a sound from flash memory
    - **mute**: Mute audio output
    - **unmute**: Unmute audio output
    """
    ensure_connected(controller)
    
    logger.info(f"Sound request: {request.action.value}")
    
    if request.action == SoundAction.PLAY:
        result = controller.play_sound(
            sound_number=request.sound_number,
            volume=request.volume
        )
    elif request.action == SoundAction.MUTE:
        result = controller.mute()
    elif request.action == SoundAction.UNMUTE:
        result = controller.unmute()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown sound action: {request.action}")
    
    return create_response(result)


# ==========================================
# Sleep Control Endpoints
# ==========================================

@router.post(
    "/sleep",
    response_model=TuxResponse,
    summary="Control Sleep",
    description="Control TUX's sleep mode: sleep or wake"
)
async def control_sleep(
    request: SleepRequest,
    controller=Depends(get_tux_controller)
):
    """
    Control TUX Droid's sleep state.
    
    Actions:
    - **sleep**: Put TUX to sleep (modes: awake, quick, normal, deep)
    - **wake**: Wake TUX up
    """
    ensure_connected(controller)
    
    logger.info(f"Sleep request: {request.action.value}, mode={request.mode.value}")
    
    if request.action == SleepAction.SLEEP:
        result = controller.sleep(mode=request.mode.value)
    elif request.action == SleepAction.WAKE:
        result = controller.wake_up()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown sleep action: {request.action}")
    
    return create_response(result)


# ==========================================
# Text-to-Speech Endpoint (Future Feature)
# ==========================================

@router.post(
    "/speak",
    response_model=TuxResponse,
    summary="Text-to-Speech (Future)",
    description="Make TUX speak text - placeholder for future TTS integration"
)
async def speak_text(
    request: SpeakRequest,
    controller=Depends(get_tux_controller)
):
    """
    Make TUX Droid speak text.
    
    **Note**: This is a placeholder for future TTS integration.
    Currently simulates mouth movement while "speaking".
    """
    ensure_connected(controller)
    
    logger.info(f"Speak request: '{request.text}' in {request.language}")
    
    # For now, just move the mouth to simulate speaking
    # Future: integrate with TTS engine
    word_count = len(request.text.split())
    result = controller.move_mouth(count=min(word_count * 2, 20))
    
    # Modify the result message
    result["message"] = f"TTS placeholder: '{request.text[:50]}...' (mouth moved {word_count * 2} times)"
    result["params"]["text"] = request.text
    result["params"]["language"] = request.language
    
    return create_response(result)


# ==========================================
# Custom Action Endpoint
# ==========================================

@router.post(
    "/custom",
    response_model=TuxResponse,
    summary="Custom Action",
    description="Execute a custom/raw TUX action"
)
async def custom_action(
    request: CustomActionRequest,
    controller=Depends(get_tux_controller)
):
    """
    Execute a custom TUX Droid action.
    
    This endpoint allows sending raw action types with custom parameters.
    Useful for advanced users or testing new actions.
    """
    ensure_connected(controller)
    
    logger.info(f"Custom action request: {request.action_type} with params {request.params}")
    
    # Map action_type string to controller method
    action_map = {
        "blink_eyes": lambda: controller.blink_eyes(request.params.get("count", 1)),
        "open_eyes": lambda: controller.open_eyes(),
        "close_eyes": lambda: controller.close_eyes(),
        "move_mouth": lambda: controller.move_mouth(request.params.get("count", 1)),
        "open_mouth": lambda: controller.open_mouth(),
        "close_mouth": lambda: controller.close_mouth(),
        "wave_wings": lambda: controller.wave_wings(
            request.params.get("count", 1),
            request.params.get("speed", 3)
        ),
        "raise_wings": lambda: controller.raise_wings(),
        "lower_wings": lambda: controller.lower_wings(),
        "spin_left": lambda: controller.spin_left(
            request.params.get("angle", 4),
            request.params.get("speed", 3)
        ),
        "spin_right": lambda: controller.spin_right(
            request.params.get("angle", 4),
            request.params.get("speed", 3)
        ),
        "led_on": lambda: controller.led_on(request.params.get("target", "both")),
        "led_off": lambda: controller.led_off(request.params.get("target", "both")),
        "led_toggle": lambda: controller.led_toggle(
            request.params.get("count", 1),
            request.params.get("delay", 25)
        ),
        "play_sound": lambda: controller.play_sound(
            request.params.get("sound_number", 0),
            request.params.get("volume", 100)
        ),
        "sleep": lambda: controller.sleep(request.params.get("mode", "normal")),
        "wake_up": lambda: controller.wake_up(),
    }
    
    action_func = action_map.get(request.action_type)
    if action_func is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown action type: {request.action_type}. "
                   f"Available: {list(action_map.keys())}"
        )
    
    result = action_func()
    return create_response(result)


# ==========================================
# Connection Control Endpoints
# ==========================================

@router.post(
    "/connect",
    response_model=TuxResponse,
    summary="Connect to TUX",
    description="Establish connection to TUX Droid"
)
async def connect_tux(controller=Depends(get_tux_controller)):
    """Connect to TUX Droid."""
    if controller is None:
        raise HTTPException(status_code=503, detail="TUX controller not initialized")
    
    success = controller.connect()
    return TuxResponse(
        success=success,
        action="connect",
        message="Connected to TUX Droid" if success else "Failed to connect",
        params={}
    )


@router.post(
    "/disconnect",
    response_model=TuxResponse,
    summary="Disconnect from TUX",
    description="Disconnect from TUX Droid"
)
async def disconnect_tux(controller=Depends(get_tux_controller)):
    """Disconnect from TUX Droid."""
    if controller is None:
        raise HTTPException(status_code=503, detail="TUX controller not initialized")
    
    success = controller.disconnect()
    return TuxResponse(
        success=success,
        action="disconnect",
        message="Disconnected from TUX Droid" if success else "Failed to disconnect",
        params={}
    )


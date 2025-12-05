"""
TUX Droid AI Control - API Client
=================================

HTTP client for communicating with the TUX backend API.
"""

import logging
from typing import Dict, Any, Optional

import httpx

logger = logging.getLogger(__name__)


class TuxAPIClient:
    """
    HTTP client for the TUX Droid backend API.
    
    Provides methods for all TUX control endpoints with
    error handling and logging.
    
    Example:
        client = TuxAPIClient("http://localhost:8000")
        result = await client.blink_eyes(count=3)
        print(result)
    """
    
    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the backend API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        logger.info(f"TuxAPIClient initialized with base URL: {self.base_url}")
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the backend.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: JSON body data
            
        Returns:
            dict: Response data
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=json_data
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.ConnectError:
            logger.error(f"Connection error: Could not connect to {url}")
            return {
                "success": False,
                "error": "connection_error",
                "message": f"Could not connect to backend at {self.base_url}"
            }
        except httpx.TimeoutException:
            logger.error(f"Timeout error: Request to {url} timed out")
            return {
                "success": False,
                "error": "timeout",
                "message": "Request timed out"
            }
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return {
                "success": False,
                "error": f"http_{e.response.status_code}",
                "message": e.response.text
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": "unknown",
                "message": str(e)
            }
    
    # ==========================================
    # Health & Status
    # ==========================================
    
    async def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        return await self._request("GET", "/health")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get TUX Droid status."""
        return await self._request("GET", "/status")
    
    # ==========================================
    # Connection
    # ==========================================
    
    async def connect(self) -> Dict[str, Any]:
        """Connect to TUX Droid."""
        return await self._request("POST", "/tux/connect")
    
    async def disconnect(self) -> Dict[str, Any]:
        """Disconnect from TUX Droid."""
        return await self._request("POST", "/tux/disconnect")
    
    # ==========================================
    # Eye Controls
    # ==========================================
    
    async def blink_eyes(self, count: int = 1) -> Dict[str, Any]:
        """Blink TUX's eyes."""
        return await self._request("POST", "/tux/eyes", {
            "action": "blink",
            "count": count
        })
    
    async def open_eyes(self) -> Dict[str, Any]:
        """Open TUX's eyes."""
        return await self._request("POST", "/tux/eyes", {"action": "open"})
    
    async def close_eyes(self) -> Dict[str, Any]:
        """Close TUX's eyes."""
        return await self._request("POST", "/tux/eyes", {"action": "close"})
    
    # ==========================================
    # Mouth Controls
    # ==========================================
    
    async def move_mouth(self, count: int = 1) -> Dict[str, Any]:
        """Move TUX's mouth."""
        return await self._request("POST", "/tux/mouth", {
            "action": "move",
            "count": count
        })
    
    async def open_mouth(self) -> Dict[str, Any]:
        """Open TUX's mouth."""
        return await self._request("POST", "/tux/mouth", {"action": "open"})
    
    async def close_mouth(self) -> Dict[str, Any]:
        """Close TUX's mouth."""
        return await self._request("POST", "/tux/mouth", {"action": "close"})
    
    # ==========================================
    # Wing Controls
    # ==========================================
    
    async def wave_wings(self, count: int = 1, speed: int = 3) -> Dict[str, Any]:
        """Wave TUX's wings."""
        return await self._request("POST", "/tux/wings", {
            "action": "wave",
            "count": count,
            "speed": speed
        })
    
    async def raise_wings(self) -> Dict[str, Any]:
        """Raise TUX's wings."""
        return await self._request("POST", "/tux/wings", {"action": "raise"})
    
    async def lower_wings(self) -> Dict[str, Any]:
        """Lower TUX's wings."""
        return await self._request("POST", "/tux/wings", {"action": "lower"})
    
    # ==========================================
    # Spin Controls
    # ==========================================
    
    async def spin_left(self, angle: int = 4, speed: int = 3) -> Dict[str, Any]:
        """Spin TUX left."""
        return await self._request("POST", "/tux/spin", {
            "action": "left",
            "angle": angle,
            "speed": speed
        })
    
    async def spin_right(self, angle: int = 4, speed: int = 3) -> Dict[str, Any]:
        """Spin TUX right."""
        return await self._request("POST", "/tux/spin", {
            "action": "right",
            "angle": angle,
            "speed": speed
        })
    
    # ==========================================
    # LED Controls
    # ==========================================
    
    async def led_on(self, target: str = "both") -> Dict[str, Any]:
        """Turn LEDs on."""
        return await self._request("POST", "/tux/leds", {
            "action": "on",
            "target": target
        })
    
    async def led_off(self, target: str = "both") -> Dict[str, Any]:
        """Turn LEDs off."""
        return await self._request("POST", "/tux/leds", {
            "action": "off",
            "target": target
        })
    
    async def led_toggle(self, count: int = 3, delay: int = 25) -> Dict[str, Any]:
        """Toggle LEDs."""
        return await self._request("POST", "/tux/leds", {
            "action": "toggle",
            "count": count,
            "delay": delay
        })
    
    async def led_pulse(self, target: str = "both", count: int = 5) -> Dict[str, Any]:
        """Pulse LEDs."""
        return await self._request("POST", "/tux/leds", {
            "action": "pulse",
            "target": target,
            "count": count
        })
    
    # ==========================================
    # Sound Controls
    # ==========================================
    
    async def play_sound(self, sound_number: int = 0, volume: int = 100) -> Dict[str, Any]:
        """Play a sound."""
        return await self._request("POST", "/tux/sound", {
            "action": "play",
            "sound_number": sound_number,
            "volume": volume
        })
    
    async def mute(self) -> Dict[str, Any]:
        """Mute audio."""
        return await self._request("POST", "/tux/sound", {"action": "mute"})
    
    async def unmute(self) -> Dict[str, Any]:
        """Unmute audio."""
        return await self._request("POST", "/tux/sound", {"action": "unmute"})
    
    # ==========================================
    # Sleep Controls
    # ==========================================
    
    async def sleep(self, mode: str = "normal") -> Dict[str, Any]:
        """Put TUX to sleep."""
        return await self._request("POST", "/tux/sleep", {
            "action": "sleep",
            "mode": mode
        })
    
    async def wake_up(self) -> Dict[str, Any]:
        """Wake TUX up."""
        return await self._request("POST", "/tux/sleep", {"action": "wake"})
    
    # ==========================================
    # Custom Actions
    # ==========================================
    
    async def custom_action(
        self,
        action_type: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a custom action."""
        return await self._request("POST", "/tux/custom", {
            "action_type": action_type,
            "params": params or {}
        })
    
    # ==========================================
    # Text-to-Speech
    # ==========================================
    
    async def speak(
        self,
        text: str,
        language: str = "en",
        speed: float = 1.0
    ) -> Dict[str, Any]:
        """Make TUX speak text."""
        return await self._request("POST", "/tux/speak", {
            "text": text,
            "language": language,
            "speed": speed
        })


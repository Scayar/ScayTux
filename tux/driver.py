"""
TUX Droid AI Control - Driver Interface
=======================================

This module defines the abstract driver interface for communicating
with TUX Droid hardware.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict

from .actions import TuxAction, ActionType, FIRMWARE_COMMANDS

logger = logging.getLogger(__name__)


class TuxDriverInterface(ABC):
    """
    Abstract base class defining the TUX Droid driver interface.
    
    All driver implementations (real hardware or mock) must implement
    these methods.
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to TUX Droid.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Disconnect from TUX Droid.
        
        Returns:
            bool: True if disconnection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if currently connected to TUX Droid.
        
        Returns:
            bool: True if connected, False otherwise
        """
        pass
    
    @abstractmethod
    def send_command(self, command: bytes) -> bool:
        """
        Send raw command bytes to TUX Droid.
        
        Args:
            command: Raw command bytes to send
            
        Returns:
            bool: True if command sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def execute_action(self, action: TuxAction) -> bool:
        """
        Execute a high-level TUX action.
        
        Args:
            action: The TuxAction to execute
            
        Returns:
            bool: True if action executed successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Get current TUX Droid status.
        
        Returns:
            dict: Status information
        """
        pass


class TuxDriver(TuxDriverInterface):
    """
    Real TUX Droid driver implementation.
    
    This driver communicates with the actual TUX Droid hardware
    via USB serial connection.
    """
    
    def __init__(self, device_path: str = "/dev/ttyUSB0"):
        """
        Initialize the TUX driver.
        
        Args:
            device_path: Path to the USB device
        """
        self.device_path = device_path
        self._connected = False
        self._serial = None
        logger.info(f"TuxDriver initialized with device: {device_path}")
    
    def connect(self) -> bool:
        """Establish connection to TUX Droid."""
        try:
            # TODO: Implement actual serial connection using pyserial or libtuxdriver
            # For now, we'll use a placeholder
            logger.info(f"Attempting to connect to TUX at {self.device_path}")
            
            # This is where you would initialize the actual connection:
            # import serial
            # self._serial = serial.Serial(self.device_path, baudrate=115200)
            # or use libtuxdriver bindings
            
            self._connected = True
            logger.info("Successfully connected to TUX Droid")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to TUX Droid: {e}")
            self._connected = False
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from TUX Droid."""
        try:
            if self._serial:
                # self._serial.close()
                pass
            self._connected = False
            logger.info("Disconnected from TUX Droid")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from TUX Droid: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to TUX Droid."""
        return self._connected
    
    def send_command(self, command: bytes) -> bool:
        """Send raw command bytes to TUX Droid."""
        if not self._connected:
            logger.warning("Cannot send command: Not connected to TUX Droid")
            return False
        
        try:
            # TODO: Implement actual command sending
            # if self._serial:
            #     self._serial.write(command)
            logger.debug(f"Sent command: {command.hex()}")
            return True
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
            return False
    
    def execute_action(self, action: TuxAction) -> bool:
        """Execute a high-level TUX action."""
        if not self._connected:
            logger.warning("Cannot execute action: Not connected")
            return False
        
        try:
            command_code = FIRMWARE_COMMANDS.get(action.action_type)
            if command_code is None:
                logger.error(f"Unknown action type: {action.action_type}")
                return False
            
            # Build command bytes based on action type and params
            command_bytes = self._build_command(action, command_code)
            
            logger.info(f"Executing action: {action.action_type.value} with params: {action.params}")
            return self.send_command(command_bytes)
            
        except Exception as e:
            logger.error(f"Failed to execute action {action.action_type}: {e}")
            return False
    
    def _build_command(self, action: TuxAction, command_code: int) -> bytes:
        """
        Build raw command bytes from action and command code.
        
        Args:
            action: The TuxAction to convert
            command_code: The firmware command code
            
        Returns:
            bytes: Raw command bytes to send
        """
        params = action.params
        
        # Commands are structured based on number of parameters:
        # 0b00xxxxxx (0x00-0x3F) - void functions (0 params)
        # 0b01xxxxxx (0x40-0x7F) - 1 parameter
        # 0b10xxxxxx (0x80-0xBF) - 2 parameters
        # 0b11xxxxxx (0xC0-0xFF) - 3 parameters
        
        if command_code < 0x40:
            # No parameters
            return bytes([command_code])
        elif command_code < 0x80:
            # 1 parameter
            param1 = params.get("count", params.get("target", 1))
            return bytes([command_code, param1])
        elif command_code < 0xC0:
            # 2 parameters
            param1 = params.get("count", params.get("angle", 1))
            param2 = params.get("speed", params.get("delay", 3))
            return bytes([command_code, param1, param2])
        else:
            # 3 parameters
            param1 = params.get("param1", 0)
            param2 = params.get("param2", 0)
            param3 = params.get("param3", 0)
            return bytes([command_code, param1, param2, param3])
    
    def get_status(self) -> Dict[str, Any]:
        """Get current TUX Droid status."""
        return {
            "connected": self._connected,
            "device_path": self.device_path,
            "driver_type": "hardware"
        }


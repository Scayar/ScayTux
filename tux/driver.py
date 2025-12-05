"""
TUX Droid AI Control - Driver Interface
=======================================

This module defines the abstract driver interface and real USB driver
for communicating with TUX Droid hardware.

The TUX Droid uses a USB dongle (fuxusb) that communicates via HID protocol.
Commands are 4 bytes each (CMD_SIZE = 4 from firmware).
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict, Tuple

from .actions import TuxAction, ActionType, FIRMWARE_COMMANDS

logger = logging.getLogger(__name__)

# TUX Droid USB identifiers
# The dongle uses FTDI chip or custom USB implementation
# Common vendor IDs to check:
TUX_USB_IDENTIFIERS = [
    # Format: (vendor_id, product_id, name)
    (0x0403, 0x6001, "FTDI FT232R"),  # Common FTDI chip
    (0x0403, 0x6010, "FTDI FT2232"),
    (0x0403, 0x6014, "FTDI FT232H"),
    (0x2341, 0x0043, "Arduino Uno"),  # In case using Arduino
    (0x1A86, 0x7523, "CH340"),  # Chinese USB-Serial chip
    (0x10C4, 0xEA60, "CP210x"),  # Silicon Labs
]

# Command size from firmware (defines.h)
CMD_SIZE = 4


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
    via USB serial connection using pyserial.
    
    The TUX Droid dongle (fuxusb) typically appears as a serial device
    at /dev/ttyUSB0 on Linux.
    """
    
    # Serial communication settings
    BAUDRATE = 115200
    TIMEOUT = 1.0
    WRITE_TIMEOUT = 1.0
    
    def __init__(self, device_path: str = "/dev/ttyUSB0"):
        """
        Initialize the TUX driver.
        
        Args:
            device_path: Path to the USB device (e.g., /dev/ttyUSB0)
        """
        self.device_path = device_path
        self._connected = False
        self._serial = None
        self._last_error: Optional[str] = None
        self._commands_sent = 0
        self._commands_failed = 0
        
        logger.info("=" * 60)
        logger.info("TuxDriver Initialization")
        logger.info("=" * 60)
        logger.info(f"Device path: {device_path}")
        logger.info(f"Baudrate: {self.BAUDRATE}")
        logger.info(f"Timeout: {self.TIMEOUT}s")
        logger.info("=" * 60)
    
    def _find_tux_device(self) -> Optional[str]:
        """
        Try to find TUX Droid USB device automatically.
        
        Returns:
            str or None: Device path if found, None otherwise
        """
        import os
        import glob
        
        logger.info("🔍 Searching for TUX Droid USB device...")
        
        # Check common USB serial device paths
        possible_paths = [
            "/dev/ttyUSB*",
            "/dev/ttyACM*",
            "/dev/serial/by-id/*",
        ]
        
        found_devices = []
        for pattern in possible_paths:
            devices = glob.glob(pattern)
            found_devices.extend(devices)
        
        if found_devices:
            logger.info(f"📋 Found USB serial devices: {found_devices}")
            # Return the first ttyUSB device as most likely
            for dev in found_devices:
                if "ttyUSB" in dev:
                    logger.info(f"✅ Selected device: {dev}")
                    return dev
            # Fall back to first device
            logger.info(f"✅ Selected device: {found_devices[0]}")
            return found_devices[0]
        
        logger.warning("❌ No USB serial devices found!")
        return None
    
    def _list_usb_devices(self) -> List[Dict[str, Any]]:
        """
        List all USB devices for debugging.
        
        Returns:
            list: List of USB device info dictionaries
        """
        devices = []
        
        try:
            import usb.core
            import usb.util
            
            logger.info("🔍 Scanning USB devices with pyusb...")
            
            for device in usb.core.find(find_all=True):
                try:
                    device_info = {
                        "vendor_id": hex(device.idVendor),
                        "product_id": hex(device.idProduct),
                        "manufacturer": usb.util.get_string(device, device.iManufacturer) if device.iManufacturer else "Unknown",
                        "product": usb.util.get_string(device, device.iProduct) if device.iProduct else "Unknown",
                    }
                    devices.append(device_info)
                    logger.debug(f"  Found: {device_info}")
                except Exception as e:
                    # Some devices may not be readable
                    devices.append({
                        "vendor_id": hex(device.idVendor),
                        "product_id": hex(device.idProduct),
                        "error": str(e)
                    })
            
            logger.info(f"📋 Total USB devices found: {len(devices)}")
            
        except ImportError:
            logger.warning("⚠️ pyusb not installed. Run: pip install pyusb")
        except Exception as e:
            logger.error(f"❌ Error scanning USB devices: {e}")
        
        return devices
    
    def connect(self) -> bool:
        """
        Establish connection to TUX Droid via USB serial.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("🐧 TUX DROID CONNECTION ATTEMPT")
        logger.info("=" * 60)
        
        # List USB devices for debugging
        usb_devices = self._list_usb_devices()
        
        # Try to find device if path doesn't exist
        import os
        if not os.path.exists(self.device_path):
            logger.warning(f"⚠️ Configured device {self.device_path} not found!")
            found_device = self._find_tux_device()
            if found_device:
                logger.info(f"🔄 Using auto-detected device: {found_device}")
                self.device_path = found_device
            else:
                self._last_error = f"Device {self.device_path} not found and no alternative detected"
                logger.error(f"❌ {self._last_error}")
                logger.error("")
                logger.error("🔧 TROUBLESHOOTING:")
                logger.error("   1. Check if TUX dongle is plugged in: lsusb")
                logger.error("   2. Check serial devices: ls -la /dev/ttyUSB*")
                logger.error("   3. Add user to dialout group: sudo usermod -a -G dialout $USER")
                logger.error("   4. Set device permissions: sudo chmod 666 /dev/ttyUSB0")
                logger.error("")
                return False
        
        try:
            import serial
            
            logger.info(f"📡 Opening serial connection to {self.device_path}...")
            logger.info(f"   Baudrate: {self.BAUDRATE}")
            logger.info(f"   Timeout: {self.TIMEOUT}s")
            
            self._serial = serial.Serial(
                port=self.device_path,
                baudrate=self.BAUDRATE,
                timeout=self.TIMEOUT,
                write_timeout=self.WRITE_TIMEOUT,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
            )
            
            # Give device time to initialize
            time.sleep(0.5)
            
            # Clear any pending data
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
            
            self._connected = True
            self._last_error = None
            
            logger.info("=" * 60)
            logger.info("✅ SUCCESSFULLY CONNECTED TO TUX DROID!")
            logger.info(f"   Device: {self.device_path}")
            logger.info(f"   Port open: {self._serial.is_open}")
            logger.info("=" * 60)
            
            # Send a test ping command
            self._send_ping()
            
            return True
            
        except ImportError:
            self._last_error = "pyserial not installed. Run: pip install pyserial"
            logger.error(f"❌ {self._last_error}")
            return False
            
        except serial.SerialException as e:
            self._last_error = f"Serial error: {e}"
            logger.error(f"❌ {self._last_error}")
            logger.error("")
            logger.error("🔧 TROUBLESHOOTING:")
            if "Permission denied" in str(e):
                logger.error("   Permission issue detected!")
                logger.error("   Run: sudo usermod -a -G dialout $USER")
                logger.error("   Then logout and login again.")
                logger.error("   Or temporarily: sudo chmod 666 " + self.device_path)
            elif "No such file" in str(e):
                logger.error("   Device not found!")
                logger.error("   Check: ls -la /dev/ttyUSB*")
                logger.error("   Make sure TUX dongle is plugged in.")
            logger.error("")
            return False
            
        except Exception as e:
            self._last_error = f"Connection failed: {e}"
            logger.error(f"❌ {self._last_error}")
            import traceback
            logger.debug(traceback.format_exc())
            return False
    
    def _send_ping(self) -> bool:
        """Send a ping command to verify connection."""
        try:
            # PING_CMD = 0x7F from commands.h
            ping_cmd = bytes([0x7F, 0x01, 0x00, 0x00])
            logger.info(f"📤 Sending PING command: {ping_cmd.hex()}")
            
            if self._serial and self._serial.is_open:
                self._serial.write(ping_cmd)
                self._serial.flush()
                
                # Wait for response
                time.sleep(0.1)
                
                if self._serial.in_waiting > 0:
                    response = self._serial.read(self._serial.in_waiting)
                    logger.info(f"📥 PING response: {response.hex()}")
                    return True
                else:
                    logger.info("📥 No PING response (TUX may not support ping)")
                    return True  # Continue anyway
                    
        except Exception as e:
            logger.warning(f"⚠️ PING failed: {e}")
        
        return False
    
    def disconnect(self) -> bool:
        """Disconnect from TUX Droid."""
        logger.info("🔌 Disconnecting from TUX Droid...")
        
        try:
            if self._serial and self._serial.is_open:
                self._serial.close()
                logger.info("✅ Serial port closed")
            
            self._connected = False
            self._serial = None
            
            logger.info(f"📊 Session stats: {self._commands_sent} commands sent, {self._commands_failed} failed")
            
            return True
            
        except Exception as e:
            self._last_error = f"Disconnect error: {e}"
            logger.error(f"❌ {self._last_error}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to TUX Droid."""
        if self._serial is None:
            return False
        try:
            return self._serial.is_open
        except:
            return False
    
    def send_command(self, command: bytes) -> bool:
        """
        Send raw command bytes to TUX Droid.
        
        Commands are padded to CMD_SIZE (4 bytes) as per firmware protocol.
        
        Args:
            command: Raw command bytes to send
            
        Returns:
            bool: True if command sent successfully, False otherwise
        """
        if not self.is_connected():
            logger.warning("❌ Cannot send command: Not connected to TUX Droid")
            self._commands_failed += 1
            return False
        
        try:
            # Ensure command is padded to CMD_SIZE
            padded_command = command.ljust(CMD_SIZE, b'\x00')[:CMD_SIZE]
            
            logger.debug(f"📤 Sending command: {padded_command.hex()}")
            logger.debug(f"   Raw bytes: {list(padded_command)}")
            
            # Write command
            bytes_written = self._serial.write(padded_command)
            self._serial.flush()
            
            logger.debug(f"   Bytes written: {bytes_written}")
            
            self._commands_sent += 1
            
            # Small delay to let TUX process
            time.sleep(0.05)
            
            # Check for any response (optional)
            if self._serial.in_waiting > 0:
                response = self._serial.read(self._serial.in_waiting)
                logger.debug(f"📥 Response: {response.hex()}")
            
            return True
            
        except Exception as e:
            self._last_error = f"Send command failed: {e}"
            logger.error(f"❌ {self._last_error}")
            self._commands_failed += 1
            return False
    
    def execute_action(self, action: TuxAction) -> bool:
        """
        Execute a high-level TUX action.
        
        Converts the action to firmware command bytes and sends them.
        
        Args:
            action: The TuxAction to execute
            
        Returns:
            bool: True if action executed successfully, False otherwise
        """
        if not self.is_connected():
            logger.warning("❌ Cannot execute action: Not connected")
            return False
        
        try:
            command_code = FIRMWARE_COMMANDS.get(action.action_type)
            if command_code is None:
                logger.error(f"❌ Unknown action type: {action.action_type}")
                return False
            
            # Build command bytes based on action type and params
            command_bytes = self._build_command(action, command_code)
            
            logger.info(f"🎯 Executing action: {action.action_type.value}")
            logger.info(f"   Parameters: {action.params}")
            logger.info(f"   Command code: 0x{command_code:02X}")
            logger.info(f"   Command bytes: {command_bytes.hex()}")
            
            result = self.send_command(command_bytes)
            
            if result:
                logger.info(f"✅ Action '{action.action_type.value}' executed successfully")
            else:
                logger.error(f"❌ Action '{action.action_type.value}' failed")
            
            return result
            
        except Exception as e:
            self._last_error = f"Execute action failed: {e}"
            logger.error(f"❌ {self._last_error}")
            import traceback
            logger.debug(traceback.format_exc())
            return False
    
    def _build_command(self, action: TuxAction, command_code: int) -> bytes:
        """
        Build raw command bytes from action and command code.
        
        Command structure from firmware (api.h):
        - 0b00xxxxxx (0x00-0x3F) - void functions (0 params)
        - 0b01xxxxxx (0x40-0x7F) - 1 parameter
        - 0b10xxxxxx (0x80-0xBF) - 2 parameters
        - 0b11xxxxxx (0xC0-0xFF) - 3 parameters
        
        Args:
            action: The TuxAction to convert
            command_code: The firmware command code
            
        Returns:
            bytes: Raw command bytes to send (padded to CMD_SIZE)
        """
        params = action.params
        
        if command_code < 0x40:
            # No parameters - command only
            return bytes([command_code, 0x00, 0x00, 0x00])
            
        elif command_code < 0x80:
            # 1 parameter
            param1 = params.get("count", params.get("target", params.get("state", 1)))
            if isinstance(param1, str):
                # Convert string targets to numeric
                param1 = {"both": 0x03, "left": 0x01, "right": 0x02}.get(param1, 1)
            return bytes([command_code, int(param1), 0x00, 0x00])
            
        elif command_code < 0xC0:
            # 2 parameters
            param1 = params.get("count", params.get("angle", 1))
            param2 = params.get("speed", params.get("delay", params.get("volume", 3)))
            return bytes([command_code, int(param1), int(param2), 0x00])
            
        else:
            # 3 parameters
            param1 = params.get("param1", params.get("mode", 0))
            param2 = params.get("param2", 0)
            param3 = params.get("param3", 0)
            
            # Handle sleep mode conversion
            if action.action_type == ActionType.SLEEP:
                mode_map = {"awake": 0, "quick": 1, "normal": 2, "deep": 4}
                param1 = mode_map.get(params.get("mode", "normal"), 2)
            elif action.action_type == ActionType.WAKE_UP:
                param1 = 0  # SLEEPTYPE_AWAKE
            
            return bytes([command_code, int(param1), int(param2), int(param3)])
    
    def get_status(self) -> Dict[str, Any]:
        """Get current TUX Droid status."""
        return {
            "connected": self.is_connected(),
            "device_path": self.device_path,
            "driver_type": "hardware",
            "commands_sent": self._commands_sent,
            "commands_failed": self._commands_failed,
            "last_error": self._last_error,
            "serial_open": self._serial.is_open if self._serial else False,
        }
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """
        Get detailed diagnostics for troubleshooting.
        
        Returns:
            dict: Diagnostic information
        """
        import os
        import glob
        
        diagnostics = {
            "device_path": self.device_path,
            "device_exists": os.path.exists(self.device_path),
            "connected": self.is_connected(),
            "last_error": self._last_error,
            "commands_sent": self._commands_sent,
            "commands_failed": self._commands_failed,
        }
        
        # Check serial devices
        diagnostics["available_devices"] = {
            "ttyUSB": glob.glob("/dev/ttyUSB*"),
            "ttyACM": glob.glob("/dev/ttyACM*"),
            "serial": glob.glob("/dev/serial/by-id/*"),
        }
        
        # Check permissions
        if os.path.exists(self.device_path):
            import stat
            st = os.stat(self.device_path)
            diagnostics["device_permissions"] = {
                "mode": oct(st.st_mode),
                "uid": st.st_uid,
                "gid": st.st_gid,
            }
        
        # USB devices
        diagnostics["usb_devices"] = self._list_usb_devices()
        
        return diagnostics

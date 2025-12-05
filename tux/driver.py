"""
TUX Droid AI Control - Driver Interface
=======================================

This module defines the abstract driver interface and real USB driver
for communicating with TUX Droid hardware.

The TUX Droid uses a USB dongle (fish dongle / fuxusb) that communicates 
via USB HID protocol on Interface 3.

Device: Kysoh TuxDroid
Vendor ID: 0x03eb
Product ID: 0xff07

USB Structure:
- Interface 0: Audio (TuxDroid-Audio)
- Interface 1: Audio (TuxDroid-Micro) 
- Interface 2: Audio (TuxDroid-Speaker)
- Interface 3: HID - COMMANDS (OUT: 0x05, IN: 0x84) ← This is what we use!
- Interface 4: Audio (TuxDroid-TTS)
- Interface 5: Audio (TuxDroid-TTS)

Commands are 4 bytes each (CMD_SIZE = 4 from firmware).
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict, Tuple

from .actions import TuxAction, ActionType, FIRMWARE_COMMANDS

logger = logging.getLogger(__name__)

# TUX Droid USB identifiers
TUX_VENDOR_ID = 0x03eb   # Atmel/Kysoh
TUX_PRODUCT_ID = 0xff07  # Tux Droid fish dongle

# USB Interface and Endpoints for commands (HID interface)
TUX_INTERFACE = 3        # HID interface for commands
TUX_ENDPOINT_OUT = 0x05  # Interrupt OUT endpoint
TUX_ENDPOINT_IN = 0x84   # Interrupt IN endpoint

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
    Real TUX Droid driver implementation using USB HID.
    
    This driver communicates with the actual TUX Droid hardware
    via USB using the pyusb library.
    
    The TUX Droid uses Interface 3 (HID) for commands:
    - Endpoint OUT: 0x05 (Interrupt transfer)
    - Endpoint IN: 0x84 (Interrupt transfer)
    """
    
    def __init__(self, device_path: str = "/dev/ttyUSB0"):
        """
        Initialize the TUX driver.
        
        Args:
            device_path: Legacy parameter (not used for USB HID)
        """
        self.device_path = device_path
        self._connected = False
        self._device = None
        self._endpoint_out = None
        self._endpoint_in = None
        self._last_error: Optional[str] = None
        self._commands_sent = 0
        self._commands_failed = 0
        self._kernel_driver_detached = False
        
        logger.info("=" * 60)
        logger.info("TuxDriver Initialization (USB HID Mode)")
        logger.info("=" * 60)
        logger.info(f"Target device: Kysoh TuxDroid")
        logger.info(f"Vendor ID:  0x{TUX_VENDOR_ID:04X}")
        logger.info(f"Product ID: 0x{TUX_PRODUCT_ID:04X}")
        logger.info(f"Interface:  {TUX_INTERFACE} (HID)")
        logger.info(f"Endpoint OUT: 0x{TUX_ENDPOINT_OUT:02X}")
        logger.info(f"Endpoint IN:  0x{TUX_ENDPOINT_IN:02X}")
        logger.info("=" * 60)
    
    def _find_tux_device(self):
        """
        Find the TUX Droid USB device.
        
        Returns:
            USB device object or None
        """
        try:
            import usb.core
            import usb.util
            
            logger.info("🔍 Searching for TUX Droid USB device...")
            
            # Find TUX device by vendor/product ID
            device = usb.core.find(idVendor=TUX_VENDOR_ID, idProduct=TUX_PRODUCT_ID)
            
            if device is not None:
                logger.info(f"✅ Found TUX Droid!")
                logger.info(f"   Bus: {device.bus}")
                logger.info(f"   Address: {device.address}")
                try:
                    manufacturer = usb.util.get_string(device, device.iManufacturer)
                    product = usb.util.get_string(device, device.iProduct)
                    logger.info(f"   Manufacturer: {manufacturer}")
                    logger.info(f"   Product: {product}")
                except:
                    pass
                return device
            else:
                logger.warning("❌ TUX Droid device not found!")
                return None
                
        except ImportError:
            logger.error("❌ pyusb not installed. Run: pip install pyusb")
            return None
        except Exception as e:
            logger.error(f"❌ Error finding device: {e}")
            return None
    
    def connect(self) -> bool:
        """
        Establish connection to TUX Droid via USB HID Interface 3.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("🐧 TUX DROID USB CONNECTION ATTEMPT")
        logger.info("=" * 60)
        
        try:
            import usb.core
            import usb.util
        except ImportError:
            self._last_error = "pyusb not installed. Run: pip install pyusb"
            logger.error(f"❌ {self._last_error}")
            return False
        
        # Find device
        self._device = self._find_tux_device()
        if self._device is None:
            self._last_error = "TUX Droid device not found"
            logger.error(f"❌ {self._last_error}")
            logger.error("")
            logger.error("🔧 TROUBLESHOOTING:")
            logger.error("   1. Check if TUX dongle is plugged in: lsusb")
            logger.error("   2. Look for: 03eb:ff07 Kysoh TuxDroid")
            logger.error("")
            return False
        
        try:
            # Detach kernel driver from Interface 3 if attached
            logger.info(f"📝 Preparing Interface {TUX_INTERFACE} (HID)...")
            
            if self._device.is_kernel_driver_active(TUX_INTERFACE):
                logger.info(f"   Detaching kernel driver from interface {TUX_INTERFACE}...")
                try:
                    self._device.detach_kernel_driver(TUX_INTERFACE)
                    self._kernel_driver_detached = True
                    logger.info("   ✅ Kernel driver detached")
                except usb.core.USBError as e:
                    logger.warning(f"   ⚠️ Could not detach kernel driver: {e}")
            
            # Set configuration (may already be set)
            try:
                self._device.set_configuration()
            except usb.core.USBError as e:
                logger.debug(f"   Configuration note: {e}")
            
            # Claim Interface 3 (HID)
            logger.info(f"   Claiming interface {TUX_INTERFACE}...")
            usb.util.claim_interface(self._device, TUX_INTERFACE)
            logger.info(f"   ✅ Interface {TUX_INTERFACE} claimed")
            
            # Get the HID interface
            cfg = self._device.get_active_configuration()
            intf = cfg[(TUX_INTERFACE, 0)]  # Interface 3, alternate setting 0
            
            # Find endpoints
            self._endpoint_out = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            )
            
            self._endpoint_in = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
            )
            
            if self._endpoint_out:
                logger.info(f"   ✅ OUT endpoint: 0x{self._endpoint_out.bEndpointAddress:02X}")
            else:
                logger.error("   ❌ No OUT endpoint found!")
                return False
            
            if self._endpoint_in:
                logger.info(f"   ✅ IN endpoint: 0x{self._endpoint_in.bEndpointAddress:02X}")
            
            self._connected = True
            self._last_error = None
            
            logger.info("=" * 60)
            logger.info("✅ SUCCESSFULLY CONNECTED TO TUX DROID!")
            logger.info("=" * 60)
            
            # Send initial ping to verify communication
            self._send_ping()
            
            return True
            
        except usb.core.USBError as e:
            self._last_error = f"USB error: {e}"
            logger.error(f"❌ {self._last_error}")
            
            if "Access denied" in str(e) or "Permission" in str(e):
                logger.error("")
                logger.error("🔧 PERMISSION FIX:")
                logger.error('   echo \'SUBSYSTEM=="usb", ATTR{idVendor}=="03eb", ATTR{idProduct}=="ff07", MODE="0666"\' | sudo tee /etc/udev/rules.d/99-tuxdroid.rules')
                logger.error("   sudo udevadm control --reload-rules")
                logger.error("   sudo udevadm trigger")
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
            
            result = self._usb_write(ping_cmd)
            if result:
                logger.info("   ✅ PING sent successfully!")
                
                # Try to read response
                response = self._usb_read(timeout=500)
                if response:
                    logger.info(f"📥 PING response: {response.hex() if isinstance(response, bytes) else list(response)}")
                else:
                    logger.info("📥 No PING response (may be normal)")
            else:
                logger.warning("   ⚠️ PING failed to send")
            
            return result
            
        except Exception as e:
            logger.warning(f"⚠️ PING error: {e}")
            return False
    
    def _usb_write(self, data: bytes) -> bool:
        """
        Write data to TUX via USB Interrupt OUT endpoint.
        
        Args:
            data: Bytes to write
            
        Returns:
            bool: True if successful
        """
        if not self._device or not self._endpoint_out:
            logger.error("   ❌ Device or endpoint not available")
            return False
        
        try:
            # Pad to CMD_SIZE
            padded_data = data.ljust(CMD_SIZE, b'\x00')[:CMD_SIZE]
            
            # Write via interrupt endpoint
            bytes_written = self._endpoint_out.write(padded_data, timeout=1000)
            logger.debug(f"   Written {bytes_written} bytes to endpoint 0x{self._endpoint_out.bEndpointAddress:02X}")
            
            return bytes_written == len(padded_data)
            
        except Exception as e:
            logger.error(f"   USB write error: {e}")
            return False
    
    def _usb_read(self, timeout: int = 1000) -> Optional[bytes]:
        """
        Read data from TUX via USB Interrupt IN endpoint.
        
        Args:
            timeout: Timeout in milliseconds
            
        Returns:
            bytes or None
        """
        if not self._device or not self._endpoint_in:
            return None
        
        try:
            data = self._endpoint_in.read(64, timeout=timeout)
            return bytes(data)
        except Exception as e:
            logger.debug(f"   Read timeout or error: {e}")
            return None
    
    def disconnect(self) -> bool:
        """Disconnect from TUX Droid."""
        logger.info("🔌 Disconnecting from TUX Droid...")
        
        try:
            import usb.util
            
            if self._device:
                # Release interface
                try:
                    usb.util.release_interface(self._device, TUX_INTERFACE)
                    logger.info(f"   ✅ Interface {TUX_INTERFACE} released")
                except:
                    pass
                
                # Dispose resources
                try:
                    usb.util.dispose_resources(self._device)
                except:
                    pass
                
                # Reattach kernel driver if we detached it
                if self._kernel_driver_detached:
                    try:
                        self._device.attach_kernel_driver(TUX_INTERFACE)
                        logger.info("   ✅ Kernel driver reattached")
                    except:
                        pass
            
            self._connected = False
            self._device = None
            self._endpoint_out = None
            self._endpoint_in = None
            
            logger.info(f"📊 Session stats: {self._commands_sent} commands sent, {self._commands_failed} failed")
            logger.info("✅ Disconnected from TUX Droid")
            
            return True
            
        except Exception as e:
            self._last_error = f"Disconnect error: {e}"
            logger.error(f"❌ {self._last_error}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to TUX Droid."""
        return self._connected and self._device is not None and self._endpoint_out is not None
    
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
            
            result = self._usb_write(padded_command)
            
            if result:
                self._commands_sent += 1
                # Small delay to let TUX process
                time.sleep(0.05)
            else:
                self._commands_failed += 1
            
            return result
            
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
            "driver_type": "hardware_usb",
            "usb_vendor_id": f"0x{TUX_VENDOR_ID:04X}",
            "usb_product_id": f"0x{TUX_PRODUCT_ID:04X}",
            "usb_interface": TUX_INTERFACE,
            "endpoint_out": f"0x{TUX_ENDPOINT_OUT:02X}",
            "endpoint_in": f"0x{TUX_ENDPOINT_IN:02X}",
            "commands_sent": self._commands_sent,
            "commands_failed": self._commands_failed,
            "last_error": self._last_error,
        }
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """
        Get detailed diagnostics for troubleshooting.
        
        Returns:
            dict: Diagnostic information
        """
        diagnostics = {
            "driver_type": "USB HID",
            "target_vendor_id": f"0x{TUX_VENDOR_ID:04X}",
            "target_product_id": f"0x{TUX_PRODUCT_ID:04X}",
            "interface": TUX_INTERFACE,
            "endpoint_out": f"0x{TUX_ENDPOINT_OUT:02X}",
            "endpoint_in": f"0x{TUX_ENDPOINT_IN:02X}",
            "connected": self.is_connected(),
            "last_error": self._last_error,
            "commands_sent": self._commands_sent,
            "commands_failed": self._commands_failed,
        }
        
        # Check if device is present
        try:
            import usb.core
            device = usb.core.find(idVendor=TUX_VENDOR_ID, idProduct=TUX_PRODUCT_ID)
            diagnostics["device_found"] = device is not None
            if device:
                diagnostics["device_bus"] = device.bus
                diagnostics["device_address"] = device.address
        except:
            diagnostics["device_found"] = "unknown (pyusb not available)"
        
        return diagnostics

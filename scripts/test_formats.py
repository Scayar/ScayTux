#!/usr/bin/env python3
"""
TUX Droid - Test Different Command Formats
==========================================

This script tests different packet formats to find the correct one
that makes TUX Droid respond.

Based on firmware analysis:
- CMD_SIZE = 4 bytes
- HID endpoint max packet size = 64 bytes
- Commands: [cmd_code, param1, param2, param3]
"""

import sys
import time

try:
    import usb.core
    import usb.util
except ImportError:
    print("❌ pyusb not installed. Run: pip install pyusb")
    sys.exit(1)

# TUX Droid USB identifiers
TUX_VENDOR_ID = 0x03EB
TUX_PRODUCT_ID = 0xFF07

# HID Interface
INTERFACE_NUM = 3
ENDPOINT_OUT = 0x05
ENDPOINT_IN = 0x84

# Test commands
BLINK_EYES_CMD = 0x40
LED_ON_CMD = 0x1A
LED_OFF_CMD = 0x1B
LED_TOGGLE_CMD = 0x9A
PING_CMD = 0x7F


def find_tux():
    """Find TUX Droid USB device."""
    dev = usb.core.find(idVendor=TUX_VENDOR_ID, idProduct=TUX_PRODUCT_ID)
    if dev is None:
        print("❌ TUX Droid not found!")
        sys.exit(1)
    print(f"✅ Found TUX Droid: Bus {dev.bus}, Address {dev.address}")
    return dev


def setup_device(dev):
    """Setup USB device for communication."""
    # Detach kernel driver if needed
    try:
        if dev.is_kernel_driver_active(INTERFACE_NUM):
            dev.detach_kernel_driver(INTERFACE_NUM)
            print(f"   Detached kernel driver from interface {INTERFACE_NUM}")
    except Exception as e:
        print(f"   Kernel driver note: {e}")
    
    # Claim interface
    try:
        usb.util.claim_interface(dev, INTERFACE_NUM)
        print(f"✅ Claimed interface {INTERFACE_NUM}")
    except Exception as e:
        print(f"❌ Failed to claim interface: {e}")
        sys.exit(1)
    
    return dev


def release_device(dev):
    """Release USB device."""
    try:
        usb.util.release_interface(dev, INTERFACE_NUM)
        dev.attach_kernel_driver(INTERFACE_NUM)
    except:
        pass


def test_format(dev, name, data, delay=0.5):
    """Test a specific packet format."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Data ({len(data)} bytes): {data[:16].hex()}{'...' if len(data) > 16 else ''}")
    print(f"{'='*60}")
    
    try:
        written = dev.write(ENDPOINT_OUT, data, timeout=1000)
        print(f"✅ Written {written} bytes")
        
        # Wait for TUX to respond
        time.sleep(delay)
        
        # Try to read response
        try:
            response = dev.read(ENDPOINT_IN, 64, timeout=500)
            print(f"📥 Response ({len(response)} bytes): {bytes(response).hex()}")
        except usb.core.USBTimeoutError:
            print("   (No response - may be normal)")
        except Exception as e:
            print(f"   Read error: {e}")
            
        return True
    except Exception as e:
        print(f"❌ Write failed: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("   🐧 TUX DROID - COMMAND FORMAT TESTER 🐧")
    print("="*70)
    print("\nWATCH TUX DROID CAREFULLY!")
    print("If any format works, TUX should blink eyes or toggle LEDs.\n")
    
    dev = find_tux()
    setup_device(dev)
    
    input("Press ENTER to start testing (watch TUX!)...")
    
    # ============================================================
    # FORMAT 1: Raw 4 bytes (current implementation)
    # ============================================================
    test_format(dev, "Format 1: Raw 4 bytes (LED ON)", 
                bytes([LED_ON_CMD, 0x00, 0x00, 0x00]))
    
    time.sleep(1)
    
    test_format(dev, "Format 1: Raw 4 bytes (LED OFF)", 
                bytes([LED_OFF_CMD, 0x00, 0x00, 0x00]))
    
    time.sleep(1)
    
    # ============================================================
    # FORMAT 2: 4 bytes padded to 64 bytes
    # ============================================================
    cmd = bytes([BLINK_EYES_CMD, 0x03, 0x00, 0x00])  # Blink 3 times
    padded = cmd + bytes(60)  # Pad to 64 bytes
    test_format(dev, "Format 2: 4 bytes padded to 64 bytes (Blink x3)", padded)
    
    time.sleep(2)
    
    # ============================================================
    # FORMAT 3: HID Report ID 0 + 4 bytes
    # ============================================================
    cmd = bytes([0x00, LED_TOGGLE_CMD, 0x05, 0x19, 0x00])  # Report ID 0 + toggle 5 times
    test_format(dev, "Format 3: Report ID 0 + command", cmd)
    
    time.sleep(2)
    
    # ============================================================
    # FORMAT 4: HID Report ID 0 + 4 bytes + padding to 64
    # ============================================================
    cmd = bytes([0x00, BLINK_EYES_CMD, 0x05, 0x00, 0x00])
    padded = cmd + bytes(59)
    test_format(dev, "Format 4: Report ID 0 + 4 bytes + padding", padded)
    
    time.sleep(2)
    
    # ============================================================
    # FORMAT 5: Based on SPI frame structure (offset 2)
    # ============================================================
    # From firmware: SPI_DATA_OFFSET = 2
    cmd = bytes([0x00, 0x00, BLINK_EYES_CMD, 0x03, 0x00, 0x00])
    test_format(dev, "Format 5: 2-byte header + command", cmd)
    
    time.sleep(2)
    
    # ============================================================
    # FORMAT 6: 2-byte header + command + padding to 64
    # ============================================================
    cmd = bytes([0x00, 0x00, BLINK_EYES_CMD, 0x03, 0x00, 0x00])
    padded = cmd + bytes(58)
    test_format(dev, "Format 6: 2-byte header + command + padding", padded)
    
    time.sleep(2)
    
    # ============================================================
    # FORMAT 7: Ping command variations
    # ============================================================
    test_format(dev, "Format 7a: PING (4 bytes)", 
                bytes([PING_CMD, 0x01, 0x00, 0x00]))
    
    time.sleep(1)
    
    test_format(dev, "Format 7b: PING (64 bytes)", 
                bytes([PING_CMD, 0x01, 0x00, 0x00]) + bytes(60))
    
    time.sleep(1)
    
    # ============================================================
    # FORMAT 8: Full 39-byte SPI frame structure
    # ============================================================
    # Based on firmware: SPI_SIZE = 39
    spi_frame = bytearray(39)
    spi_frame[0] = 0x00  # Index
    spi_frame[1] = 0x02  # Config: CFG_DATA_MK
    spi_frame[2] = BLINK_EYES_CMD  # Command
    spi_frame[3] = 0x03  # Param1: count
    spi_frame[4] = 0x00  # Param2
    spi_frame[5] = 0x00  # Param3
    test_format(dev, "Format 8: SPI frame (39 bytes)", bytes(spi_frame))
    
    time.sleep(2)
    
    # ============================================================
    # FORMAT 9: Full SPI frame padded to 64
    # ============================================================
    padded = bytes(spi_frame) + bytes(25)
    test_format(dev, "Format 9: SPI frame padded to 64", padded)
    
    time.sleep(2)
    
    # ============================================================
    # FORMAT 10: Try LED commands with different padding
    # ============================================================
    for size in [4, 8, 16, 32, 64]:
        cmd = bytes([LED_ON_CMD, 0x00, 0x00, 0x00])
        if size > 4:
            cmd = cmd + bytes(size - 4)
        test_format(dev, f"Format 10: LED_ON with {size} bytes", cmd)
        time.sleep(0.5)
        
        cmd = bytes([LED_OFF_CMD, 0x00, 0x00, 0x00])
        if size > 4:
            cmd = cmd + bytes(size - 4)
        test_format(dev, f"Format 10: LED_OFF with {size} bytes", cmd)
        time.sleep(0.5)
    
    print("\n" + "="*70)
    print("   TESTING COMPLETE!")
    print("="*70)
    print("\nDid TUX respond to any format?")
    print("If YES, note which format number worked.")
    print("If NO, the issue might be RF connection or firmware.\n")
    
    release_device(dev)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


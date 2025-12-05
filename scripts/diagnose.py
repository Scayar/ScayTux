#!/usr/bin/env python3
"""
TUX Droid AI Control - USB Diagnostic Tool
==========================================

This script helps diagnose USB connection issues with TUX Droid.

Usage:
    python -m scripts.diagnose
    
    # Or directly:
    python scripts/diagnose.py
"""

import sys
import os
import glob
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_section(title: str):
    """Print a section header."""
    print(f"\n--- {title} ---")


def check_python_packages():
    """Check if required packages are installed."""
    print_header("PYTHON PACKAGES CHECK")
    
    packages = {
        "pyserial": "serial",
        "pyusb": "usb.core",
        "libusb1": "usb1",
    }
    
    results = {}
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}: Installed")
            results[package_name] = True
        except ImportError:
            print(f"  ❌ {package_name}: NOT INSTALLED")
            print(f"     Install with: pip install {package_name}")
            results[package_name] = False
    
    return results


def check_serial_devices():
    """Check available serial devices."""
    print_header("SERIAL DEVICES CHECK")
    
    patterns = [
        ("/dev/ttyUSB*", "USB Serial"),
        ("/dev/ttyACM*", "ACM Serial"),
        ("/dev/serial/by-id/*", "Serial by ID"),
    ]
    
    found_devices = []
    
    for pattern, description in patterns:
        devices = glob.glob(pattern)
        print_section(f"{description} ({pattern})")
        if devices:
            for dev in devices:
                found_devices.append(dev)
                # Check permissions
                try:
                    st = os.stat(dev)
                    readable = os.access(dev, os.R_OK)
                    writable = os.access(dev, os.W_OK)
                    print(f"  📟 {dev}")
                    print(f"     Permissions: {oct(st.st_mode)[-3:]}")
                    print(f"     Readable: {'✅' if readable else '❌'}")
                    print(f"     Writable: {'✅' if writable else '❌'}")
                    if not readable or not writable:
                        print(f"     ⚠️  FIX: sudo chmod 666 {dev}")
                except Exception as e:
                    print(f"  ❌ {dev}: Error - {e}")
        else:
            print("  (none found)")
    
    return found_devices


def check_usb_devices():
    """Check USB devices using pyusb."""
    print_header("USB DEVICES CHECK (pyusb)")
    
    try:
        import usb.core
        import usb.util
    except ImportError:
        print("  ❌ pyusb not installed. Run: pip install pyusb")
        return []
    
    devices = []
    
    print_section("All USB Devices")
    for device in usb.core.find(find_all=True):
        try:
            manufacturer = ""
            product = ""
            try:
                manufacturer = usb.util.get_string(device, device.iManufacturer) or ""
            except:
                pass
            try:
                product = usb.util.get_string(device, device.iProduct) or ""
            except:
                pass
            
            info = {
                "vendor_id": device.idVendor,
                "product_id": device.idProduct,
                "manufacturer": manufacturer,
                "product": product,
            }
            devices.append(info)
            
            vid = f"0x{device.idVendor:04X}"
            pid = f"0x{device.idProduct:04X}"
            name = f"{manufacturer} {product}".strip() or "Unknown"
            
            # Highlight potential TUX devices
            if any(term in name.lower() for term in ["ftdi", "serial", "uart", "tux"]):
                print(f"  🐧 VID:{vid} PID:{pid} - {name} ⬅️ POSSIBLE TUX DEVICE")
            else:
                print(f"  📱 VID:{vid} PID:{pid} - {name}")
                
        except Exception as e:
            print(f"  ⚠️ Device error: {e}")
    
    if not devices:
        print("  (no USB devices found)")
    
    return devices


def check_user_groups():
    """Check if user is in dialout group."""
    print_header("USER PERMISSIONS CHECK")
    
    try:
        import grp
        import pwd
        
        username = os.getlogin()
        groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
        
        # Also get primary group
        user_info = pwd.getpwnam(username)
        primary_group = grp.getgrgid(user_info.pw_gid).gr_name
        groups.insert(0, primary_group)
        
        print(f"  Current user: {username}")
        print(f"  Groups: {', '.join(groups)}")
        
        if "dialout" in groups:
            print("  ✅ User is in 'dialout' group")
            return True
        else:
            print("  ❌ User is NOT in 'dialout' group")
            print(f"     FIX: sudo usermod -a -G dialout {username}")
            print("     Then logout and login again!")
            return False
            
    except Exception as e:
        print(f"  ⚠️ Could not check groups: {e}")
        return None


def test_serial_connection(device_path: str):
    """Test serial connection to a device."""
    print_header(f"SERIAL CONNECTION TEST: {device_path}")
    
    try:
        import serial
    except ImportError:
        print("  ❌ pyserial not installed. Run: pip install pyserial")
        return False
    
    try:
        print(f"  📡 Opening {device_path} at 115200 baud...")
        
        ser = serial.Serial(
            port=device_path,
            baudrate=115200,
            timeout=1.0,
            write_timeout=1.0,
        )
        
        print(f"  ✅ Connection successful!")
        print(f"     Port: {ser.name}")
        print(f"     Baudrate: {ser.baudrate}")
        print(f"     Is open: {ser.is_open}")
        
        # Try to send a ping command
        print_section("Sending Test Commands")
        
        # PING_CMD = 0x7F
        test_commands = [
            (bytes([0x7F, 0x01, 0x00, 0x00]), "PING"),
            (bytes([0x02, 0x00, 0x00, 0x00]), "INFO_TUXCORE"),
        ]
        
        for cmd, name in test_commands:
            print(f"  📤 Sending {name}: {cmd.hex()}")
            ser.write(cmd)
            ser.flush()
            
            import time
            time.sleep(0.2)
            
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting)
                print(f"  📥 Response: {response.hex()}")
            else:
                print(f"  📥 No response (may be normal)")
        
        ser.close()
        print("\n  ✅ Serial test completed!")
        return True
        
    except serial.SerialException as e:
        print(f"  ❌ Serial error: {e}")
        if "Permission denied" in str(e):
            print(f"     FIX: sudo chmod 666 {device_path}")
            print("     Or: sudo usermod -a -G dialout $USER")
        return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tux_driver():
    """Test the TUX driver module."""
    print_header("TUX DRIVER TEST")
    
    try:
        from tux.driver import TuxDriver
        from tux.actions import TuxAction
        
        print("  ✅ TUX driver module imported successfully")
        
        # Try to find device
        print_section("Auto-detecting TUX Device")
        
        driver = TuxDriver()
        
        # Get diagnostics
        diag = driver.get_diagnostics()
        print(f"  Device path: {diag['device_path']}")
        print(f"  Device exists: {'✅' if diag['device_exists'] else '❌'}")
        print(f"  Available ttyUSB: {diag['available_devices'].get('ttyUSB', [])}")
        
        # Try to connect
        print_section("Connection Attempt")
        
        if driver.connect():
            print("  ✅ Connected to TUX!")
            
            # Test a simple command
            print_section("Testing Blink Eyes Command")
            action = TuxAction.blink_eyes(count=1)
            result = driver.execute_action(action)
            print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
            
            driver.disconnect()
            return True
        else:
            print("  ❌ Connection failed")
            print(f"  Error: {driver._last_error}")
            return False
            
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        print("     Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(results: dict):
    """Print diagnostic summary."""
    print_header("DIAGNOSTIC SUMMARY")
    
    all_ok = True
    
    print("\n  Status:")
    for check, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"    {status} {check}")
        if not passed:
            all_ok = False
    
    print("\n" + "-" * 70)
    
    if all_ok:
        print("  ✅ All checks passed! TUX Droid should be ready to use.")
    else:
        print("  ⚠️  Some checks failed. Follow the FIX instructions above.")
        print("\n  Quick fixes:")
        print("    1. Install packages: pip install pyserial pyusb")
        print("    2. Add to dialout: sudo usermod -a -G dialout $USER")
        print("    3. Set permissions: sudo chmod 666 /dev/ttyUSB0")
        print("    4. Logout and login after group change")
    
    print("-" * 70 + "\n")


def main():
    """Run all diagnostics."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          🐧 TUX DROID USB DIAGNOSTIC TOOL 🐧                         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Check Python packages
    packages = check_python_packages()
    results["Python packages"] = all(packages.values())
    
    # Check user groups
    in_dialout = check_user_groups()
    results["User in dialout group"] = in_dialout or False
    
    # Check serial devices
    serial_devices = check_serial_devices()
    results["Serial devices found"] = len(serial_devices) > 0
    
    # Check USB devices
    usb_devices = check_usb_devices()
    results["USB devices found"] = len(usb_devices) > 0
    
    # Test serial connection if device found
    if serial_devices:
        # Prefer ttyUSB devices
        test_device = None
        for dev in serial_devices:
            if "ttyUSB" in dev:
                test_device = dev
                break
        if not test_device:
            test_device = serial_devices[0]
        
        serial_ok = test_serial_connection(test_device)
        results["Serial connection test"] = serial_ok
    
    # Test TUX driver
    driver_ok = test_tux_driver()
    results["TUX driver test"] = driver_ok
    
    # Print summary
    print_summary(results)
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())


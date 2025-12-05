#!/usr/bin/env python3
"""
TUX DROID SMART DIAGNOSTIC TEST
================================
This test will find exactly what works and what doesn't.

Run: sudo python3 smart_test.py
"""

import sys
import time

try:
    import usb.core
    import usb.util
except ImportError:
    print("ERROR: Run 'pip install pyusb' first")
    sys.exit(1)

# USB Config
VID = 0x03EB
PID = 0xFF07
IFACE = 3
EP_OUT = 0x05
EP_IN = 0x84

# All TUX commands from firmware
COMMANDS = {
    # Eyes
    "BLINK_EYES": (0x40, 3, 0, 0),
    "OPEN_EYES": (0x33, 0, 0, 0),
    "CLOSE_EYES": (0x38, 0, 0, 0),
    "STOP_EYES": (0x32, 0, 0, 0),
    
    # Mouth
    "MOVE_MOUTH": (0x41, 3, 0, 0),
    "OPEN_MOUTH": (0x34, 0, 0, 0),
    "CLOSE_MOUTH": (0x35, 0, 0, 0),
    "STOP_MOUTH": (0x36, 0, 0, 0),
    
    # Wings
    "WAVE_WINGS": (0x80, 3, 3, 0),
    "RAISE_WINGS": (0x39, 0, 0, 0),
    "LOWER_WINGS": (0x3A, 0, 0, 0),
    "STOP_WINGS": (0x30, 0, 0, 0),
    
    # Spin
    "SPIN_LEFT": (0x82, 2, 3, 0),
    "SPIN_RIGHT": (0x83, 2, 3, 0),
    "STOP_SPIN": (0x37, 0, 0, 0),
    
    # LEDs
    "LED_ON": (0x1A, 0, 0, 0),
    "LED_OFF": (0x1B, 0, 0, 0),
    "LED_TOGGLE": (0x9A, 5, 25, 0),
    
    # System
    "PING": (0x7F, 1, 0, 0),
}


class TuxTester:
    def __init__(self):
        self.dev = None
        self.results = {}
        
    def connect(self):
        print("\n" + "="*60)
        print("CONNECTING TO TUX DROID")
        print("="*60)
        
        self.dev = usb.core.find(idVendor=VID, idProduct=PID)
        if self.dev is None:
            print("ERROR: TUX Droid not found!")
            print("Make sure the USB dongle is connected.")
            return False
            
        print(f"Found: Bus {self.dev.bus}, Address {self.dev.address}")
        
        try:
            if self.dev.is_kernel_driver_active(IFACE):
                self.dev.detach_kernel_driver(IFACE)
                print("Detached kernel driver")
        except Exception as e:
            print(f"Kernel driver note: {e}")
            
        try:
            usb.util.claim_interface(self.dev, IFACE)
            print("Claimed interface 3 (HID)")
            return True
        except Exception as e:
            print(f"ERROR claiming interface: {e}")
            return False
    
    def disconnect(self):
        if self.dev:
            try:
                usb.util.release_interface(self.dev, IFACE)
                self.dev.attach_kernel_driver(IFACE)
            except:
                pass
    
    def send(self, data):
        try:
            self.dev.write(EP_OUT, data, timeout=1000)
            return True
        except Exception as e:
            print(f"  Write error: {e}")
            return False
    
    def ask_user(self, question):
        while True:
            ans = input(f"\n>>> {question} (y/n/q): ").lower().strip()
            if ans in ['y', 'yes']:
                return True
            elif ans in ['n', 'no']:
                return False
            elif ans in ['q', 'quit']:
                return None
            print("    Please answer y (yes), n (no), or q (quit)")
    
    def test_command(self, name, cmd_tuple):
        cmd = bytes(cmd_tuple)
        print(f"\n{'─'*50}")
        print(f"TESTING: {name}")
        print(f"Command: {cmd.hex().upper()}")
        print(f"{'─'*50}")
        
        if not self.send(cmd):
            self.results[name] = "SEND_FAILED"
            return False
            
        print("Command sent! Watch TUX...")
        time.sleep(1.5)
        
        result = self.ask_user(f"Did TUX respond to {name}?")
        
        if result is None:  # quit
            return None
        elif result:
            self.results[name] = "WORKS"
            print(f"   >>> {name} WORKS!")
            return True
        else:
            self.results[name] = "NO_RESPONSE"
            return False
    
    def run_quick_test(self):
        """Quick test with most visible commands"""
        print("\n" + "="*60)
        print("QUICK TEST - Most Visible Commands")
        print("="*60)
        print("\nWATCH TUX CAREFULLY!")
        print("Answer 'y' if TUX moves, 'n' if nothing happens.\n")
        
        quick_cmds = [
            ("LED_ON", COMMANDS["LED_ON"]),
            ("LED_OFF", COMMANDS["LED_OFF"]),
            ("BLINK_EYES", COMMANDS["BLINK_EYES"]),
            ("OPEN_EYES", COMMANDS["OPEN_EYES"]),
            ("WAVE_WINGS", COMMANDS["WAVE_WINGS"]),
        ]
        
        for name, cmd in quick_cmds:
            result = self.test_command(name, cmd)
            if result is None:
                break
                
        return len([r for r in self.results.values() if r == "WORKS"])
    
    def run_full_test(self):
        """Test all commands"""
        print("\n" + "="*60)
        print("FULL TEST - All Commands")
        print("="*60)
        
        for name, cmd in COMMANDS.items():
            if name in self.results:
                continue
            result = self.test_command(name, cmd)
            if result is None:
                break
    
    def print_results(self):
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        
        works = []
        fails = []
        errors = []
        
        for name, result in self.results.items():
            if result == "WORKS":
                works.append(name)
            elif result == "NO_RESPONSE":
                fails.append(name)
            else:
                errors.append(name)
        
        if works:
            print("\n WORKING COMMANDS:")
            for name in works:
                print(f"   - {name}")
        
        if fails:
            print("\n NO RESPONSE:")
            for name in fails:
                print(f"   - {name}")
        
        if errors:
            print("\n SEND ERRORS:")
            for name in errors:
                print(f"   - {name}")
        
        print("\n" + "="*60)
        print(f"TOTAL: {len(works)} working, {len(fails)} no response, {len(errors)} errors")
        print("="*60)
        
        if len(works) == 0:
            print("\nPOSSIBLE ISSUES:")
            print("1. TUX might be in sleep mode - restart it")
            print("2. RF connection lost - restart both TUX and dongle")
            print("3. Wrong command format - need to investigate")
            print("4. Firmware issue - may need update")
        elif len(works) > 0:
            print("\nGOOD NEWS: Some commands work!")
            print("We can now update the driver to use the working format.")


def main():
    print("\n" + "="*60)
    print("   TUX DROID SMART DIAGNOSTIC TEST")
    print("="*60)
    
    print("""
INSTRUCTIONS:
1. Make sure TUX is ON (blue eyes)
2. Make sure USB dongle is connected (blue light)
3. Watch TUX carefully during the test
4. Answer 'y' if TUX moves, 'n' if nothing happens

Press ENTER to start...""")
    input()
    
    tester = TuxTester()
    
    if not tester.connect():
        sys.exit(1)
    
    try:
        # First, try to wake up TUX
        print("\nSending OPEN_EYES to wake up TUX...")
        tester.send(bytes(COMMANDS["OPEN_EYES"]))
        time.sleep(1)
        
        # Run quick test
        working = tester.run_quick_test()
        
        if working == 0:
            print("\n" + "="*60)
            print("No commands worked in quick test.")
            print("="*60)
            
            ans = input("\nTry full test with ALL commands? (y/n): ").lower()
            if ans == 'y':
                tester.run_full_test()
        else:
            ans = input(f"\n{working} commands work! Run full test? (y/n): ").lower()
            if ans == 'y':
                tester.run_full_test()
        
        tester.print_results()
        
    finally:
        tester.disconnect()
        print("\nTest complete. Connection closed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()


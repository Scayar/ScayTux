#!/usr/bin/env python3
"""Quick TUX command tester"""
import sys
import usb.core
import usb.util

def setup():
    dev = usb.core.find(idVendor=0x03EB, idProduct=0xFF07)
    if dev is None:
        print("TUX not found")
        sys.exit(1)
    try:
        if dev.is_kernel_driver_active(3):
            dev.detach_kernel_driver(3)
    except:
        pass
    usb.util.claim_interface(dev, 3)
    return dev

def send(dev, cmd):
    dev.write(0x05, cmd)
    print(f"Sent: {cmd.hex()}")

dev = setup()

# Commands from firmware
OPEN_EYES = bytes([0x33, 0x00, 0x00, 0x00])
CLOSE_EYES = bytes([0x38, 0x00, 0x00, 0x00])
BLINK_EYES = bytes([0x40, 0x03, 0x00, 0x00])
WAVE_WINGS = bytes([0x80, 0x03, 0x03, 0x00])
LED_ON = bytes([0x1A, 0x00, 0x00, 0x00])
LED_OFF = bytes([0x1B, 0x00, 0x00, 0x00])

if len(sys.argv) < 2:
    print("Usage: python quick_test.py [open|close|blink|wings|ledon|ledoff]")
    sys.exit(1)

cmd = sys.argv[1].lower()

if cmd == "open":
    print("Opening eyes...")
    send(dev, OPEN_EYES)
elif cmd == "close":
    print("Closing eyes...")
    send(dev, CLOSE_EYES)
elif cmd == "blink":
    print("Blinking eyes...")
    send(dev, BLINK_EYES)
elif cmd == "wings":
    print("Waving wings...")
    send(dev, WAVE_WINGS)
elif cmd == "ledon":
    print("LED ON...")
    send(dev, LED_ON)
elif cmd == "ledoff":
    print("LED OFF...")
    send(dev, LED_OFF)
else:
    print(f"Unknown command: {cmd}")

usb.util.release_interface(dev, 3)
print("Done")


#!/usr/bin/env python3
"""
TUX Droid USB Explorer - Explore all USB interfaces and endpoints
"""

import sys
import usb.core
import usb.util

TUX_VENDOR_ID = 0x03eb
TUX_PRODUCT_ID = 0xff07

def explore_tux():
    """Explore TUX Droid USB device structure."""
    print("\n" + "=" * 70)
    print(" TUX DROID USB STRUCTURE EXPLORER")
    print("=" * 70)
    
    # Find device
    device = usb.core.find(idVendor=TUX_VENDOR_ID, idProduct=TUX_PRODUCT_ID)
    
    if device is None:
        print("❌ TUX Droid not found!")
        return
    
    print(f"\n✅ Device found: VID=0x{device.idVendor:04X} PID=0x{device.idProduct:04X}")
    print(f"   Bus: {device.bus}, Address: {device.address}")
    
    try:
        print(f"   Manufacturer: {usb.util.get_string(device, device.iManufacturer)}")
        print(f"   Product: {usb.util.get_string(device, device.iProduct)}")
    except:
        pass
    
    print(f"\n   bNumConfigurations: {device.bNumConfigurations}")
    
    # Iterate through configurations
    for cfg in device:
        print(f"\n{'='*60}")
        print(f" CONFIGURATION {cfg.bConfigurationValue}")
        print(f"{'='*60}")
        print(f"   bNumInterfaces: {cfg.bNumInterfaces}")
        
        # Iterate through interfaces
        for intf in cfg:
            print(f"\n   --- INTERFACE {intf.bInterfaceNumber} (alt {intf.bAlternateSetting}) ---")
            print(f"       bInterfaceClass: 0x{intf.bInterfaceClass:02X} ({get_class_name(intf.bInterfaceClass)})")
            print(f"       bInterfaceSubClass: 0x{intf.bInterfaceSubClass:02X}")
            print(f"       bInterfaceProtocol: 0x{intf.bInterfaceProtocol:02X}")
            print(f"       bNumEndpoints: {intf.bNumEndpoints}")
            
            try:
                intf_name = usb.util.get_string(device, intf.iInterface)
                print(f"       iInterface: {intf_name}")
            except:
                pass
            
            # Iterate through endpoints
            for ep in intf:
                ep_dir = "IN" if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN else "OUT"
                ep_type = get_transfer_type(ep.bmAttributes)
                print(f"\n       ENDPOINT 0x{ep.bEndpointAddress:02X}:")
                print(f"           Direction: {ep_dir}")
                print(f"           Transfer Type: {ep_type}")
                print(f"           Max Packet Size: {ep.wMaxPacketSize}")
                print(f"           Interval: {ep.bInterval}")
    
    # Try to claim each interface and test
    print(f"\n{'='*60}")
    print(" TESTING INTERFACES")
    print(f"{'='*60}")
    
    cfg = device.get_active_configuration()
    
    for intf in cfg:
        intf_num = intf.bInterfaceNumber
        print(f"\n--- Testing Interface {intf_num} ---")
        
        # Check if kernel driver is active
        try:
            if device.is_kernel_driver_active(intf_num):
                print(f"    Kernel driver active, detaching...")
                device.detach_kernel_driver(intf_num)
                print(f"    ✅ Detached")
        except Exception as e:
            print(f"    ⚠️ Kernel driver check: {e}")
        
        # Try to claim interface
        try:
            usb.util.claim_interface(device, intf_num)
            print(f"    ✅ Claimed interface {intf_num}")
            
            # Find endpoints
            ep_out = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            )
            ep_in = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
            )
            
            if ep_out:
                print(f"    ✅ Found OUT endpoint: 0x{ep_out.bEndpointAddress:02X}")
                # Try to write
                try:
                    test_cmd = bytes([0x7F, 0x01, 0x00, 0x00])  # PING
                    written = ep_out.write(test_cmd, timeout=1000)
                    print(f"    ✅ Wrote {written} bytes!")
                except Exception as e:
                    print(f"    ❌ Write failed: {e}")
            else:
                print(f"    ℹ️ No OUT endpoint on this interface")
            
            if ep_in:
                print(f"    ✅ Found IN endpoint: 0x{ep_in.bEndpointAddress:02X}")
            else:
                print(f"    ℹ️ No IN endpoint on this interface")
            
            # Release interface
            usb.util.release_interface(device, intf_num)
            
        except Exception as e:
            print(f"    ❌ Claim failed: {e}")
    
    # Test control transfers
    print(f"\n{'='*60}")
    print(" TESTING CONTROL TRANSFERS")
    print(f"{'='*60}")
    
    test_cmd = bytes([0x7F, 0x01, 0x00, 0x00])  # PING command
    
    # Try different control transfer types
    transfers_to_try = [
        (0x21, 0x09, 0x0200, 0, "HID SET_REPORT (Output, ID 0)"),
        (0x21, 0x09, 0x0300, 0, "HID SET_REPORT (Feature, ID 0)"),
        (0x40, 0x00, 0x0000, 0, "Vendor Device OUT"),
        (0x41, 0x00, 0x0000, 0, "Vendor Interface OUT"),
        (0x42, 0x00, 0x0000, 0, "Vendor Endpoint OUT"),
        (0x21, 0x01, 0x0000, 0, "Class Interface (bRequest=1)"),
        (0x21, 0x09, 0x0201, 0, "HID SET_REPORT (Output, ID 1)"),
    ]
    
    for bmRequestType, bRequest, wValue, wIndex, desc in transfers_to_try:
        try:
            result = device.ctrl_transfer(
                bmRequestType=bmRequestType,
                bRequest=bRequest,
                wValue=wValue,
                wIndex=wIndex,
                data_or_wLength=test_cmd,
                timeout=1000
            )
            print(f"  ✅ {desc}: Wrote {result} bytes")
        except usb.core.USBError as e:
            print(f"  ❌ {desc}: {e}")
    
    print("\n" + "=" * 70)
    print(" DONE")
    print("=" * 70 + "\n")


def get_class_name(class_code):
    """Get USB class name."""
    classes = {
        0x00: "Use Interface",
        0x01: "Audio",
        0x02: "CDC",
        0x03: "HID",
        0x05: "Physical",
        0x06: "Image",
        0x07: "Printer",
        0x08: "Mass Storage",
        0x09: "Hub",
        0x0A: "CDC-Data",
        0x0B: "Smart Card",
        0x0D: "Content Security",
        0x0E: "Video",
        0x0F: "Personal Healthcare",
        0xDC: "Diagnostic",
        0xE0: "Wireless Controller",
        0xEF: "Miscellaneous",
        0xFE: "Application Specific",
        0xFF: "Vendor Specific",
    }
    return classes.get(class_code, "Unknown")


def get_transfer_type(attributes):
    """Get transfer type name."""
    transfer_type = attributes & 0x03
    types = {
        0: "Control",
        1: "Isochronous",
        2: "Bulk",
        3: "Interrupt",
    }
    return types.get(transfer_type, "Unknown")


if __name__ == "__main__":
    try:
        explore_tux()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


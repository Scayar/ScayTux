package com.kowalski7cc.jtuxdriver.cli;

import org.hid4java.HidDevice;
import org.hid4java.HidManager;
import org.hid4java.HidServices;

import com.kowalski7cc.jtuxdriver.USBDefines;

/**
 * Debug utility to list all HID devices seen by hid4java.
 */
public class Debug {
    public static void main(String[] args) {
        System.out.println("=== hid4java Debug - Listing ALL HID devices ===\n");

        try {
            HidServices hidServices = HidManager.getHidServices();

            System.out.println("HidServices started. Scanning devices...\n");

            int count = 0;
            for (HidDevice device : hidServices.getAttachedHidDevices()) {
                count++;
                System.out.println("Device #" + count + ":");
                System.out.println("  Vendor ID:  0x" + String.format("%04x", device.getVendorId()));
                System.out.println("  Product ID: 0x" + String.format("%04x", device.getProductId()));
                System.out.println("  Product:    " + device.getProduct());
                System.out.println("  Manufacturer: " + device.getManufacturer());
                System.out.println("  Path:       " + device.getPath());
                System.out.println();
            }

            if (count == 0) {
                System.out.println("NO HID DEVICES FOUND BY hid4java!");
                System.out.println("\nPossible issues:");
                System.out.println("1. libhidapi-hidraw0 not installed");
                System.out.println("2. Architecture mismatch (32-bit vs 64-bit)");
                System.out.println("3. HIDAPI native library not loading");
            } else {
                System.out.println("Total: " + count + " HID device(s) found.");
            }

            System.out.println(String.format("\n--- Checking for Tux Droid (%04x:%04x) ---", USBDefines.VID, USBDefines.PID));
            HidDevice tux = hidServices.getHidDevice(USBDefines.VID, USBDefines.PID, null);
            if (tux != null) {
                System.out.println("FOUND: " + tux.getProduct());
            } else {
                System.out.println("NOT FOUND via getHidDevice()");
            }

        } catch (Exception e) {
            System.err.println("ERROR: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

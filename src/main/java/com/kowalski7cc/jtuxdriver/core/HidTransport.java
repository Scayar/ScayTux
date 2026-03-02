package com.kowalski7cc.jtuxdriver.core;

import org.hid4java.HidDevice;
import org.hid4java.HidManager;
import org.hid4java.HidServices;
import org.hid4java.HidServicesListener;
import org.hid4java.event.HidServicesEvent;

import java.io.IOException;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;
import java.util.Arrays;

import com.kowalski7cc.jtuxdriver.USBDefines;

/**
 * Concrete implementation of {@link UsbTransport} using hid4java.
 * Targets the Tux Droid fishtank dongle (03eb:ff07).
 */
public class HidTransport implements UsbTransport, HidServicesListener {

    private static final int VID = USBDefines.VID;
    private static final int PID = USBDefines.PID;
    private static final int PACKET_LENGTH = USBDefines.PACKET_LENGTH;

    private HidServices hidServices;
    private HidDevice device;
    private Consumer<byte[]> eventListener;
    private final AtomicBoolean running = new AtomicBoolean(false);
    private Thread readThread;

    public HidTransport() {
        // Get HID services
        this.hidServices = HidManager.getHidServices();
        this.hidServices.addHidServicesListener(this);
    }

    @Override
    @SuppressWarnings("deprecation")
    public void open() throws IOException {
        // Try to find device if not already held
        if (device == null || !device.isOpen()) {
            device = hidServices.getHidDevice(VID, PID, null);
        }

        if (device == null) {
            throw new IOException(String.format(
                    "Tux Droid dongle not found (VID: 0x%04x, PID: 0x%04x). Check connections and udev rules.", VID,
                    PID));
        }

        if (!device.isOpen()) {
            boolean success = device.open();
            if (!success) {
                throw new IOException("Failed to open Tux Droid HID device. Permissions issue?");
            }
        }

        // Start reading loop
        startReadLoop();
    }

    private void startReadLoop() {
        if (running.get())
            return;
        running.set(true);

        readThread = new Thread(() -> {
            byte[] buffer = new byte[PACKET_LENGTH];
            while (running.get()) {
                if (device != null && isDeviceOpenSafe()) {
                    try {
                        // blocking read with timeout
                        int bytesRead = device.read(buffer, 1000);
                        if (bytesRead > 0 && eventListener != null) {
                            byte[] copy = Arrays.copyOf(buffer, PACKET_LENGTH);
                            eventListener.accept(copy);
                        }
                    } catch (Exception e) {
                        // Ignore read errors
                    }
                } else {
                    // Device not ready
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }
        }, "TuxDroid-Reader");
        readThread.start();
    }

    @Override
    public void close() {
        running.set(false);
        if (readThread != null) {
            readThread.interrupt();
        }
        if (device != null) {
            device.close();
            device = null;
        }
        // clean up listener? kept global for auto-reconnect logic usually
        // hidServices.removeHidServicesListener(this);
        // We keep the listener to detect re-insertion
    }

    @Override
    public boolean isOpen() {
        return isDeviceOpenSafe();
    }

    @SuppressWarnings("deprecation")
    private boolean isDeviceOpenSafe() {
        return device != null && device.isOpen();
    }

    @Override
    public void write(byte[] data) throws IOException {
        if (!isOpen()) {
            throw new IOException("Device not connected");
        }

        // Ensure 64 bytes
        byte[] packet = data;
        if (data.length != PACKET_LENGTH) {
            packet = Arrays.copyOf(data, PACKET_LENGTH);
        }

        // HID Report ID 0 usually
        int val = device.write(packet, PACKET_LENGTH, (byte) 0);
        if (val < 0) {
            throw new IOException("Failed to write to HID device, error code: " + device.getLastErrorMessage());
        }
    }

    @Override
    public void setEventListener(Consumer<byte[]> listener) {
        this.eventListener = listener;
    }

    // --- HidServicesListener implementation ---

    @Override
    public void hidDeviceAttached(HidServicesEvent event) {
        if (event.getHidDevice().isVidPidSerial(VID, PID, null)) {
            System.out.println("Tux Droid dongle attached!");
            this.device = event.getHidDevice();
            this.device.open();
        }
    }

    @Override
    public void hidDeviceDetached(HidServicesEvent event) {
        if (event.getHidDevice().isVidPidSerial(VID, PID, null)) {
            System.out.println("Tux Droid dongle detached!");
            if (this.device != null) {
                this.device.close();
                this.device = null;
            }
        }
    }

    @Override
    public void hidFailure(HidServicesEvent event) {
        System.err.println("HID Helper failure: " + event);
    }

    @Override
    public void hidDataReceived(HidServicesEvent event) {
        // We use our own polling thread for data reading to ensure consistency across
        // platforms
        // and to handle the specific packet structure of Tux Droid if needed.
        // So we ignore this event callback.
    }
}

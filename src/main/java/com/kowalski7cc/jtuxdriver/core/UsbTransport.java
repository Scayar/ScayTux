package com.kowalski7cc.jtuxdriver.core;

import java.io.Closeable;
import java.io.IOException;
import java.util.function.Consumer;

/**
 * Abstraction for the physical transport layer (USB/HID).
 * This allows mocking or swapping implementations.
 */
public interface UsbTransport extends Closeable {

    /**
     * Open connection to the Tux Droid dongle.
     * 
     * @throws IOException if connection fails or device not found.
     */
    void open() throws IOException;

    /**
     * Close connection.
     */
    void close();

    /**
     * Check if currently connected and open.
     */
    boolean isOpen();

    /**
     * Send a raw packet to the device.
     * 
     * @param data The bytes to send (usually 64 bytes).
     * @throws IOException if write fails.
     */
    void write(byte[] data) throws IOException;

    /**
     * Set a listener for incoming data packets.
     * 
     * @param listener Callback for received bytes.
     */
    void setEventListener(Consumer<byte[]> listener);
}

package com.kowalski7cc.jtuxdriver;

import com.kowalski7cc.jtuxdriver.core.UsbTransport;

import java.io.Closeable;
import java.io.IOException;

public class TuxDroid implements Closeable {

    private final UsbTransport transport;
    private final Object writeLock = new Object();

    public TuxDroid(UsbTransport transport) {
        this.transport = transport;
    }

    private void write(byte[] packet) throws IOException {
        synchronized (writeLock) {
            transport.write(packet);
        }
    }

    public void open() throws IOException {
        transport.open();
        write(Command.Dongle.connect());
    }

    public void setInputListener(java.util.function.Consumer<byte[]> listener) {
        transport.setEventListener(listener);
    }

    @Override
    public void close() {
        try {
            if (transport.isOpen()) {
                write(Command.Dongle.disconnect());
            }
        } catch (Exception e) {
            System.err.println("[TuxDroid] Error during disconnect: " + e.getMessage());
        } finally {
            try {
                transport.close();
            } catch (Exception e) {
                System.err.println("[TuxDroid] Error closing transport: " + e.getMessage());
            }
        }
    }

    public void flapWings() throws IOException {
        write(Command.Tux.Flippers.raise());
        sleep(500);
        write(Command.Tux.Flippers.lower());
        sleep(500);
        write(Command.Tux.Flippers.raise());
        sleep(500);
        write(Command.Tux.Flippers.lower());
    }

    public void setEyes(boolean on) throws IOException {
        if (on)
            write(Command.Tux.Eyes.open());
        else
            write(Command.Tux.Eyes.close());
    }

    public void blinkEyes(int times) throws IOException {
        write(Command.Tux.Eyes.blink((byte) times));
    }

    public void setMouth(boolean open) throws IOException {
        if (open)
            write(Command.Tux.Mouth.open());
        else
            write(Command.Tux.Mouth.close());
    }

    public void moveMouth(int times) throws IOException {
        write(Command.Tux.Mouth.move((byte) times));
    }

    public void openMouth() throws IOException {
        write(Command.Tux.Mouth.open());
    }

    public void closeMouth() throws IOException {
        write(Command.Tux.Mouth.close());
    }

    public void spinLeft() throws IOException {
        spinLeft(20);
    }

    public void spinLeft(int duration) throws IOException {
        for (int i = 0; i < duration; i++) {
            write(Command.Tux.Spin.left((byte) 0xFF));
            sleep(20);
        }
        write(Command.Tux.Spin.stop());
    }

    public void spinRight() throws IOException {
        spinRight(20);
    }

    public void spinRight(int duration) throws IOException {
        for (int i = 0; i < duration; i++) {
            write(Command.Tux.Spin.right((byte) 0xFF));
            sleep(20);
        }
        write(Command.Tux.Spin.stop());
    }

    public void setLed(int color, int intensity) throws IOException {
        write(Command.Tux.Led.set((byte) color, (byte) intensity));
    }

    private void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

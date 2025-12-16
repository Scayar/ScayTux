package com.kowalski7cc.jtuxdriver;

/**
 * Parses raw HID Input Reports from Tux Droid.
 * <p>
 * Standard Packet: 64 bytes.
 * Byte 0: Status flags?
 * Byte 1: Buttons/Sensors?
 * </p>
 */
public class TuxInput {

    private final byte[] data;

    public TuxInput(byte[] data) {
        this.data = data;
    }

    /**
     * @return Raw byte array of the report
     */
    public byte[] getRaw() {
        return data;
    }

    /**
     * Check if the head button is pressed.
     * (Logic to be verified via debug mode)
     */
    public boolean isHeadButton() {
        if (data == null || data.length < 2)
            return false;
        // Hypothesis: Byte 1, Bit 0
        return (data[1] & 0x01) != 0;
    }

    public boolean isLeftWing() {
        if (data == null || data.length < 2)
            return false;
        return (data[1] & 0x02) != 0;
    }

    public boolean isRightWing() {
        if (data == null || data.length < 2)
            return false;
        return (data[1] & 0x04) != 0;
    }

    @Override
    public String toString() {
        if (data == null)
            return "null";
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < Math.min(data.length, 8); i++) {
            sb.append(String.format("%02X ", data[i]));
        }
        return sb.toString().trim() + "...]";
    }
}

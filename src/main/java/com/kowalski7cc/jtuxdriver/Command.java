// Copyright (C) 2019 Kowalski7cc
// 
// JTuxDriver is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// JTuxDriver is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with JTuxDriver. If not, see <http://www.gnu.org/licenses/>.

package com.kowalski7cc.jtuxdriver;

/**
 * Factory for creating Tux Droid USB Command packets.
 * <p>
 * Commands are 64-byte packets.
 * The first byte is usually the target (TUX=0, FUX/Dongle=1).
 * The second byte is the command opcode.
 * </p>
 */
public class Command {

    // Initial byte targets
    public final static byte TARGET_TUX = 0x00;
    public final static byte TARGET_DONGLE = 0x01; // Also known as FUX
    public final static byte TARGET_BOOTLOADER = 0x02;

    public static class Tux {

        public static class Eyes {
            public final static byte OPEN = 0x33;
            public final static byte CLOSE = 0x38;
            public final static byte BLINK = 0x40;
            public final static byte STOP = 0x32;

            public static byte[] open() {
                return Packet.of(TARGET_TUX, OPEN);
            }

            public static byte[] close() {
                return Packet.of(TARGET_TUX, CLOSE);
            }

            public static byte[] blink(byte times) {
                return Packet.of(TARGET_TUX, BLINK, times);
            }

            public static byte[] stop() {
                return Packet.of(TARGET_TUX, STOP);
            }
        }

        public static class Mouth {
            public final static byte OPEN = 0x34;
            public final static byte CLOSE = 0x35;
            public final static byte MOVE = 0x41;
            public final static byte STOP = 0x36;

            public static byte[] open() {
                // Protocol weirdness: open expects a parameter '1' based on old code
                return Packet.of(TARGET_TUX, OPEN, (byte) 1);
            }

            public static byte[] close() {
                return Packet.of(TARGET_TUX, CLOSE);
            }

            public static byte[] move(byte times) {
                return Packet.of(TARGET_TUX, MOVE, times);
            }

            public static byte[] stop() {
                return Packet.of(TARGET_TUX, STOP);
            }
        }

        public static class Flippers {
            public final static byte RAISE = 0x39;
            public final static byte LOWER = 0x3A;
            public final static byte WAVE = (byte) 0x80;
            public final static byte STOP = 0x30;

            public static byte[] raise() {
                return Packet.of(TARGET_TUX, RAISE);
            }

            public static byte[] lower() {
                return Packet.of(TARGET_TUX, LOWER);
            }

            public static byte[] wave(byte times, byte speed) {
                return Packet.of(TARGET_TUX, WAVE, times, speed);
            }

            public static byte[] stop() {
                return Packet.of(TARGET_TUX, STOP);
            }
        }

        public static class Led {
            // 0xD0 - 0xD3 range
            private final static byte PULSE = (byte) 0xD3;
            private final static byte SET = (byte) 0xD1;

            public static byte[] pulse(byte color, byte speed) {
                return Packet.of(TARGET_TUX, PULSE, color, speed);
            }

            public static byte[] set(byte color, byte intensity) {
                return Packet.of(TARGET_TUX, SET, color, intensity);
            }
        }

        public static class Spin {
            private final static byte LEFT = (byte) 0x83;
            private final static byte RIGHT = (byte) 0x82;
            private final static byte STOP = 0x37; // Standard stop?

            public static byte[] left(byte degrees) {
                return Packet.of(TARGET_TUX, LEFT, degrees);
            }

            public static byte[] right(byte degrees) {
                return Packet.of(TARGET_TUX, RIGHT, degrees);
            }

            public static byte[] stop() {
                return Packet.of(TARGET_TUX, STOP);
            }
        }
    }

    public static class Dongle {
        private final static byte CMD_CONNECTION = 0;

        private final static byte CONN_DISCONNECT = 1;
        private final static byte CONN_CONNECT = 2;
        private final static byte CONN_ID_REQUEST = 3;
        private final static byte CONN_ID_LOOKUP = 4;
        private final static byte CONN_WAKEUP = 6;

        public static byte[] connect() {
            return Packet.of(TARGET_DONGLE, CMD_CONNECTION, CONN_CONNECT);
        }

        public static byte[] disconnect() {
            // Old code had extra 0s?
            return Packet.of(TARGET_DONGLE, CMD_CONNECTION, CONN_DISCONNECT, (byte) 0, (byte) 0);
        }

        public static byte[] wakeup() {
            return Packet.of(TARGET_DONGLE, CMD_CONNECTION, CONN_WAKEUP);
        }
    }

    /** Helper for creating padded packets */
    private static class Packet {
        static byte[] of(byte... bytes) {
            byte[] p = new byte[USBDefines.PACKET_LENGTH]; // 64
            System.arraycopy(bytes, 0, p, 0, Math.min(bytes.length, 64));
            return p;
        }
    }
}
package com.kowalski7cc.jtuxdriver;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.kowalski7cc.jtuxdriver.Command.Tux;
import com.kowalski7cc.jtuxdriver.Command.Dongle;

public class CommandTest {

    @Test
    public void testPacketLength() {
        byte[] packet = Tux.Eyes.open();
        assertEquals(USBDefines.PACKET_LENGTH, packet.length, "Packet must be 64 bytes");
    }

    @Test
    public void testEyesOpenPacket() {
        byte[] packet = Tux.Eyes.open();
        assertEquals(Command.TARGET_TUX, packet[0]);
        assertEquals(Tux.Eyes.OPEN, packet[1]);
        // Updated protocol check: does it have 3rd byte?
        // My implementation: Packet.of(TARGET_TUX, OPEN) -> [0, 0x33, 0...0]
        assertEquals(0, packet[2]);
    }

    @Test
    public void testMouthOpenPacket() {
        byte[] packet = Tux.Mouth.open();
        assertEquals(Command.TARGET_TUX, packet[0]);
        assertEquals(Tux.Mouth.OPEN, packet[1]);
        assertEquals(1, packet[2], "Mouth open command expects parameter 1");
    }

    @Test
    public void testDongleConnect() {
        byte[] packet = Dongle.connect();
        assertEquals(Command.TARGET_DONGLE, packet[0]);
        // Command.Dongle.CMD_CONNECTION = 0
        assertEquals(0, packet[1]);
        // Command.Dongle.CONN_CONNECT = 2
        assertEquals(2, packet[2]);
    }
}

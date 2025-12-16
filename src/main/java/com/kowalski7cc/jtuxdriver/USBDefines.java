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
 * USB Identifiers and Constants for Tux Droid
 */
public class USBDefines {

    /** Vendor ID for Atmel/Tux Droid Dongle */
    public final static int VID = 0x03eb;

    /** Product ID for Tux Droid 'Fish' Dongle */
    public final static int PID = 0xff07;

    public final static String PRODUCT_NAME = "TuxDroid";

    /** Standard status request packet */
    public final static byte[] STATUS_REQUEST = new byte[] { 0x01, 0x01, 0x00, 0x00 };

    /** HID Report Packet Length */
    public final static int PACKET_LENGTH = 64;

}
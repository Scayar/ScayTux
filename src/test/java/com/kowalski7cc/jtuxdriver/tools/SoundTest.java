package com.kowalski7cc.jtuxdriver.tools;

import javax.sound.sampled.*;

public class SoundTest {
    public static void main(String[] args) throws Exception {
        System.out.println(">>> TUX DROID AUDIO HARDWARE TEST <<<");
        System.out.println("Scanning for TuxDroid / USB Sound Devices...");

        Mixer.Info[] mixers = AudioSystem.getMixerInfo();
        Mixer.Info selectedInfo = null;
        Mixer selectedMixer = null;

        for (Mixer.Info info : mixers) {
            String name = info.getName().toLowerCase();
            String desc = info.getDescription().toLowerCase();
            System.out.println("  Found: " + info.getName() + " [" + info.getDescription() + "]");

            // Logic to find Tux: Look for "tux" or "usb" and NOT "port" (ports are
            // inputs/outputs, not mixers usually)
            if ((name.contains("tux") || name.contains("usb")) && !name.contains("port")) {
                Mixer m = AudioSystem.getMixer(info);
                System.out.println("     -> MATCH! Checking if it supports SourceLines...");
                // Check if it supports playback (SourceDataLine)
                Line.Info lineInfo = new Line.Info(SourceDataLine.class);
                if (m.isLineSupported(lineInfo)) {
                    selectedInfo = info;
                    selectedMixer = m;
                    System.out.println("     -> SUCCESS! This device supports Audio Output.");
                    break;
                } else {
                    System.out.println("     -> Skipping: Does not support Audio Output (maybe Microphone?)");
                }
            }
        }

        if (selectedMixer == null) {
            System.err.println("\n[ERROR] Could not find a 'TuxDroid' or 'USB' output device!");
            System.err.println("Please check your connections.");
            System.out.println("\nAttempting to use DEFAULT system audio as fallback...");
            selectedMixer = AudioSystem.getMixer(null); // Default
        }

        System.out.println("\n>>> PLAYING TEST TONE (BEEP) on: "
                + (selectedInfo != null ? selectedInfo.getName() : "Default Device"));

        // Generate 1 second of 440Hz sine wave
        byte[] buf = new byte[44100];
        for (int i = 0; i < buf.length; i++) {
            double angle = i / (44100.0 / 440.0) * 2.0 * Math.PI;
            buf[i] = (byte) (Math.sin(angle) * 127.0);
        }

        AudioFormat format = new AudioFormat(44100, 8, 1, true, false);
        SourceDataLine line;

        if (selectedInfo != null) {
            line = (SourceDataLine) selectedMixer.getLine(new DataLine.Info(SourceDataLine.class, format));
        } else {
            line = AudioSystem.getSourceDataLine(format);
        }

        line.open(format);
        line.start();
        line.write(buf, 0, buf.length);
        line.drain();
        line.close();

        System.out.println(">>> TEST COMPLETE. Did you hear the beep?");
    }
}

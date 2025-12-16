package com.kowalski7cc.jtuxdriver.tools;

import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Mixer;

public class ListAudio {
    public static void main(String[] args) {
        System.out.println("Available Audio Devices:");
        Mixer.Info[] mixers = AudioSystem.getMixerInfo();
        for (Mixer.Info mixer : mixers) {
            System.out.println("- " + mixer.getName() + " [" + mixer.getDescription() + "]");
        }
    }
}

package com.kowalski7cc.jtuxdriver;

import javazoom.jl.decoder.JavaLayerException;
import javazoom.jl.player.JavaSoundAudioDevice;
import javax.sound.sampled.*;

public class TuxAudioDevice extends JavaSoundAudioDevice {

    /*
     * // Method signature mismatch with JLayer 1.0.1, disabling custom hardware
     * selection for now.
     * // @Override
     * // protected void createSource(AudioFormat fmt) throws JavaLayerException {
     * // ...
     * // }
     */

    private void setSourceLine(SourceDataLine line) throws Exception {
        // Reflection hack because 'source' is private in JavaSoundAudioDevice
        java.lang.reflect.Field f = JavaSoundAudioDevice.class.getDeclaredField("source");
        f.setAccessible(true);
        f.set(this, line);

        // Also need to set 'byteVals' buffer if parent uses it?
        // Verification: JavaSoundAudioDevice initiates buffer in createSource...
        // We probably need to start the line too?
        line.start();
    }
}

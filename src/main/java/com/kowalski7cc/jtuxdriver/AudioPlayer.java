package com.kowalski7cc.jtuxdriver;

import javazoom.jl.decoder.*;
import javazoom.jl.player.Player;
import javax.sound.sampled.*;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;

/**
 * Cross-platform MP3 Player for TuxDroid.
 * - On Windows: Attempts to use TuxDroid-Audio device, falls back to default
 * - On Linux: Uses system default or TUX_AUDIO_DEV environment variable
 */
public class AudioPlayer {

    private static volatile boolean playing = false;
    private static Player jlayerPlayer = null;
    private static SourceDataLine currentLine = null;
    
    // OS Detection
    private static final boolean IS_WINDOWS = System.getProperty("os.name").toLowerCase().contains("win");

    /**
     * Play an audio file (MP3, M4A, etc). This method BLOCKS until the song finishes or is stopped.
     */
    public static void play(String filepath) {
        stop(); // Ensure any previous song is stopped
        playing = true;

        System.out.println("[Audio] Playing: " + filepath);

        // Resolve file path - try multiple locations
        File audioFile = resolveAudioFile(filepath);
        if (audioFile == null) {
            System.err.println("[Audio Error] Cannot find audio file: " + filepath);
            System.err.println("[Audio] Searched in: current directory, assets/audio, parent/assets/audio");
            playing = false;
            return;
        }
        System.out.println("[Audio] Found file at: " + audioFile.getAbsolutePath());

        // Check file extension - use system player for non-MP3 files
        String fileName = audioFile.getName().toLowerCase();
        if (fileName.endsWith(".m4a") || fileName.endsWith(".aac") || fileName.endsWith(".wav") || fileName.endsWith(".flac")) {
            playWithSystemPlayer(audioFile);
            return;
        }

        // Try to use TuxDroid-specific audio device on Windows
        if (IS_WINDOWS) {
            Mixer.Info tuxMixer = findTuxMixer();
            if (tuxMixer != null) {
                System.out.println("[Audio] Using TuxDroid hardware: " + tuxMixer.getName());
                playWithDirectOutput(audioFile, tuxMixer);
                return;
            }
        }
        
        // Fallback: Use JLayer's default player (works on both platforms)
        playWithJLayer(audioFile);
    }

    /**
     * Play using JLayer's built-in player (default audio output).
     */
    private static void playWithJLayer(File audioFile) {
        try {
            InputStream fis = new FileInputStream(audioFile);
            jlayerPlayer = new Player(fis);
            jlayerPlayer.play(); // This blocks!
        } catch (Exception e) {
            if (playing) { // Only show error if not manually stopped
                System.err.println("[Audio Error] " + e.getMessage());
            }
        } finally {
            jlayerPlayer = null;
            playing = false;
        }
    }

    /**
     * Play with direct output to TuxDroid hardware (Windows).
     * Decodes MP3 and outputs 8-bit mono which the TuxDroid hardware prefers.
     */
    private static void playWithDirectOutput(File audioFile, Mixer.Info targetMixer) {
        try {
            InputStream fis = new FileInputStream(audioFile);
            Bitstream bitstream = new Bitstream(fis);
            Decoder decoder = new Decoder();

            // Decode first frame to get audio format
            Header header = bitstream.readFrame();
            if (header == null) {
                System.err.println("[Audio Error] Cannot read MP3 header!");
                playing = false;
                return;
            }

            int sampleRate = header.frequency();
            // Use 8-bit Mono for TuxDroid hardware compatibility
            AudioFormat format = new AudioFormat(sampleRate, 8, 1, true, false);
            System.out.println("[Audio] Format: " + sampleRate + "Hz, 8-bit, Mono (hardware mode)");

            // Open audio line on TuxDroid device
            DataLine.Info lineInfo = new DataLine.Info(SourceDataLine.class, format);
            Mixer mixer = AudioSystem.getMixer(targetMixer);
            currentLine = (SourceDataLine) mixer.getLine(lineInfo);
            currentLine.open(format);
            currentLine.start();

            // Try to maximize volume
            try {
                if (currentLine.isControlSupported(FloatControl.Type.MASTER_GAIN)) {
                    FloatControl vol = (FloatControl) currentLine.getControl(FloatControl.Type.MASTER_GAIN);
                    vol.setValue(vol.getMaximum());
                }
            } catch (Exception e) {
                // Volume control not available, ignore
            }

            // Decode and play loop
            bitstream.closeFrame();
            while (playing) {
                header = bitstream.readFrame();
                if (header == null) break;

                SampleBuffer output = (SampleBuffer) decoder.decodeFrame(header, bitstream);
                short[] samples = output.getBuffer();
                int len = output.getBufferLength();

                boolean isStereo = (header.mode() != Header.SINGLE_CHANNEL);

                // Convert 16-bit to 8-bit Mono
                byte[] bytes;
                if (isStereo) {
                    int stereoLen = len - (len % 2);
                    bytes = new byte[stereoLen / 2];
                    for (int i = 0; i < stereoLen; i += 2) {
                        int val = (samples[i] + samples[i + 1]) / 2;
                        bytes[i / 2] = (byte) (val >> 8);
                    }
                } else {
                    bytes = new byte[len];
                    for (int i = 0; i < len; i++) {
                        bytes[i] = (byte) (samples[i] >> 8);
                    }
                }

                currentLine.write(bytes, 0, bytes.length);
                bitstream.closeFrame();
            }

            currentLine.drain();
            currentLine.close();
            bitstream.close();
            System.out.println("[Audio] Playback finished.");

        } catch (Exception e) {
            if (playing) {
                System.err.println("[Audio Error] " + e.getMessage());
                e.printStackTrace();
            }
        } finally {
            playing = false;
            currentLine = null;
        }
    }

    private static Process systemPlayerProcess = null;

    /**
     * Stop playback immediately. Can be called from another thread.
     */
    public static void stop() {
        playing = false;
        
        // Stop JLayer player
        if (jlayerPlayer != null) {
            try {
                jlayerPlayer.close();
            } catch (Exception e) {
                // Ignore
            }
            jlayerPlayer = null;
        }
        
        // Stop direct output line
        if (currentLine != null) {
            try {
                currentLine.stop();
                currentLine.close();
            } catch (Exception e) {
                // Ignore
            }
            currentLine = null;
        }
        
        // Stop system player process
        if (systemPlayerProcess != null && systemPlayerProcess.isAlive()) {
            try {
                systemPlayerProcess.destroyForcibly();
            } catch (Exception e) {
                // Ignore
            }
            systemPlayerProcess = null;
        }
    }

    /**
     * Find the TuxDroid audio mixer on Windows.
     */
    private static Mixer.Info findTuxMixer() {
        try {
            Mixer.Info[] mixers = AudioSystem.getMixerInfo();
            for (Mixer.Info info : mixers) {
                String name = info.getName();
                // Look for TuxDroid-Audio (not TuxDroid-TTS or Port devices)
                if (name.contains("TuxDroid-Audio") && !name.contains("Port")) {
                    return info;
                }
            }
        } catch (Exception e) {
            // Ignore errors in mixer detection
        }
        return null;
    }

    /**
     * Play audio file using system's default audio player (for M4A, AAC, etc.)
     */
    private static void playWithSystemPlayer(File audioFile) {
        try {
            String os = System.getProperty("os.name").toLowerCase();
            ProcessBuilder pb;
            
            if (os.contains("win")) {
                // Windows: Use Windows Media Player or default player
                String filePath = audioFile.getAbsolutePath();
                // Use cmd to open with default player (hidden window)
                pb = new ProcessBuilder("cmd", "/c", "start", "/MIN", "\"\"" , filePath);
            } else {
                // Linux: Use ffplay, mpg123, or aplay
                if (commandExists("ffplay")) {
                    pb = new ProcessBuilder("ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", 
                        audioFile.getAbsolutePath());
                } else if (commandExists("mpg123")) {
                    pb = new ProcessBuilder("mpg123", "-q", audioFile.getAbsolutePath());
                } else if (commandExists("aplay")) {
                    pb = new ProcessBuilder("aplay", audioFile.getAbsolutePath());
                } else {
                    System.err.println("[Audio Error] No suitable audio player found for M4A files!");
                    System.err.println("[Audio] Install ffplay: sudo apt install ffmpeg");
                    System.err.println("[Audio] Continuing dance without audio...");
                    playing = false;
                    return;
                }
            }
            
            pb.redirectErrorStream(true);
            systemPlayerProcess = pb.start();
            
            System.out.println("[Audio] Playing with system player...");
            
            // Wait for process to finish (or until stopped)
            Thread waitThread = new Thread(() -> {
                try {
                    systemPlayerProcess.waitFor();
                    playing = false;
                    System.out.println("[Audio] Playback finished.");
                } catch (InterruptedException e) {
                    if (systemPlayerProcess != null) {
                        systemPlayerProcess.destroyForcibly();
                    }
                    playing = false;
                }
            });
            waitThread.start();
            
            // Monitor playing flag and stop if needed
            while (playing && systemPlayerProcess != null && systemPlayerProcess.isAlive()) {
                Thread.sleep(100);
            }
            
            if (systemPlayerProcess != null && systemPlayerProcess.isAlive()) {
                systemPlayerProcess.destroyForcibly();
                System.out.println("[Audio] Stopped by user.");
            }
            
            systemPlayerProcess = null;
            playing = false;
            
        } catch (Exception e) {
            System.err.println("[Audio Error] Failed to play with system player: " + e.getMessage());
            System.err.println("[Audio] Continuing dance without audio...");
            playing = false;
        }
    }

    /**
     * Check if a command exists in PATH
     */
    private static boolean commandExists(String command) {
        try {
            String os = System.getProperty("os.name").toLowerCase();
            ProcessBuilder pb;
            if (os.contains("win")) {
                pb = new ProcessBuilder("where", command);
            } else {
                pb = new ProcessBuilder("which", command);
            }
            Process p = pb.start();
            int exitCode = p.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Try to find the audio file in multiple locations.
     */
    private static File resolveAudioFile(String filename) {
        // If it's already an absolute path or exists as-is
        File direct = new File(filename);
        if (direct.exists() && direct.isFile()) {
            return direct;
        }
        
        // Extract just the filename if a path was given
        String baseName = new File(filename).getName();
        
        // Try paths in order of priority
        String[] searchPaths = {
            filename,                           // As given
            "./" + filename,                    // Current directory
            "assets/audio/" + baseName,         // Local assets folder
            "../assets/audio/" + baseName,      // Parent's assets folder
            "assets/audio/" + filename,         // Local assets with full name
            "../assets/audio/" + filename,      // Parent's assets with full name
        };

        for (String path : searchPaths) {
            File f = new File(path);
            if (f.exists() && f.isFile()) {
                return f;
            }
        }
        return null;
    }
}

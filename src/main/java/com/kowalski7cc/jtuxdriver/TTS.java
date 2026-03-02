package com.kowalski7cc.jtuxdriver;


/**
 * Cross-platform Text-to-Speech for TuxDroid.
 * - Windows: Uses built-in PowerShell Speech Synthesis (no installation needed)
 * - Linux: Uses espeak or espeak-ng (install with: sudo apt install espeak)
 */
public class TTS {

    private static final boolean IS_WINDOWS = System.getProperty("os.name").toLowerCase().contains("win");
    private static final boolean IS_LINUX = System.getProperty("os.name").toLowerCase().contains("linux");
    
    // Cache for Linux TTS availability check
    private static Boolean espeakAvailable = null;

    public enum Voice {
        NORMAL("", ""),
        WHISPER("-a 20", "-s 120"),      // Quiet, slower
        ANGRY("-p 20", "-s 200"),        // Deep pitch, fast
        CUTE("-p 80", "-s 150"),         // High pitch
        SAD("-p 30", "-s 80"),           // Deep, slow
        ROBOT("-p 50", "-s 140"),        // Monotone
        ANNOUNCER("-p 10", "-s 110");    // Deep, authoritarian

        final String args;

        Voice(String... args) {
            this.args = String.join(" ", args);
        }
    }

    /**
     * Speak text using default voice.
     */
    public static void say(String text) {
        say(text, Voice.NORMAL);
    }

    /**
     * Speak text using specified voice.
     */
    public static void say(String text, Voice voice) {
        if (text == null || text.trim().isEmpty()) {
            return;
        }
        
        System.out.println("[TTS] Speaking: " + text);

        try {
            if (IS_WINDOWS) {
                sayWindows(text, voice);
            } else if (IS_LINUX) {
                sayLinux(text, voice);
            } else {
                System.err.println("[TTS] Unsupported operating system");
            }
        } catch (Exception e) {
            System.err.println("[TTS Error] " + e.getMessage());
        }
    }

    /**
     * Windows TTS using PowerShell Speech Synthesis.
     */
    private static void sayWindows(String text, Voice voice) throws Exception {
        // Escape single quotes for PowerShell
        String escapedText = text.replace("'", "''").replace("\"", "\\\"");
        
        // Build PowerShell command
        String psCommand = String.format(
            "Add-Type -AssemblyName System.Speech; " +
            "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; " +
            "try { $synth.SelectVoiceByHints('Male'); } catch { }; " +  // Try male voice, ignore if not available
            "$synth.Speak('%s');",
            escapedText
        );

        ProcessBuilder pb = new ProcessBuilder("powershell", "-NoProfile", "-NonInteractive", "-Command", psCommand);
        pb.redirectErrorStream(true);
        Process process = pb.start();
        
        // Wait for speech to complete (with timeout)
        boolean finished = process.waitFor(30, java.util.concurrent.TimeUnit.SECONDS);
        if (!finished) {
            process.destroyForcibly();
            System.err.println("[TTS] Speech timed out");
        }
    }

    /**
     * Linux TTS using espeak or espeak-ng.
     */
    private static void sayLinux(String text, Voice voice) throws Exception {
        // Check if espeak is available
        if (espeakAvailable == null) {
            espeakAvailable = checkEspeakAvailable();
        }
        
        if (!espeakAvailable) {
            System.err.println("[TTS] espeak not installed! Install with: sudo apt install espeak");
            System.err.println("[TTS] Text was: " + text);
            return;
        }

        String device = System.getProperty("tux.audio.dev");
        String voiceArgs = (voice.args != null && !voice.args.isEmpty()) ? " " + voice.args : "";
        String espeakCmd = String.format("espeak -v en%s \"%s\"", voiceArgs, text.replace("\"", "\\\""));

        ProcessBuilder pb;
        if (device != null && !device.isEmpty() && !device.equals("default")) {
            // Pipe through aplay to specific device
            String cmd = String.format("%s --stdout | aplay -D %s 2>/dev/null", espeakCmd, device);
            pb = new ProcessBuilder("sh", "-c", cmd);
        } else {
            // Direct espeak output
            pb = new ProcessBuilder("sh", "-c", espeakCmd);
        }
        
        pb.redirectErrorStream(true);
        Process process = pb.start();
        
        // Wait for speech to complete (with timeout)
        boolean finished = process.waitFor(30, java.util.concurrent.TimeUnit.SECONDS);
        if (!finished) {
            process.destroyForcibly();
            System.err.println("[TTS] Speech timed out");
        }
    }

    /**
     * Check if espeak or espeak-ng is available on Linux.
     */
    private static boolean checkEspeakAvailable() {
        try {
            Process p = new ProcessBuilder("which", "espeak").start();
            int exitCode = p.waitFor();
            if (exitCode == 0) {
                return true;
            }
            
            // Try espeak-ng as fallback
            p = new ProcessBuilder("which", "espeak-ng").start();
            exitCode = p.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Check if TTS is available on current platform.
     */
    public static boolean isAvailable() {
        if (IS_WINDOWS) {
            return true; // PowerShell is always available on Windows
        } else if (IS_LINUX) {
            if (espeakAvailable == null) {
                espeakAvailable = checkEspeakAvailable();
            }
            return espeakAvailable;
        }
        return false;
    }
}

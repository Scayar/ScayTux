package com.kowalski7cc.jtuxdriver.cli;

/**
 * ScayTux - The Ultimate Tux Droid Controller
 * 
 * @author Scayar
 * @version 3.0
 * @website https://github.com/Scayar
 * @email Scayar.exe@gmail.com
 */

import com.kowalski7cc.jtuxdriver.TuxDroid;
import com.kowalski7cc.jtuxdriver.TuxCombos;
import com.kowalski7cc.jtuxdriver.TTS;
import com.kowalski7cc.jtuxdriver.AudioPlayer;
import com.kowalski7cc.jtuxdriver.core.HidTransport;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;

import java.io.IOException;
import java.util.concurrent.Callable;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.ThreadLocalRandom;

@Command(name = "scaytux", mixinStandardHelpOptions = true, version = "ScayTux 3.0 by Scayar", 
         description = "ScayTux - The Ultimate Tux Droid Controller",
         header = {
             "",
             "@|cyan  ███████╗ ██████╗ █████╗ ██╗   ██╗████████╗██╗   ██╗██╗  ██╗|@",
             "@|cyan  ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║   ██║╚██╗██╔╝|@",
             "@|cyan  ███████╗██║     ███████║ ╚████╔╝    ██║   ██║   ██║ ╚███╔╝ |@",
             "@|cyan  ╚════██║██║     ██╔══██║  ╚██╔╝     ██║   ██║   ██║ ██╔██╗ |@",
             "@|cyan  ███████║╚██████╗██║  ██║   ██║      ██║   ╚██████╔╝██╔╝ ██╗|@",
             "@|cyan  ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═╝|@",
             "",
             "@|yellow Made with ♥ by Scayar - github.com/Scayar|@",
             ""
         })
public class Main implements Callable<Integer> {

    @Option(names = { "-l", "--list" }, description = "List connected devices (dummy check)")
    boolean listDevices;

    @Option(names = { "-d", "--debug" }, description = "Run deep generic HID debug")
    boolean debugMode;

    @Option(names = { "--flap" }, description = "Flap wings")
    boolean flap;

    @Option(names = { "--eyes" }, description = "Set eyes (true/on or false/off)", arity = "1")
    Boolean eyes;

    @Option(names = { "--blink" }, description = "Blink eyes N times")
    Integer blink;

    @Option(names = { "--mouth" }, description = "Set mouth (true/open or false/closed)", arity = "1")
    Boolean mouth;

    @Option(names = { "--talk" }, description = "Move mouth N times (simulate talking)")
    Integer talk;

    @Option(names = { "--spin" }, description = "Spin direction (left/right)")
    String spin;

    @Option(names = { "--val" }, description = "Duration (loops) for spin command", defaultValue = "20")
    int genericValue;

    @Option(names = { "--led" }, description = "Set LED color ID (0-255)")
    Integer ledColor;

    @Option(names = { "--intensity" }, description = "Set LED intensity (0-255, default 1)", defaultValue = "1")
    Integer ledIntensity;

    @Option(names = { "--say" }, description = "Speak text using TTS")
    String sayText;

    @Option(names = { "--combo" }, description = "Run a combo (1-20)")
    Integer comboId;

    @Option(names = { "--play" }, description = "Play MP3 file and dance")
    String musicFile;

    @Option(names = { "--spin-doctor" }, description = "Run spin motor diagnostic")
    boolean spinDoctor;

    @Option(names = { "-i", "--interactive" }, description = "Force interactive mode")
    boolean interactiveMode;

    @Override
    public Integer call() throws Exception {
        if (debugMode) {
            runDebug();
            return 0;
        }

        if (listDevices) {
            checkDevices();
            return 0;
        }

        try (TuxDroid tux = new TuxDroid(new HidTransport())) {
            tux.open();

            // --- Music Player + Auto Dance ---
            if (musicFile != null) {
                System.out.println("[CMD] DJ Mode Activated: Playing " + musicFile);

                AtomicBoolean isPlaying = new AtomicBoolean(true);
                Thread audioThread = new Thread(() -> {
                    AudioPlayer.play(musicFile);
                    isPlaying.set(false);
                });
                audioThread.start();

                // Dance while music plays!
                TuxCombos combos = new TuxCombos(tux);
                System.out.println(">>> DANCING STARTED <<<");
                while (isPlaying.get()) {
                    // Pick a random dance move
                    int move = ThreadLocalRandom.current().nextInt(1, 4);
                    switch (move) {
                        case 1:
                            combos.runCombo(49);
                            break; // DJ Mode
                        case 2:
                            combos.runCombo(46);
                            break; // Rap Mode (Beatbox)
                        case 3:
                            combos.runCombo(17);
                            break; // Basic Beatbox
                        default:
                            tux.flapWings();
                    }
                    // Wait a bit between moves to let them finish
                    try {
                        Thread.sleep(500);
                    } catch (Exception e) {
                    }
                }
                System.out.println(">>> MUSIC FINISHED <<<");
                tux.flapWings(); // Bow

                return 0;
            }

            // --- Lip Sync with Organic Randomness ---
            if (sayText != null) {
                System.out.println("[CMD] Speaking with Organic Lip Sync: \"" + sayText + "\"");

                AtomicBoolean isTalking = new AtomicBoolean(true);
                Thread mouthThread = new Thread(() -> {
                    try {
                        while (isTalking.get()) {
                            tux.openMouth();
                            Thread.sleep(ThreadLocalRandom.current().nextInt(50, 250));
                            tux.closeMouth();
                            Thread.sleep(ThreadLocalRandom.current().nextInt(50, 150));
                        }
                    } catch (Exception e) {
                    }
                });
                mouthThread.start();

                TTS.say(sayText);

                isTalking.set(false);
                mouthThread.join(1000);
                tux.closeMouth();

                if (!hasHardwareAction())
                    return 0;
            }

            if (spinDoctor) {
                runSpinDoctor(tux);
                return 0;
            }

            if (comboId != null) {
                System.out.println("[CMD] Running Combo #" + comboId);
                new TuxCombos(tux).runCombo(comboId);
            }
            if (eyes != null)
                tux.setEyes(eyes);
            if (blink != null)
                tux.blinkEyes(blink);
            if (mouth != null)
                tux.setMouth(mouth);
            if (talk != null)
                tux.moveMouth(talk);
            if (flap)
                tux.flapWings();
            if (ledColor != null)
                tux.setLed(ledColor, ledIntensity);

            if (spin != null) {
                System.out.println("[CMD] Spinning " + spin + " (Duration=" + genericValue + " loops)...");
                if ("left".equalsIgnoreCase(spin))
                    tux.spinLeft(genericValue);
                else if ("right".equalsIgnoreCase(spin))
                    tux.spinRight(genericValue);
            }

            Thread.sleep(200);
        } catch (IOException e) {
            System.err.println("[ERROR] Communication failure: " + e.getMessage());
            return 1;
        }
        return 0;
    }

    private boolean hasHardwareAction() {
        return comboId != null || flap || eyes != null || blink != null
                || mouth != null || talk != null || spin != null || ledColor != null || spinDoctor;
    }

    private void checkDevices() {
        System.out.println("[CMD] Checking for Tux Droid...");
        try (HidTransport transport = new HidTransport()) {
            transport.open();
            if (transport.isOpen())
                System.out.println("FOUND: Tux Droid connected!");
        } catch (Exception e) {
            System.out.println("No Tux Droid found.");
        }
    }

    private void runSpinDoctor(TuxDroid tux) throws IOException {
        System.out.println("=== SPIN DOCTOR V2 ===");
        tux.spinLeft(50);
    }

    private void runDebug() throws IOException {
        System.out.println(InteractiveMode.BOLD + "[DEBUG] HID Input Monitor Started" + InteractiveMode.RESET);
        System.out.println("Press Ctrl+C to stop.");
        System.out.println("Waiting for data...");

        try (TuxDroid tux = new TuxDroid(new HidTransport())) {
            tux.open();

            // Register a listener to print every packet
            tux.setInputListener((data) -> {
                StringBuilder sb = new StringBuilder();
                for (byte b : data) {
                    sb.append(String.format("%02X ", b));
                }
                System.out.print("\r[IN] " + sb.toString());
            });

            // Keep alive and probe
            System.out.println("Sending status probes every 2s...");
            while (true) {
                try {
                    // Sending CONNECT as a heartbeat/ping
                    tux.open();
                    Thread.sleep(2000);
                } catch (IOException e) {
                    // ignore connection errors (device might be busy or disconnected)
                }
            }
        } catch (InterruptedException e) {
            System.out.println("\n[DEBUG] Stopped.");
        }
    }

    public static void main(String[] args) {
        // Check for --interactive or -i flag, or no arguments
        boolean forceInteractive = false;
        for (String arg : args) {
            if (arg.equals("-i") || arg.equals("--interactive")) {
                forceInteractive = true;
                break;
            }
        }
        
        // Launch Interactive Mode if no arguments or --interactive flag
        if (args.length == 0 || forceInteractive) {
            new InteractiveMode().start();
        } else {
            // Otherwise classic CLI behavior
            int exitCode = new CommandLine(new Main()).execute(args);
            System.exit(exitCode);
        }
    }
}

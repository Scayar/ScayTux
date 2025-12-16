package com.kowalski7cc.jtuxdriver.cli;

import picocli.CommandLine;
import com.kowalski7cc.jtuxdriver.telegram.TelegramManager;
import com.kowalski7cc.jtuxdriver.telegram.TelegramManager.TelegramConfig;

import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * ScayTux - Interactive Mode
 * 
 * @author Scayar
 * @website https://github.com/Scayar
 * @email Scayar.exe@gmail.com
 */
public class InteractiveMode {

    // ANSI Colors
    public static final String RESET = "\u001B[0m";
    public static final String RED = "\u001B[31m";
    public static final String GREEN = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String BLUE = "\u001B[34m";
    public static final String PURPLE = "\u001B[35m";
    public static final String CYAN = "\u001B[36m";
    public static final String BOLD = "\u001B[1m";
    public static final String DIM = "\u001B[2m";

    private final Scanner scanner;
    private TelegramManager telegramManager;

    public InteractiveMode() {
        this.scanner = new Scanner(System.in);
        this.telegramManager = new TelegramManager();
    }

    public void start() {
        clearScreen();
        printBanner();

        while (true) {
            System.out.println(BOLD + "\n[ MAIN MENU ]" + RESET);
            System.out.println("1. " + CYAN + "Interactive Menu" + RESET + " (Select combos by number)");
            System.out.println("2. " + PURPLE + "Manual / REPL Mode" + RESET + " (Type commands freely)");
            System.out.println("3. " + BLUE + "📱 Telegram Control" + RESET + " (Control via Telegram Bot)");
            System.out.println("4. " + RED + "Exit" + RESET);
            printFooter();
            System.out.print("\n" + YELLOW + "scaytux> " + RESET);

            String input = scanner.nextLine().trim();

            switch (input) {
                case "1":
                    runInteractiveMenu();
                    break;
                case "2":
                    runManualMode();
                    break;
                case "3":
                    runTelegramMenu();
                    break;
                case "4":
                case "exit":
                case "quit":
                    // Cleanup
                    if (telegramManager != null && telegramManager.isRunning()) {
                        telegramManager.stopBot();
                    }
                    System.out.println(GREEN + "Goodbye, human! 🐧" + RESET);
                    return;
                default:
                    System.out.println(RED + "Invalid option." + RESET);
            }
        }
    }

    private void runTelegramMenu() {
        while (true) {
            clearScreen();
            System.out.println(BOLD + BLUE + "\n╔═══════════════════════════════════════════════════════════╗" + RESET);
            System.out.println(BOLD + BLUE + "║          📱 TELEGRAM REMOTE CONTROL 📱                    ║" + RESET);
            System.out.println(BOLD + BLUE + "╚═══════════════════════════════════════════════════════════╝" + RESET);
            
            // Show current status
            TelegramConfig config = telegramManager.loadConfig();
            boolean hasConfig = config.isValid();
            boolean isRunning = telegramManager.isRunning();
            
            System.out.println();
            System.out.println(DIM + "Current Status:" + RESET);
            System.out.println("  Bot Token: " + (hasConfig ? GREEN + "✓ Configured" + RESET : RED + "✗ Not set" + RESET));
            System.out.println("  Chat ID:   " + (hasConfig ? GREEN + "✓ Configured" + RESET : RED + "✗ Not set" + RESET));
            System.out.println("  Bot:       " + (isRunning ? GREEN + "🟢 Running" + RESET : RED + "🔴 Stopped" + RESET));
            System.out.println();
            
            System.out.println(CYAN + "--- OPTIONS ---" + RESET);
            System.out.println("1. " + YELLOW + "📝 Configure Bot" + RESET + " (Set Token & Chat ID)");
            System.out.println("2. " + GREEN + "▶️  Start Bot" + RESET);
            System.out.println("3. " + RED + "⏹️  Stop Bot" + RESET);
            System.out.println("4. " + BLUE + "📖 How to Create a Bot" + RESET);
            System.out.println("5. " + PURPLE + "🔍 Test Connection" + RESET);
            System.out.println("0. " + DIM + "Back to Main Menu" + RESET);
            printFooter();
            System.out.print("\n" + YELLOW + "telegram> " + RESET);

            String input = scanner.nextLine().trim();
            
            switch (input) {
                case "1":
                    configureTelegram();
                    break;
                case "2":
                    startTelegramBot();
                    break;
                case "3":
                    stopTelegramBot();
                    break;
                case "4":
                    showBotInstructions();
                    break;
                case "5":
                    testTelegramConnection();
                    break;
                case "0":
                case "back":
                    return;
                default:
                    System.out.println(RED + "Invalid option." + RESET);
                    pause();
            }
        }
    }

    private void configureTelegram() {
        clearScreen();
        System.out.println(BOLD + YELLOW + "\n=== CONFIGURE TELEGRAM BOT ===" + RESET);
        System.out.println();
        System.out.println(DIM + "You need two things:" + RESET);
        System.out.println("  1. Bot Token (from @BotFather)");
        System.out.println("  2. Your Chat ID (from @userinfobot)");
        System.out.println();
        System.out.println(DIM + "Press Enter without typing to keep current value." + RESET);
        System.out.println();

        TelegramConfig config = telegramManager.loadConfig();

        // Get Bot Token
        System.out.print(CYAN + "Bot Token" + RESET);
        if (!config.botToken.isEmpty()) {
            String masked = config.botToken.substring(0, Math.min(10, config.botToken.length())) + "...";
            System.out.print(" [current: " + masked + "]");
        }
        System.out.print(": ");
        String token = scanner.nextLine().trim();
        if (!token.isEmpty()) {
            if (TelegramManager.isValidTokenFormat(token)) {
                config.botToken = token;
                System.out.println(GREEN + "✓ Token saved" + RESET);
            } else {
                System.out.println(RED + "✗ Invalid token format! Should be like: 123456789:ABCdef..." + RESET);
                pause();
                return;
            }
        }

        // Get Chat ID
        System.out.print(CYAN + "Chat ID" + RESET);
        if (!config.chatId.isEmpty()) {
            System.out.print(" [current: " + config.chatId + "]");
        }
        System.out.print(": ");
        String chatId = scanner.nextLine().trim();
        if (!chatId.isEmpty()) {
            if (TelegramManager.isValidChatIdFormat(chatId)) {
                config.chatId = chatId;
                System.out.println(GREEN + "✓ Chat ID saved" + RESET);
            } else {
                System.out.println(RED + "✗ Invalid Chat ID format! Should be numbers only." + RESET);
                pause();
                return;
            }
        }

        // Save configuration
        telegramManager.saveConfig(config);
        System.out.println();
        System.out.println(GREEN + "✅ Configuration saved successfully!" + RESET);
        System.out.println(DIM + "You can now start the bot from the Telegram menu." + RESET);
        pause();
    }

    private void startTelegramBot() {
        if (telegramManager.isRunning()) {
            System.out.println(YELLOW + "⚠️ Bot is already running!" + RESET);
            pause();
            return;
        }

        TelegramConfig config = telegramManager.loadConfig();
        
        if (!config.isValid()) {
            System.out.println(RED + "❌ Bot not configured!" + RESET);
            System.out.println("Please configure the bot first (Option 1).");
            pause();
            return;
        }

        System.out.println();
        System.out.println(YELLOW + "🔄 Starting Telegram bot..." + RESET);
        
        boolean success = telegramManager.startBot(config.botToken, config.chatId);
        
        if (success) {
            System.out.println();
            System.out.println(GREEN + "╔═══════════════════════════════════════════════════════════╗" + RESET);
            System.out.println(GREEN + "║              ✅ BOT STARTED SUCCESSFULLY!                 ║" + RESET);
            System.out.println(GREEN + "╠═══════════════════════════════════════════════════════════╣" + RESET);
            System.out.println(GREEN + "║                                                           ║" + RESET);
            System.out.println(GREEN + "║  📱 Open Telegram and send /start to your bot!           ║" + RESET);
            System.out.println(GREEN + "║                                                           ║" + RESET);
            System.out.println(GREEN + "║  The bot will keep running in the background.            ║" + RESET);
            System.out.println(GREEN + "║  You can use other ScayTux features while it runs!       ║" + RESET);
            System.out.println(GREEN + "║                                                           ║" + RESET);
            System.out.println(GREEN + "╚═══════════════════════════════════════════════════════════╝" + RESET);
        } else {
            System.out.println();
            System.out.println(RED + "❌ Failed to start bot!" + RESET);
            System.out.println("Please check:");
            System.out.println("  • Bot token is correct");
            System.out.println("  • Internet connection is working");
        }
        
        pause();
    }

    private void stopTelegramBot() {
        if (!telegramManager.isRunning()) {
            System.out.println(YELLOW + "ℹ️ Bot is not running." + RESET);
            pause();
            return;
        }

        telegramManager.stopBot();
        System.out.println(GREEN + "✅ Bot stopped successfully." + RESET);
        pause();
    }

    private void showBotInstructions() {
        clearScreen();
        System.out.println(TelegramManager.getBotCreationInstructions());
        pause();
    }

    private void testTelegramConnection() {
        TelegramConfig config = telegramManager.loadConfig();
        
        if (!config.isValid()) {
            System.out.println(RED + "❌ Please configure the bot first!" + RESET);
            pause();
            return;
        }

        System.out.println(YELLOW + "🔄 Testing connection..." + RESET);
        
        // Just try to start and immediately check
        if (!telegramManager.isRunning()) {
            boolean success = telegramManager.startBot(config.botToken, config.chatId);
            if (success) {
                System.out.println(GREEN + "✅ Connection successful! Bot is now running." + RESET);
                System.out.println(DIM + "Send /start in Telegram to test." + RESET);
            }
        } else {
            System.out.println(GREEN + "✅ Bot is running and connected!" + RESET);
        }
        
        pause();
    }

    private void pause() {
        System.out.println();
        System.out.print(DIM + "Press Enter to continue..." + RESET);
        scanner.nextLine();
    }

    private void printFooter() {
        System.out.println();
        System.out.println(DIM + "─────────────────────────────────────────────────────" + RESET);
        System.out.println(DIM + "  Made with " + RED + "♥" + DIM + " by " + CYAN + "Scayar" + DIM + " | github.com/Scayar" + RESET);
        System.out.println(DIM + "─────────────────────────────────────────────────────" + RESET);
    }

    private void runInteractiveMenu() {
        while (true) {
            System.out.println(BOLD + "\n[ INTERACTIVE MENU ]" + RESET);
            System.out.println(CYAN + "--- CATEGORIES ---" + RESET);
            System.out.println("1. " + BLUE + "Show Top 10 Cinematic Combos" + RESET);
            System.out.println("2. " + BLUE + "Show All 50 Combos" + RESET);
            System.out.println("3. " + BLUE + "Basic Controls (Eyes, Wings, Spin...)" + RESET);
            System.out.println("4. " + BLUE + "Diagnostics" + RESET);
            System.out.println("5. " + PURPLE + "Music Player Menu" + RESET);
            System.out.println("0. " + YELLOW + "Back to Main Menu" + RESET);
            printFooter();
            System.out.print("\n" + YELLOW + "select> " + RESET);

            String input = scanner.nextLine().trim();
            if (input.equals("0"))
                return;

            switch (input) {
                case "1":
                    showCombos(1, 10);
                    break;
                case "2":
                    showCombos(1, 50);
                    break;
                case "3":
                    showBasicControls();
                    break;
                case "4":
                    executeCmd("--spin-doctor");
                    break;
                case "5":
                    runMusicMenu();
                    break;
                case "6":
                    runMusicMenu();
                    break;
                default:
                    try {
                        int id = Integer.parseInt(input);
                        if (id >= 1 && id <= 55)
                            executeCmd("--combo " + id);
                        else
                            System.out.println(RED + "Invalid selection." + RESET);
                    } catch (NumberFormatException e) {
                        System.out.println(RED + "Invalid input." + RESET);
                    }
            }
        }
    }

    private void runMusicMenu() {
        while (true) {
            System.out.println(BOLD + "\n[ MUSIC PLAYER MENU ]" + RESET);
            System.out.println("1. " + RED + "Michael Jackson Mode" + RESET + " (Billie Jean)");
            System.out.println("2. " + YELLOW + "Chicken Song Mode" + RESET + " (Crazy Dance)");
            System.out.println("3. " + PURPLE + "Suirian Dabkah Mode" + RESET + " (Traditional Dance - 2 mins)");
            System.out.println("4. " + CYAN + "Crazy Mode" + RESET + " (crazy.mp3 - 2 mins)");
            System.out.println("5. " + GREEN + "Say My Name Mode" + RESET + " (Say My Name.mp3 - 2 mins)");
            System.out.println("6. " + BLUE + "Manual Play" + RESET + " (Enter Filename)");
            System.out.println("0. " + GREEN + "Back" + RESET);
            printFooter();
            System.out.print("\n" + PURPLE + "music> " + RESET);

            String sub = scanner.nextLine().trim();
            if (sub.equals("0"))
                return;

            switch (sub) {
                case "1":
                    runSpecialDance(51);
                    break;
                case "2":
                    runSpecialDance(52);
                    break;
                case "3":
                    runSpecialDance(53);
                    break;
                case "4":
                    runSpecialDance(54);
                    break;
                case "5":
                    runSpecialDance(55);
                    break;
                case "6":
                    System.out.print("Enter path to MP3: ");
                    String f = scanner.nextLine().trim();
                    if (!f.isEmpty())
                        executeCmd("--play \"" + f + "\"");
                    break;
            }
        }
    }

    private void runSpecialDance(int comboId) {
        System.out.println(RED + ">>> STARTING DANCE MODE. Type 'stop' + Enter to kill it. <<<" + RESET);
        java.util.concurrent.atomic.AtomicBoolean runFlag = new java.util.concurrent.atomic.AtomicBoolean(true);
        Thread t = new Thread(() -> {
            try (com.kowalski7cc.jtuxdriver.TuxDroid tux = new com.kowalski7cc.jtuxdriver.TuxDroid(
                    new com.kowalski7cc.jtuxdriver.core.HidTransport())) {
                tux.open();
                new com.kowalski7cc.jtuxdriver.TuxCombos(tux).runCombo(comboId, runFlag);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        t.start();

        while (runFlag.get()) {
            if (scanner.hasNextLine()) {
                String cmd = scanner.nextLine().trim();
                if (cmd.equalsIgnoreCase("stop")) {
                    System.out.println("Stopping...");
                    runFlag.set(false);
                    try {
                        t.join(2000);
                    } catch (Exception e) {
                    }
                    break;
                }
            }
        }
    }

    private void showCombos(int start, int end) {
        System.out.println(BOLD + "\n--- CINEMATIC COMBOS (" + start + "-" + end + ") ---" + RESET);

        String[] specificNames = {
                "Royal Entrance", "Bird Flex", "Brain Loading", "Sleep Mode", "Hacker Alert",
                "Police Mode", "Shy Bird", "Laugh Mode", "Kiss 😘", "Bird Crying"
        };

        for (int i = start; i <= end; i++) {
            String name = (i <= 10) ? specificNames[i - 1] : getComboName(i);
            System.out.printf("[%2d] %-25s ", i, name);
            if (i % 2 == 0)
                System.out.println();
        }
        System.out.println("\n" + GREEN + "Enter ID number to run:" + RESET);
        String choice = scanner.nextLine().trim();
        try {
            int id = Integer.parseInt(choice);
            executeCmd("--combo " + id);
        } catch (Exception e) {
            System.out.println(RED + "Cancelled." + RESET);
        }
    }

    private String getComboName(int id) {
        switch (id) {
            case 11: return "Death Restart";
            case 12: return "Power Up";
            case 13: return "Wake from Dead";
            case 14: return "Celebration Jump";
            case 15: return "Virus Mode";
            case 16: return "TikTok Headshake";
            case 17: return "Bird Beatbox";
            case 18: return "Matrix Enter";
            case 19: return "Soldier Salute";
            case 20: return "Confused Bird";
            case 21: return "Wait What?";
            case 22: return "Suspicious";
            case 23: return "Sir Yes Sir";
            case 24: return "Cyber Scan";
            case 25: return "Great Idea";
            case 26: return "No No No";
            case 27: return "Yesss!";
            case 28: return "Broken Robot";
            case 29: return "Romantic Bird";
            case 30: return "Mafia Don";
            case 31: return "Ninja Silent";
            case 32: return "Wake Ninja";
            case 33: return "Jump Scare";
            case 34: return "Sad Apology";
            case 35: return "Switch Off";
            case 36: return "Magic Portal";
            case 37: return "Taunting";
            case 38: return "Game Won";
            case 39: return "Game Lost";
            case 40: return "Loading Bar";
            case 41: return "Binary Speak";
            case 42: return "Shout Mode";
            case 43: return "Fake Shutoff";
            case 44: return "Notification";
            case 45: return "Dad Joke";
            case 46: return "Rap Mode";
            case 47: return "Helicopter";
            case 48: return "Cyber Knight";
            case 49: return "DJ Mode";
            case 50: return "Grand Closing";
            case 51: return "Michael Jackson";
            case 52: return "Chicken Dance";
            case 53: return "Suirian Dabkah";
            case 54: return "Crazy";
            case 55: return "Say My Name";
            default: return "Cinematic Act";
        }
    }

    private void showBasicControls() {
        System.out.println(BOLD + "\n--- BASIC CONTROLS ---" + RESET);
        System.out.println("1. Flap Wings");
        System.out.println("2. Spin Left (360)");
        System.out.println("3. Spin Right (360)");
        System.out.println("4. Say 'Hello'");
        System.out.println("5. Blink Eyes");
        printFooter();
        System.out.print("\n" + YELLOW + "action> " + RESET);

        String input = scanner.nextLine().trim();
        switch (input) {
            case "1":
                executeCmd("--flap");
                break;
            case "2":
                executeCmd("--spin left --val 100");
                break;
            case "3":
                executeCmd("--spin right --val 100");
                break;
            case "4":
                executeCmd("--say \"Hello there!\"");
                break;
            case "5":
                executeCmd("--blink 3");
                break;
            default:
                System.out.println("Cancelled.");
        }
    }

    private void runManualMode() {
        System.out.println(BOLD + "\n[ MANUAL REPL MODE ]" + RESET);
        System.out.println("Type complete commands like " + CYAN + "--spin left --val 100" + RESET);
        System.out.println("Type " + RED + "back" + RESET + " to return to menu.");
        printFooter();

        while (true) {
            System.out.print("\n" + PURPLE + "manual> " + RESET);
            String line = scanner.nextLine().trim();
            if (line.equalsIgnoreCase("back") || line.equalsIgnoreCase("exit"))
                return;
            if (line.isEmpty())
                continue;

            executeCmd(line);
        }
    }

    private void executeCmd(String line) {
        String[] args = parseArgs(line);
        System.out.println(YELLOW + ">>> RUNNING: " + line + RESET);
        new CommandLine(new Main()).execute(args);
        System.out.println(YELLOW + ">>> DONE" + RESET);
    }

    private String[] parseArgs(String command) {
        List<String> list = new ArrayList<>();
        Matcher m = Pattern.compile("([^\"]\\S*|\".+?\")\\s*").matcher(command);
        while (m.find()) {
            list.add(m.group(1).replace("\"", ""));
        }
        return list.toArray(new String[0]);
    }

    private void printBanner() {
        String[] art = {
            "",
            CYAN + "  ███████╗ ██████╗ █████╗ ██╗   ██╗████████╗██╗   ██╗██╗  ██╗" + RESET,
            CYAN + "  ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║   ██║╚██╗██╔╝" + RESET,
            CYAN + "  ███████╗██║     ███████║ ╚████╔╝    ██║   ██║   ██║ ╚███╔╝ " + RESET,
            CYAN + "  ╚════██║██║     ██╔══██║  ╚██╔╝     ██║   ██║   ██║ ██╔██╗ " + RESET,
            CYAN + "  ███████║╚██████╗██║  ██║   ██║      ██║   ╚██████╔╝██╔╝ ██╗" + RESET,
            CYAN + "  ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═╝" + RESET,
            "",
            YELLOW + "          🐧 The Ultimate Tux Droid Controller 🐧" + RESET,
            "",
            DIM + "  ┌─────────────────────────────────────────────────────────┐" + RESET,
            DIM + "  │" + RESET + "  Version: " + GREEN + "3.0" + RESET + "                                          " + DIM + "│" + RESET,
            DIM + "  │" + RESET + "  Author:  " + CYAN + "Scayar" + RESET + "                                        " + DIM + "│" + RESET,
            DIM + "  │" + RESET + "  GitHub:  " + BLUE + "github.com/Scayar" + RESET + "                             " + DIM + "│" + RESET,
            DIM + "  │" + RESET + "  Email:   " + PURPLE + "Scayar.exe@gmail.com" + RESET + "                         " + DIM + "│" + RESET,
            DIM + "  └─────────────────────────────────────────────────────────┘" + RESET,
            ""
        };

        for (String line : art) {
            System.out.println(line);
        }
    }

    private void clearScreen() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
}

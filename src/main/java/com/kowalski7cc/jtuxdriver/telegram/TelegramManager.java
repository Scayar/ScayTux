package com.kowalski7cc.jtuxdriver.telegram;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

import java.io.*;
import java.nio.file.*;

/**
 * Manages Telegram Bot configuration and lifecycle
 * 
 * @author Scayar
 * @website https://github.com/Scayar
 */
public class TelegramManager {

    private static final String CONFIG_FILE = "telegram_config.json";
    private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();
    
    private TelegramController bot;
    private TelegramBotsApi botsApi;
    private Thread botThread;
    private boolean isRunning = false;

    /**
     * Configuration class for Telegram settings
     */
    public static class TelegramConfig {
        public String botToken = "";
        public String chatId = "";
        public boolean autoStart = false;

        public boolean isValid() {
            return botToken != null && !botToken.isEmpty() 
                && chatId != null && !chatId.isEmpty();
        }
    }

    /**
     * Load configuration from file
     */
    public TelegramConfig loadConfig() {
        try {
            Path configPath = Paths.get(CONFIG_FILE);
            if (Files.exists(configPath)) {
                String json = new String(Files.readAllBytes(configPath));
                return gson.fromJson(json, TelegramConfig.class);
            }
        } catch (Exception e) {
            System.err.println("[Telegram] Error loading config: " + e.getMessage());
        }
        return new TelegramConfig();
    }

    /**
     * Save configuration to file
     */
    public void saveConfig(TelegramConfig config) {
        try {
            String json = gson.toJson(config);
            Files.write(Paths.get(CONFIG_FILE), json.getBytes());
            System.out.println("[Telegram] Configuration saved!");
        } catch (Exception e) {
            System.err.println("[Telegram] Error saving config: " + e.getMessage());
        }
    }

    /**
     * Start the Telegram bot
     */
    public boolean startBot(String token, String chatId) {
        if (isRunning) {
            System.out.println("[Telegram] Bot is already running!");
            return true;
        }

        System.out.println("[Telegram] Starting bot...");

        try {
            botsApi = new TelegramBotsApi(DefaultBotSession.class);
            bot = new TelegramController(token, chatId);
            botsApi.registerBot(bot);
            isRunning = true;
            
            System.out.println("[Telegram] ✅ Bot started successfully!");
            System.out.println("[Telegram] Open Telegram and send /start to your bot!");
            
            return true;
        } catch (Exception e) {
            System.err.println("[Telegram] ❌ Failed to start bot: " + e.getMessage());
            if (e.getMessage().contains("401")) {
                System.err.println("[Telegram] Invalid bot token! Please check your token.");
            }
            isRunning = false;
            return false;
        }
    }

    /**
     * Stop the Telegram bot
     */
    public void stopBot() {
        if (!isRunning) {
            return;
        }

        System.out.println("[Telegram] Stopping bot...");
        
        if (bot != null) {
            bot.shutdown();
            bot = null;
        }
        
        isRunning = false;
        System.out.println("[Telegram] Bot stopped.");
    }

    /**
     * Check if bot is running
     */
    public boolean isRunning() {
        return isRunning;
    }

    /**
     * Validate bot token format
     */
    public static boolean isValidTokenFormat(String token) {
        // Basic validation: token should be like "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        if (token == null || token.isEmpty()) {
            return false;
        }
        return token.matches("\\d+:[A-Za-z0-9_-]+");
    }

    /**
     * Validate chat ID format
     */
    public static boolean isValidChatIdFormat(String chatId) {
        if (chatId == null || chatId.isEmpty()) {
            return false;
        }
        // Chat ID can be positive (user) or negative (group)
        return chatId.matches("-?\\d+");
    }

    /**
     * Get instructions for creating a bot
     */
    public static String getBotCreationInstructions() {
        return "╔═══════════════════════════════════════════════════════════╗\n" +
               "║         📱 HOW TO CREATE A TELEGRAM BOT 📱               ║\n" +
               "╠═══════════════════════════════════════════════════════════╣\n" +
               "║                                                           ║\n" +
               "║  1️⃣  Open Telegram and search for @BotFather              ║\n" +
               "║                                                           ║\n" +
               "║  2️⃣  Send /newbot command                                 ║\n" +
               "║                                                           ║\n" +
               "║  3️⃣  Choose a name for your bot (e.g. \"My Tux Bot\")       ║\n" +
               "║                                                           ║\n" +
               "║  4️⃣  Choose a username ending with 'bot'                  ║\n" +
               "║      (e.g. \"MyScayTux_bot\")                               ║\n" +
               "║                                                           ║\n" +
               "║  5️⃣  Copy the token that BotFather gives you              ║\n" +
               "║      (looks like: 123456789:ABCdefGHI...)                 ║\n" +
               "║                                                           ║\n" +
               "╠═══════════════════════════════════════════════════════════╣\n" +
               "║                                                           ║\n" +
               "║  🔑 TO GET YOUR CHAT ID:                                  ║\n" +
               "║                                                           ║\n" +
               "║  1. Search for @userinfobot on Telegram                   ║\n" +
               "║  2. Send /start to it                                     ║\n" +
               "║  3. It will reply with your Chat ID                       ║\n" +
               "║                                                           ║\n" +
               "╚═══════════════════════════════════════════════════════════╝";
    }
}


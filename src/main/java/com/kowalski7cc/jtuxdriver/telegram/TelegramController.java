package com.kowalski7cc.jtuxdriver.telegram;

import com.kowalski7cc.jtuxdriver.TuxDroid;
import com.kowalski7cc.jtuxdriver.TuxCombos;
import com.kowalski7cc.jtuxdriver.TTS;
import com.kowalski7cc.jtuxdriver.AudioPlayer;
import com.kowalski7cc.jtuxdriver.core.HidTransport;

import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.methods.updatingmessages.EditMessageText;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * ScayTux Telegram Bot Controller
 * Control your Tux Droid remotely via Telegram with Inline Keyboards!
 * 
 * @author Scayar
 * @website https://github.com/Scayar
 */
public class TelegramController extends TelegramLongPollingBot {

    private final String botToken;
    private final String authorizedChatId;
    private TuxDroid tux;
    private TuxCombos combos;
    private final AtomicBoolean isConnected = new AtomicBoolean(false);
    private final AtomicBoolean isRunning = new AtomicBoolean(true);
    private final AtomicBoolean isMusicPlaying = new AtomicBoolean(false);

    public TelegramController(String botToken, String chatId) {
        this.botToken = botToken;
        this.authorizedChatId = chatId;
    }

    @Override
    public String getBotUsername() {
        return "ScayTuxBot";
    }

    @Override
    public String getBotToken() {
        return botToken;
    }

    @Override
    public void onUpdateReceived(Update update) {
        // Handle callback queries (button clicks)
        if (update.hasCallbackQuery()) {
            String chatId = update.getCallbackQuery().getMessage().getChatId().toString();
            String callbackData = update.getCallbackQuery().getData();
            Integer messageId = update.getCallbackQuery().getMessage().getMessageId();
            
            // Security check
            if (!chatId.equals(authorizedChatId)) {
                return;
            }
            
            handleCallback(chatId, callbackData, messageId);
            return;
        }

        // Handle text messages
        if (!update.hasMessage() || !update.getMessage().hasText()) {
            return;
        }

        String chatId = update.getMessage().getChatId().toString();
        String messageText = update.getMessage().getText().trim();

        // Security: Only respond to authorized chat
        if (!chatId.equals(authorizedChatId)) {
            sendMessage(chatId, "⛔ Unauthorized! This bot only responds to the owner.");
            return;
        }

        // Process text command
        processTextCommand(chatId, messageText);
    }

    private void handleCallback(String chatId, String data, Integer messageId) {
        try {
            // Menu navigation
            if (data.equals("menu_main")) {
                editMessageWithMainMenu(chatId, messageId);
                return;
            }
            if (data.equals("menu_controls")) {
                editMessageWithControlsMenu(chatId, messageId);
                return;
            }
            if (data.equals("menu_music")) {
                editMessageWithMusicMenu(chatId, messageId);
                return;
            }
            if (data.equals("menu_combos")) {
                editMessageWithCombosMenu(chatId, messageId);
                return;
            }
            if (data.equals("menu_combos2")) {
                editMessageWithCombosMenu2(chatId, messageId);
                return;
            }
            if (data.equals("menu_combos3")) {
                editMessageWithCombosMenu3(chatId, messageId);
                return;
            }

            // Connection actions
            if (data.equals("action_connect")) {
                connectTux(chatId);
                return;
            }
            if (data.equals("action_disconnect")) {
                disconnectTux(chatId);
                return;
            }
            if (data.equals("action_status")) {
                sendStatus(chatId);
                return;
            }

            // Control actions
            if (data.equals("action_flap")) {
                executeAction(chatId, "🦅 Flapping wings...", () -> tux.flapWings());
                return;
            }
            if (data.equals("action_blink")) {
                executeAction(chatId, "✨ Blinking...", () -> tux.blinkEyes(3));
                return;
            }
            if (data.equals("action_eyes_open")) {
                executeAction(chatId, "👀 Opening eyes...", () -> tux.setEyes(true));
                return;
            }
            if (data.equals("action_eyes_close")) {
                executeAction(chatId, "😴 Closing eyes...", () -> tux.setEyes(false));
                return;
            }
            if (data.equals("action_mouth_open")) {
                executeAction(chatId, "😮 Opening mouth...", () -> tux.setMouth(true));
                return;
            }
            if (data.equals("action_mouth_close")) {
                executeAction(chatId, "😶 Closing mouth...", () -> tux.setMouth(false));
                return;
            }
            if (data.equals("action_spin_left")) {
                executeAction(chatId, "↩️ Spinning left...", () -> tux.spinLeft(50));
                return;
            }
            if (data.equals("action_spin_right")) {
                executeAction(chatId, "↪️ Spinning right...", () -> tux.spinRight(50));
                return;
            }
            if (data.equals("action_dance")) {
                executeAction(chatId, "💃 Dancing!", () -> combos.runCombo(14));
                return;
            }

            // Music actions
            if (data.equals("music_mj")) {
                playMusicWithDance(chatId, "Michael Jackson - Billie Jean 🕺", 51);
                return;
            }
            if (data.equals("music_chicken")) {
                playMusicWithDance(chatId, "Chicken Dance 🐔", 52);
                return;
            }
            if (data.equals("music_dabkah")) {
                playMusicWithDance(chatId, "Suirian Dabkah - Traditional Dance 🎵", 53);
                return;
            }
            if (data.equals("music_crazy")) {
                playMusicWithDance(chatId, "Crazy 🎵", 54);
                return;
            }
            if (data.equals("music_saymyname")) {
                playMusicWithDance(chatId, "Say My Name 🎵", 55);
                return;
            }
            if (data.equals("music_stop")) {
                stopMusic(chatId);
                return;
            }

            // Combo actions
            if (data.startsWith("combo_")) {
                String numStr = data.replace("combo_", "");
                try {
                    int comboId = Integer.parseInt(numStr);
                    String comboName = getComboName(comboId);
                    executeAction(chatId, "🎭 Running: " + comboName + "...", () -> combos.runCombo(comboId));
                } catch (NumberFormatException e) {
                    sendMessage(chatId, "❌ Invalid combo!");
                }
                return;
            }

        } catch (Exception e) {
            sendMessage(chatId, "❌ Error: " + e.getMessage());
        }
    }

    private void processTextCommand(String chatId, String command) {
        String cmd = command.toLowerCase().replace("_", "").replace(" ", "");

        // Start command - show main menu
        if (cmd.equals("/start") || cmd.equals("start")) {
            sendMainMenu(chatId);
            return;
        }

        // Help command
        if (cmd.equals("/help") || cmd.equals("help")) {
            sendHelp(chatId);
            return;
        }

        // Say command (needs text parameter)
        if (command.toLowerCase().startsWith("/say ") || command.toLowerCase().startsWith("say ")) {
            String text = command.substring(command.indexOf(" ") + 1).trim();
            if (!text.isEmpty()) {
                executeAction(chatId, "🗣️ Speaking: \"" + text + "\"", () -> {
                    AtomicBoolean speaking = new AtomicBoolean(true);
                    Thread mouthThread = new Thread(() -> {
                        try {
                            while (speaking.get()) {
                                tux.openMouth();
                                Thread.sleep(100);
                                tux.closeMouth();
                                Thread.sleep(80);
                            }
                        } catch (Exception e) {}
                    });
                    mouthThread.start();
                    TTS.say(text);
                    speaking.set(false);
                    try {
                        mouthThread.join(500);
                        tux.closeMouth();
                    } catch (Exception e) {}
                });
            } else {
                sendMessage(chatId, "❌ Usage: /say Hello World");
            }
            return;
        }

        // Quick commands (all formats accepted)
        if (cmd.equals("/connect") || cmd.equals("connect")) {
            connectTux(chatId);
            return;
        }
        if (cmd.equals("/disconnect") || cmd.equals("disconnect")) {
            disconnectTux(chatId);
            return;
        }
        if (cmd.equals("/status") || cmd.equals("status")) {
            sendStatus(chatId);
            return;
        }
        if (cmd.equals("/flap") || cmd.equals("flap")) {
            executeAction(chatId, "🦅 Flapping wings...", () -> tux.flapWings());
            return;
        }
        if (cmd.equals("/blink") || cmd.equals("blink")) {
            executeAction(chatId, "✨ Blinking...", () -> tux.blinkEyes(3));
            return;
        }
        if (cmd.equals("/dance") || cmd.equals("dance")) {
            executeAction(chatId, "💃 Dancing!", () -> combos.runCombo(14));
            return;
        }

        // Music commands
        if (cmd.equals("/music") || cmd.equals("music")) {
            sendMusicMenu(chatId);
            return;
        }
        if (cmd.equals("/stopmusicкие") || cmd.equals("/stop") || cmd.equals("stop")) {
            stopMusic(chatId);
            return;
        }

        // Combo commands (accept: /combo1, /combo_1, combo1, combo 1)
        if (cmd.startsWith("/combo") || cmd.startsWith("combo")) {
            String numStr = cmd.replace("/combo", "").replace("combo", "").trim();
            try {
                int comboId = Integer.parseInt(numStr);
                if (comboId >= 1 && comboId <= 55) {
                    String comboName = getComboName(comboId);
                    executeAction(chatId, "🎭 Running: " + comboName + "...", () -> combos.runCombo(comboId));
                } else {
                    sendMessage(chatId, "❌ Combo ID must be 1-55");
                }
            } catch (NumberFormatException e) {
                sendMessage(chatId, "❌ Usage: /combo1 to /combo55");
            }
            return;
        }

        // Show main menu for any other input
        sendMessage(chatId, "🤖 Use the buttons below or type /start");
        sendMainMenu(chatId);
    }

    private void executeAction(String chatId, String message, TuxAction action) {
        if (!isConnected.get() || tux == null) {
            sendMessage(chatId, "⚠️ Not connected!\n\nPress 🔌 Connect first.");
            return;
        }

        sendMessage(chatId, message);
        
        new Thread(() -> {
            try {
                action.execute();
                sendMessage(chatId, "✅ Done!");
            } catch (Exception e) {
                sendMessage(chatId, "❌ Failed: " + e.getMessage());
            }
        }).start();
    }

    private void playMusicWithDance(String chatId, String songName, int comboId) {
        if (!isConnected.get() || tux == null) {
            sendMessage(chatId, "⚠️ Not connected!\n\nPress 🔌 Connect first.");
            return;
        }

        if (isMusicPlaying.get()) {
            sendMessage(chatId, "⚠️ Music already playing!\nPress 🛑 Stop first.");
            return;
        }

        sendMessage(chatId, "🎵 Playing: " + songName + "\n\n💃 Tux is dancing!\n\nPress 🛑 Stop to stop.");
        isMusicPlaying.set(true);

        new Thread(() -> {
            try {
                AtomicBoolean running = new AtomicBoolean(true);
                
                // Start the combo (which includes music)
                combos.runCombo(comboId, running);
                
                isMusicPlaying.set(false);
                sendMessage(chatId, "🎵 Music finished!");
            } catch (Exception e) {
                isMusicPlaying.set(false);
                sendMessage(chatId, "❌ Music error: " + e.getMessage());
            }
        }).start();
    }

    private void stopMusic(String chatId) {
        if (!isMusicPlaying.get()) {
            sendMessage(chatId, "ℹ️ No music playing.");
            return;
        }

        AudioPlayer.stop();
        isMusicPlaying.set(false);
        sendMessage(chatId, "🛑 Music stopped!");
    }

    @FunctionalInterface
    interface TuxAction {
        void execute() throws Exception;
    }

    // ==================== MENUS ====================

    private void sendMainMenu(String chatId) {
        String text = "🐧 *ScayTux Controller* 🐧\n\n" +
                     "Control your Tux Droid with the buttons below!\n\n" +
                     "Status: " + (isConnected.get() ? "🟢 Connected" : "🔴 Disconnected") + "\n" +
                     "Music: " + (isMusicPlaying.get() ? "🎵 Playing" : "⏹️ Stopped") + "\n\n" +
                     "_Made with ♥ by Scayar_";

        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(text);
        message.setParseMode("Markdown");
        message.setReplyMarkup(createMainMenuKeyboard());

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private void editMessageWithMainMenu(String chatId, Integer messageId) {
        String text = "🐧 *ScayTux Controller* 🐧\n\n" +
                     "Control your Tux Droid with the buttons below!\n\n" +
                     "Status: " + (isConnected.get() ? "🟢 Connected" : "🔴 Disconnected") + "\n" +
                     "Music: " + (isMusicPlaying.get() ? "🎵 Playing" : "⏹️ Stopped") + "\n\n" +
                     "_Made with ♥ by Scayar_";

        EditMessageText editMessage = new EditMessageText();
        editMessage.setChatId(chatId);
        editMessage.setMessageId(messageId);
        editMessage.setText(text);
        editMessage.setParseMode("Markdown");
        editMessage.setReplyMarkup(createMainMenuKeyboard());

        try {
            execute(editMessage);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private InlineKeyboardMarkup createMainMenuKeyboard() {
        InlineKeyboardMarkup markup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rows = new ArrayList<>();

        // Row 1: Connection
        List<InlineKeyboardButton> row1 = new ArrayList<>();
        row1.add(createButton("🔌 Connect", "action_connect"));
        row1.add(createButton("🔴 Disconnect", "action_disconnect"));
        rows.add(row1);

        // Row 2: Status
        List<InlineKeyboardButton> row2 = new ArrayList<>();
        row2.add(createButton("📊 Status", "action_status"));
        rows.add(row2);

        // Row 3: Sub-menus
        List<InlineKeyboardButton> row3 = new ArrayList<>();
        row3.add(createButton("🎮 Controls", "menu_controls"));
        row3.add(createButton("🎵 Music", "menu_music"));
        rows.add(row3);

        // Row 4: Combos
        List<InlineKeyboardButton> row4 = new ArrayList<>();
        row4.add(createButton("🎭 Combos", "menu_combos"));
        rows.add(row4);

        markup.setKeyboard(rows);
        return markup;
    }

    private void editMessageWithControlsMenu(String chatId, Integer messageId) {
        String text = "🎮 *Controls Menu*\n\n" +
                     "Select an action:";

        EditMessageText editMessage = new EditMessageText();
        editMessage.setChatId(chatId);
        editMessage.setMessageId(messageId);
        editMessage.setText(text);
        editMessage.setParseMode("Markdown");
        editMessage.setReplyMarkup(createControlsKeyboard());

        try {
            execute(editMessage);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private InlineKeyboardMarkup createControlsKeyboard() {
        InlineKeyboardMarkup markup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rows = new ArrayList<>();

        // Row 1
        List<InlineKeyboardButton> row1 = new ArrayList<>();
        row1.add(createButton("🦅 Flap Wings", "action_flap"));
        row1.add(createButton("✨ Blink", "action_blink"));
        rows.add(row1);

        // Row 2
        List<InlineKeyboardButton> row2 = new ArrayList<>();
        row2.add(createButton("👀 Eyes Open", "action_eyes_open"));
        row2.add(createButton("😴 Eyes Close", "action_eyes_close"));
        rows.add(row2);

        // Row 3
        List<InlineKeyboardButton> row3 = new ArrayList<>();
        row3.add(createButton("😮 Mouth Open", "action_mouth_open"));
        row3.add(createButton("😶 Mouth Close", "action_mouth_close"));
        rows.add(row3);

        // Row 4
        List<InlineKeyboardButton> row4 = new ArrayList<>();
        row4.add(createButton("↩️ Spin Left", "action_spin_left"));
        row4.add(createButton("↪️ Spin Right", "action_spin_right"));
        rows.add(row4);

        // Row 5
        List<InlineKeyboardButton> row5 = new ArrayList<>();
        row5.add(createButton("💃 Dance!", "action_dance"));
        rows.add(row5);

        // Back button
        List<InlineKeyboardButton> rowBack = new ArrayList<>();
        rowBack.add(createButton("⬅️ Back to Menu", "menu_main"));
        rows.add(rowBack);

        markup.setKeyboard(rows);
        return markup;
    }

    private void sendMusicMenu(String chatId) {
        String text = "🎵 *Music Menu*\n\n" +
                     "Select a song to play with dance!\n\n" +
                     "Status: " + (isMusicPlaying.get() ? "🎵 Playing" : "⏹️ Stopped");

        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(text);
        message.setParseMode("Markdown");
        message.setReplyMarkup(createMusicKeyboard());

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private void editMessageWithMusicMenu(String chatId, Integer messageId) {
        String text = "🎵 *Music Menu*\n\n" +
                     "Select a song to play with dance!\n\n" +
                     "Status: " + (isMusicPlaying.get() ? "🎵 Playing" : "⏹️ Stopped");

        EditMessageText editMessage = new EditMessageText();
        editMessage.setChatId(chatId);
        editMessage.setMessageId(messageId);
        editMessage.setText(text);
        editMessage.setParseMode("Markdown");
        editMessage.setReplyMarkup(createMusicKeyboard());

        try {
            execute(editMessage);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private InlineKeyboardMarkup createMusicKeyboard() {
        InlineKeyboardMarkup markup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rows = new ArrayList<>();

        // Row 1: Songs
        List<InlineKeyboardButton> row1 = new ArrayList<>();
        row1.add(createButton("🕺 Billie Jean", "music_mj"));
        rows.add(row1);

        // Row 2
        List<InlineKeyboardButton> row2 = new ArrayList<>();
        row2.add(createButton("🐔 Chicken Dance", "music_chicken"));
        rows.add(row2);

        // Row 3: New song
        List<InlineKeyboardButton> row3 = new ArrayList<>();
        row3.add(createButton("🎵 Suirian Dabkah", "music_dabkah"));
        rows.add(row3);

        // Row 4: New songs
        List<InlineKeyboardButton> row4 = new ArrayList<>();
        row4.add(createButton("🔥 Crazy", "music_crazy"));
        row4.add(createButton("👑 Say My Name", "music_saymyname"));
        rows.add(row4);

        // Row 5: Stop
        List<InlineKeyboardButton> row5 = new ArrayList<>();
        row5.add(createButton("🛑 Stop Music", "music_stop"));
        rows.add(row5);

        // Back button
        List<InlineKeyboardButton> rowBack = new ArrayList<>();
        rowBack.add(createButton("⬅️ Back to Menu", "menu_main"));
        rows.add(rowBack);

        markup.setKeyboard(rows);
        return markup;
    }

    private void editMessageWithCombosMenu(String chatId, Integer messageId) {
        String text = "🎭 *Combos (1-10)*\n\n" +
                     "Select a combo to run:";

        EditMessageText editMessage = new EditMessageText();
        editMessage.setChatId(chatId);
        editMessage.setMessageId(messageId);
        editMessage.setText(text);
        editMessage.setParseMode("Markdown");
        editMessage.setReplyMarkup(createCombosKeyboard1());

        try {
            execute(editMessage);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private InlineKeyboardMarkup createCombosKeyboard1() {
        InlineKeyboardMarkup markup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rows = new ArrayList<>();

        // Combos 1-10 (2 per row)
        for (int i = 1; i <= 10; i += 2) {
            List<InlineKeyboardButton> row = new ArrayList<>();
            row.add(createButton(i + ". " + getComboName(i), "combo_" + i));
            if (i + 1 <= 10) {
                row.add(createButton((i+1) + ". " + getComboName(i+1), "combo_" + (i+1)));
            }
            rows.add(row);
        }

        // Navigation
        List<InlineKeyboardButton> rowNav = new ArrayList<>();
        rowNav.add(createButton("➡️ More (11-30)", "menu_combos2"));
        rows.add(rowNav);

        // Back button
        List<InlineKeyboardButton> rowBack = new ArrayList<>();
        rowBack.add(createButton("⬅️ Back to Menu", "menu_main"));
        rows.add(rowBack);

        markup.setKeyboard(rows);
        return markup;
    }

    private void editMessageWithCombosMenu2(String chatId, Integer messageId) {
        String text = "🎭 *Combos (11-30)*\n\n" +
                     "Select a combo to run:";

        EditMessageText editMessage = new EditMessageText();
        editMessage.setChatId(chatId);
        editMessage.setMessageId(messageId);
        editMessage.setText(text);
        editMessage.setParseMode("Markdown");
        editMessage.setReplyMarkup(createCombosKeyboard2());

        try {
            execute(editMessage);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private InlineKeyboardMarkup createCombosKeyboard2() {
        InlineKeyboardMarkup markup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rows = new ArrayList<>();

        // Combos 11-30 (2 per row)
        for (int i = 11; i <= 30; i += 2) {
            List<InlineKeyboardButton> row = new ArrayList<>();
            row.add(createButton(i + ". " + getShortComboName(i), "combo_" + i));
            if (i + 1 <= 30) {
                row.add(createButton((i+1) + ". " + getShortComboName(i+1), "combo_" + (i+1)));
            }
            rows.add(row);
        }

        // Navigation
        List<InlineKeyboardButton> rowNav = new ArrayList<>();
        rowNav.add(createButton("⬅️ (1-10)", "menu_combos"));
        rowNav.add(createButton("➡️ (31-52)", "menu_combos3"));
        rows.add(rowNav);

        // Back button
        List<InlineKeyboardButton> rowBack = new ArrayList<>();
        rowBack.add(createButton("🏠 Main Menu", "menu_main"));
        rows.add(rowBack);

        markup.setKeyboard(rows);
        return markup;
    }

    private void editMessageWithCombosMenu3(String chatId, Integer messageId) {
        String text = "🎭 *Combos (31-52)*\n\n" +
                     "Select a combo to run:";

        EditMessageText editMessage = new EditMessageText();
        editMessage.setChatId(chatId);
        editMessage.setMessageId(messageId);
        editMessage.setText(text);
        editMessage.setParseMode("Markdown");
        editMessage.setReplyMarkup(createCombosKeyboard3());

        try {
            execute(editMessage);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private InlineKeyboardMarkup createCombosKeyboard3() {
        InlineKeyboardMarkup markup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rows = new ArrayList<>();

        // Combos 31-50 (2 per row) - Skip 51 and 52 (music combos)
        for (int i = 31; i <= 50; i += 2) {
            List<InlineKeyboardButton> row = new ArrayList<>();
            row.add(createButton(i + ". " + getShortComboName(i), "combo_" + i));
            if (i + 1 <= 50) {
                row.add(createButton((i+1) + ". " + getShortComboName(i+1), "combo_" + (i+1)));
            }
            rows.add(row);
        }

        // Navigation
        List<InlineKeyboardButton> rowNav = new ArrayList<>();
        rowNav.add(createButton("⬅️ (11-30)", "menu_combos2"));
        rows.add(rowNav);

        // Back button
        List<InlineKeyboardButton> rowBack = new ArrayList<>();
        rowBack.add(createButton("🏠 Main Menu", "menu_main"));
        rows.add(rowBack);

        markup.setKeyboard(rows);
        return markup;
    }

    private InlineKeyboardButton createButton(String text, String callbackData) {
        InlineKeyboardButton button = new InlineKeyboardButton();
        button.setText(text);
        button.setCallbackData(callbackData);
        return button;
    }

    // ==================== ACTIONS ====================

    private void connectTux(String chatId) {
        if (isConnected.get()) {
            sendMessage(chatId, "✅ Already connected!");
            return;
        }

        sendMessage(chatId, "🔄 Connecting to Tux Droid...");

        new Thread(() -> {
            try {
                tux = new TuxDroid(new HidTransport());
                tux.open();
                combos = new TuxCombos(tux);
                isConnected.set(true);
                sendMessage(chatId, "✅ Connected to Tux Droid! 🐧\n\nYou can now control it!");
                sendMainMenu(chatId);
            } catch (Exception e) {
                isConnected.set(false);
                sendMessage(chatId, "❌ Failed to connect!\n\n" +
                    "Make sure:\n" +
                    "• Tux Droid dongle is plugged in\n" +
                    "• USB permissions are set up\n\n" +
                    "Error: " + e.getMessage());
            }
        }).start();
    }

    private void disconnectTux(String chatId) {
        if (!isConnected.get()) {
            sendMessage(chatId, "ℹ️ Not connected.");
            return;
        }

        // Stop music if playing
        if (isMusicPlaying.get()) {
            AudioPlayer.stop();
            isMusicPlaying.set(false);
        }

        try {
            if (tux != null) {
                tux.close();
                tux = null;
                combos = null;
            }
            isConnected.set(false);
            sendMessage(chatId, "🔴 Disconnected from Tux Droid.");
        } catch (Exception e) {
            sendMessage(chatId, "⚠️ Error: " + e.getMessage());
        }
    }

    private void sendStatus(String chatId) {
        String status = "📊 *Status*\n\n" +
            "Connection: " + (isConnected.get() ? "✅ Connected" : "🔴 Disconnected") + "\n" +
            "Music: " + (isMusicPlaying.get() ? "🎵 Playing" : "⏹️ Stopped") + "\n\n" +
            (isConnected.get() ? "🟢 Ready for commands!" : "Press 🔌 Connect to connect.");

        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(status);
        message.setParseMode("Markdown");

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private void sendHelp(String chatId) {
        String help = 
            "📖 *ScayTux Bot Help*\n\n" +
            "Just use the *buttons* in the menu!\n" +
            "Type /start to see the menu.\n\n" +
            "Quick commands:\n" +
            "`/connect` - Connect to Tux\n" +
            "`/flap` - Flap wings\n" +
            "`/dance` - Dance!\n" +
            "`/combo1` to `/combo50` - Run combo\n" +
            "`/say Hello` - Make Tux speak\n" +
            "`/stop` - Stop music\n\n" +
            "_Made with ♥ by Scayar_";

        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(help);
        message.setParseMode("Markdown");

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private void sendMessage(String chatId, String text) {
        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(text);

        try {
            execute(message);
        } catch (TelegramApiException e) {
            System.err.println("[Telegram] Failed to send message: " + e.getMessage());
        }
    }

    // ==================== COMBO NAMES ====================

    private String getComboName(int id) {
        switch (id) {
            case 1: return "Royal Entrance";
            case 2: return "Bird Flex";
            case 3: return "Brain Loading";
            case 4: return "Sleep Mode";
            case 5: return "Hacker Alert";
            case 6: return "Police Mode";
            case 7: return "Shy Bird";
            case 8: return "Laugh Mode";
            case 9: return "Kiss 😘";
            case 10: return "Bird Crying";
            case 11: return "Death Restart";
            case 12: return "Power Up";
            case 13: return "Wake from Dead";
            case 14: return "Celebration";
            case 15: return "Virus Mode";
            case 16: return "TikTok Shake";
            case 17: return "Beatbox";
            case 18: return "Matrix Enter";
            case 19: return "Soldier Salute";
            case 20: return "Confused";
            case 21: return "Wait What?";
            case 22: return "Suspicious";
            case 23: return "Sir Yes Sir";
            case 24: return "Cyber Scan";
            case 25: return "Great Idea";
            case 26: return "No No No";
            case 27: return "Yesss!";
            case 28: return "Broken Robot";
            case 29: return "Romantic";
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
            case 50: return "Grand Close";
            case 51: return "Michael Jackson";
            case 52: return "Chicken Dance";
            case 53: return "Suirian Dabkah";
            case 54: return "Crazy";
            case 55: return "Say My Name";
            default: return "Combo " + id;
        }
    }

    private String getShortComboName(int id) {
        String name = getComboName(id);
        // Shorten names for buttons (max ~12 chars)
        if (name.length() > 12) {
            return name.substring(0, 10) + "..";
        }
        return name;
    }

    public void shutdown() {
        isRunning.set(false);
        if (isMusicPlaying.get()) {
            AudioPlayer.stop();
        }
        if (tux != null) {
            try {
                tux.close();
            } catch (Exception e) {}
        }
    }

    public boolean isRunning() {
        return isRunning.get();
    }
}

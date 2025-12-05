"""
TUX Droid AI Control - Telegram Keyboards
=========================================

Button layouts and keyboard builders for the Telegram bot.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


# ==========================================
# Callback Data Constants
# ==========================================

class CallbackData:
    """Callback data constants for button actions."""
    
    # Menu navigation
    MENU_MAIN = "menu:main"
    MENU_EYES = "menu:eyes"
    MENU_MOUTH = "menu:mouth"
    MENU_WINGS = "menu:wings"
    MENU_SPIN = "menu:spin"
    MENU_LEDS = "menu:leds"
    MENU_SOUND = "menu:sound"
    MENU_SLEEP = "menu:sleep"
    MENU_STATUS = "menu:status"
    
    # Eye actions
    EYES_BLINK_1 = "eyes:blink:1"
    EYES_BLINK_3 = "eyes:blink:3"
    EYES_BLINK_5 = "eyes:blink:5"
    EYES_OPEN = "eyes:open"
    EYES_CLOSE = "eyes:close"
    
    # Mouth actions
    MOUTH_MOVE_1 = "mouth:move:1"
    MOUTH_MOVE_3 = "mouth:move:3"
    MOUTH_MOVE_5 = "mouth:move:5"
    MOUTH_OPEN = "mouth:open"
    MOUTH_CLOSE = "mouth:close"
    
    # Wing actions
    WINGS_WAVE_1 = "wings:wave:1"
    WINGS_WAVE_3 = "wings:wave:3"
    WINGS_WAVE_5 = "wings:wave:5"
    WINGS_RAISE = "wings:raise"
    WINGS_LOWER = "wings:lower"
    
    # Spin actions
    SPIN_LEFT_45 = "spin:left:2"
    SPIN_LEFT_90 = "spin:left:4"
    SPIN_LEFT_180 = "spin:left:8"
    SPIN_RIGHT_45 = "spin:right:2"
    SPIN_RIGHT_90 = "spin:right:4"
    SPIN_RIGHT_180 = "spin:right:8"
    
    # LED actions
    LEDS_ON_BOTH = "leds:on:both"
    LEDS_ON_LEFT = "leds:on:left"
    LEDS_ON_RIGHT = "leds:on:right"
    LEDS_OFF = "leds:off"
    LEDS_TOGGLE = "leds:toggle"
    LEDS_PULSE = "leds:pulse"
    
    # Sound actions
    SOUND_PLAY_0 = "sound:play:0"
    SOUND_PLAY_1 = "sound:play:1"
    SOUND_PLAY_2 = "sound:play:2"
    SOUND_MUTE = "sound:mute"
    SOUND_UNMUTE = "sound:unmute"
    
    # Sleep actions
    SLEEP_NORMAL = "sleep:normal"
    SLEEP_QUICK = "sleep:quick"
    SLEEP_DEEP = "sleep:deep"
    WAKE_UP = "wake:up"


# ==========================================
# Main Menu Keyboard
# ==========================================

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Get the main menu keyboard.
    
    Returns:
        InlineKeyboardMarkup: Main menu with action categories
    """
    keyboard = [
        [
            InlineKeyboardButton("👀 Eyes", callback_data=CallbackData.MENU_EYES),
            InlineKeyboardButton("👄 Mouth", callback_data=CallbackData.MENU_MOUTH),
        ],
        [
            InlineKeyboardButton("🐧 Wings", callback_data=CallbackData.MENU_WINGS),
            InlineKeyboardButton("🔄 Spin", callback_data=CallbackData.MENU_SPIN),
        ],
        [
            InlineKeyboardButton("💡 LEDs", callback_data=CallbackData.MENU_LEDS),
            InlineKeyboardButton("🔊 Sound", callback_data=CallbackData.MENU_SOUND),
        ],
        [
            InlineKeyboardButton("😴 Sleep/Wake", callback_data=CallbackData.MENU_SLEEP),
            InlineKeyboardButton("📊 Status", callback_data=CallbackData.MENU_STATUS),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Eyes Menu Keyboard
# ==========================================

def get_eyes_keyboard() -> InlineKeyboardMarkup:
    """Get the eyes control keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("👁️ Open", callback_data=CallbackData.EYES_OPEN),
            InlineKeyboardButton("😌 Close", callback_data=CallbackData.EYES_CLOSE),
        ],
        [
            InlineKeyboardButton("Blink x1", callback_data=CallbackData.EYES_BLINK_1),
            InlineKeyboardButton("Blink x3", callback_data=CallbackData.EYES_BLINK_3),
            InlineKeyboardButton("Blink x5", callback_data=CallbackData.EYES_BLINK_5),
        ],
        [
            InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Mouth Menu Keyboard
# ==========================================

def get_mouth_keyboard() -> InlineKeyboardMarkup:
    """Get the mouth control keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("😮 Open", callback_data=CallbackData.MOUTH_OPEN),
            InlineKeyboardButton("😶 Close", callback_data=CallbackData.MOUTH_CLOSE),
        ],
        [
            InlineKeyboardButton("Move x1", callback_data=CallbackData.MOUTH_MOVE_1),
            InlineKeyboardButton("Move x3", callback_data=CallbackData.MOUTH_MOVE_3),
            InlineKeyboardButton("Move x5", callback_data=CallbackData.MOUTH_MOVE_5),
        ],
        [
            InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Wings Menu Keyboard
# ==========================================

def get_wings_keyboard() -> InlineKeyboardMarkup:
    """Get the wings control keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🙌 Raise", callback_data=CallbackData.WINGS_RAISE),
            InlineKeyboardButton("👇 Lower", callback_data=CallbackData.WINGS_LOWER),
        ],
        [
            InlineKeyboardButton("Wave x1", callback_data=CallbackData.WINGS_WAVE_1),
            InlineKeyboardButton("Wave x3", callback_data=CallbackData.WINGS_WAVE_3),
            InlineKeyboardButton("Wave x5", callback_data=CallbackData.WINGS_WAVE_5),
        ],
        [
            InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Spin Menu Keyboard
# ==========================================

def get_spin_keyboard() -> InlineKeyboardMarkup:
    """Get the spin control keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("↩️ Left 45°", callback_data=CallbackData.SPIN_LEFT_45),
            InlineKeyboardButton("↪️ Right 45°", callback_data=CallbackData.SPIN_RIGHT_45),
        ],
        [
            InlineKeyboardButton("↩️ Left 90°", callback_data=CallbackData.SPIN_LEFT_90),
            InlineKeyboardButton("↪️ Right 90°", callback_data=CallbackData.SPIN_RIGHT_90),
        ],
        [
            InlineKeyboardButton("↩️ Left 180°", callback_data=CallbackData.SPIN_LEFT_180),
            InlineKeyboardButton("↪️ Right 180°", callback_data=CallbackData.SPIN_RIGHT_180),
        ],
        [
            InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# LEDs Menu Keyboard
# ==========================================

def get_leds_keyboard() -> InlineKeyboardMarkup:
    """Get the LED control keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("💡 Both ON", callback_data=CallbackData.LEDS_ON_BOTH),
            InlineKeyboardButton("🔌 OFF", callback_data=CallbackData.LEDS_OFF),
        ],
        [
            InlineKeyboardButton("👁️ Left ON", callback_data=CallbackData.LEDS_ON_LEFT),
            InlineKeyboardButton("👁️ Right ON", callback_data=CallbackData.LEDS_ON_RIGHT),
        ],
        [
            InlineKeyboardButton("✨ Toggle", callback_data=CallbackData.LEDS_TOGGLE),
            InlineKeyboardButton("🌟 Pulse", callback_data=CallbackData.LEDS_PULSE),
        ],
        [
            InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Sound Menu Keyboard
# ==========================================

def get_sound_keyboard() -> InlineKeyboardMarkup:
    """Get the sound control keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🔊 Sound 1", callback_data=CallbackData.SOUND_PLAY_0),
            InlineKeyboardButton("🔊 Sound 2", callback_data=CallbackData.SOUND_PLAY_1),
            InlineKeyboardButton("🔊 Sound 3", callback_data=CallbackData.SOUND_PLAY_2),
        ],
        [
            InlineKeyboardButton("🔇 Mute", callback_data=CallbackData.SOUND_MUTE),
            InlineKeyboardButton("🔈 Unmute", callback_data=CallbackData.SOUND_UNMUTE),
        ],
        [
            InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Sleep Menu Keyboard
# ==========================================

def get_sleep_keyboard() -> InlineKeyboardMarkup:
    """Get the sleep control keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("😴 Normal Sleep", callback_data=CallbackData.SLEEP_NORMAL),
        ],
        [
            InlineKeyboardButton("💤 Quick Sleep", callback_data=CallbackData.SLEEP_QUICK),
            InlineKeyboardButton("🌙 Deep Sleep", callback_data=CallbackData.SLEEP_DEEP),
        ],
        [
            InlineKeyboardButton("⏰ Wake Up!", callback_data=CallbackData.WAKE_UP),
        ],
        [
            InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Back Button Only
# ==========================================

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Get a keyboard with only the back button."""
    keyboard = [
        [InlineKeyboardButton("« Back to Menu", callback_data=CallbackData.MENU_MAIN)],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==========================================
# Quick Action Reply Keyboard
# ==========================================

def get_quick_actions_keyboard() -> ReplyKeyboardMarkup:
    """
    Get a reply keyboard for quick actions.
    
    This appears as persistent buttons at the bottom of the chat.
    """
    keyboard = [
        ["👀 Blink", "🐧 Wave", "💡 Toggle"],
        ["↩️ Spin Left", "↪️ Spin Right"],
        ["📋 Menu", "📊 Status"],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


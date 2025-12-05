"""
TUX Droid AI Control - Telegram Bot Handlers
============================================

Command and callback handlers for the Telegram bot.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from .keyboards import (
    CallbackData,
    get_main_menu_keyboard,
    get_eyes_keyboard,
    get_mouth_keyboard,
    get_wings_keyboard,
    get_spin_keyboard,
    get_leds_keyboard,
    get_sound_keyboard,
    get_sleep_keyboard,
    get_back_keyboard,
    get_quick_actions_keyboard,
)
from .api_client import TuxAPIClient

logger = logging.getLogger(__name__)

# Global API client (initialized in main.py)
api_client: TuxAPIClient = None


def set_api_client(client: TuxAPIClient):
    """Set the global API client."""
    global api_client
    api_client = client


# ==========================================
# Helper Functions
# ==========================================

def escape_markdown(text: str) -> str:
    """Escape special Markdown characters for Telegram."""
    if text is None:
        return "?"
    if not isinstance(text, str):
        text = str(text)
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text


def format_result(result: dict) -> str:
    """Format API result for display."""
    if result.get("success"):
        return f"✅ {result.get('message', 'Action completed!')}"
    else:
        error = result.get("error", "unknown")
        message = result.get("message", "Something went wrong")
        return f"❌ Error ({error}): {message}"


async def send_action_result(
    update: Update,
    result: dict,
    keyboard=None
):
    """Send action result as a message or edit."""
    text = format_result(result)
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=keyboard or get_back_keyboard()
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=keyboard or get_back_keyboard()
        )


# ==========================================
# Command Handlers
# ==========================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    welcome_text = f"""
🐧 *Welcome to TUX Droid AI Control!*

Hello {user.first_name}! I'm your TUX Droid controller.

Use the buttons below to control your TUX:
• 👀 *Eyes* - Blink, open, close
• 👄 *Mouth* - Move, open, close
• 🐧 *Wings* - Wave, raise, lower
• 🔄 *Spin* - Rotate left/right
• 💡 *LEDs* - Control eye lights
• 🔊 *Sound* - Play sounds
• 😴 *Sleep* - Sleep and wake modes

*Quick Commands:*
/menu - Show main menu
/status - Check TUX status
/help - Show help message

Choose an action from the menu below:
"""
    
    await update.message.reply_text(
        text=welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )
    
    # Also send quick actions keyboard
    await update.message.reply_text(
        "Quick actions:",
        reply_markup=get_quick_actions_keyboard()
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu command."""
    await update.message.reply_text(
        "🐧 *TUX Droid Control Menu*\n\nChoose an action:",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command."""
    if api_client is None:
        await update.message.reply_text("❌ API client not configured")
        return
    
    result = await api_client.get_status()
    
    if "connected" in result:
        driver_type = escape_markdown(result.get('driver_type', 'unknown'))
        status_text = f"""
📊 *TUX Droid Status*

• Connected: {'✅ Yes' if result.get('connected') else '❌ No'}
• Driver: {driver_type}
• Mode: {'🧪 Mock' if result.get('driver_type') == 'mock' else '🔧 Hardware'}
"""
        if result.get("simulated_state"):
            state = result["simulated_state"]
            eyes = escape_markdown(state.get('eyes', 'unknown'))
            mouth = escape_markdown(state.get('mouth', 'unknown'))
            wings = escape_markdown(state.get('wings', 'unknown'))
            leds_left = escape_markdown(state.get('leds_left', '?'))
            leds_right = escape_markdown(state.get('leds_right', '?'))
            status_text += f"""
*Simulated State:*
• Eyes: {eyes}
• Mouth: {mouth}
• Wings: {wings}
• LEDs: L={leds_left} R={leds_right}
"""
    else:
        status_text = format_result(result)
    
    await update.message.reply_text(
        status_text,
        parse_mode="Markdown",
        reply_markup=get_back_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
🐧 *TUX Droid AI Control - Help*

*Commands:*
/start - Start the bot
/menu - Show main menu
/status - Check TUX status
/help - Show this help

*Quick Actions (text):*
• "👀 Blink" - Blink eyes once
• "🐧 Wave" - Wave wings once
• "💡 Toggle" - Toggle LEDs
• "↩️ Spin Left" - Spin left 90°
• "↪️ Spin Right" - Spin right 90°

*Tips:*
• Use the inline buttons for precise control
• Check status to see TUX's current state
• In DEV mode, actions are simulated

*Need Help?*
Contact the administrator for support.
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )


# ==========================================
# Text Message Handler (Quick Actions)
# ==========================================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages for quick actions."""
    if api_client is None:
        return
    
    text = update.message.text.strip()
    result = None
    
    # Quick action mapping
    if text in ["👀 Blink", "blink"]:
        result = await api_client.blink_eyes(count=1)
    elif text in ["🐧 Wave", "wave"]:
        result = await api_client.wave_wings(count=1)
    elif text in ["💡 Toggle", "toggle"]:
        result = await api_client.led_toggle(count=3)
    elif text in ["↩️ Spin Left", "spin left"]:
        result = await api_client.spin_left(angle=4)
    elif text in ["↪️ Spin Right", "spin right"]:
        result = await api_client.spin_right(angle=4)
    elif text in ["📋 Menu", "menu"]:
        await menu_command(update, context)
        return
    elif text in ["📊 Status", "status"]:
        await status_command(update, context)
        return
    
    if result:
        await update.message.reply_text(format_result(result))


# ==========================================
# Callback Query Handler
# ==========================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    data = query.data
    
    logger.info(f"Callback: {data}")
    
    if api_client is None:
        await query.answer("API not configured!")
        return
    
    # Menu navigation
    if data == CallbackData.MENU_MAIN:
        await query.answer()
        await query.edit_message_text(
            "🐧 *TUX Droid Control Menu*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_EYES:
        await query.answer()
        await query.edit_message_text(
            "👀 *Eye Controls*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_eyes_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_MOUTH:
        await query.answer()
        await query.edit_message_text(
            "👄 *Mouth Controls*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_mouth_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_WINGS:
        await query.answer()
        await query.edit_message_text(
            "🐧 *Wing Controls*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_wings_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_SPIN:
        await query.answer()
        await query.edit_message_text(
            "🔄 *Spin Controls*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_spin_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_LEDS:
        await query.answer()
        await query.edit_message_text(
            "💡 *LED Controls*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_leds_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_SOUND:
        await query.answer()
        await query.edit_message_text(
            "🔊 *Sound Controls*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_sound_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_SLEEP:
        await query.answer()
        await query.edit_message_text(
            "😴 *Sleep Controls*\n\nChoose an action:",
            parse_mode="Markdown",
            reply_markup=get_sleep_keyboard()
        )
        return
    
    elif data == CallbackData.MENU_STATUS:
        result = await api_client.get_status()
        status_text = "📊 *TUX Status*\n\n"
        if "connected" in result:
            status_text += f"Connected: {'✅' if result.get('connected') else '❌'}\n"
            status_text += f"Driver: {escape_markdown(result.get('driver_type', '?'))}\n"
            if result.get("simulated_state"):
                state = result["simulated_state"]
                eyes = escape_markdown(state.get('eyes', '?'))
                mouth = escape_markdown(state.get('mouth', '?'))
                status_text += f"\n*State:* Eyes={eyes}, Mouth={mouth}"
        else:
            status_text += format_result(result)
        
        await query.answer()
        await query.edit_message_text(
            status_text,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        return
    
    # Action handlers
    result = None
    
    # Eyes
    if data == CallbackData.EYES_BLINK_1:
        result = await api_client.blink_eyes(count=1)
    elif data == CallbackData.EYES_BLINK_3:
        result = await api_client.blink_eyes(count=3)
    elif data == CallbackData.EYES_BLINK_5:
        result = await api_client.blink_eyes(count=5)
    elif data == CallbackData.EYES_OPEN:
        result = await api_client.open_eyes()
    elif data == CallbackData.EYES_CLOSE:
        result = await api_client.close_eyes()
    
    # Mouth
    elif data == CallbackData.MOUTH_MOVE_1:
        result = await api_client.move_mouth(count=1)
    elif data == CallbackData.MOUTH_MOVE_3:
        result = await api_client.move_mouth(count=3)
    elif data == CallbackData.MOUTH_MOVE_5:
        result = await api_client.move_mouth(count=5)
    elif data == CallbackData.MOUTH_OPEN:
        result = await api_client.open_mouth()
    elif data == CallbackData.MOUTH_CLOSE:
        result = await api_client.close_mouth()
    
    # Wings
    elif data == CallbackData.WINGS_WAVE_1:
        result = await api_client.wave_wings(count=1)
    elif data == CallbackData.WINGS_WAVE_3:
        result = await api_client.wave_wings(count=3)
    elif data == CallbackData.WINGS_WAVE_5:
        result = await api_client.wave_wings(count=5)
    elif data == CallbackData.WINGS_RAISE:
        result = await api_client.raise_wings()
    elif data == CallbackData.WINGS_LOWER:
        result = await api_client.lower_wings()
    
    # Spin
    elif data == CallbackData.SPIN_LEFT_45:
        result = await api_client.spin_left(angle=2)
    elif data == CallbackData.SPIN_LEFT_90:
        result = await api_client.spin_left(angle=4)
    elif data == CallbackData.SPIN_LEFT_180:
        result = await api_client.spin_left(angle=8)
    elif data == CallbackData.SPIN_RIGHT_45:
        result = await api_client.spin_right(angle=2)
    elif data == CallbackData.SPIN_RIGHT_90:
        result = await api_client.spin_right(angle=4)
    elif data == CallbackData.SPIN_RIGHT_180:
        result = await api_client.spin_right(angle=8)
    
    # LEDs
    elif data == CallbackData.LEDS_ON_BOTH:
        result = await api_client.led_on(target="both")
    elif data == CallbackData.LEDS_ON_LEFT:
        result = await api_client.led_on(target="left")
    elif data == CallbackData.LEDS_ON_RIGHT:
        result = await api_client.led_on(target="right")
    elif data == CallbackData.LEDS_OFF:
        result = await api_client.led_off()
    elif data == CallbackData.LEDS_TOGGLE:
        result = await api_client.led_toggle(count=5)
    elif data == CallbackData.LEDS_PULSE:
        result = await api_client.led_pulse(count=5)
    
    # Sound
    elif data == CallbackData.SOUND_PLAY_0:
        result = await api_client.play_sound(sound_number=0)
    elif data == CallbackData.SOUND_PLAY_1:
        result = await api_client.play_sound(sound_number=1)
    elif data == CallbackData.SOUND_PLAY_2:
        result = await api_client.play_sound(sound_number=2)
    elif data == CallbackData.SOUND_MUTE:
        result = await api_client.mute()
    elif data == CallbackData.SOUND_UNMUTE:
        result = await api_client.unmute()
    
    # Sleep
    elif data == CallbackData.SLEEP_NORMAL:
        result = await api_client.sleep(mode="normal")
    elif data == CallbackData.SLEEP_QUICK:
        result = await api_client.sleep(mode="quick")
    elif data == CallbackData.SLEEP_DEEP:
        result = await api_client.sleep(mode="deep")
    elif data == CallbackData.WAKE_UP:
        result = await api_client.wake_up()
    
    # Send result
    if result:
        await send_action_result(update, result)
    else:
        await query.answer("Unknown action")


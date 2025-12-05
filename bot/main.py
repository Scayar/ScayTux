"""
TUX Droid AI Control - Telegram Bot
===================================

Main entry point for the Telegram bot.

Usage:
    python -m bot.main
    
    # Or directly:
    python bot/main.py
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config.settings import settings
from bot.handlers import (
    start_command,
    menu_command,
    status_command,
    help_command,
    text_handler,
    callback_handler,
    set_api_client,
)
from bot.api_client import TuxAPIClient

# ==========================================
# Logging Configuration
# ==========================================

def setup_logging():
    """Configure logging for the bot."""
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

setup_logging()
logger = logging.getLogger(__name__)


# ==========================================
# Bot Setup
# ==========================================

def create_bot() -> Application:
    """
    Create and configure the Telegram bot application.
    
    Returns:
        Application: Configured bot application
    """
    # Validate token
    if not settings.telegram_bot_token or settings.telegram_bot_token == "your_telegram_bot_token_here":
        logger.error("=" * 50)
        logger.error("TELEGRAM_BOT_TOKEN not configured!")
        logger.error("Please set your bot token in .env file")
        logger.error("Get a token from @BotFather on Telegram")
        logger.error("=" * 50)
        sys.exit(1)
    
    # Initialize API client
    api_client = TuxAPIClient(settings.backend_api_url)
    set_api_client(api_client)
    
    logger.info(f"API client configured: {settings.backend_api_url}")
    
    # Create application
    application = Application.builder().token(settings.telegram_bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # Add text message handler for quick actions
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_handler
    ))
    
    logger.info("Bot handlers configured")
    
    return application


# ==========================================
# Main Entry Point
# ==========================================

def main():
    """Start the Telegram bot."""
    logger.info("=" * 50)
    logger.info("🐧 TUX Droid AI Control - Telegram Bot")
    logger.info("=" * 50)
    logger.info(f"Backend API: {settings.backend_api_url}")
    logger.info(f"Log Level: {settings.log_level}")
    logger.info("=" * 50)
    
    # Create and run bot
    application = create_bot()
    
    logger.info("🚀 Starting bot... (Press Ctrl+C to stop)")
    
    # Run the bot until Ctrl+C
    application.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()


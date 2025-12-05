"""
TUX Droid AI Control - Centralized Configuration Settings
=========================================================

This module provides a centralized configuration system using Pydantic Settings.
It loads configuration from environment variables and .env files.
"""

from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Telegram Bot Settings
    telegram_bot_token: str = ""
    
    # Backend API Settings
    backend_api_url: str = "http://localhost:8000"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # TUX Droid Settings
    tux_mode: Literal["DEV", "PROD"] = "DEV"
    tux_device_path: str = "/dev/ttyUSB0"
    
    # Logging Settings
    log_level: str = "INFO"
    
    @property
    def is_dev_mode(self) -> bool:
        """Check if running in development mode (using stub driver)."""
        return self.tux_mode.upper() == "DEV"
    
    @property
    def is_prod_mode(self) -> bool:
        """Check if running in production mode (using real hardware)."""
        return self.tux_mode.upper() == "PROD"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()


# Convenience function for quick access
settings = get_settings()


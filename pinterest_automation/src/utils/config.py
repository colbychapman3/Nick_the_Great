"""
Configuration loader for Pinterest automation.
Loads settings from environment variables and config files.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class Config:
    """Configuration manager for Pinterest automation."""
    
    def __init__(self, env_file: str = ".env"):
        """
        Initialize configuration from environment variables.
        
        Args:
            env_file: Path to .env file (relative to config directory)
        """
        # Construct path to .env file
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")
        env_path = os.path.join(config_dir, env_file)
        
        # Load environment variables from .env file
        if os.path.exists(env_path):
            load_dotenv(env_path)
            logger.info(f"Loaded configuration from {env_path}")
        else:
            logger.warning(f"Environment file {env_path} not found. Using system environment variables.")
        
        # Pinterest API credentials
        self.app_id = os.getenv("PINTEREST_APP_ID")
        self.app_secret = os.getenv("PINTEREST_APP_SECRET")
        self.access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
        self.refresh_token = os.getenv("PINTEREST_REFRESH_TOKEN")
        
        # API settings
        self.api_url = os.getenv("PINTEREST_API_URL", "https://api.pinterest.com/v5")
        
        # Pinterest board IDs
        board_ids = os.getenv("PINTEREST_BOARD_IDS", "")
        self.board_ids = [bid.strip() for bid in board_ids.split(",")] if board_ids else []
        
        # Scheduling settings
        self.pin_creation_schedule = os.getenv("PIN_CREATION_SCHEDULE", "0 9 * * *")
        self.analytics_collection_schedule = os.getenv("ANALYTICS_COLLECTION_SCHEDULE", "0 5 * * *")
        
        # Limits
        self.max_pins_per_day = int(os.getenv("MAX_PINS_PER_DAY", "5"))
        self.max_pins_per_board_per_day = int(os.getenv("MAX_PINS_PER_BOARD_PER_DAY", "2"))
        
        # Paths
        data_dir = os.path.join(os.path.dirname(config_dir), "data")
        self.image_folder = os.path.abspath(os.path.join(data_dir, "images"))
        self.analytics_output = os.path.abspath(os.path.join(data_dir, "analytics"))
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Set up logging after loading config
        from .logging_setup import setup_logging
        setup_logging(self.log_level)
    
    def validate(self) -> bool:
        """
        Check if all required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        required_fields = ["app_id", "app_secret"]
        missing_fields = [field for field in required_fields if not getattr(self, field)]
        
        if missing_fields:
            logger.error(f"Missing required configuration: {', '.join(missing_fields)}")
            return False
            
        if not self.board_ids:
            logger.warning("No Pinterest board IDs configured")
            
        return True
    
    def get_auth_config(self) -> Dict[str, str]:
        """
        Get authentication configuration.
        
        Returns:
            Dict containing authentication parameters
        """
        return {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        }
    
    def __str__(self) -> str:
        """String representation of configuration (with sensitive data masked)."""
        return (
            f"Pinterest API Configuration:\n"
            f"  API URL: {self.api_url}\n"
            f"  App ID: {'*' * 8}{self.app_id[-4:] if self.app_id else 'Not set'}\n"
            f"  Boards: {', '.join(self.board_ids) if self.board_ids else 'None configured'}\n"
            f"  Pin Creation Schedule: {self.pin_creation_schedule}\n"
            f"  Analytics Collection Schedule: {self.analytics_collection_schedule}\n"
            f"  Max Pins Per Day: {self.max_pins_per_day}\n"
        )


# Singleton instance
_config_instance = None

def get_config(env_file: str = ".env") -> Config:
    """
    Get configuration singleton instance.
    
    Args:
        env_file: Path to .env file (relative to config directory)
        
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(env_file)
    return _config_instance

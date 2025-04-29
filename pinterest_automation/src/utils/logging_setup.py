"""
Logging configuration for Pinterest automation.
Sets up logging with appropriate handlers and formatters.
"""

import os
import logging
import sys
from datetime import datetime
import colorlog

def setup_logging(log_level: str = "INFO", log_file: bool = True) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Whether to also log to a file
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler with color formatting
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(numeric_level)
    
    # Color formatter
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(color_formatter)
    root_logger.addHandler(console_handler)
    
    # Create file handler if requested
    if log_file:
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        log_filename = f"pinterest_{datetime.now().strftime('%Y%m%d')}.log"
        log_path = os.path.join(logs_dir, log_filename)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(numeric_level)
        
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        
        root_logger.addHandler(file_handler)
        logging.info(f"Logging to file: {log_path}")

    # Configure library loggers to reduce verbosity
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

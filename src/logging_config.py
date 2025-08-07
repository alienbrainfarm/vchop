"""
Logging configuration for the vchop application.

This module sets up centralized logging with appropriate levels
and formatting for better debugging and monitoring.
"""

import logging
import os
from pathlib import Path

# Create logs directory in the same location as settings
LOGS_DIR = Path.home() / '.vchop' / 'logs'

def setup_logging(level=logging.INFO, log_to_file=True):
    """Setup logging configuration for the application.
    
    Args:
        level: Logging level (default: INFO)
        log_to_file: Whether to also log to a file (default: True)
    """
    # Create logs directory if it doesn't exist
    if log_to_file:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if log_to_file:
        log_file = LOGS_DIR / 'vchop.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name):
    """Get a logger with the specified name.
    
    Args:
        name: Name for the logger (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
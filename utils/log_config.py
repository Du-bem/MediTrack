"""
Logging configuration for MediTrack
"""
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(log_file=None, log_level=logging.INFO, log_format=None, console_output=True):
    """
    Configure logging for the application
    
    Args:
        log_file: Path to the log file
        log_level: Logging level
        log_format: Log message format
        console_output: Whether to output logs to console
    """
    # Create logs directory if it doesn't exist
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    else:
        # Default log file in logs directory
        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_file = f"logs/meditrack_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Set default log format if not provided
    if not log_format:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Add file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Reduce verbosity of some loggers
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    return root_logger

def get_logger(name):
    """
    Get a logger with the specified name
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


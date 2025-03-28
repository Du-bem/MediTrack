"""
Configuration module for MediTrack
Handles configuration settings, database connection, and logging setup
"""
import os
import logging
import logging.handlers
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def load_config():
    """Load configuration from config file or environment variables"""
    config = {
        "database": {
            "url": os.getenv("DB_URL", "postgresql://postgres:2005@localhost/meditrack_db"),
            "echo": os.getenv("DB_ECHO", "False").lower() == "true"
        },
        "logging": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "file": os.getenv("LOG_FILE", "meditrack.log")
        },
        "export": {
            "default_directory": os.getenv("EXPORT_DIR", "./exports")
        }
    }
    
    # Try to load from config file if it exists
    config_file = os.getenv("CONFIG_FILE", "config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                # Merge configurations
                for section in file_config:
                    if section in config:
                        config[section].update(file_config[section])
                    else:
                        config[section] = file_config[section]
        except Exception as e:
            logging.warning(f"Failed to load config file: {e}")
    
    # Create database engine and session
    engine = create_engine(
        config["database"]["url"], 
        echo=config["database"]["echo"]
    )
    Session = sessionmaker(bind=engine)
    config["db_session"] = Session
    config["db_engine"] = engine
    
    # Ensure export directory exists
    os.makedirs(config["export"]["default_directory"], exist_ok=True)
    
    return config

def setup_logging():
    """Configure logging for the application"""
    log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
    log_file = os.getenv("LOG_FILE", "meditrack.log")
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format
    )
    
    # Add file handler with rotation
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger('').addHandler(handler)
    
    # Reduce verbosity of SQLAlchemy and other libraries
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


#!/usr/bin/env python3
"""
Simple script to create all database tables for MediTrack
This script creates all tables defined in SQLAlchemy models in the meditrack_db database.
"""
import os
import sys
import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the current directory to the Python path to ensure imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # Import the SQLAlchemy models and create_engine
    from sqlalchemy import create_engine
    from db.models import Base
    
    # Database connection URL - modify as needed
    DB_URL = "postgresql://postgres:2005@localhost/meditrack_db"
    
    logger.info(f"Connecting to database: {DB_URL}")
    
    # Create engine
    engine = create_engine(DB_URL)
    
    logger.info("Creating all tables...")
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    logger.info("All tables created successfully!")
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure you're running this script from the project root directory")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error creating tables: {e}")
    sys.exit(1)
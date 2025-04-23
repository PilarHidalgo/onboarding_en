#!/usr/bin/env python3
"""
Fruit Inventory Management Application

A desktop application for managing fruit inventory with features for
tracking, adding, updating, and deleting fruit items.

Usage:
    python app.py [options]

Options:
    --config FILE     Path to configuration file
    --debug           Enable debug mode
    --log-level LEVEL Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    --db-path PATH    Path to database file
"""

import os
import sys
import logging
import traceback
from typing import Optional

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import configuration
from config import config

# Setup logger
logger = logging.getLogger(__name__)

# Import application components
from ui import start_application
from services import initialize_services
from models import initialize_database


def setup_environment() -> None:
    """Setup application environment
    
    Creates necessary directories and files for the application.
    """
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(config.database.path), exist_ok=True)
    
    # Create backup directory if it doesn't exist
    os.makedirs(config.database.backup_dir, exist_ok=True)
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(config.logging.file), exist_ok=True)
    
    logger.debug("Application environment setup complete")


def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler
    
    Args:
        exc_type: Exception type
        exc_value: Exception value
        exc_traceback: Exception traceback
    """
    # Log the exception
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Show error message to user
    import tkinter as tk
    from tkinter import messagebox
    
    # Format the error message
    error_msg = f"An unexpected error occurred:\n\n{exc_value}"
    
    if config.app.debug:
        # In debug mode, show the traceback
        error_msg += f"\n\nTraceback:\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}"
    
    # Create a root window if one doesn't exist
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror("Application Error", error_msg)
        root.destroy()
    except:
        # If we can't create a Tkinter window, just print to console
        print(error_msg, file=sys.stderr)
    
    # Exit the application
    sys.exit(1)


def main() -> None:
    """Main application entry point"""
    try:
        # Setup application environment
        setup_environment()
        
        # Initialize database
        logger.info("Initializing database...")
        initialize_database(config.database)
        
        # Initialize services
        logger.info("Initializing services...")
        services = initialize_services(config)
        
        # Start the UI
        logger.info("Starting application UI...")
        app = start_application(config)
        
        # Inject services into the application
        app.inject_services(services)
        
        # Run the application
        logger.info(f"Running {config.app.name} v{config.app.version}")
        app.run()
        
        logger.info("Application exited normally")
        
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        
        # Show error message to user
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror(
            "Startup Error",
            f"Failed to start the application:\n\n{str(e)}\n\n"
            f"Please check the log file for more details:\n{config.logging.file}"
        )
        root.destroy()
        
        sys.exit(1)


if __name__ == "__main__":
    # Set up global exception handler
    if not config.app.debug:
        sys.excepthook = handle_exception
    
    # Run the application
    main()
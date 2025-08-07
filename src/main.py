
"""
Main entry point for the vchop video browser application.

This module initializes the PyQt5 application and starts the main window.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from video_browser import VideoBrowser
from logging_config import setup_logging, get_logger
from __version__ import __version__

def main():
    """Main entry point for the application."""
    # Setup logging
    setup_logging()
    logger = get_logger(__name__)
    
    logger.info("Starting vchop application")
    
    # Get command line arguments
    start_dir = sys.argv[1] if len(sys.argv) > 1 else None
    if start_dir:
        logger.info(f"Starting with directory: {start_dir}")
    
    # Create PyQt5 application
    app = QApplication(sys.argv)
    app.setApplicationName("vchop")
    app.setApplicationVersion(__version__)
    
    try:
        # Create and show main window
        window = VideoBrowser(start_dir)
        window.show()
        
        logger.info("Application window created and displayed")
        
        # Start event loop
        exit_code = app.exec_()
        logger.info(f"Application exiting with code: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.error(f"Fatal error starting application: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()

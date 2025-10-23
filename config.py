"""
Configuration module for CyberLearn application.
Handles debug mode, logging, and application settings.
"""

import os
import sys
import logging
from pathlib import Path

class Config:
    """Application configuration"""

    def __init__(self):
        # Check for verbose flag
        self.debug = '-v' in sys.argv or '--verbose' in sys.argv or '--debug' in sys.argv
        self.verbose = self.debug

        # Paths
        self.base_dir = Path(__file__).parent
        self.content_dir = self.base_dir / 'content'
        self.db_path = self.base_dir / 'cyberlearn.db'

        # Database settings
        self.db_echo = self.debug  # SQLAlchemy echo mode

        # Streamlit settings
        self.page_title = "CyberLearn - Adaptive Cyber Training"
        self.page_icon = "🛡️"
        self.layout = "wide"

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging based on debug mode"""
        if self.debug:
            log_level = logging.DEBUG
            log_format = '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
        else:
            log_level = logging.WARNING
            log_format = '[%(asctime)s] %(levelname)s: %(message)s'

        logging.basicConfig(
            level=log_level,
            format=log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.logger = logging.getLogger('cyberlearn')

        if self.debug:
            self.logger.debug("Debug mode enabled")
            self.logger.debug(f"Base directory: {self.base_dir}")
            self.logger.debug(f"Content directory: {self.content_dir}")
            self.logger.debug(f"Database path: {self.db_path}")

    def log_debug(self, message):
        """Log debug message if debug mode is enabled"""
        if self.debug:
            self.logger.debug(message)

    def log_info(self, message):
        """Log info message"""
        self.logger.info(message)

    def log_warning(self, message):
        """Log warning message"""
        self.logger.warning(message)

    def log_error(self, message):
        """Log error message"""
        self.logger.error(message)

# Global config instance
config = Config()

# Convenience function for debug printing
def debug_print(message):
    """Print debug message if debug mode is enabled"""
    if config.debug:
        print(f"[DEBUG] {message}")

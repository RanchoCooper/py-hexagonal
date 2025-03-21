"""
Main application entry point.
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cmd.server.app import Application

from util.env_checker import check_environment


def main() -> None:
    """
    Main application entry point.
    Creates and runs the application.
    """
    # Check if required environment variables are set
    check_environment()
    
    # Create and run the application
    app = Application()
    app.run()


if __name__ == '__main__':
    main() 
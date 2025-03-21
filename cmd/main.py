"""
Application entry point.

This module provides the main entry point for the application.
"""
import argparse
import logging
import os
from pathlib import Path

from adapter.di.container import (
    AppContainer,
    _set_container_instance,
    initialize_database,
    initialize_event_handlers,
)
from config.config import load_config

logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Hexagonal Architecture Example')
    parser.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    return parser.parse_args()


def main():
    """
    Main entry point for the application.
    
    This function initializes the application components and starts the
    Flask server.
    """
    # Parse command-line arguments
    args = parse_args()
    
    # Load configuration
    config_path = args.config
    config = load_config(config_path)
    
    # Set up logging early
    logging.basicConfig(
        level=getattr(logging, config['logging']['level']),
        format=config['logging']['format']
    )
    
    logger.info(f"Starting application with config from {config_path}")
    
    # Create and configure the dependency injection container
    container = AppContainer()
    container.config.from_dict(config)
    
    # Set container instance for global access
    _set_container_instance(container)
    
    # 触发数据库注册
    db_registry_configurator = container.db_registry_configurator()
    
    # Initialize database
    initialize_database(container)
    
    # Initialize event handlers
    initialize_event_handlers(container)
    
    # Get the Flask app from the container
    app = container.flask_app()
    
    # Start the Flask server
    app.run(host=args.host, port=args.port)
    
    logger.info("Application stopped")


if __name__ == '__main__':
    main() 
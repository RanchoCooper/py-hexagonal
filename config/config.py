"""
Application configuration.

This module provides the configuration for the application, loaded from
environment variables or configuration files.
"""
import logging
import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load application configuration.
    
    Configuration is loaded from a YAML file and can be overridden by
    environment variables.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    # Default configuration
    config = {
        'flask': {
            'DEBUG': False,
            'TESTING': False,
            'SECRET_KEY': os.getenv('FLASK_SECRET_KEY', 'dev-secret-key'),
        },
        'db': {
            'mysql': {
                'url': os.getenv('DATABASE_URL', 'sqlite:///app.db'),
                'echo': os.getenv('DATABASE_ECHO', '').lower() in ('true', '1', 'yes'),
            },
            'postgresql': {
                'url': os.getenv('DATABASE_URL', 'sqlite:///app.db'),
                'echo': os.getenv('DATABASE_ECHO', '').lower() in ('true', '1', 'yes'),
            },
        },
        'redis': {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', '6379')),
            'db': int(os.getenv('REDIS_DB', '0')),
            'prefix': os.getenv('REDIS_PREFIX', 'app:'),
        },
        'logging': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        }
    }
    
    # Load configuration from file if provided
    if config_path:
        path = Path(config_path)
        if path.exists():
            with open(path, 'r') as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    # Deep merge the file configuration with the default configuration
                    deep_merge(config, file_config)
    
    return config


def deep_merge(dest: Dict[str, Any], src: Dict[str, Any]) -> None:
    """
    Deep merge two dictionaries.
    
    The source dictionary is merged into the destination dictionary, with
    source values taking precedence for overlapping keys.
    
    Args:
        dest: Destination dictionary
        src: Source dictionary
    """
    for key, value in src.items():
        if key in dest and isinstance(dest[key], dict) and isinstance(value, dict):
            deep_merge(dest[key], value)
        else:
            dest[key] = value 
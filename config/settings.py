"""Configuration settings module for the application."""
import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()


# Application configuration
class Config:
    """Application Configuration Class."""

    # Basic configuration
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Service configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))

    # Database configuration
    DB_URI = os.getenv("DB_URI", "sqlite:///app.db")

    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development Environment Configuration."""

    DEBUG = True


class TestingConfig(Config):
    """Testing Environment Configuration."""

    TESTING = True
    DB_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production Environment Configuration."""

    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")  # Must be set


# Configuration mapping
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


# Get current configuration
def get_config():
    """Get current environment configuration."""
    env = os.getenv("ENV", "development")
    return config_by_name[env]

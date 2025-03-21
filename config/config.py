"""
Configuration module for the application.
This module loads configuration from environment variables and config files.
"""

import os
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator


class DatabaseConfig(BaseModel):
    """Database configuration model."""
    driver: str = Field("sqlite", description="Database driver")
    host: str = Field("localhost", description="Database host")
    port: int = Field(3306, description="Database port")
    username: str = Field("root", description="Database username")
    password: str = Field("password", description="Database password")
    database: str = Field("hexagonal", description="Database name")
    
    @property
    def connection_string(self) -> str:
        """Get the database connection string."""
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseModel):
    """Redis configuration model."""
    host: str = Field("localhost", description="Redis host")
    port: int = Field(6379, description="Redis port")
    password: Optional[str] = Field(None, description="Redis password")
    db: int = Field(0, description="Redis database index")
    
    @property
    def connection_string(self) -> str:
        """Get the Redis connection string."""
        password_part = f":{self.password}@" if self.password else ""
        return f"redis://{password_part}{self.host}:{self.port}/{self.db}"


class ServerConfig(BaseModel):
    """Server configuration model."""
    host: str = Field("127.0.0.1", description="Server host")
    port: int = Field(5000, description="Server port")
    debug: bool = Field(False, description="Debug mode")
    secret_key: str = Field("your-secret-key", description="Secret key for sessions")
    
    @validator("port")
    def validate_port(cls, v):
        """Validate that the port is within valid range."""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v


class Config(BaseModel):
    """Application configuration model."""
    server: ServerConfig = Field(default_factory=ServerConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    log_level: str = Field("INFO", description="Logging level")
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate that the log level is a valid level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v.upper()


def load_config() -> Config:
    """
    Load configuration from environment variables and config files.
    
    Returns:
        Config: The application configuration.
    """
    # First, try to load from .env file
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # If .env doesn't exist, try .env.example
        env_example_path = Path(__file__).parent / ".env.example"
        if env_example_path.exists():
            load_dotenv(env_example_path)
    
    # Create and return the configuration object
    return Config(
        server=ServerConfig(
            host=os.getenv("SERVER_HOST", "127.0.0.1"),
            port=int(os.getenv("SERVER_PORT", "5000")),
            debug=os.getenv("DEBUG", "False").lower() == "true",
            secret_key=os.getenv("SECRET_KEY", "your-secret-key")
        ),
        database=DatabaseConfig(
            driver=os.getenv("DB_DRIVER", "sqlite"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            username=os.getenv("DB_USERNAME", "root"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_DATABASE", "hexagonal")
        ),
        redis=RedisConfig(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            password=os.getenv("REDIS_PASSWORD", None),
            db=int(os.getenv("REDIS_DB", "0"))
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO")
    )


# Application config instance
config = load_config() 
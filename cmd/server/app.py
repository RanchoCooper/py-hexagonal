"""
Flask application entry point.
"""

import logging
import os
import sys
from typing import List

from flask import Flask
from flask_cors import CORS

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from adapter.http.error_handler import register_error_handlers
from adapter.http.example_controller import ExampleController
from adapter.http.health_controller import HealthController
from adapter.http.middleware import request_logger_middleware
from config.config import config
from util.di.container import Container
from util.logging import configure_logging


class Application:
    """
    Flask application initialization and configuration.
    This wires up all the components of the application.
    """
    
    def __init__(self):
        """Initialize the application."""
        # Configure logging early
        self._configure_logging()
        
        # Create Flask app
        self._app = Flask(__name__)
        self._configure_app()
        self._configure_cors()
        self._configure_middleware()
        self._configure_error_handlers()
        self._container = self._create_container()
        self._register_routes()
        
        # Log application startup
        logging.getLogger(__name__).info("Application initialized")
    
    def _configure_app(self) -> None:
        """Configure the Flask application."""
        self._app.config['SECRET_KEY'] = config.server.secret_key
        self._app.config['JSON_SORT_KEYS'] = False
        self._app.config['DEBUG'] = config.server.debug
    
    def _configure_logging(self) -> None:
        """Configure application logging."""
        # Use structured logging
        configure_logging(
            level=config.log_level,
            use_json=os.getenv("LOG_FORMAT", "").lower() == "json"
        )
    
    def _configure_cors(self) -> None:
        """Configure CORS for the application."""
        CORS(self._app, resources={r"/api/*": {"origins": "*"}})
    
    def _configure_middleware(self) -> None:
        """Configure application middleware."""
        # Register request logging middleware
        request_logger_middleware(self._app)
    
    def _configure_error_handlers(self) -> None:
        """Configure error handlers for the application."""
        register_error_handlers(self._app)
    
    def _create_container(self) -> Container:
        """Create and configure the dependency injection container."""
        container = Container()
        
        # Configure the container with application settings
        container.config.from_dict({
            "server": {
                "host": config.server.host,
                "port": config.server.port,
                "debug": config.server.debug,
            },
            "database": {
                "connection_string": config.database.connection_string,
            },
        })
        
        # Initialize resources that require setup
        container.wire_events()
        
        return container
    
    def _register_routes(self) -> None:
        """Register the routes for the application."""
        # Create controllers with dependencies from container
        example_controller = ExampleController(self._container.example_app_service())
        health_controller = HealthController()
        
        # Register blueprints
        self._app.register_blueprint(example_controller.blueprint)
        self._app.register_blueprint(health_controller.blueprint)
        
        # Log registered routes
        logger = logging.getLogger(__name__)
        for rule in self._app.url_map.iter_rules():
            logger.debug(f"Registered route: {rule}")
    
    @property
    def app(self) -> Flask:
        """Get the Flask application."""
        return self._app
    
    @property
    def container(self) -> Container:
        """Get the dependency injection container."""
        return self._container
    
    def run(self) -> None:
        """Run the application."""
        logging.getLogger(__name__).info(
            f"Starting application on {config.server.host}:{config.server.port}"
        )
        self._app.run(
            host=config.server.host,
            port=config.server.port,
            debug=config.server.debug
        )


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application.
    """
    application = Application()
    return application.app


if __name__ == '__main__':
    application = Application()
    application.run() 
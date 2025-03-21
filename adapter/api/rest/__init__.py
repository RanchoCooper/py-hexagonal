"""REST API Adapter."""
import logging

from flask import Flask
from flask.logging import default_handler

from api.middleware import error_handler, request_logger
from api.routes import api_blueprint
from application.di.container import container
from config.settings import get_config

# Get configuration
config = get_config()

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create Flask application.

    Returns:
        Configured Flask application instance
    """
    # Create application
    app = Flask(__name__)

    # Configure application
    app.config.from_object(config)

    # Register middleware
    error_handler(app)
    request_logger(app)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")

    # Initialize database
    with app.app_context():
        container.db_init()

    # Log route information
    logger.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.info(f"{rule.endpoint}: {rule.rule} {rule.methods}")

    return app

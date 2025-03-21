"""Main Program Entry."""
import logging

from adapter.api.rest import create_app
from config.settings import get_config

# Get configuration
config = get_config()

# Setup root logger
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Run the main application."""
    # Create Flask application
    app = create_app()

    # Run application
    logger.info(f"Starting application on {config.HOST}:{config.PORT}, environment: {config.ENV}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()

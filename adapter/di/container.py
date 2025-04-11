"""
Dependency injection container.

This module provides the dependency injection container for the application,
which manages the instantiation and wiring of application components.
"""
import logging

import redis
from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from adapter.cache.redis_cache import ExampleRedisCache, RedisCache
from adapter.event.memory_event_bus import MemoryEventBus
from adapter.http.app_factory import create_app
from adapter.http.flask_app import register_resources
from adapter.http.resources.example_resource import ExampleListResource, ExampleResource
from adapter.repository import db_registry
from adapter.repository.sqlalchemy import (
    create_mysql_engine,
    create_postgresql_engine,
    create_scoped_session,
    create_session_factory,
    init_db_schema,
)
from adapter.repository.sqlalchemy.example_repository import SQLAlchemyExampleRepository
from adapter.repository.sqlalchemy.models import Base
from application.event.example_event_handlers import (
    ExampleCreatedEventHandler,
    ExampleDeletedEventHandler,
    ExampleUpdatedEventHandler,
)
from application.service.example_app_service import ExampleAppService
from domain.event.example_events import (
    ExampleCreatedEvent,
    ExampleDeletedEvent,
    ExampleUpdatedEvent,
)
from domain.service.example_service_impl import ExampleServiceImpl

logger = logging.getLogger(__name__)


def register_resources_with_deps(api):
    """
    Register API resources with the Flask-RESTful API, injecting dependencies.
    
    Args:
        api: Flask-RESTful API instance
    """
    # Get global container instance
    container = _get_container_instance()
    
    if container is not None:
        example_app_service = container.example_app_service()
        register_resources(api, example_app_service=example_app_service)
    else:
        logger.warning("Container instance not available, resources will not have dependencies injected")
        register_resources(api)


# Global variable for storing the container instance reference
_container_instance = None


def _get_container_instance():
    return _container_instance


def _set_container_instance(container):
    global _container_instance
    _container_instance = container


def register_databases(mysql_engine, postgresql_engine, mysql_session, postgresql_session, default_db):
    """
    Register databases to the global registry
    
    Args:
        mysql_engine: MySQL engine instance
        postgresql_engine: PostgreSQL engine instance
        mysql_session: MySQL session instance
        postgresql_session: PostgreSQL session instance
        default_db: Default database name
    """
    db_registry.register('mysql', mysql_engine, mysql_session)
    db_registry.register('postgresql', postgresql_engine, postgresql_session)
    if default_db in ('mysql', 'postgresql'):
        db_registry.set_default(default_db)
    logger.info(f"Databases registered: mysql, postgresql. Default: {db_registry._default}")


class AppContainer(containers.DeclarativeContainer):
    """
    Dependency injection container for the application.
    
    This container manages the instantiation and wiring of application
    components, following the dependency injection pattern.
    """
    
    # Configuration
    config = providers.Configuration()
    
    # Logging
    logging = providers.Resource(
        logging.basicConfig,
        level=config.logging.level,
        format=config.logging.format
    )
    
    # Database
    mysql_engine = providers.Singleton(
        create_mysql_engine,
        config.db.mysql.url,
        echo=config.db.mysql.echo,
    )
    
    postgresql_engine = providers.Singleton(
        create_postgresql_engine,
        config.db.postgresql.url,
        echo=config.db.postgresql.echo,
    )
    
    mysql_session_factory = providers.Singleton(
        create_session_factory,
        engine=mysql_engine
    )
    
    postgresql_session_factory = providers.Singleton(
        create_session_factory,
        engine=postgresql_engine
    )
    
    mysql_session = providers.Singleton(
        create_scoped_session,
        mysql_session_factory
    )
    
    postgresql_session = providers.Singleton(
        create_scoped_session,
        postgresql_session_factory
    )
    
    # Database Registry
    db_registry_configurator = providers.Resource(
        register_databases,
        mysql_engine=mysql_engine,
        postgresql_engine=postgresql_engine,
        mysql_session=mysql_session,
        postgresql_session=postgresql_session,
        default_db=config.db.default
    )
    
    # Redis
    redis_client = providers.Singleton(
        redis.Redis,
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        decode_responses=False
    )
    
    # Cache
    redis_cache = providers.Singleton(
        RedisCache,
        redis_client=redis_client,
        prefix=config.redis.prefix
    )
    
    example_cache = providers.Singleton(
        ExampleRedisCache,
        redis_cache=redis_cache
    )
    
    # Event Bus
    event_bus = providers.Singleton(
        MemoryEventBus
    )
    
    # Event Handlers
    example_created_handler = providers.Singleton(
        ExampleCreatedEventHandler
    )
    
    example_updated_handler = providers.Singleton(
        ExampleUpdatedEventHandler
    )
    
    example_deleted_handler = providers.Singleton(
        ExampleDeletedEventHandler
    )
    
    # Repositories
    example_repository = providers.Singleton(
        SQLAlchemyExampleRepository,
        db_name=config.db.examples_db
    )
    
    # Domain Services
    example_service = providers.Singleton(
        ExampleServiceImpl,
        repository=example_repository,
        event_bus=event_bus
    )
    
    # Application Services
    example_app_service = providers.Singleton(
        ExampleAppService,
        example_service=example_service
    )
    
    # HTTP Resources
    example_resource = providers.Factory(
        ExampleResource,
        example_app_service=example_app_service
    )
    
    example_list_resource = providers.Factory(
        ExampleListResource,
        example_app_service=example_app_service
    )
    
    # Flask App
    flask_app = providers.Singleton(
        create_app,
        config=config.flask,
        register_resources_func=register_resources_with_deps
    )


def initialize_event_handlers(container):
    """
    Initialize event handlers by subscribing them to the event bus.
    
    Args:
        container: The dependency injection container
    """
    event_bus = container.event_bus()
    
    # Subscribe to example events
    event_bus.subscribe("example.created", container.example_created_handler())
    event_bus.subscribe("example.updated", container.example_updated_handler())
    event_bus.subscribe("example.deleted", container.example_deleted_handler())
    
    logger.info("Event handlers initialized and subscribed to event bus")


def initialize_database(container):
    """
    Initialize and setup database connections.
    
    Args:
        container: The dependency injection container
    """
    # Ensure database registry is configured
    db_registry_configurator = container.db_registry_configurator()
    
    # Initialize MySQL database
    mysql_engine = container.mysql_engine()
    init_db_schema(mysql_engine)
    
    # Initialize PostgreSQL database
    postgresql_engine = container.postgresql_engine()
    init_db_schema(postgresql_engine)
    
    logger.info("Database initialized") 
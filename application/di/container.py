"""Dependency Injection Container."""
import logging
from typing import Callable

from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from adapter.repository.example_repo import Base, SQLAlchemyTaskRepository, SQLAlchemyUserRepository
from config.settings import get_config

# Setup logging
logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container."""

    # Configuration
    config = providers.Singleton(get_config)

    # Database engine
    engine = providers.Singleton(lambda config: create_engine(config.DB_URI), config=config)

    # Session factory
    session_factory = providers.Singleton(
        lambda engine: scoped_session(sessionmaker(bind=engine)), engine=engine
    )

    # Initialize database
    db_init = providers.Resource(lambda engine: Base.metadata.create_all(engine), engine=engine)

    # Repositories
    user_repository = providers.Factory(SQLAlchemyUserRepository, session=session_factory)

    task_repository = providers.Factory(SQLAlchemyTaskRepository, session=session_factory)


# Global container instance
container = Container()


def get_container() -> Container:
    """Get global container instance."""
    return container


def inject(dependency_name: str) -> Callable:
    """Dependency injection decorator.

    Usage:
    @inject('user_repository')
    def some_function(user_repository, ...):
        # Use user_repository

    Args:
        dependency_name: The name of the dependency to inject
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if dependency_name not in kwargs:
                # Get dependency from container
                dependency = getattr(container, dependency_name)()
                kwargs[dependency_name] = dependency
            return func(*args, **kwargs)

        return wrapper

    return decorator

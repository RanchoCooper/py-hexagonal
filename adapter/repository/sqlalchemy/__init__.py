"""
SQLAlchemy repository adapters.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from adapter.repository.sqlalchemy.models import Base


def create_mysql_engine(url, echo=False):
    """
    Create MySQL database engine
    
    Args:
        url: MySQL database connection URL
        echo: Whether to output SQL statements (for debugging)
    """
    return create_engine(
        url,
        echo=echo,
        pool_recycle=3600,
        pool_pre_ping=True,
    )


def create_postgresql_engine(url, echo=False):
    """
    Create PostgreSQL database engine
    
    Args:
        url: PostgreSQL database connection URL
        echo: Whether to output SQL statements (for debugging)
        
    Returns:
        SQLAlchemy Engine instance
    """
    return create_engine(url, echo=echo)


def create_session_factory(engine):
    """
    Create database session factory
    
    Args:
        engine: SQLAlchemy engine instance
        
    Returns:
        SQLAlchemy session factory
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_scoped_session(session_factory):
    """
    Create thread-safe database session
    
    Args:
        session_factory: SQLAlchemy session factory
        
    Returns:
        Thread-safe SQLAlchemy session
    """
    return scoped_session(session_factory)


def init_db_schema(engine):
    """
    Initialize database schema
    
    Args:
        engine: SQLAlchemy engine instance
    """
    Base.metadata.create_all(bind=engine) 
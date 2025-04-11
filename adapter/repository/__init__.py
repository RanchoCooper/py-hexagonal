"""
Repository adapters module.

This package contains adapter implementations for the domain repositories.
"""
import logging

logger = logging.getLogger(__name__)


def register_db(name, engine, session):
    """
    Register a database connection
    
    Args:
        name: Database name
        engine: SQLAlchemy engine
        session: SQLAlchemy session
    """

class DatabaseRegistry:
    """Database registry to manage different database connections"""

    def __init__(self):
        self._engines = {}
        self._sessions = {}
        self._default = None

    def register(self, name, engine, session):
        """
        Register a database connection
        
        Args:
            name: Database connection name
            engine: SQLAlchemy Engine instance
            session: SQLAlchemy Session instance
        """
        self._engines[name] = engine
        self._sessions[name] = session
        if self._default is None:
            self._default = name

    def set_default(self, name):
        """
        Set default database connection
        
        Args:
            name: Database connection name
        """
        if name not in self._engines:
            raise ValueError(f"No database registered with name '{name}'")
        self._default = name

    def get_engine(self, name=None):
        """
        Get database engine
        
        Args:
            name: Database connection name, returns default if None
            
        Returns:
            SQLAlchemy Engine instance
        """
        if name is None:
            name = self._default
        if name not in self._engines:
            raise ValueError(f"No database registered with name '{name}'")
        return self._engines[name]

    def get_session(self, name=None):
        """
        Get database session
        
        Args:
            name: Database connection name, returns default if None
            
        Returns:
            SQLAlchemy Session instance
        """
        if name is None:
            name = self._default
        if name not in self._sessions:
            raise ValueError(f"No database registered with name '{name}'")
        return self._sessions[name]


# Create global database registry instance
db_registry = DatabaseRegistry()

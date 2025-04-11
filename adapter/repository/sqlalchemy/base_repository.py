"""
SQLAlchemy base repository implementation.

This module provides base repository implementations using SQLAlchemy.
"""
import logging

from adapter.repository import db_registry
from domain.repository import Repository

logger = logging.getLogger(__name__)


class SQLAlchemyRepository(Repository):
    """
    Base SQLAlchemy repository implementation
    
    Provides basic database operations and the ability to dynamically select databases
    """
    
    def __init__(self, db_name=None):
        """
        Initialize repository
        
        Args:
            db_name: Database name to use, uses default if None
        """
        self.db_name = db_name
    
    @property
    def session(self):
        """
        Get current session
        
        Returns:
            SQLAlchemy Session instance
        """
        return db_registry.get_session(self.db_name)
    
    def commit(self):
        """Commit transaction"""
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
    
    def rollback(self):
        """Rollback transaction"""
        self.session.rollback() 
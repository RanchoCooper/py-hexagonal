"""
SQLAlchemy ORM models.

This module contains the SQLAlchemy ORM models for database persistence.
These models are part of the infrastructure layer, and are separate from
the domain models.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExampleModel(Base):
    """
    SQLAlchemy ORM model for the Example entity.
    
    This is a data access model used by the SQLAlchemy-based repository
    implementation to persist Example entities.
    """
    __tablename__ = "examples"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    
    def __init__(self, id: str, name: str, description: Optional[str] = None,
                created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        """
        Initialize a new ExampleModel instance.
        
        Args:
            id: The ID of the example
            name: The name of the example
            description: Optional description of the example
            created_at: The creation timestamp (defaults to now)
            updated_at: The last update timestamp (defaults to now)
        """
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or self.created_at 
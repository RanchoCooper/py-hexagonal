"""
Example entity definition for MySQL ORM.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExampleEntity(Base):
    """Example entity in MySQL representation."""
    
    __tablename__ = "examples"
    
    id = Column(BINARY(16), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(1000), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def to_domain(self) -> 'domain.model.example.Example':
        """
        Convert the ORM entity to a domain entity.
        
        Returns:
            A domain Example entity
        """
        # Import here to avoid circular imports
        from domain.model.example import Example
        
        return Example(
            id=self.id,
            name=self.name,
            description=self.description,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain(cls, example: 'domain.model.example.Example') -> 'ExampleEntity':
        """
        Create an ORM entity from a domain entity.
        
        Args:
            example: The domain entity
            
        Returns:
            An ORM entity
        """
        return cls(
            id=example.id,
            name=example.name,
            description=example.description,
            is_active=example.is_active,
            created_at=example.created_at,
            updated_at=example.updated_at
        ) 
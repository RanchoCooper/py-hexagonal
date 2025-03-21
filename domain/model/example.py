"""
Example domain model.

This module contains the Example entity, which represents a core business concept 
in the domain model. It follows domain-driven design principles by encapsulating
business rules and behaviors.
"""
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Example:
    """
    Example domain entity represents a core business concept.
    
    This entity encapsulates the state and behavior of an example object,
    following the domain-driven design principles where entities have
    identity and lifecycle.
    """
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values after instance creation."""
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    @classmethod
    def create(cls, name: str, description: Optional[str] = None) -> 'Example':
        """
        Factory method to create a new Example instance.
        
        Args:
            name: The name of the example
            description: Optional description of the example
            
        Returns:
            A new Example instance with generated ID
        """
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description
        )
    
    def update(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Updates the example with new values.
        
        Args:
            name: New name for the example (if provided)
            description: New description for the example (if provided)
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entity to a dictionary.
        
        Returns:
            Dictionary representation of the entity
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Example':
        """
        Create an entity from a dictionary.
        
        Args:
            data: Dictionary containing entity data
            
        Returns:
            Example entity instance
        """
        created_at = data.get('created_at')
        updated_at = data.get('updated_at')
        
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
            
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description'),
            created_at=created_at,
            updated_at=updated_at
        ) 
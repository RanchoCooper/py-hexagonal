"""
Data Transfer Objects for the Example entity.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from domain.model.example import Example


@dataclass
class ExampleDTO:
    """
    Data Transfer Object for the Example entity.
    Used to transfer example data between layers.
    """
    id: str  # UUID as string
    name: str
    description: str
    is_active: bool
    created_at: str  # ISO format string
    updated_at: str  # ISO format string
    
    @classmethod
    def from_entity(cls, entity: Example) -> "ExampleDTO":
        """
        Create a DTO from an entity.
        
        Args:
            entity (Example): The entity to convert.
            
        Returns:
            ExampleDTO: The created DTO.
        """
        return cls(
            id=str(entity.id),
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat()
        )
    
    @classmethod
    def from_entity_list(cls, entities: List[Example]) -> List["ExampleDTO"]:
        """
        Create DTOs from a list of entities.
        
        Args:
            entities (List[Example]): The entities to convert.
            
        Returns:
            List[ExampleDTO]: The created DTOs.
        """
        return [cls.from_entity(entity) for entity in entities]


@dataclass
class CreateExampleRequest:
    """
    Request object for creating a new example.
    """
    name: str
    description: str


@dataclass
class UpdateExampleRequest:
    """
    Request object for updating an example.
    """
    name: Optional[str] = None
    description: Optional[str] = None 
"""
Converter interface for the domain layer.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Converter(Generic[T, U], ABC):
    """
    Converter interface for transforming between different object types.
    """
    
    @abstractmethod
    def to_dto(self, entity: T) -> U:
        """
        Convert an entity to a DTO.
        
        Args:
            entity: The entity to convert
            
        Returns:
            The converted DTO
        """
        pass
    
    @abstractmethod
    def to_entity(self, dto: U) -> T:
        """
        Convert a DTO to an entity.
        
        Args:
            dto: The DTO to convert
            
        Returns:
            The converted entity
        """
        pass 
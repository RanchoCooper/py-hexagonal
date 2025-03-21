"""
Base repository module that defines the repository interface for all repositories.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from domain.model.entity import Entity

T = TypeVar('T', bound=Entity)


class Repository(Generic[T], ABC):
    """
    Base repository interface that defines the standard operations to be performed on a model.
    This is a port in the hexagonal architecture terminology.
    """
    
    @abstractmethod
    def find_by_id(self, entity_id: UUID) -> Optional[T]:
        """
        Find an entity by its ID.
        
        Args:
            entity_id (UUID): The ID of the entity to find.
            
        Returns:
            Optional[T]: The found entity, or None if not found.
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Find all entities.
        
        Returns:
            List[T]: A list of all entities.
        """
        pass
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save an entity to the repository.
        
        Args:
            entity (T): The entity to save.
            
        Returns:
            T: The saved entity.
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """
        Delete an entity from the repository.
        
        Args:
            entity_id (UUID): The ID of the entity to delete.
        """
        pass 
"""
In-memory example repository implementation.
"""

from typing import Dict, List, Optional
from uuid import UUID

from domain.model.example import Example
from domain.repository.example_repository import ExampleRepository


class MemoryExampleRepository(ExampleRepository):
    """
    An in-memory implementation of the ExampleRepository interface.
    This is an adapter in the hexagonal architecture terminology.
    """
    
    def __init__(self):
        """Initialize the repository."""
        self._examples: Dict[UUID, Example] = {}
    
    def find_by_id(self, entity_id: UUID) -> Optional[Example]:
        """
        Find an example by its ID.
        
        Args:
            entity_id (UUID): The ID of the example to find.
            
        Returns:
            Optional[Example]: The found example, or None if not found.
        """
        return self._examples.get(entity_id)
    
    def find_all(self) -> List[Example]:
        """
        Find all examples.
        
        Returns:
            List[Example]: A list of all examples.
        """
        return list(self._examples.values())
    
    def save(self, entity: Example) -> Example:
        """
        Save an example to the repository.
        
        Args:
            entity (Example): The example to save.
            
        Returns:
            Example: The saved example.
        """
        self._examples[entity.id] = entity
        return entity
    
    def delete(self, entity_id: UUID) -> None:
        """
        Delete an example from the repository.
        
        Args:
            entity_id (UUID): The ID of the example to delete.
        """
        if entity_id in self._examples:
            del self._examples[entity_id]
    
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name (str): The name to search for.
            
        Returns:
            Optional[Example]: The found example, or None if not found.
        """
        for example in self._examples.values():
            if example.name == name:
                return example
        return None
    
    def find_active(self) -> List[Example]:
        """
        Find all active examples.
        
        Returns:
            List[Example]: A list of all active examples.
        """
        return [example for example in self._examples.values() if example.is_active] 
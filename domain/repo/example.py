"""
Example repository interface for the domain layer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.model.example import Example


class ExampleRepository(ABC):
    """Example repository interface."""
    
    @abstractmethod
    def find_by_id(self, example_id: UUID) -> Optional[Example]:
        """
        Find an example by its ID.
        
        Args:
            example_id: The ID of the example
            
        Returns:
            The example if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Example]:
        """
        Find all examples.
        
        Returns:
            A list of all examples
        """
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name: The name of the example
            
        Returns:
            The example if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save(self, example: Example) -> Example:
        """
        Save an example.
        
        Args:
            example: The example to save
            
        Returns:
            The saved example
        """
        pass
    
    @abstractmethod
    def delete(self, example_id: UUID) -> None:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example to delete
        """
        pass 
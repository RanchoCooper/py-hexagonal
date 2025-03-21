"""
Example repository interface (port).

This module defines the repository interface for the Example entity. It follows the
repository pattern from Domain-Driven Design, providing a collection-like interface
to access domain objects.

In hexagonal architecture, this is a "port" that the application core uses to
communicate with the outside world. The actual implementation (adapter) will be
provided by the infrastructure layer.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model.example import Example


class ExampleRepository(ABC):
    """
    Repository interface for Example entities.
    
    This interface defines the contract that any Example repository implementation
    must fulfill. It follows the repository pattern from Domain-Driven Design,
    providing a collection-like interface for domain objects.
    """
    
    @abstractmethod
    def save(self, example: Example) -> Example:
        """
        Save an example to the repository.
        
        Args:
            example: The example entity to save
            
        Returns:
            The saved example with any updates (e.g., generated ID)
        """
        pass
    
    @abstractmethod
    def find_by_id(self, example_id: str) -> Optional[Example]:
        """
        Find an example by its ID.
        
        Args:
            example_id: The ID of the example to find
            
        Returns:
            The found example entity or None if not found
        """
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name: The name of the example to find
            
        Returns:
            The found example entity or None if not found
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Example]:
        """
        Find all examples in the repository.
        
        Returns:
            A list of all example entities
        """
        pass
    
    @abstractmethod
    def delete(self, example_id: str) -> bool:
        """
        Delete an example from the repository.
        
        Args:
            example_id: The ID of the example to delete
            
        Returns:
            True if the example was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """
        Check if an example with the given name exists.
        
        Args:
            name: The name to check
            
        Returns:
            True if an example with the given name exists, False otherwise
        """
        pass 
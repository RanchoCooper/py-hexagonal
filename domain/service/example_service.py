"""
Example domain service.

This module defines the domain service for the Example entity. Domain services
contain domain logic that doesn't naturally fit within an entity or value object.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model.example import Example


class ExampleService(ABC):
    """
    Domain service for the Example entity.
    
    This service contains domain logic that doesn't naturally fit within the
    Example entity or related value objects.
    """
    
    @abstractmethod
    def create_example(self, name: str, description: Optional[str] = None) -> Example:
        """
        Create a new example.
        
        Args:
            name: The name of the example
            description: Optional description of the example
            
        Returns:
            The created example
            
        Raises:
            ExampleNameAlreadyExistsError: If an example with the given name already exists
        """
        pass
    
    @abstractmethod
    def update_example(self, example_id: str, name: Optional[str] = None, 
                      description: Optional[str] = None) -> Example:
        """
        Update an existing example.
        
        Args:
            example_id: The ID of the example to update
            name: The new name of the example (if provided)
            description: The new description of the example (if provided)
            
        Returns:
            The updated example
            
        Raises:
            EntityNotFoundError: If the example with the given ID doesn't exist
            ExampleNameAlreadyExistsError: If the new name is already used by another example
        """
        pass
    
    @abstractmethod
    def delete_example(self, example_id: str) -> bool:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example to delete
            
        Returns:
            True if the example was deleted, False if it didn't exist
        """
        pass
    
    @abstractmethod
    def get_example(self, example_id: str) -> Example:
        """
        Get an example by its ID.
        
        Args:
            example_id: The ID of the example to get
            
        Returns:
            The found example
            
        Raises:
            EntityNotFoundError: If the example with the given ID doesn't exist
        """
        pass
    
    @abstractmethod
    def get_all_examples(self) -> List[Example]:
        """
        Get all examples.
        
        Returns:
            A list of all examples
        """
        pass 
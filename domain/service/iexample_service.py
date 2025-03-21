"""
Example service interface for the domain layer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.model.example import Example


class IExampleService(ABC):
    """Example service interface."""
    
    @abstractmethod
    def get_by_id(self, example_id: UUID) -> Example:
        """
        Get an example by its ID.
        
        Args:
            example_id: The ID of the example
            
        Returns:
            The example
            
        Raises:
            EntityNotFoundError: If the example is not found
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Example]:
        """
        Get all examples.
        
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
    def create(self, name: str, description: Optional[str] = None) -> Example:
        """
        Create a new example.
        
        Args:
            name: The name of the example
            description: The description of the example
            
        Returns:
            The created example
            
        Raises:
            DuplicateEntityError: If an example with the same name already exists
        """
        pass
    
    @abstractmethod
    def update(self, example_id: UUID, name: Optional[str] = None, 
               description: Optional[str] = None) -> Example:
        """
        Update an example.
        
        Args:
            example_id: The ID of the example
            name: The new name of the example
            description: The new description of the example
            
        Returns:
            The updated example
            
        Raises:
            EntityNotFoundError: If the example is not found
            DuplicateEntityError: If the new name conflicts with an existing example
        """
        pass
    
    @abstractmethod
    def delete(self, example_id: UUID) -> None:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example
            
        Raises:
            EntityNotFoundError: If the example is not found
        """
        pass
    
    @abstractmethod
    def activate(self, example_id: UUID) -> Example:
        """
        Activate an example.
        
        Args:
            example_id: The ID of the example
            
        Returns:
            The activated example
            
        Raises:
            EntityNotFoundError: If the example is not found
        """
        pass
    
    @abstractmethod
    def deactivate(self, example_id: UUID) -> Example:
        """
        Deactivate an example.
        
        Args:
            example_id: The ID of the example
            
        Returns:
            The deactivated example
            
        Raises:
            EntityNotFoundError: If the example is not found
        """
        pass 
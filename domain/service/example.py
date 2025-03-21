"""
Example service implementation for the domain layer.
"""

from typing import List, Optional
from uuid import UUID

from domain.model.example import Example
from domain.repo.error import DuplicateEntityError, EntityNotFoundError
from domain.repo.example import ExampleRepository
from domain.service.iexample_service import IExampleService


class ExampleService(IExampleService):
    """Example service implementation."""
    
    def __init__(self, example_repository: ExampleRepository):
        """
        Initialize the example service.
        
        Args:
            example_repository: The example repository
        """
        self.example_repository = example_repository
    
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
        example = self.example_repository.find_by_id(example_id)
        if example is None:
            raise EntityNotFoundError("Example", example_id)
        return example
    
    def get_all(self) -> List[Example]:
        """
        Get all examples.
        
        Returns:
            A list of all examples
        """
        return self.example_repository.find_all()
    
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name: The name of the example
            
        Returns:
            The example if found, None otherwise
        """
        return self.example_repository.find_by_name(name)
    
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
        # Check if an example with the same name already exists
        existing = self.example_repository.find_by_name(name)
        if existing is not None:
            raise DuplicateEntityError("Example", "name", name)
        
        # Create a new example
        example = Example.create(name, description)
        
        # Save the example to the repository
        return self.example_repository.save(example)
    
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
        # Get the example
        example = self.get_by_id(example_id)
        
        # Check for name conflicts if the name is being changed
        if name is not None and name != example.name:
            existing = self.example_repository.find_by_name(name)
            if existing is not None and existing.id != example_id:
                raise DuplicateEntityError("Example", "name", name)
        
        # Update the example
        example.update(name, description)
        
        # Save the example to the repository
        return self.example_repository.save(example)
    
    def delete(self, example_id: UUID) -> None:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example
            
        Raises:
            EntityNotFoundError: If the example is not found
        """
        # Check if the example exists
        self.get_by_id(example_id)
        
        # Delete the example
        self.example_repository.delete(example_id)
    
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
        # Get the example
        example = self.get_by_id(example_id)
        
        # Activate the example
        example.activate()
        
        # Save the example to the repository
        return self.example_repository.save(example)
    
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
        # Get the example
        example = self.get_by_id(example_id)
        
        # Deactivate the example
        example.deactivate()
        
        # Save the example to the repository
        return self.example_repository.save(example) 
"""
Example domain service module that contains business logic for Example entities.
"""

from typing import List, Optional
from uuid import UUID

from domain.model.example import Example
from domain.repository.example_repository import ExampleRepository


class ExampleService:
    """
    Domain service that contains business logic for Example entities.
    """
    
    def __init__(self, example_repository: ExampleRepository):
        """
        Initialize the Example domain service.
        
        Args:
            example_repository (ExampleRepository): The repository for Example entities.
        """
        self._repository = example_repository
    
    def create_example(self, name: str, description: str) -> Example:
        """
        Create a new Example entity.
        
        Args:
            name (str): The name of the new example.
            description (str): The description of the new example.
            
        Returns:
            Example: The created example.
        """
        # Check if an example with this name already exists
        existing = self._repository.find_by_name(name)
        if existing:
            raise ValueError(f"Example with name '{name}' already exists")
        
        # Create and save the new example
        example = Example(name=name, description=description)
        return self._repository.save(example)
    
    def get_example(self, example_id: UUID) -> Optional[Example]:
        """
        Get an example by its ID.
        
        Args:
            example_id (UUID): The ID of the example to get.
            
        Returns:
            Optional[Example]: The found example, or None if not found.
        """
        return self._repository.find_by_id(example_id)
    
    def get_all_examples(self) -> List[Example]:
        """
        Get all examples.
        
        Returns:
            List[Example]: A list of all examples.
        """
        return self._repository.find_all()
    
    def get_active_examples(self) -> List[Example]:
        """
        Get all active examples.
        
        Returns:
            List[Example]: A list of all active examples.
        """
        return self._repository.find_active()
    
    def update_example(self, example_id: UUID, name: Optional[str] = None, 
                      description: Optional[str] = None) -> Optional[Example]:
        """
        Update an example's details.
        
        Args:
            example_id (UUID): The ID of the example to update.
            name (Optional[str]): The new name, if any.
            description (Optional[str]): The new description, if any.
            
        Returns:
            Optional[Example]: The updated example, or None if not found.
        """
        example = self._repository.find_by_id(example_id)
        if not example:
            return None
        
        # Check for name uniqueness if name is being updated
        if name and name != example.name:
            existing = self._repository.find_by_name(name)
            if existing and existing.id != example_id:
                raise ValueError(f"Example with name '{name}' already exists")
        
        # Update the example
        example.update_details(name, description)
        return self._repository.save(example)
    
    def activate_example(self, example_id: UUID) -> Optional[Example]:
        """
        Activate an example.
        
        Args:
            example_id (UUID): The ID of the example to activate.
            
        Returns:
            Optional[Example]: The activated example, or None if not found.
        """
        example = self._repository.find_by_id(example_id)
        if not example:
            return None
        
        example.activate()
        return self._repository.save(example)
    
    def deactivate_example(self, example_id: UUID) -> Optional[Example]:
        """
        Deactivate an example.
        
        Args:
            example_id (UUID): The ID of the example to deactivate.
            
        Returns:
            Optional[Example]: The deactivated example, or None if not found.
        """
        example = self._repository.find_by_id(example_id)
        if not example:
            return None
        
        example.deactivate()
        return self._repository.save(example)
    
    def delete_example(self, example_id: UUID) -> bool:
        """
        Delete an example.
        
        Args:
            example_id (UUID): The ID of the example to delete.
            
        Returns:
            bool: True if the example was deleted, False if not found.
        """
        example = self._repository.find_by_id(example_id)
        if not example:
            return False
        
        self._repository.delete(example_id)
        return True 
"""
Example application service.

This module contains the application service for the Example entity, which
coordinates domain objects and services to fulfill use cases.
"""
from typing import Any, Dict, List, Optional

from domain.model.errors import EntityNotFoundError, ExampleNameAlreadyExistsError
from domain.model.example import Example
from domain.service.example_service import ExampleService


class ExampleAppService:
    """
    Application service for the Example entity.
    
    This service implements application-specific use cases by coordinating
    domain objects and services. It acts as a facade for the application's
    functionality related to the Example entity.
    """
    
    def __init__(self, example_service: ExampleService):
        """
        Initialize the service with its dependencies.
        
        Args:
            example_service: The domain service for Example entities
        """
        self._example_service = example_service
    
    def create_example(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new example.
        
        Args:
            name: The name of the example
            description: Optional description of the example
            
        Returns:
            The created example as a dictionary
            
        Raises:
            ExampleNameAlreadyExistsError: If an example with the given name already exists
        """
        example = self._example_service.create_example(name, description)
        return example.to_dict()
    
    def update_example(self, example_id: str, name: Optional[str] = None, 
                      description: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing example.
        
        Args:
            example_id: The ID of the example to update
            name: The new name of the example (if provided)
            description: The new description of the example (if provided)
            
        Returns:
            The updated example as a dictionary
            
        Raises:
            EntityNotFoundError: If the example with the given ID doesn't exist
            ExampleNameAlreadyExistsError: If the new name is already used by another example
        """
        example = self._example_service.update_example(example_id, name, description)
        return example.to_dict()
    
    def delete_example(self, example_id: str) -> bool:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example to delete
            
        Returns:
            True if the example was deleted, False if it didn't exist
        """
        return self._example_service.delete_example(example_id)
    
    def get_example(self, example_id: str) -> Dict[str, Any]:
        """
        Get an example by its ID.
        
        Args:
            example_id: The ID of the example to get
            
        Returns:
            The found example as a dictionary
            
        Raises:
            EntityNotFoundError: If the example with the given ID doesn't exist
        """
        example = self._example_service.get_example(example_id)
        return example.to_dict()
    
    def get_all_examples(self) -> List[Dict[str, Any]]:
        """
        Get all examples.
        
        Returns:
            A list of all examples as dictionaries
        """
        examples = self._example_service.get_all_examples()
        return [example.to_dict() for example in examples] 
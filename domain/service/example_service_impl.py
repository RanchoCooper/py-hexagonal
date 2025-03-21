"""
Example domain service implementation.

This module provides the implementation of the Example domain service.
"""
from typing import List, Optional

from domain.event.event_bus import EventBus
from domain.event.example_events import (
    ExampleCreatedEvent,
    ExampleDeletedEvent,
    ExampleUpdatedEvent,
)
from domain.model.errors import EntityNotFoundError, ExampleNameAlreadyExistsError
from domain.model.example import Example
from domain.repository.example_repository import ExampleRepository
from domain.service.example_service import ExampleService


class ExampleServiceImpl(ExampleService):
    """
    Implementation of the Example domain service.
    
    This service contains domain logic for the Example entity and
    coordinates with the repository and event bus.
    """
    
    def __init__(self, repository: ExampleRepository, event_bus: EventBus):
        """
        Initialize the service with its dependencies.
        
        Args:
            repository: The repository for Example entities
            event_bus: The event bus for publishing domain events
        """
        self._repository = repository
        self._event_bus = event_bus
    
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
        # Check if an example with the given name already exists
        if self._repository.exists_by_name(name):
            raise ExampleNameAlreadyExistsError(name)
        
        # Create a new example
        example = Example.create(name, description)
        
        # Save the example
        saved_example = self._repository.save(example)
        
        # Publish an event
        self._event_bus.publish(
            ExampleCreatedEvent(
                event_id="",  # Will be auto-generated
                event_type="",  # Will be set by the event class
                occurred_at=None,  # Will be auto-generated
                example_id=saved_example.id,
                name=saved_example.name,
                description=saved_example.description
            )
        )
        
        return saved_example
    
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
        # Get the example
        example = self._repository.find_by_id(example_id)
        if not example:
            raise EntityNotFoundError("Example", example_id)
        
        # Check if the new name is already used by another example
        if name and name != example.name and self._repository.exists_by_name(name):
            raise ExampleNameAlreadyExistsError(name)
        
        # Update the example
        example.update(name, description)
        
        # Save the example
        updated_example = self._repository.save(example)
        
        # Publish an event
        self._event_bus.publish(
            ExampleUpdatedEvent(
                event_id="",  # Will be auto-generated
                event_type="",  # Will be set by the event class
                occurred_at=None,  # Will be auto-generated
                example_id=updated_example.id,
                name=updated_example.name,
                description=updated_example.description
            )
        )
        
        return updated_example
    
    def delete_example(self, example_id: str) -> bool:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example to delete
            
        Returns:
            True if the example was deleted, False if it didn't exist
        """
        # Check if the example exists
        example = self._repository.find_by_id(example_id)
        if not example:
            return False
        
        # Delete the example
        if not self._repository.delete(example_id):
            return False
        
        # Publish an event
        self._event_bus.publish(
            ExampleDeletedEvent(
                event_id="",  # Will be auto-generated
                event_type="",  # Will be set by the event class
                occurred_at=None,  # Will be auto-generated
                example_id=example_id
            )
        )
        
        return True
    
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
        example = self._repository.find_by_id(example_id)
        if not example:
            raise EntityNotFoundError("Example", example_id)
        return example
    
    def get_all_examples(self) -> List[Example]:
        """
        Get all examples.
        
        Returns:
            A list of all examples
        """
        return self._repository.find_all() 
"""
Example domain events module that defines events related to the Example entity.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from domain.event.event import DomainEvent


class ExampleCreatedEvent(DomainEvent):
    """
    Event that is triggered when a new Example is created.
    """
    
    def __init__(self, example_id: UUID, name: str, event_id: Optional[UUID] = None,
                 timestamp: Optional[datetime] = None):
        """
        Initialize a new ExampleCreatedEvent.
        
        Args:
            example_id (UUID): The ID of the created example.
            name (str): The name of the created example.
            event_id (Optional[UUID]): The event ID. Defaults to a generated UUID.
            timestamp (Optional[datetime]): The event timestamp. Defaults to current time.
        """
        super().__init__(event_id, timestamp)
        self._example_id = example_id
        self._name = name
    
    @property
    def example_id(self) -> UUID:
        """Get the ID of the created example."""
        return self._example_id
    
    @property
    def name(self) -> str:
        """Get the name of the created example."""
        return self._name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary.
        
        Returns:
            Dict[str, Any]: The event as a dictionary.
        """
        data = super().to_dict()
        data.update({
            "example_id": str(self._example_id),
            "name": self._name
        })
        return data


class ExampleUpdatedEvent(DomainEvent):
    """
    Event that is triggered when an Example is updated.
    """
    
    def __init__(self, example_id: UUID, name: str, event_id: Optional[UUID] = None,
                 timestamp: Optional[datetime] = None):
        """
        Initialize a new ExampleUpdatedEvent.
        
        Args:
            example_id (UUID): The ID of the updated example.
            name (str): The name of the updated example.
            event_id (Optional[UUID]): The event ID. Defaults to a generated UUID.
            timestamp (Optional[datetime]): The event timestamp. Defaults to current time.
        """
        super().__init__(event_id, timestamp)
        self._example_id = example_id
        self._name = name
    
    @property
    def example_id(self) -> UUID:
        """Get the ID of the updated example."""
        return self._example_id
    
    @property
    def name(self) -> str:
        """Get the name of the updated example."""
        return self._name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary.
        
        Returns:
            Dict[str, Any]: The event as a dictionary.
        """
        data = super().to_dict()
        data.update({
            "example_id": str(self._example_id),
            "name": self._name
        })
        return data


class ExampleDeletedEvent(DomainEvent):
    """
    Event that is triggered when an Example is deleted.
    """
    
    def __init__(self, example_id: UUID, event_id: Optional[UUID] = None,
                 timestamp: Optional[datetime] = None):
        """
        Initialize a new ExampleDeletedEvent.
        
        Args:
            example_id (UUID): The ID of the deleted example.
            event_id (Optional[UUID]): The event ID. Defaults to a generated UUID.
            timestamp (Optional[datetime]): The event timestamp. Defaults to current time.
        """
        super().__init__(event_id, timestamp)
        self._example_id = example_id
    
    @property
    def example_id(self) -> UUID:
        """Get the ID of the deleted example."""
        return self._example_id
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary.
        
        Returns:
            Dict[str, Any]: The event as a dictionary.
        """
        data = super().to_dict()
        data.update({
            "example_id": str(self._example_id)
        })
        return data 
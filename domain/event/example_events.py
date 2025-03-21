"""
Example domain events.

This module defines the domain events related to the Example entity.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.event.event import DomainEvent


@dataclass
class ExampleCreatedEvent(DomainEvent):
    """
    Event raised when a new Example is created.
    
    This event contains all the information about the newly created Example.
    """
    example_id: str
    name: str
    description: Optional[str] = None
    
    def __post_init__(self):
        """Initialize the event type after instance creation."""
        self.event_type = "example.created"
        super().__post_init__()


@dataclass
class ExampleUpdatedEvent(DomainEvent):
    """
    Event raised when an Example is updated.
    
    This event contains the ID of the updated Example and the updated fields.
    """
    example_id: str
    name: str
    description: Optional[str] = None
    
    def __post_init__(self):
        """Initialize the event type after instance creation."""
        self.event_type = "example.updated"
        super().__post_init__()


@dataclass
class ExampleDeletedEvent(DomainEvent):
    """
    Event raised when an Example is deleted.
    
    This event contains the ID of the deleted Example.
    """
    example_id: str
    
    def __post_init__(self):
        """Initialize the event type after instance creation."""
        self.event_type = "example.deleted"
        super().__post_init__() 
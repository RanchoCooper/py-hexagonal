"""
Example event handlers module that contains handlers for Example-related events.
"""

import logging
from typing import Any

from domain.event.event import DomainEvent
from domain.event.event_bus import EventHandler
from domain.event.example_events import (
    ExampleCreatedEvent,
    ExampleDeletedEvent,
    ExampleUpdatedEvent,
)


class ExampleCreatedEventHandler(EventHandler):
    """
    Handler for ExampleCreatedEvent.
    """
    
    def __init__(self):
        """Initialize the handler."""
        self._logger = logging.getLogger(__name__)
    
    def handle(self, event: Any) -> None:
        """
        Handle an ExampleCreatedEvent.
        
        Args:
            event (Any): The event to handle.
        """
        if not isinstance(event, ExampleCreatedEvent):
            return
        
        self._logger.info(
            f"Example created: ID={event.example_id}, Name={event.name}"
        )
        
        # Business logic for handling example creation could go here
        # For instance, sending a notification, updating analytics, etc.


class ExampleUpdatedEventHandler(EventHandler):
    """
    Handler for ExampleUpdatedEvent.
    """
    
    def __init__(self):
        """Initialize the handler."""
        self._logger = logging.getLogger(__name__)
    
    def handle(self, event: Any) -> None:
        """
        Handle an ExampleUpdatedEvent.
        
        Args:
            event (Any): The event to handle.
        """
        if not isinstance(event, ExampleUpdatedEvent):
            return
        
        self._logger.info(
            f"Example updated: ID={event.example_id}, Name={event.name}"
        )
        
        # Business logic for handling example update could go here


class ExampleDeletedEventHandler(EventHandler):
    """
    Handler for ExampleDeletedEvent.
    """
    
    def __init__(self):
        """Initialize the handler."""
        self._logger = logging.getLogger(__name__)
    
    def handle(self, event: Any) -> None:
        """
        Handle an ExampleDeletedEvent.
        
        Args:
            event (Any): The event to handle.
        """
        if not isinstance(event, ExampleDeletedEvent):
            return
        
        self._logger.info(
            f"Example deleted: ID={event.example_id}"
        )
        
        # Business logic for handling example deletion could go here 
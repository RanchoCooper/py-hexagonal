"""
In-memory event bus implementation.
"""

import logging
from collections import defaultdict
from typing import Dict, List, Type

from domain.event.event import DomainEvent
from domain.event.event_bus import EventBus, EventHandler


class MemoryEventBus(EventBus):
    """
    An in-memory implementation of the EventBus interface.
    """
    
    def __init__(self):
        """Initialize the event bus."""
        self._handlers: Dict[Type[DomainEvent], List[EventHandler]] = defaultdict(list)
        self._logger = logging.getLogger(__name__)
    
    def publish(self, event: DomainEvent) -> None:
        """
        Publish an event to the event bus.
        
        Args:
            event (DomainEvent): The event to publish.
        """
        event_type = type(event)
        self._logger.debug(f"Publishing event: {event_type.__name__}")
        
        if event_type not in self._handlers:
            self._logger.debug(f"No handlers registered for event type: {event_type.__name__}")
            return
        
        for handler in self._handlers[event_type]:
            try:
                handler.handle(event)
            except Exception as e:
                self._logger.error(f"Error handling event {event_type.__name__}: {str(e)}")
    
    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """
        Subscribe to events of a specific type.
        
        Args:
            event_type (Type[DomainEvent]): The type of event to subscribe to.
            handler (EventHandler): The handler to call when an event of the specified type is published.
        """
        self._logger.debug(f"Subscribing handler {handler.__class__.__name__} to event type: {event_type.__name__}")
        self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """
        Unsubscribe from events of a specific type.
        
        Args:
            event_type (Type[DomainEvent]): The type of event to unsubscribe from.
            handler (EventHandler): The handler to remove.
        """
        if event_type in self._handlers:
            self._logger.debug(f"Unsubscribing handler {handler.__class__.__name__} from event type: {event_type.__name__}")
            self._handlers[event_type] = [h for h in self._handlers[event_type] if h != handler] 
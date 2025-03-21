"""
Event bus module that defines the interface for publishing and subscribing to events.
"""

from abc import ABC, abstractmethod
from typing import Callable, Type

from domain.event.event import DomainEvent


class EventHandler:
    """
    Base event handler class that all event handlers should inherit from.
    """
    
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        """
        Handle an event.
        
        Args:
            event (DomainEvent): The event to handle.
        """
        pass


class EventBus(ABC):
    """
    Event bus interface that defines the methods for publishing and subscribing to events.
    This is a port in the hexagonal architecture terminology.
    """
    
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """
        Publish an event to the event bus.
        
        Args:
            event (DomainEvent): The event to publish.
        """
        pass
    
    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """
        Subscribe to events of a specific type.
        
        Args:
            event_type (Type[DomainEvent]): The type of event to subscribe to.
            handler (EventHandler): The handler to call when an event of the specified type is published.
        """
        pass
    
    @abstractmethod
    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """
        Unsubscribe from events of a specific type.
        
        Args:
            event_type (Type[DomainEvent]): The type of event to unsubscribe from.
            handler (EventHandler): The handler to remove.
        """
        pass 
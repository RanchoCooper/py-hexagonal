"""
Event bus interface.

This module defines the interface for the event bus, which is responsible for
publishing domain events and notifying subscribers.
"""
from abc import ABC, abstractmethod
from typing import Any, Callable, List

from domain.event.event import DomainEvent


class EventHandler(ABC):
    """
    Base class for all event handlers.

    Event handlers are responsible for reacting to domain events.
    """

    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        """
        Handle a domain event.

        Args:
            event: The domain event to handle
        """
        pass


class EventBus(ABC):
    """
    Interface for the event bus.

    The event bus is responsible for publishing domain events and notifying subscribers.
    It follows the publish-subscribe pattern.
    """

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """
        Publish a domain event to all subscribers.

        Args:
            event: The domain event to publish
        """
        pass

    @abstractmethod
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """
        Subscribe to a specific event type.

        Args:
            event_type: The type of event to subscribe to
            handler: The handler to call when the event occurs
        """
        pass

    @abstractmethod
    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """
        Unsubscribe from a specific event type.

        Args:
            event_type: The type of event to unsubscribe from
            handler: The handler to remove
        """
        pass

    @abstractmethod
    def get_handlers(self, event_type: str) -> List[EventHandler]:
        """
        Get all handlers for a specific event type.

        Args:
            event_type: The type of event to get handlers for

        Returns:
            A list of handlers for the given event type
        """
        pass

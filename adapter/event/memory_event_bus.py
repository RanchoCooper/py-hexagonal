"""
In-memory event bus implementation.

This module provides an in-memory implementation of the event bus interface.
"""
import logging
from typing import Dict, List, Set

from domain.event.event import DomainEvent
from domain.event.event_bus import EventBus, EventHandler

logger = logging.getLogger(__name__)


class MemoryEventBus(EventBus):
    """
    In-memory implementation of the event bus.

    This implementation stores event handlers in memory and dispatches
    events synchronously.
    """

    def __init__(self):
        """Initialize the event bus."""
        self._handlers: Dict[str, List[EventHandler]] = {}

    def publish(self, event: DomainEvent) -> None:
        """
        Publish a domain event to all subscribers.

        Args:
            event: The domain event to publish
        """
        event_type = event.event_type
        handlers = self.get_handlers(event_type)

        if not handlers:
            logger.debug(f"No handlers registered for event type: {event_type}")
            return

        logger.debug(
            f"Publishing event {event.event_id} of type {event_type} to {len(handlers)} handlers"
        )

        for handler in handlers:
            try:
                handler.handle(event)
            except Exception as e:
                logger.exception(
                    f"Error handling event {event.event_id} with handler {handler.__class__.__name__}: {e}"
                )

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """
        Subscribe to a specific event type.

        Args:
            event_type: The type of event to subscribe to
            handler: The handler to call when the event occurs
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        # Avoid duplicate handlers
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logger.debug(
                f"Handler {handler.__class__.__name__} subscribed to event type: {event_type}"
            )

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """
        Unsubscribe from a specific event type.

        Args:
            event_type: The type of event to unsubscribe from
            handler: The handler to remove
        """
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            logger.debug(
                f"Handler {handler.__class__.__name__} unsubscribed from event type: {event_type}"
            )

    def get_handlers(self, event_type: str) -> List[EventHandler]:
        """
        Get all handlers for a specific event type.

        Args:
            event_type: The type of event to get handlers for

        Returns:
            A list of handlers for the given event type
        """
        return self._handlers.get(event_type, [])

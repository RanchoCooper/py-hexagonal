"""
Example event handlers.

This module contains event handlers for Example domain events.
"""
import logging
from typing import Any, Dict

from domain.event.event import DomainEvent
from domain.event.event_bus import EventHandler
from domain.event.example_events import (
    ExampleCreatedEvent,
    ExampleDeletedEvent,
    ExampleUpdatedEvent,
)

logger = logging.getLogger(__name__)


class ExampleCreatedEventHandler(EventHandler):
    """Handler for ExampleCreatedEvent."""

    def handle(self, event: DomainEvent) -> None:
        """
        Handle the ExampleCreatedEvent.

        This handler logs information about the created example and could perform
        additional actions such as sending notifications or updating caches.

        Args:
            event: The domain event to handle
        """
        if not isinstance(event, ExampleCreatedEvent):
            logger.warning(
                f"Expected ExampleCreatedEvent but got {type(event).__name__}"
            )
            return

        logger.info(
            f"Example created: id={event.example_id}, name={event.name}",
            extra={
                "event_id": event.event_id,
                "event_type": event.event_type,
                "example_id": event.example_id,
            },
        )

        # Additional application-specific logic could be implemented here
        # For example, sending notifications or updating caches


class ExampleUpdatedEventHandler(EventHandler):
    """Handler for ExampleUpdatedEvent."""

    def handle(self, event: DomainEvent) -> None:
        """
        Handle the ExampleUpdatedEvent.

        This handler logs information about the updated example and could perform
        additional actions such as sending notifications or updating caches.

        Args:
            event: The domain event to handle
        """
        if not isinstance(event, ExampleUpdatedEvent):
            logger.warning(
                f"Expected ExampleUpdatedEvent but got {type(event).__name__}"
            )
            return

        logger.info(
            f"Example updated: id={event.example_id}, name={event.name}",
            extra={
                "event_id": event.event_id,
                "event_type": event.event_type,
                "example_id": event.example_id,
            },
        )

        # Additional application-specific logic could be implemented here
        # For example, updating search indexes or caches


class ExampleDeletedEventHandler(EventHandler):
    """Handler for ExampleDeletedEvent."""

    def handle(self, event: DomainEvent) -> None:
        """
        Handle the ExampleDeletedEvent.

        This handler logs information about the deleted example and could perform
        additional actions such as updating related data or caches.

        Args:
            event: The domain event to handle
        """
        if not isinstance(event, ExampleDeletedEvent):
            logger.warning(
                f"Expected ExampleDeletedEvent but got {type(event).__name__}"
            )
            return

        logger.info(
            f"Example deleted: id={event.example_id}",
            extra={
                "event_id": event.event_id,
                "event_type": event.event_type,
                "example_id": event.example_id,
            },
        )

        # Additional application-specific logic could be implemented here
        # For example, removing the example from caches or search indexes

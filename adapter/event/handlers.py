"""Event Handler Implementation."""
import logging

from application.event.bus import subscribe
from application.event.events import (
    Event,
    TaskCompletedEvent,
    TaskCreatedEvent,
    TaskDeletedEvent,
    TaskUpdatedEvent,
    UserCreatedEvent,
    UserDeletedEvent,
    UserUpdatedEvent,
)

# Setup logging
logger = logging.getLogger(__name__)


@subscribe("user.created")
def handle_user_created(event: UserCreatedEvent) -> None:
    """Handle user creation event."""
    logger.info(f"User created: {event.username} (ID: {event.user_id})")
    # Add business logic here, like sending welcome emails


@subscribe("user.updated")
def handle_user_updated(event: UserUpdatedEvent) -> None:
    """Handle user update event."""
    logger.info(f"User updated: ID {event.user_id}, changes: {event.changes}")
    # Execute operations based on update content


@subscribe("user.deleted")
def handle_user_deleted(event: UserDeletedEvent) -> None:
    """Handle user deletion event."""
    logger.info(f"User deleted: ID {event.user_id}")
    # Perform cleanup operations


@subscribe("task.created")
def handle_task_created(event: TaskCreatedEvent) -> None:
    """Handle task creation event."""
    user_info = f"(User: {event.user_id})" if event.user_id else ""
    logger.info(f"Task created: '{event.title}' {user_info}")
    # Execute other business logic


@subscribe("task.updated")
def handle_task_updated(event: TaskUpdatedEvent) -> None:
    """Handle task update event."""
    user_info = f"(User: {event.user_id})" if event.user_id else ""
    logger.info(f"Task updated: ID {event.task_id} {user_info}, changes: {event.changes}")
    # Execute operations based on update content


@subscribe("task.completed")
def handle_task_completed(event: TaskCompletedEvent) -> None:
    """Handle task completion event."""
    user_info = f"(User: {event.user_id})" if event.user_id else ""
    logger.info(f"Task completed: ID {event.task_id} {user_info}")
    # Execute business logic after task completion, like notifications


@subscribe("task.deleted")
def handle_task_deleted(event: TaskDeletedEvent) -> None:
    """Handle task deletion event."""
    user_info = f"(User: {event.user_id})" if event.user_id else ""
    logger.info(f"Task deleted: ID {event.task_id} {user_info}")
    # Perform cleanup operations


# General event logger
@subscribe("user.created")
@subscribe("user.updated")
@subscribe("user.deleted")
@subscribe("task.created")
@subscribe("task.updated")
@subscribe("task.completed")
@subscribe("task.deleted")
def log_all_events(event: Event) -> None:
    """Log all events to event log."""
    logger.debug(f"Event log: {event.event_type} - {event.to_dict()}")
    # Here you can persist events to a database or other storage

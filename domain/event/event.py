"""
Domain event module that defines the base event structure.
"""

from abc import ABC
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """
    Base domain event class that all domain events should inherit from.
    """
    
    def __init__(self, event_id: Optional[UUID] = None, timestamp: Optional[datetime] = None):
        """
        Initialize a new domain event.
        
        Args:
            event_id (Optional[UUID]): The event ID. Defaults to a generated UUID.
            timestamp (Optional[datetime]): The event timestamp. Defaults to current time.
        """
        self._event_id = event_id or uuid4()
        self._timestamp = timestamp or datetime.utcnow()
    
    @property
    def event_id(self) -> UUID:
        """Get the event ID."""
        return self._event_id
    
    @property
    def timestamp(self) -> datetime:
        """Get the event timestamp."""
        return self._timestamp
    
    @property
    def event_type(self) -> str:
        """Get the event type."""
        return self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary.
        
        Returns:
            Dict[str, Any]: The event as a dictionary.
        """
        return {
            "event_id": str(self._event_id),
            "timestamp": self._timestamp.isoformat(),
            "event_type": self.event_type
        } 
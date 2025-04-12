"""
Domain event base classes.

This module defines the base classes for domain events in the system.
Domain events represent something interesting that happened in the domain.
"""
import uuid
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class DomainEvent(ABC):
    """
    Base class for all domain events.

    Domain events represent something interesting that happened in the domain.
    They are immutable and contain all the information necessary to describe
    the event that happened.
    """

    event_id: str
    event_type: str
    occurred_at: datetime

    def __post_init__(self):
        """Initialize default values after instance creation."""
        if not hasattr(self, "event_id") or not self.event_id:
            self.event_id = str(uuid.uuid4())
        if not hasattr(self, "occurred_at") or not self.occurred_at:
            self.occurred_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary.

        Returns:
            Dictionary representation of the event
        """
        result = {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
        }

        # Add all additional fields from the dataclass
        for key, value in self.__dict__.items():
            if key not in result:
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value

        return result

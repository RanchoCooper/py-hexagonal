"""
Aggregate base module for the domain layer.
"""

from abc import ABC
from uuid import UUID


class Aggregate(ABC):
    """
    Base class for aggregates.
    
    Aggregates are clusters of domain objects that can be treated as a single unit.
    They are the basic unit of consistency, transactions, and distribution.
    """
    
    def __init__(self, aggregate_id: UUID):
        """
        Initialize an aggregate.
        
        Args:
            aggregate_id: The ID of the aggregate
        """
        self._id = aggregate_id
    
    @property
    def id(self) -> UUID:
        """Get the aggregate's ID."""
        return self._id 
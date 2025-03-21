"""
Value object base module for the domain layer.
"""

from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject(ABC):
    """
    Base class for value objects.
    
    Value objects are immutable objects that are defined by their attributes.
    They have no identity and are used to represent concepts in the domain.
    """
    pass 
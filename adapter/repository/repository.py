"""
Repository base module for the repository adapter.
"""

from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')


class Repository(Generic[T], ABC):
    """Base repository implementation."""
    pass 
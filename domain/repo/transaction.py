"""
Transaction interface for the domain layer.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, TypeVar

T = TypeVar('T')


class Transaction(ABC):
    """Transaction interface."""
    
    @abstractmethod
    def commit(self) -> None:
        """Commit the transaction."""
        pass
    
    @abstractmethod
    def rollback(self) -> None:
        """Rollback the transaction."""
        pass
    
    def __enter__(self) -> 'Transaction':
        """Enter the transaction context."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the transaction context."""
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()


class TransactionManager(ABC):
    """Transaction manager interface."""
    
    @abstractmethod
    def begin_transaction(self) -> Transaction:
        """Begin a new transaction."""
        pass
    
    @abstractmethod
    def with_transaction(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute a function within a transaction."""
        pass 
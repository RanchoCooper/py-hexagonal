"""
Transaction implementation for the repository adapter.
"""

from typing import Any, Callable, TypeVar

from domain.repo.transaction import Transaction, TransactionManager

T = TypeVar('T')


class NoopTransaction(Transaction):
    """
    No-operation transaction implementation.
    
    This is a fallback implementation that doesn't actually perform any transaction operations.
    """
    
    def commit(self) -> None:
        """Commit the transaction."""
        pass
    
    def rollback(self) -> None:
        """Rollback the transaction."""
        pass


class NoopTransactionManager(TransactionManager):
    """
    No-operation transaction manager implementation.
    
    This is a fallback implementation that doesn't actually manage transactions.
    """
    
    def begin_transaction(self) -> Transaction:
        """Begin a new transaction."""
        return NoopTransaction()
    
    def with_transaction(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute a function within a transaction."""
        return func(*args, **kwargs) 
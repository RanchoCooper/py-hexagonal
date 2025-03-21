"""
PostgreSQL transaction manager implementation.
"""

from typing import Any, Callable, TypeVar

from sqlalchemy.orm import Session

from adapter.repository.error import PersistenceError
from adapter.repository.postgre.client import (
    PostgreSQLClient,
    PostgreSQLError,
    PostgreSQLTransaction,
)
from domain.repo.transaction import Transaction, TransactionManager

T = TypeVar('T')


class PostgreSQLTransactionManager(TransactionManager):
    """PostgreSQL transaction manager implementation."""
    
    def __init__(self, postgresql_client: PostgreSQLClient):
        """
        Initialize the transaction manager.
        
        Args:
            postgresql_client: The PostgreSQL client
        """
        self.postgresql_client = postgresql_client
    
    def begin_transaction(self) -> Transaction:
        """
        Begin a new transaction.
        
        Returns:
            A new transaction
            
        Raises:
            PostgreSQLError: If the transaction cannot be created
        """
        try:
            session = self.postgresql_client._session_factory()
            return PostgreSQLTransaction(session)
        except Exception as e:
            raise PostgreSQLError(f"Failed to begin transaction: {e}", e)
    
    def with_transaction(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        Execute a function within a transaction.
        
        Args:
            func: The function to execute
            *args: The positional arguments to pass to the function
            **kwargs: The keyword arguments to pass to the function
            
        Returns:
            The result of the function
            
        Raises:
            PostgreSQLError: If the transaction fails
        """
        transaction = self.begin_transaction()
        try:
            with transaction:
                result = func(*args, **kwargs)
                transaction.commit()
                return result
        except Exception as e:
            if isinstance(e, PostgreSQLError):
                raise
            raise PostgreSQLError(f"Transaction failed: {e}", e) 
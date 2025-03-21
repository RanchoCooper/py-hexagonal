"""
MySQL transaction manager implementation.
"""

from typing import Any, Callable, TypeVar

from adapter.repository.error import MySQLError
from adapter.repository.mysql.client import MySQLClient, MySQLTransaction
from domain.repo.transaction import Transaction, TransactionManager

T = TypeVar('T')


class MySQLTransactionManager(TransactionManager):
    """MySQL transaction manager implementation."""
    
    def __init__(self, mysql_client: MySQLClient):
        """
        Initialize the transaction manager.
        
        Args:
            mysql_client: The MySQL client
        """
        self.mysql_client = mysql_client
    
    def begin_transaction(self) -> Transaction:
        """
        Begin a new transaction.
        
        Returns:
            A new transaction
            
        Raises:
            MySQLError: If the transaction cannot be created
        """
        try:
            session = self.mysql_client._session_factory()
            return MySQLTransaction(session)
        except Exception as e:
            raise MySQLError(f"Failed to begin transaction: {e}", e)
    
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
            MySQLError: If the transaction fails
        """
        transaction = self.begin_transaction()
        try:
            with transaction:
                result = func(*args, **kwargs)
                return result
        except Exception as e:
            if isinstance(e, MySQLError):
                raise
            raise MySQLError(f"Transaction failed: {e}", e) 
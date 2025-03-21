"""
Redis transaction manager implementation.
"""

from typing import Any, Callable, TypeVar

from adapter.repository.error import RedisError
from adapter.repository.redis.client import RedisClient, RedisTransaction
from domain.repo.transaction import Transaction, TransactionManager

T = TypeVar('T')


class RedisTransactionManager(TransactionManager):
    """Redis transaction manager implementation."""
    
    def __init__(self, redis_client: RedisClient):
        """
        Initialize the transaction manager.
        
        Args:
            redis_client: The Redis client
        """
        self.redis_client = redis_client
    
    def begin_transaction(self) -> Transaction:
        """
        Begin a new transaction.
        
        Returns:
            A new transaction
            
        Raises:
            RedisError: If the transaction cannot be created
        """
        try:
            return RedisTransaction(self.redis_client)
        except Exception as e:
            raise RedisError(f"Failed to begin transaction: {e}", e)
    
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
            RedisError: If the transaction fails
        """
        transaction = self.begin_transaction()
        try:
            with transaction:
                result = func(*args, **kwargs)
                return result
        except Exception as e:
            if isinstance(e, RedisError):
                raise
            raise RedisError(f"Transaction failed: {e}", e) 
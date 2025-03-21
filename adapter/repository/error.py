"""
Repository error definitions for the adapter layer.
"""

from typing import Any, Optional

from domain.repo.error import (
    DuplicateEntityError,
    EntityNotFoundError,
    PersistenceError,
    RepositoryError,
)


class MySQLError(PersistenceError):
    """Error raised when there's a problem with MySQL."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(f"MySQL error: {message}", cause)


class RedisError(PersistenceError):
    """Error raised when there's a problem with Redis."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(f"Redis error: {message}", cause)


class TransactionError(PersistenceError):
    """Error raised when there's a problem with a transaction."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(f"Transaction error: {message}", cause) 
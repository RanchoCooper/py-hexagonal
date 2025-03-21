"""
Repository error definitions for the domain layer.
"""

from typing import Any, Optional


class RepositoryError(Exception):
    """Base repository error."""
    
    def __init__(self, message: str = "Repository error occurred"):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(RepositoryError):
    """Error raised when an entity is not found."""
    
    def __init__(self, entity_type: str, entity_id: Any):
        self.entity_type = entity_type
        self.entity_id = entity_id
        message = f"{entity_type} with ID {entity_id} not found"
        super().__init__(message)


class DuplicateEntityError(RepositoryError):
    """Error raised when attempting to create a duplicate entity."""
    
    def __init__(self, entity_type: str, field: str, value: Any):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        message = f"{entity_type} with {field}={value} already exists"
        super().__init__(message)


class PersistenceError(RepositoryError):
    """Error raised when there's a problem with persistence layer."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        self.cause = cause
        super().__init__(message) 
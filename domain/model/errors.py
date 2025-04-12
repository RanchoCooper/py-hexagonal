"""
Domain model exceptions.

This module contains domain-specific exceptions that represent business rule violations
or domain constraints. These exceptions are part of the domain language and should be
meaningful to domain experts.
"""
from typing import Optional


class DomainError(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(DomainError):
    """Exception raised when an entity cannot be found."""

    def __init__(self, entity_name: str, entity_id: Optional[str] = None):
        message = f"{entity_name} not found"
        if entity_id:
            message = f"{entity_name} with id '{entity_id}' not found"
        super().__init__(message)


class ValidationError(DomainError):
    """Exception raised when an entity fails validation."""

    pass


class BusinessRuleViolationError(DomainError):
    """Exception raised when a business rule is violated."""

    pass


class ExampleNameAlreadyExistsError(ValidationError):
    """Exception raised when trying to create an example with a name that already exists."""

    def __init__(self, name: str):
        super().__init__(f"Example with name '{name}' already exists")

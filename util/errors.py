"""
Error handling utilities.

This module provides standardized error classes and handling mechanisms for the application.
"""

from typing import Any, Dict, Optional, Type


class AppError(Exception):
    """
    Base application error class.
    All application-specific errors should inherit from this class.
    """
    
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    
    def __init__(self, message: str = None, details: Any = None):
        """
        Initialize a new AppError.
        
        Args:
            message (str, optional): Error message. Defaults to "An unknown error occurred."
            details (Any, optional): Additional error details. Defaults to None.
        """
        self.message = message or "An unknown error occurred"
        self.details = details
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error to a dictionary representation.
        
        Returns:
            Dict[str, Any]: The error as a dictionary.
        """
        result = {
            "error": self.error_code,
            "message": self.message,
        }
        
        if self.details:
            result["details"] = self.details
            
        return result


class ValidationError(AppError):
    """Error raised when input validation fails."""
    
    status_code = 400
    error_code = "VALIDATION_ERROR"


class NotFoundError(AppError):
    """Error raised when a requested resource is not found."""
    
    status_code = 404
    error_code = "NOT_FOUND"
    
    def __init__(self, resource_type: str, resource_id: str):
        """
        Initialize a new NotFoundError.
        
        Args:
            resource_type (str): The type of resource not found.
            resource_id (str): The ID of the resource not found.
        """
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message)


class ConflictError(AppError):
    """Error raised when there is a conflict with the current state of the resource."""
    
    status_code = 409
    error_code = "CONFLICT"


class UnauthorizedError(AppError):
    """Error raised when authentication is required but not provided or invalid."""
    
    status_code = 401
    error_code = "UNAUTHORIZED"


class ForbiddenError(AppError):
    """Error raised when the authenticated user doesn't have permission for the requested operation."""
    
    status_code = 403
    error_code = "FORBIDDEN"


def handle_app_error(error: AppError) -> tuple[Dict[str, Any], int]:
    """
    Handle an AppError and convert it to an HTTP response.
    
    Args:
        error (AppError): The error to handle.
        
    Returns:
        tuple[Dict[str, Any], int]: The error response and HTTP status code.
    """
    return error.to_dict(), error.status_code 
"""Error Handling Module."""
import logging
import traceback
from typing import Any, Dict, Optional

# Setup logging
logger = logging.getLogger(__name__)


class AppError(Exception):
    """Application Base Exception."""

    def __init__(
        self,
        message: str = "Application error occurred",
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the application error.

        Args:
            message: Error message
            code: Error code
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"error": {"code": self.code, "message": self.message, "details": self.details}}

    @classmethod
    def from_exception(cls, exc: Exception) -> "AppError":
        """Create AppError from exception."""
        logger.error(f"Exception caught: {exc}")
        logger.debug(traceback.format_exc())
        if isinstance(exc, AppError):
            return exc
        return cls(message=str(exc))


class NotFoundError(AppError):
    """Resource Not Found Exception."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize not found error.

        Args:
            message: Error message
            code: Error code
            details: Additional error details
        """
        super().__init__(message=message, code=code, status_code=404, details=details)


class ValidationError(AppError):
    """Data Validation Error."""

    def __init__(
        self,
        message: str = "Data validation failed",
        code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize validation error.

        Args:
            message: Error message
            code: Error code
            details: Additional error details
        """
        super().__init__(message=message, code=code, status_code=400, details=details)


class AuthenticationError(AppError):
    """Authentication Error."""

    def __init__(
        self,
        message: str = "Authentication failed",
        code: str = "AUTHENTICATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize authentication error.

        Args:
            message: Error message
            code: Error code
            details: Additional error details
        """
        super().__init__(message=message, code=code, status_code=401, details=details)


class AuthorizationError(AppError):
    """Authorization Error."""

    def __init__(
        self,
        message: str = "No permission to perform operation",
        code: str = "AUTHORIZATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize authorization error.

        Args:
            message: Error message
            code: Error code
            details: Additional error details
        """
        super().__init__(message=message, code=code, status_code=403, details=details)


class DatabaseError(AppError):
    """Database Error."""

    def __init__(
        self,
        message: str = "Database operation failed",
        code: str = "DATABASE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize database error.

        Args:
            message: Error message
            code: Error code
            details: Additional error details
        """
        super().__init__(message=message, code=code, status_code=500, details=details)

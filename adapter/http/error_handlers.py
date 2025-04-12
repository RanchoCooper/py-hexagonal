"""
HTTP error handlers.

This module provides error handlers for the Flask application.
"""
import logging

from flask import Flask, jsonify, request

from domain.model.errors import (
    BusinessRuleViolationError,
    DomainError,
    EntityNotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask):
    """
    Register error handlers with the Flask application.

    Args:
        app: Flask application instance
    """

    @app.errorhandler(EntityNotFoundError)
    def handle_entity_not_found_error(error):
        """Handle EntityNotFoundError, returning a 404 response."""
        logger.info(f"Entity not found: {error.message}")
        return jsonify({"error": "Not Found", "message": error.message}), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle ValidationError, returning a 400 response."""
        logger.info(f"Validation error: {error.message}")
        return jsonify({"error": "Validation Error", "message": error.message}), 400

    @app.errorhandler(BusinessRuleViolationError)
    def handle_business_rule_violation_error(error):
        """Handle BusinessRuleViolationError, returning a 422 response."""
        logger.info(f"Business rule violation: {error.message}")
        return (
            jsonify({"error": "Business Rule Violation", "message": error.message}),
            422,
        )

    @app.errorhandler(DomainError)
    def handle_domain_error(error):
        """Handle other DomainError, returning a 400 response."""
        logger.warning(f"Domain error: {error.message}")
        return jsonify({"error": "Domain Error", "message": error.message}), 400

    @app.errorhandler(Exception)
    def handle_exception(error):
        """
        Handle unhandled exceptions, returning a 500 response.

        This handler logs the exception and returns a generic error message
        to avoid exposing sensitive information.
        """
        logger.exception(f"Unhandled exception: {str(error)}")
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                }
            ),
            500,
        )

    @app.errorhandler(404)
    def handle_not_found(_):
        """Handle 404 Not Found errors for routes that don't exist."""
        logger.info(f"Route not found: {request.path}")
        return (
            jsonify(
                {"error": "Not Found", "message": f"Route '{request.path}' not found"}
            ),
            404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        logger.info(f"Method not allowed: {request.method} {request.path}")
        return (
            jsonify(
                {
                    "error": "Method Not Allowed",
                    "message": f"Method '{request.method}' not allowed for '{request.path}'",
                }
            ),
            405,
        )

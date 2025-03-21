"""
Error handling middleware for HTTP requests.
"""

import logging
import traceback
from typing import Any, Callable, Dict, Type

from flask import Flask, jsonify, request

from util.errors import AppError


def register_error_handlers(app: Flask) -> None:
    """
    Register error handlers for the Flask application.
    
    Args:
        app (Flask): The Flask application.
    """
    logger = logging.getLogger(__name__)
    
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        """Handle application errors."""
        logger.error(f"Application error: {error.message}")
        return jsonify(error.to_dict()), error.status_code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        logger.info(f"Not found: {request.path}")
        return jsonify({
            "error": "NOT_FOUND",
            "message": f"The requested URL {request.path} was not found on the server"
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 errors."""
        logger.info(f"Method not allowed: {request.method} {request.path}")
        return jsonify({
            "error": "METHOD_NOT_ALLOWED",
            "message": f"The method {request.method} is not allowed for the URL {request.path}"
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {str(error)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred"
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unhandled_exception(error: Exception):
        """Handle unhandled exceptions."""
        logger.error(f"Unhandled exception: {str(error)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        }), 500 
"""
HTTP middlewares.

This module provides middlewares for the Flask application.
"""
import logging
import time
from uuid import uuid4

from flask import Flask, g, request

logger = logging.getLogger(__name__)


def register_middlewares(app: Flask):
    """
    Register middlewares with the Flask application.

    Args:
        app: Flask application instance
    """

    @app.before_request
    def before_request():
        """
        Execute before each request.

        This middleware:
        1. Adds a request ID to the request context
        2. Records the start time for request timing
        3. Logs the incoming request
        """
        # Add request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        g.request_id = request_id

        # Record start time
        g.start_time = time.time()

        # Log the request
        logger.info(
            f"Request: {request.method} {request.path}",
            extra={
                "request_id": g.request_id,
                "method": request.method,
                "path": request.path,
                "remote_addr": request.remote_addr,
            },
        )

    @app.after_request
    def after_request(response):
        """
        Execute after each request.

        This middleware:
        1. Adds the request ID to the response headers
        2. Logs the response with timing information
        3. Calculates and logs the request duration

        Args:
            response: Flask response object

        Returns:
            The response object
        """
        # Add request ID to response
        response.headers["X-Request-ID"] = g.get("request_id", "unknown")

        # Calculate duration
        duration_ms = 0
        if hasattr(g, "start_time"):
            duration_ms = int((time.time() - g.start_time) * 1000)
            response.headers["X-Response-Time"] = f"{duration_ms}ms"

        # Log the response
        log_level = logging.INFO
        if 400 <= response.status_code < 500:
            log_level = logging.WARNING
        elif response.status_code >= 500:
            log_level = logging.ERROR

        logger.log(
            log_level,
            f"Response: {response.status_code} - {request.method} {request.path} - {duration_ms}ms",
            extra={
                "request_id": g.get("request_id", "unknown"),
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        return response

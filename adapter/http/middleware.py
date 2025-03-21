"""
HTTP middleware for Flask applications.
"""

import time
import uuid
from functools import wraps
from typing import Any, Callable, Optional

from flask import Flask, Request, g, request, session

from util.logging import clear_request_context, set_request_context


def request_logger_middleware(app: Flask) -> None:
    """
    Register request logging middleware for a Flask application.
    
    Args:
        app (Flask): The Flask application.
    """
    
    @app.before_request
    def before_request() -> None:
        """Setup before each request."""
        # Generate a unique request ID if not already present
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Get trace ID for distributed tracing
        trace_id = request.headers.get("X-Trace-ID")
        
        # Get user ID if authenticated
        user_id = None
        if hasattr(g, "user") and g.user:
            user_id = getattr(g.user, "id", None)
        
        # Get session ID if available
        session_id = session.get("id") if session else None
        
        # Set up request context for logging
        set_request_context(
            request_id=request_id,
            trace_id=trace_id,
            user_id=user_id,
            session_id=session_id
        )
        
        # Store the start time for timing the request
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response: Any) -> Any:
        """Clean up after each request."""
        # Calculate request duration
        if hasattr(g, "start_time"):
            duration = time.time() - g.start_time
            response.headers["X-Response-Time"] = str(int(duration * 1000))  # in ms
        
        # Return the request ID for tracking
        response.headers["X-Request-ID"] = request.headers.get(
            "X-Request-ID", str(uuid.uuid4())
        )
        
        return response
    
    @app.teardown_request
    def teardown_request(exception: Optional[Exception] = None) -> None:
        """Clean up request context."""
        clear_request_context()


def timed_route(f: Callable) -> Callable:
    """
    Decorator to time a route execution.
    
    Args:
        f (Callable): The route function to time.
    
    Returns:
        Callable: The wrapped function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start_time
        
        # Add timing information to the response headers
        if hasattr(result, "headers"):
            result.headers["X-Route-Time"] = str(int(duration * 1000))  # in ms
        
        return result
    
    return decorated_function 
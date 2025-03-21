"""
Structured logging module.

This module provides structured logging capabilities for the application.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

# Thread-local storage for request context
_request_context = {}


class StructuredLogRecord(logging.LogRecord):
    """
    Enhanced LogRecord that includes structured data.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize a new StructuredLogRecord."""
        super().__init__(*args, **kwargs)
        self.request_id = _request_context.get("request_id", str(uuid.uuid4()))
        self.trace_id = _request_context.get("trace_id")
        self.user_id = _request_context.get("user_id")
        self.session_id = _request_context.get("session_id")


class StructuredLogger(logging.Logger):
    """
    Logger that creates StructuredLogRecord instances.
    """
    
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """Create a StructuredLogRecord."""
        return StructuredLogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo)


class JsonFormatter(logging.Formatter):
    """
    JSON formatter for structured logs.
    """
    
    def formatTime(self, record, datefmt=None):
        """Format time in ISO8601 format."""
        return datetime.fromtimestamp(record.created).isoformat()
    
    def format(self, record):
        """Format the record as a JSON object."""
        message = record.getMessage()
        
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": message,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add request context information
        if hasattr(record, "request_id") and record.request_id:
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "trace_id") and record.trace_id:
            log_data["trace_id"] = record.trace_id
        
        if hasattr(record, "user_id") and record.user_id:
            log_data["user_id"] = record.user_id
        
        if hasattr(record, "session_id") and record.session_id:
            log_data["session_id"] = record.session_id
        
        # Include exception info if available
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra attributes
        for key, value in record.__dict__.items():
            if key not in ["args", "asctime", "created", "exc_info", "exc_text",
                          "filename", "funcName", "id", "levelname", "levelno",
                          "lineno", "module", "msecs", "message", "msg", "name",
                          "pathname", "process", "processName", "relativeCreated",
                          "request_id", "session_id", "stack_info", "thread",
                          "threadName", "trace_id", "user_id"] and not key.startswith("_"):
                log_data[key] = value
        
        return json.dumps(log_data)


def set_request_context(request_id: Optional[str] = None, trace_id: Optional[str] = None,
                       user_id: Optional[str] = None, session_id: Optional[str] = None):
    """
    Set the request context for the current thread.
    
    Args:
        request_id (Optional[str]): The request ID.
        trace_id (Optional[str]): The trace ID.
        user_id (Optional[str]): The user ID.
        session_id (Optional[str]): The session ID.
    """
    if request_id:
        _request_context["request_id"] = request_id
    
    if trace_id:
        _request_context["trace_id"] = trace_id
    
    if user_id:
        _request_context["user_id"] = user_id
    
    if session_id:
        _request_context["session_id"] = session_id


def clear_request_context():
    """Clear the request context for the current thread."""
    _request_context.clear()


def configure_logging(level: str = "INFO", use_json: bool = False):
    """
    Configure logging for the application.
    
    Args:
        level (str): The logging level.
        use_json (bool): Whether to use JSON formatting.
    """
    # Register the custom logger class
    logging.setLoggerClass(StructuredLogger)
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create and add the handler
    handler = logging.StreamHandler()
    
    if use_json:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] [%(request_id)s] %(message)s"
        ))
    
    root_logger.addHandler(handler)
    
    # Set the logger for urllib3 and requests to WARNING to reduce noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING) 
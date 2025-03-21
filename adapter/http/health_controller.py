"""
Health check controller for the application.
"""

import logging
from typing import Any, Dict

from flask import Blueprint, jsonify


class HealthController:
    """
    Controller for health check endpoints.
    Provides endpoints for liveness and readiness probes.
    """
    
    def __init__(self):
        """Initialize the Health controller."""
        self._logger = logging.getLogger(__name__)
        self._blueprint = Blueprint('health', __name__, url_prefix='/health')
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register the routes for this controller."""
        self._blueprint.route('/live', methods=['GET'])(self.liveness)
        self._blueprint.route('/ready', methods=['GET'])(self.readiness)
    
    @property
    def blueprint(self) -> Blueprint:
        """Get the Flask blueprint for this controller."""
        return self._blueprint
    
    def liveness(self) -> tuple[Dict[str, Any], int]:
        """
        Liveness probe - checks if the application is running.
        
        Returns:
            tuple[Dict[str, Any], int]: Response data and HTTP status code.
        """
        self._logger.debug("Liveness probe requested")
        return jsonify({"status": "UP"}), 200
    
    def readiness(self) -> tuple[Dict[str, Any], int]:
        """
        Readiness probe - checks if the application is ready to handle requests.
        
        Returns:
            tuple[Dict[str, Any], int]: Response data and HTTP status code.
        """
        self._logger.debug("Readiness probe requested")
        
        checks = {
            "database": self._check_database(),
            "cache": self._check_cache()
        }
        
        status = "UP" if all(c["status"] == "UP" for c in checks.values()) else "DOWN"
        status_code = 200 if status == "UP" else 503
        
        return jsonify({"status": status, "checks": checks}), status_code
    
    def _check_database(self) -> Dict[str, str]:
        """
        Check database connection.
        
        Returns:
            Dict[str, str]: Check result.
        """
        # This would be replaced with actual database connection check in a real app
        try:
            # Simulate database check
            return {"status": "UP"}
        except Exception as e:
            self._logger.error(f"Database health check failed: {str(e)}")
            return {"status": "DOWN", "error": str(e)}
    
    def _check_cache(self) -> Dict[str, str]:
        """
        Check cache connection.
        
        Returns:
            Dict[str, str]: Check result.
        """
        # This would be replaced with actual cache connection check in a real app
        try:
            # Simulate cache check
            return {"status": "UP"}
        except Exception as e:
            self._logger.error(f"Cache health check failed: {str(e)}")
            return {"status": "DOWN", "error": str(e)} 
"""
Flask application factory.

This module provides the Flask application factory and configuration.
"""
import logging

from flask import Flask
from flask_restful import Api

from adapter.http.error_handlers import register_error_handlers
from adapter.http.middlewares import register_middlewares

logger = logging.getLogger(__name__)


def create_app(config=None, register_resources_func=None):
    """
    Create and configure a Flask application instance.
    
    This function follows the Flask application factory pattern.
    
    Args:
        config: Configuration dictionary to apply to the app
        register_resources_func: Function to register resources with the API
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Apply configuration
    app.config.from_mapping(
        DEBUG=False,
        TESTING=False,
        JSON_AS_ASCII=False,  # 允许非ASCII字符直接显示，不转为Unicode转义序列
    )
    
    if config:
        app.config.from_mapping(config)
    
    # Register middlewares
    register_middlewares(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create API
    api = Api(app)
    
    # 配置Flask-RESTful以正确处理中文
    @api.representation('application/json')
    def output_json(data, code, headers=None):
        import json

        from flask import current_app, make_response
        resp = make_response(json.dumps(data, ensure_ascii=False), code)
        resp.headers.extend(headers or {})
        return resp
    
    # Register resources
    if register_resources_func:
        register_resources_func(api)
    
    return app 
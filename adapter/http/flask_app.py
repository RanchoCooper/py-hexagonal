"""
Flask resources registration.

This module provides functions to register API resources with the Flask application.
"""
import logging

from flask_restful import Api

from adapter.http.resources.example_resource import ExampleListResource, ExampleResource

logger = logging.getLogger(__name__)


def register_resources(api, example_app_service=None):
    """
    Register API resources with the Flask-RESTful API.

    Args:
        api: Flask-RESTful API instance
        example_app_service: Example application service instance
    """
    # Example resources
    api.add_resource(
        ExampleListResource,
        "/api/examples",
        resource_class_kwargs={"example_app_service": example_app_service},
    )
    api.add_resource(
        ExampleResource,
        "/api/examples/<string:example_id>",
        resource_class_kwargs={"example_app_service": example_app_service},
    )

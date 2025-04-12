"""
Example HTTP resources.

This module provides REST API resources for the Example entity.
"""
from flask import request
from flask_restful import Resource
from marshmallow import Schema, ValidationError, fields

from application.service.example_app_service import ExampleAppService
from domain.model.errors import EntityNotFoundError, ExampleNameAlreadyExistsError


class ExampleSchema(Schema):
    """
    Marshmallow schema for Example entity serialization/deserialization.

    This schema is used to validate incoming request data and serialize
    outgoing response data.
    """

    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


class ExampleResource(Resource):
    """
    REST resource for individual Example entities.

    This resource handles GET, PUT, and DELETE operations for a single
    Example identified by its ID.
    """

    def __init__(self, **kwargs):
        """
        Initialize the resource with its dependencies.

        Args:
            example_app_service: The application service for Examples
        """
        self.example_app_service = kwargs["example_app_service"]
        self.schema = ExampleSchema()

    def get(self, example_id):
        """
        Get an Example by its ID.

        Args:
            example_id: The ID of the Example to get

        Returns:
            JSON representation of the Example

        Raises:
            EntityNotFoundError: If the Example doesn't exist
        """
        try:
            example = self.example_app_service.get_example(example_id)
            return self.schema.dump(example)
        except EntityNotFoundError as e:
            return {"error": "Not Found", "message": str(e)}, 404

    def put(self, example_id):
        """
        Update an Example by its ID.

        Args:
            example_id: The ID of the Example to update

        Returns:
            JSON representation of the updated Example

        Raises:
            EntityNotFoundError: If the Example doesn't exist
            ValidationError: If the request data is invalid
            ExampleNameAlreadyExistsError: If the new name is already in use
        """
        try:
            # Parse and validate the request data
            json_data = request.get_json() or {}
            errors = self.schema.validate(json_data, partial=True)
            if errors:
                return {"error": "Validation Error", "message": errors}, 400

            # Update the example
            example = self.example_app_service.update_example(
                example_id=example_id,
                name=json_data.get("name"),
                description=json_data.get("description"),
            )

            return self.schema.dump(example)

        except EntityNotFoundError as e:
            return {"error": "Not Found", "message": str(e)}, 404
        except ExampleNameAlreadyExistsError as e:
            return {"error": "Conflict", "message": str(e)}, 409

    def delete(self, example_id):
        """
        Delete an Example by its ID.

        Args:
            example_id: The ID of the Example to delete

        Returns:
            JSON response indicating success or failure
        """
        success = self.example_app_service.delete_example(example_id)

        if success:
            return {"message": "Example deleted successfully"}, 204
        else:
            return {
                "error": "Not Found",
                "message": f"Example with id '{example_id}' not found",
            }, 404


class ExampleListResource(Resource):
    """
    REST resource for collections of Example entities.

    This resource handles GET and POST operations for collections of Examples.
    """

    def __init__(self, **kwargs):
        """
        Initialize the resource with its dependencies.

        Args:
            example_app_service: The application service for Examples
        """
        self.example_app_service = kwargs["example_app_service"]
        self.schema = ExampleSchema()

    def get(self):
        """
        Get all Examples.

        Returns:
            JSON array of all Examples
        """
        examples = self.example_app_service.get_all_examples()
        return self.schema.dump(examples, many=True)

    def post(self):
        """
        Create a new Example.

        Returns:
            JSON representation of the created Example

        Raises:
            ValidationError: If the request data is invalid
            ExampleNameAlreadyExistsError: If the name is already in use
        """
        try:
            # Parse and validate the request data
            json_data = request.get_json() or {}
            errors = self.schema.validate(json_data)
            if errors:
                return {"error": "Validation Error", "message": errors}, 400

            # Create the example
            example = self.example_app_service.create_example(
                name=json_data["name"], description=json_data.get("description")
            )

            return self.schema.dump(example), 201

        except ExampleNameAlreadyExistsError as e:
            return {"error": "Conflict", "message": str(e)}, 409

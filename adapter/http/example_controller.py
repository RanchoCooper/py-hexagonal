"""
Example HTTP controller that handles HTTP requests for Examples.
"""

import logging
import uuid
from typing import Any, Dict, List, Tuple

from flask import Blueprint, jsonify, request

from adapter.dto.example_dto import (
    CreateExampleRequest,
    ExampleDTO,
    UpdateExampleRequest,
)
from application.service.example_service import ExampleApplicationService


class ExampleController:
    """
    Controller for Example-related HTTP endpoints.
    This is an adapter in the hexagonal architecture terminology.
    """
    
    def __init__(self, example_service: ExampleApplicationService):
        """
        Initialize the Example controller.
        
        Args:
            example_service (ExampleApplicationService): The application service for Example entities.
        """
        self._example_service = example_service
        self._logger = logging.getLogger(__name__)
        self._blueprint = Blueprint('examples', __name__, url_prefix='/api/examples')
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register the routes for this controller."""
        self._blueprint.route('/', methods=['POST'])(self.create_example)
        self._blueprint.route('/', methods=['GET'])(self.get_all_examples)
        self._blueprint.route('/active', methods=['GET'])(self.get_active_examples)
        self._blueprint.route('/<example_id>', methods=['GET'])(self.get_example)
        self._blueprint.route('/<example_id>', methods=['PUT'])(self.update_example)
        self._blueprint.route('/<example_id>/activate', methods=['PUT'])(self.activate_example)
        self._blueprint.route('/<example_id>/deactivate', methods=['PUT'])(self.deactivate_example)
        self._blueprint.route('/<example_id>', methods=['DELETE'])(self.delete_example)
    
    @property
    def blueprint(self) -> Blueprint:
        """Get the Flask blueprint for this controller."""
        return self._blueprint
    
    def create_example(self) -> Tuple[Dict[str, Any], int]:
        """
        Create a new Example.
        
        Returns:
            Tuple[Dict[str, Any], int]: The created example as JSON and the HTTP status code.
        """
        try:
            data = request.get_json()
            
            # Validate request data
            if not data or not isinstance(data, dict):
                return {"error": "Invalid request data"}, 400
            
            create_request = CreateExampleRequest(
                name=data.get('name'),
                description=data.get('description', '')
            )
            
            # Validate required fields
            if not create_request.name:
                return {"error": "Name is required"}, 400
            
            # Create the example
            example = self._example_service.create_example(
                name=create_request.name,
                description=create_request.description
            )
            
            # Convert to DTO and return
            example_dto = ExampleDTO.from_entity(example)
            return example_dto.__dict__, 201
        
        except ValueError as e:
            self._logger.error(f"Error creating example: {str(e)}")
            return {"error": str(e)}, 400
        
        except Exception as e:
            self._logger.error(f"Unexpected error creating example: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    
    def get_all_examples(self) -> Tuple[Dict[str, Any], int]:
        """
        Get all examples.
        
        Returns:
            Tuple[Dict[str, Any], int]: The examples as JSON and the HTTP status code.
        """
        try:
            examples = self._example_service.get_all_examples()
            example_dtos = ExampleDTO.from_entity_list(examples)
            return {"examples": [dto.__dict__ for dto in example_dtos]}, 200
        
        except Exception as e:
            self._logger.error(f"Unexpected error getting all examples: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    
    def get_active_examples(self) -> Tuple[Dict[str, Any], int]:
        """
        Get all active examples.
        
        Returns:
            Tuple[Dict[str, Any], int]: The active examples as JSON and the HTTP status code.
        """
        try:
            examples = self._example_service.get_active_examples()
            example_dtos = ExampleDTO.from_entity_list(examples)
            return {"examples": [dto.__dict__ for dto in example_dtos]}, 200
        
        except Exception as e:
            self._logger.error(f"Unexpected error getting active examples: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    
    def get_example(self, example_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Get an example by its ID.
        
        Args:
            example_id (str): The ID of the example to get.
            
        Returns:
            Tuple[Dict[str, Any], int]: The example as JSON and the HTTP status code.
        """
        try:
            # Convert string ID to UUID
            try:
                uuid_id = uuid.UUID(example_id)
            except ValueError:
                return {"error": "Invalid example ID format"}, 400
            
            example = self._example_service.get_example(uuid_id)
            
            if not example:
                return {"error": f"Example with ID {example_id} not found"}, 404
            
            example_dto = ExampleDTO.from_entity(example)
            return example_dto.__dict__, 200
        
        except Exception as e:
            self._logger.error(f"Unexpected error getting example {example_id}: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    
    def update_example(self, example_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Update an example.
        
        Args:
            example_id (str): The ID of the example to update.
            
        Returns:
            Tuple[Dict[str, Any], int]: The updated example as JSON and the HTTP status code.
        """
        try:
            data = request.get_json()
            
            # Validate request data
            if not data or not isinstance(data, dict):
                return {"error": "Invalid request data"}, 400
            
            # Convert string ID to UUID
            try:
                uuid_id = uuid.UUID(example_id)
            except ValueError:
                return {"error": "Invalid example ID format"}, 400
            
            update_request = UpdateExampleRequest(
                name=data.get('name'),
                description=data.get('description')
            )
            
            # Update the example
            example = self._example_service.update_example(
                example_id=uuid_id,
                name=update_request.name,
                description=update_request.description
            )
            
            if not example:
                return {"error": f"Example with ID {example_id} not found"}, 404
            
            # Convert to DTO and return
            example_dto = ExampleDTO.from_entity(example)
            return example_dto.__dict__, 200
        
        except ValueError as e:
            self._logger.error(f"Error updating example {example_id}: {str(e)}")
            return {"error": str(e)}, 400
        
        except Exception as e:
            self._logger.error(f"Unexpected error updating example {example_id}: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    
    def activate_example(self, example_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Activate an example.
        
        Args:
            example_id (str): The ID of the example to activate.
            
        Returns:
            Tuple[Dict[str, Any], int]: The activated example as JSON and the HTTP status code.
        """
        try:
            # Convert string ID to UUID
            try:
                uuid_id = uuid.UUID(example_id)
            except ValueError:
                return {"error": "Invalid example ID format"}, 400
            
            example = self._example_service.activate_example(uuid_id)
            
            if not example:
                return {"error": f"Example with ID {example_id} not found"}, 404
            
            # Convert to DTO and return
            example_dto = ExampleDTO.from_entity(example)
            return example_dto.__dict__, 200
        
        except Exception as e:
            self._logger.error(f"Unexpected error activating example {example_id}: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    
    def deactivate_example(self, example_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Deactivate an example.
        
        Args:
            example_id (str): The ID of the example to deactivate.
            
        Returns:
            Tuple[Dict[str, Any], int]: The deactivated example as JSON and the HTTP status code.
        """
        try:
            # Convert string ID to UUID
            try:
                uuid_id = uuid.UUID(example_id)
            except ValueError:
                return {"error": "Invalid example ID format"}, 400
            
            example = self._example_service.deactivate_example(uuid_id)
            
            if not example:
                return {"error": f"Example with ID {example_id} not found"}, 404
            
            # Convert to DTO and return
            example_dto = ExampleDTO.from_entity(example)
            return example_dto.__dict__, 200
        
        except Exception as e:
            self._logger.error(f"Unexpected error deactivating example {example_id}: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    
    def delete_example(self, example_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Delete an example.
        
        Args:
            example_id (str): The ID of the example to delete.
            
        Returns:
            Tuple[Dict[str, Any], int]: A success message as JSON and the HTTP status code.
        """
        try:
            # Convert string ID to UUID
            try:
                uuid_id = uuid.UUID(example_id)
            except ValueError:
                return {"error": "Invalid example ID format"}, 400
            
            result = self._example_service.delete_example(uuid_id)
            
            if not result:
                return {"error": f"Example with ID {example_id} not found"}, 404
            
            return {"message": f"Example with ID {example_id} deleted successfully"}, 200
        
        except Exception as e:
            self._logger.error(f"Unexpected error deleting example {example_id}: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500 
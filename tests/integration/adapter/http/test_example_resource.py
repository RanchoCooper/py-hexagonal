"""
Integration tests for the Example HTTP resources.
"""
import json
import unittest
from unittest.mock import Mock, patch

from flask import Flask
from flask_restful import Api

from adapter.http.resources.example_resource import ExampleListResource, ExampleResource
from application.service.example_app_service import ExampleAppService
from domain.model.errors import EntityNotFoundError, ExampleNameAlreadyExistsError


class TestExampleResource(unittest.TestCase):
    """Integration tests for the Example HTTP resources."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.config["TESTING"] = True

        self.example_app_service = Mock(spec=ExampleAppService)

        # Create a test client
        self.client = self.app.test_client()

        # Create API and register resources
        api = Api(self.app)

        # Properly inject dependencies
        api.add_resource(
            ExampleListResource,
            "/api/examples",
            resource_class_kwargs={"example_app_service": self.example_app_service},
        )
        api.add_resource(
            ExampleResource,
            "/api/examples/<string:example_id>",
            resource_class_kwargs={"example_app_service": self.example_app_service},
        )

    def tearDown(self):
        """Clean up after each test."""
        pass

    def test_get_example(self):
        """Test GET /api/examples/{id}."""
        # Arrange
        example_id = "123"
        example_dict = {
            "id": example_id,
            "name": "Test Example",
            "description": "This is a test example",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }

        self.example_app_service.get_example.return_value = example_dict

        # Act
        response = self.client.get(f"/api/examples/{example_id}")

        # Assert
        self.example_app_service.get_example.assert_called_once_with(example_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, example_dict)

    def test_get_example_not_found(self):
        """Test GET /api/examples/{id} for a non-existent example."""
        # Arrange
        example_id = "123"

        self.example_app_service.get_example.side_effect = EntityNotFoundError(
            "Example", example_id
        )

        # Act
        response = self.client.get(f"/api/examples/{example_id}")

        # Assert
        self.example_app_service.get_example.assert_called_once_with(example_id)

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)

    def test_update_example(self):
        """Test PUT /api/examples/{id}."""
        # Arrange
        example_id = "123"
        update_data = {
            "name": "Updated Example",
            "description": "This is an updated example",
        }

        updated_example = {
            "id": example_id,
            "name": "Updated Example",
            "description": "This is an updated example",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
        }

        self.example_app_service.update_example.return_value = updated_example

        # Act
        response = self.client.put(
            f"/api/examples/{example_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert
        self.example_app_service.update_example.assert_called_once_with(
            example_id=example_id,
            name=update_data["name"],
            description=update_data["description"],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, updated_example)

    def test_update_example_not_found(self):
        """Test PUT /api/examples/{id} for a non-existent example."""
        # Arrange
        example_id = "123"
        update_data = {"name": "Updated Example"}

        self.example_app_service.update_example.side_effect = EntityNotFoundError(
            "Example", example_id
        )

        # Act
        response = self.client.put(
            f"/api/examples/{example_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)

    def test_update_example_name_exists(self):
        """Test PUT /api/examples/{id} with a name that already exists."""
        # Arrange
        example_id = "123"
        name = "Existing Name"
        update_data = {"name": name}

        self.example_app_service.update_example.side_effect = (
            ExampleNameAlreadyExistsError(name)
        )

        # Act
        response = self.client.put(
            f"/api/examples/{example_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)

    def test_delete_example(self):
        """Test DELETE /api/examples/{id}."""
        # Arrange
        example_id = "123"

        self.example_app_service.delete_example.return_value = True

        # Act
        response = self.client.delete(f"/api/examples/{example_id}")

        # Assert
        self.example_app_service.delete_example.assert_called_once_with(example_id)

        self.assertEqual(response.status_code, 204)

    def test_delete_example_not_found(self):
        """Test DELETE /api/examples/{id} for a non-existent example."""
        # Arrange
        example_id = "123"

        self.example_app_service.delete_example.return_value = False

        # Act
        response = self.client.delete(f"/api/examples/{example_id}")

        # Assert
        self.example_app_service.delete_example.assert_called_once_with(example_id)

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)

    def test_get_all_examples(self):
        """Test GET /api/examples."""
        # Arrange
        examples = [
            {
                "id": "1",
                "name": "Example 1",
                "description": "Description 1",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
            },
            {
                "id": "2",
                "name": "Example 2",
                "description": "Description 2",
                "created_at": "2023-01-02T00:00:00",
                "updated_at": "2023-01-02T00:00:00",
            },
        ]

        self.example_app_service.get_all_examples.return_value = examples

        # Act
        response = self.client.get("/api/examples")

        # Assert
        self.example_app_service.get_all_examples.assert_called_once()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, examples)

    def test_create_example(self):
        """Test POST /api/examples."""
        # Arrange
        new_example_data = {
            "name": "New Example",
            "description": "This is a new example",
        }

        created_example = {
            "id": "123",
            "name": "New Example",
            "description": "This is a new example",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }

        self.example_app_service.create_example.return_value = created_example

        # Act
        response = self.client.post(
            "/api/examples",
            data=json.dumps(new_example_data),
            content_type="application/json",
        )

        # Assert
        self.example_app_service.create_example.assert_called_once_with(
            name=new_example_data["name"], description=new_example_data["description"]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, created_example)

    def test_create_example_name_exists(self):
        """Test POST /api/examples with a name that already exists."""
        # Arrange
        name = "Existing Name"
        new_example_data = {"name": name}

        self.example_app_service.create_example.side_effect = (
            ExampleNameAlreadyExistsError(name)
        )

        # Act
        response = self.client.post(
            "/api/examples",
            data=json.dumps(new_example_data),
            content_type="application/json",
        )

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)

    def test_create_example_invalid_data(self):
        """Test POST /api/examples with invalid data."""
        # Arrange
        invalid_data = {"description": "Missing required name field"}

        # Act
        response = self.client.post(
            "/api/examples",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )

        # Assert
        self.example_app_service.create_example.assert_not_called()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)


if __name__ == "__main__":
    unittest.main()

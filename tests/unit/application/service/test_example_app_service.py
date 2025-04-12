"""
Tests for the Example application service.
"""
import unittest
from unittest.mock import MagicMock, Mock

from application.service.example_app_service import ExampleAppService
from domain.model.errors import EntityNotFoundError, ExampleNameAlreadyExistsError
from domain.model.example import Example
from domain.service.example_service import ExampleService


class TestExampleAppService(unittest.TestCase):
    """Test cases for the Example application service."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.example_service = Mock(spec=ExampleService)
        self.app_service = ExampleAppService(self.example_service)

    def test_create_example(self):
        """Test creating a new example."""
        # Arrange
        name = "Test Example"
        description = "This is a test example"

        example = Example(id="123", name=name, description=description)

        self.example_service.create_example.return_value = example

        # Act
        result = self.app_service.create_example(name, description)

        # Assert
        self.example_service.create_example.assert_called_once_with(name, description)

        self.assertEqual(result["id"], "123")
        self.assertEqual(result["name"], name)
        self.assertEqual(result["description"], description)

    def test_create_example_error(self):
        """Test error handling when creating an example."""
        # Arrange
        name = "Test Example"

        self.example_service.create_example.side_effect = ExampleNameAlreadyExistsError(
            name
        )

        # Act & Assert
        with self.assertRaises(ExampleNameAlreadyExistsError):
            self.app_service.create_example(name)

    def test_update_example(self):
        """Test updating an example."""
        # Arrange
        example_id = "123"
        name = "Test Example"
        description = "This is a test example"

        example = Example(id=example_id, name=name, description=description)

        self.example_service.update_example.return_value = example

        # Act
        result = self.app_service.update_example(example_id, name, description)

        # Assert
        self.example_service.update_example.assert_called_once_with(
            example_id, name, description
        )

        self.assertEqual(result["id"], example_id)
        self.assertEqual(result["name"], name)
        self.assertEqual(result["description"], description)

    def test_update_example_error(self):
        """Test error handling when updating an example."""
        # Arrange
        example_id = "123"

        self.example_service.update_example.side_effect = EntityNotFoundError(
            "Example", example_id
        )

        # Act & Assert
        with self.assertRaises(EntityNotFoundError):
            self.app_service.update_example(example_id, "New Name")

    def test_delete_example(self):
        """Test deleting an example."""
        # Arrange
        example_id = "123"

        self.example_service.delete_example.return_value = True

        # Act
        result = self.app_service.delete_example(example_id)

        # Assert
        self.example_service.delete_example.assert_called_once_with(example_id)

        self.assertTrue(result)

    def test_delete_example_not_found(self):
        """Test deleting a non-existent example."""
        # Arrange
        example_id = "123"

        self.example_service.delete_example.return_value = False

        # Act
        result = self.app_service.delete_example(example_id)

        # Assert
        self.example_service.delete_example.assert_called_once_with(example_id)

        self.assertFalse(result)

    def test_get_example(self):
        """Test getting an example by ID."""
        # Arrange
        example_id = "123"
        name = "Test Example"
        description = "This is a test example"

        example = Example(id=example_id, name=name, description=description)

        self.example_service.get_example.return_value = example

        # Act
        result = self.app_service.get_example(example_id)

        # Assert
        self.example_service.get_example.assert_called_once_with(example_id)

        self.assertEqual(result["id"], example_id)
        self.assertEqual(result["name"], name)
        self.assertEqual(result["description"], description)

    def test_get_example_error(self):
        """Test error handling when getting an example."""
        # Arrange
        example_id = "123"

        self.example_service.get_example.side_effect = EntityNotFoundError(
            "Example", example_id
        )

        # Act & Assert
        with self.assertRaises(EntityNotFoundError):
            self.app_service.get_example(example_id)

    def test_get_all_examples(self):
        """Test getting all examples."""
        # Arrange
        examples = [
            Example(id="1", name="Example 1"),
            Example(id="2", name="Example 2"),
        ]

        self.example_service.get_all_examples.return_value = examples

        # Act
        result = self.app_service.get_all_examples()

        # Assert
        self.example_service.get_all_examples.assert_called_once()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "1")
        self.assertEqual(result[1]["id"], "2")


if __name__ == "__main__":
    unittest.main()

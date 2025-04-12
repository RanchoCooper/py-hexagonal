"""
Tests for the Example domain service.
"""
import unittest
from unittest.mock import MagicMock, Mock

from domain.event.event_bus import EventBus
from domain.model.errors import EntityNotFoundError, ExampleNameAlreadyExistsError
from domain.model.example import Example
from domain.repository.example_repository import ExampleRepository
from domain.service.example_service_impl import ExampleServiceImpl


class TestExampleService(unittest.TestCase):
    """Test cases for the Example domain service."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.repository = Mock(spec=ExampleRepository)
        self.event_bus = Mock(spec=EventBus)
        self.service = ExampleServiceImpl(self.repository, self.event_bus)

    def test_create_example(self):
        """Test creating a new example."""
        # Arrange
        name = "Test Example"
        description = "This is a test example"

        self.repository.exists_by_name.return_value = False
        self.repository.save.return_value = Example(
            id="123", name=name, description=description
        )

        # Act
        result = self.service.create_example(name, description)

        # Assert
        self.repository.exists_by_name.assert_called_once_with(name)
        self.repository.save.assert_called_once()
        self.event_bus.publish.assert_called_once()

        self.assertEqual(result.name, name)
        self.assertEqual(result.description, description)

    def test_create_example_name_exists(self):
        """Test creating an example with a name that already exists."""
        # Arrange
        name = "Test Example"

        self.repository.exists_by_name.return_value = True

        # Act & Assert
        with self.assertRaises(ExampleNameAlreadyExistsError):
            self.service.create_example(name)

    def test_update_example(self):
        """Test updating an example."""
        # Arrange
        example_id = "123"
        name = "Test Example"
        description = "This is a test example"

        existing_example = Example(
            id=example_id, name="Old Name", description="Old Description"
        )

        updated_example = Example(id=example_id, name=name, description=description)

        self.repository.find_by_id.return_value = existing_example
        self.repository.exists_by_name.return_value = False
        self.repository.save.return_value = updated_example

        # Act
        result = self.service.update_example(example_id, name, description)

        # Assert
        self.repository.find_by_id.assert_called_once_with(example_id)
        self.repository.exists_by_name.assert_called_once_with(name)
        self.repository.save.assert_called_once()
        self.event_bus.publish.assert_called_once()

        self.assertEqual(result.id, example_id)
        self.assertEqual(result.name, name)
        self.assertEqual(result.description, description)

    def test_update_example_not_found(self):
        """Test updating a non-existent example."""
        # Arrange
        example_id = "123"

        self.repository.find_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(EntityNotFoundError):
            self.service.update_example(example_id, "New Name")

    def test_update_example_name_exists(self):
        """Test updating an example with a name that already exists."""
        # Arrange
        example_id = "123"
        name = "Existing Name"

        existing_example = Example(
            id=example_id, name="Old Name", description="Old Description"
        )

        self.repository.find_by_id.return_value = existing_example
        self.repository.exists_by_name.return_value = True

        # Act & Assert
        with self.assertRaises(ExampleNameAlreadyExistsError):
            self.service.update_example(example_id, name)

    def test_delete_example(self):
        """Test deleting an example."""
        # Arrange
        example_id = "123"

        example = Example(
            id=example_id, name="Test Example", description="This is a test example"
        )

        self.repository.find_by_id.return_value = example
        self.repository.delete.return_value = True

        # Act
        result = self.service.delete_example(example_id)

        # Assert
        self.repository.find_by_id.assert_called_once_with(example_id)
        self.repository.delete.assert_called_once_with(example_id)
        self.event_bus.publish.assert_called_once()

        self.assertTrue(result)

    def test_delete_example_not_found(self):
        """Test deleting a non-existent example."""
        # Arrange
        example_id = "123"

        self.repository.find_by_id.return_value = None

        # Act
        result = self.service.delete_example(example_id)

        # Assert
        self.repository.find_by_id.assert_called_once_with(example_id)
        self.repository.delete.assert_not_called()
        self.event_bus.publish.assert_not_called()

        self.assertFalse(result)

    def test_get_example(self):
        """Test getting an example by ID."""
        # Arrange
        example_id = "123"

        example = Example(
            id=example_id, name="Test Example", description="This is a test example"
        )

        self.repository.find_by_id.return_value = example

        # Act
        result = self.service.get_example(example_id)

        # Assert
        self.repository.find_by_id.assert_called_once_with(example_id)

        self.assertEqual(result.id, example_id)

    def test_get_example_not_found(self):
        """Test getting a non-existent example."""
        # Arrange
        example_id = "123"

        self.repository.find_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(EntityNotFoundError):
            self.service.get_example(example_id)

    def test_get_all_examples(self):
        """Test getting all examples."""
        # Arrange
        examples = [
            Example(id="1", name="Example 1"),
            Example(id="2", name="Example 2"),
        ]

        self.repository.find_all.return_value = examples

        # Act
        result = self.service.get_all_examples()

        # Assert
        self.repository.find_all.assert_called_once()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")


if __name__ == "__main__":
    unittest.main()

"""
Tests for the Example domain model.
"""
import unittest
from datetime import datetime, timedelta

from domain.model.example import Example


class TestExample(unittest.TestCase):
    """Test cases for the Example domain entity."""

    def test_create(self):
        """Test creating a new example."""
        name = "Test Example"
        description = "This is a test example"

        example = Example.create(name, description)

        self.assertIsNotNone(example.id)
        self.assertEqual(example.name, name)
        self.assertEqual(example.description, description)
        self.assertIsNotNone(example.created_at)
        self.assertIsNotNone(example.updated_at)
        self.assertEqual(example.created_at, example.updated_at)

    def test_update(self):
        """Test updating an example."""
        example = Example.create("Original Name", "Original Description")
        original_created_at = example.created_at

        # Wait a bit to ensure updated_at will be different
        example.update(name="New Name", description="New Description")

        self.assertEqual(example.name, "New Name")
        self.assertEqual(example.description, "New Description")
        self.assertEqual(example.created_at, original_created_at)
        self.assertNotEqual(example.updated_at, original_created_at)

    def test_update_partial(self):
        """Test partial update of an example."""
        example = Example.create("Original Name", "Original Description")

        # Update only name
        example.update(name="New Name")

        self.assertEqual(example.name, "New Name")
        self.assertEqual(example.description, "Original Description")

        # Update only description
        example.update(description="New Description")

        self.assertEqual(example.name, "New Name")
        self.assertEqual(example.description, "New Description")

    def test_to_dict(self):
        """Test converting an example to a dictionary."""
        name = "Test Example"
        description = "This is a test example"
        created_at = datetime.now()
        updated_at = created_at + timedelta(hours=1)

        example = Example(
            id="123",
            name=name,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
        )

        example_dict = example.to_dict()

        self.assertEqual(example_dict["id"], "123")
        self.assertEqual(example_dict["name"], name)
        self.assertEqual(example_dict["description"], description)
        self.assertEqual(example_dict["created_at"], created_at.isoformat())
        self.assertEqual(example_dict["updated_at"], updated_at.isoformat())

    def test_from_dict(self):
        """Test creating an example from a dictionary."""
        name = "Test Example"
        description = "This is a test example"
        created_at = datetime.now()
        updated_at = created_at + timedelta(hours=1)

        example_dict = {
            "id": "123",
            "name": name,
            "description": description,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat(),
        }

        example = Example.from_dict(example_dict)

        self.assertEqual(example.id, "123")
        self.assertEqual(example.name, name)
        self.assertEqual(example.description, description)
        self.assertEqual(example.created_at, created_at)
        self.assertEqual(example.updated_at, updated_at)


if __name__ == "__main__":
    unittest.main()

"""
Unit tests for the Example entity.
"""

import unittest
from uuid import uuid4

from domain.model.example import Example


class TestExampleEntity(unittest.TestCase):
    """Tests for the Example entity."""
    
    def test_create_example(self):
        """Test creating an Example entity."""
        # Arrange
        example_id = uuid4()
        name = "Test Example"
        description = "This is a test example"
        
        # Act
        example = Example(name, description, example_id=example_id)
        
        # Assert
        self.assertEqual(example.id, example_id)
        self.assertEqual(example.name, name)
        self.assertEqual(example.description, description)
        self.assertTrue(example.is_active)
    
    def test_update_example_details(self):
        """Test updating an Example entity's details."""
        # Arrange
        example = Example("Original Name", "Original Description")
        new_name = "Updated Name"
        new_description = "Updated Description"
        
        # Act
        example.update_details(new_name, new_description)
        
        # Assert
        self.assertEqual(example.name, new_name)
        self.assertEqual(example.description, new_description)
    
    def test_activate_example(self):
        """Test activating an Example entity."""
        # Arrange
        example = Example("Test Example", "This is a test example")
        example.deactivate()
        self.assertFalse(example.is_active)
        
        # Act
        example.activate()
        
        # Assert
        self.assertTrue(example.is_active)
    
    def test_deactivate_example(self):
        """Test deactivating an Example entity."""
        # Arrange
        example = Example("Test Example", "This is a test example")
        self.assertTrue(example.is_active)
        
        # Act
        example.deactivate()
        
        # Assert
        self.assertFalse(example.is_active)
    
    def test_equality(self):
        """Test equality comparison between Example entities."""
        # Arrange
        example_id = uuid4()
        example1 = Example("Example 1", "Description 1", example_id=example_id)
        example2 = Example("Example 2", "Description 2", example_id=example_id)
        example3 = Example("Example 3", "Description 3")
        
        # Assert
        self.assertEqual(example1, example2)  # Same ID, different properties
        self.assertNotEqual(example1, example3)  # Different IDs


if __name__ == '__main__':
    unittest.main() 
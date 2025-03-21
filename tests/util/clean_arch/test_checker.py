"""
Tests for the architecture checker.
"""

import os
import tempfile
import unittest
from pathlib import Path

from util.clean_arch.checker import ArchitectureChecker


class TestArchitectureChecker(unittest.TestCase):
    """Tests for the ArchitectureChecker class."""
    
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = self.temp_dir.name
        
        # Create directory structure
        for layer in ["domain", "application", "adapter", "api", "cmd", "config", "util"]:
            os.makedirs(os.path.join(self.project_root, layer), exist_ok=True)
    
    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()
    
    def create_file(self, path, content):
        """Create a file with the given content."""
        full_path = os.path.join(self.project_root, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return full_path
    
    def test_valid_imports(self):
        """Test that valid imports are not reported as violations."""
        # Domain importing domain
        self.create_file(
            "domain/service/service.py",
            "from domain.model.entity import Entity\n"
        )
        
        # Application importing domain and application
        self.create_file(
            "application/service/service.py",
            "from domain.model.entity import Entity\n"
            "from application.event.handler import EventHandler\n"
        )
        
        # Adapter importing domain, application, and adapter
        self.create_file(
            "adapter/http/controller.py",
            "from domain.model.entity import Entity\n"
            "from application.service.service import Service\n"
            "from adapter.repository.repository import Repository\n"
        )
        
        checker = ArchitectureChecker(self.project_root)
        violations = checker.check_project()
        
        self.assertEqual(len(violations), 0, "No violations should be found")
    
    def test_invalid_imports(self):
        """Test that invalid imports are reported as violations."""
        # Domain importing application (not allowed)
        self.create_file(
            "domain/service/invalid.py",
            "from application.service.service import Service\n"
        )
        
        # Application importing adapter (not allowed)
        self.create_file(
            "application/service/invalid.py",
            "from adapter.repository.repository import Repository\n"
        )
        
        checker = ArchitectureChecker(self.project_root)
        violations = checker.check_project()
        
        self.assertEqual(len(violations), 2, "Two violations should be found")
        self.assertIn("domain should not import from application", violations[0])
        self.assertIn("application should not import from adapter", violations[1])
    
    def test_excluded_paths(self):
        """Test that excluded paths are not checked."""
        # Create a file in a path that should be excluded
        self.create_file(
            ".git/config.py",
            "from domain.model.entity import Entity\n"
            "from application.service.service import Service\n"
            "from adapter.repository.repository import Repository\n"
        )
        
        checker = ArchitectureChecker(self.project_root)
        violations = checker.check_project()
        
        self.assertEqual(len(violations), 0, "No violations should be found in excluded paths")
    
    def test_non_project_imports(self):
        """Test that imports from outside the project are not checked."""
        self.create_file(
            "domain/service/valid.py",
            "import os\n"
            "import sys\n"
            "import flask\n"
            "from typing import List\n"
        )
        
        checker = ArchitectureChecker(self.project_root)
        violations = checker.check_project()
        
        self.assertEqual(len(violations), 0, "No violations should be found for external imports")


if __name__ == "__main__":
    unittest.main() 
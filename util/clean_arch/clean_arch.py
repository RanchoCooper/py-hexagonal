"""
Clean Architecture validator.

This module provides functionality to validate Clean Architecture rules in a project.
It checks that dependencies between layers follow the correct hierarchy.
"""
import ast
import logging
import os
from enum import Enum
from typing import Dict, List, Optional, Tuple

# Configure logger
logger = logging.getLogger(__name__)


class Layer(str, Enum):
    """Represents architectural layers in Clean Architecture"""

    # Domain layer
    DOMAIN = "domain"
    # Application layer
    APPLICATION = "application"
    # Infrastructure layer (aka adapters)
    INFRASTRUCTURE = "infrastructure"
    # Interfaces layer (aka api)
    INTERFACES = "interfaces"


# Layer weights for hierarchy validation
LAYER_WEIGHTS = {
    Layer.DOMAIN: 1,
    Layer.APPLICATION: 2,
    Layer.INTERFACES: 3,
    Layer.INFRASTRUCTURE: 4,
}


class LayerMetadata:
    """Contains information about directory module and software layer."""

    def __init__(self, module: str = "", layer: Optional[Layer] = None):
        """
        Initialize layer metadata.

        Args:
            module: The module name
            layer: The architectural layer
        """
        self.module = module
        self.layer = layer


class ValidationError(Exception):
    """Represents an error when Clean Architecture rule is not kept."""

    pass


class Validator:
    """Responsible for Clean Architecture validation."""

    def __init__(self, alias: Dict[str, Layer]):
        """
        Initialize the validator.

        Args:
            alias: Mapping from directory patterns to layers
        """
        self.files_metadata: Dict[str, LayerMetadata] = {}
        self.alias = alias

    def validate(
        self, root: str, ignore_tests: bool = False, ignored_packages: List[str] = None
    ) -> Tuple[int, bool, List[ValidationError]]:
        """
        Validate a path for Clean Architecture rules.

        Args:
            root: Root directory to validate
            ignore_tests: Whether to ignore test files
            ignored_packages: List of packages to ignore

        Returns:
            Tuple containing:
                - Count of processed files
                - Whether validation passed (True) or failed (False)
                - List of validation errors
        """
        if ignored_packages is None:
            ignored_packages = []

        errors = []
        count = 0

        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                path = os.path.join(dirpath, filename)

                # Skip ignored packages
                if any(ignored in path for ignored in ignored_packages):
                    continue

                # Only process Python files
                if not filename.endswith(".py"):
                    continue

                # Skip test files if requested
                if ignore_tests and filename.endswith("_test.py"):
                    continue

                # Skip hidden files and vendor directories
                if "/vendor/" in path or "/." in path:
                    continue

                try:
                    with open(path, "r", encoding="utf-8") as file:
                        tree = ast.parse(file.read(), path)
                except Exception as e:
                    logger.error(f"Error parsing {path}: {e}")
                    continue

                importer_meta = self.file_metadata(path)
                logger.info(f"file: {path}, metadata: {importer_meta.__dict__}")

                count += 1

                if not importer_meta.layer or not importer_meta.module:
                    logger.warning(
                        f"Cannot parse metadata for file {path}, meta: {importer_meta.__dict__}"
                    )
                    continue

                # Process imports in the file
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            import_path = name.name
                            if any(
                                ignored in import_path for ignored in ignored_packages
                            ):
                                continue

                            validation_errors = self.validate_import(
                                import_path, importer_meta, path
                            )
                            errors.extend(validation_errors)

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            import_path = node.module
                            if any(
                                ignored in import_path for ignored in ignored_packages
                            ):
                                continue

                            validation_errors = self.validate_import(
                                import_path, importer_meta, path
                            )
                            errors.extend(validation_errors)

        return count, len(errors) == 0, errors

    def validate_import(
        self, import_path: str, importer_meta: LayerMetadata, path: str
    ) -> List[ValidationError]:
        """
        Validate an import according to Clean Architecture rules.

        Args:
            import_path: Path being imported
            importer_meta: Metadata of the importing file
            path: Path of the importing file

        Returns:
            List of validation errors
        """
        errors = []

        # Get metadata for the import
        import_meta = self.file_metadata(import_path)

        # Skip third-party dependencies
        app_name = os.path.basename(
            os.getcwd()
        )  # Equivalent to config.GlobalConfig.App.Name in Go
        if app_name not in import_path:
            logger.debug(f"[{import_path}] filtered due to third party dependency")
            return []

        # Check layer hierarchy
        if import_meta.layer != importer_meta.layer:
            import_hierarchy = LAYER_WEIGHTS.get(import_meta.layer, 0)
            importer_hierarchy = LAYER_WEIGHTS.get(importer_meta.layer, 0)

            if import_hierarchy > importer_hierarchy:
                err = ValidationError(
                    f"anti-clean [hit-0]: {path} import {import_meta.layer}({import_path}) to {importer_meta.layer}"
                )
                errors.append(err)

        # Log results
        if not errors:
            logger.info(
                f"{path} imported: {import_path} passed ✅ ({import_meta.layer} import {importer_meta.layer})"
            )
        else:
            for err in errors:
                logger.warning(err)

        return errors

    def file_metadata(self, path: str) -> LayerMetadata:
        """
        Get metadata for a file, caching results.

        Args:
            path: Path to the file

        Returns:
            LayerMetadata object
        """
        if path in self.files_metadata:
            return self.files_metadata[path]

        self.files_metadata[path] = parse_layer_metadata(path, self.alias)
        return self.files_metadata[path]


def parse_layer_metadata(path: str, alias: Dict[str, Layer]) -> LayerMetadata:
    """
    Parse metadata from a file path.

    Args:
        path: Path to parse
        alias: Mapping from directory patterns to layers

    Returns:
        LayerMetadata object
    """
    metadata = LayerMetadata()

    for alia, layer in alias.items():
        if alia in path:
            if metadata.module and len(layer) < len(metadata.module):
                continue

            metadata.layer = layer
            metadata.module = alia
            break  # Assume one file belongs to one module

    return metadata

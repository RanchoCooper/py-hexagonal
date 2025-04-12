"""
Clean Architecture checker.

This module provides a tool to check if the project adheres to the
Clean Architecture and Hexagonal Architecture principles.
"""
import ast
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ImportInfo:
    """
    Information about an import statement.

    Attributes:
        module: The module being imported
        name: The name being imported (for 'from ... import ...' statements)
        alias: The alias (for 'import ... as ...' statements)
        lineno: The line number where the import appears
    """

    module: str
    name: Optional[str] = None
    alias: Optional[str] = None
    lineno: int = 0


@dataclass
class ModuleInfo:
    """
    Information about a module.

    Attributes:
        path: The file path of the module
        layer: The architectural layer the module belongs to
        imports: The imports in the module
    """

    path: str
    layer: str
    imports: List[ImportInfo]


class DependencyRule:
    """
    A rule defining allowed dependencies between layers.

    Attributes:
        source_layer: The layer that depends on the target layer
        target_layer: The layer being depended on
    """

    def __init__(self, source_layer: str, target_layer: str):
        """
        Initialize a new dependency rule.

        Args:
            source_layer: The layer that depends on the target layer
            target_layer: The layer being depended on
        """
        self.source_layer = source_layer
        self.target_layer = target_layer

    def allows(self, source_module: ModuleInfo, target_module: ModuleInfo) -> bool:
        """
        Check if the rule allows a dependency.

        Args:
            source_module: The module that depends on the target module
            target_module: The module being depended on

        Returns:
            True if the dependency is allowed, False otherwise
        """
        return (
            source_module.layer == self.source_layer
            and target_module.layer == self.target_layer
        )


class CleanArchChecker:
    """
    Clean Architecture checker.

    This class checks if a project adheres to the Clean Architecture and
    Hexagonal Architecture principles by analyzing imports between modules.
    """

    def __init__(self, project_root: str):
        """
        Initialize the checker.

        Args:
            project_root: The root directory of the project
        """
        self.project_root = Path(project_root)
        self.modules: Dict[str, ModuleInfo] = {}
        self.rules: List[DependencyRule] = []

        # Define allowed dependencies between layers (Clean Architecture rules)
        self._init_rules()

    def _init_rules(self):
        """
        Initialize the dependency rules.

        These rules define the allowed dependencies between layers according
        to the Clean Architecture and Hexagonal Architecture principles.
        """
        # API layer can depend on application layer
        self.rules.append(DependencyRule("api", "application"))

        # Application layer can depend on domain layer
        self.rules.append(DependencyRule("application", "domain"))

        # Adapter layer can depend on domain layer
        self.rules.append(DependencyRule("adapter", "domain"))

        # Adapter layer can depend on application layer
        self.rules.append(DependencyRule("adapter", "application"))

        # Any layer can depend on util layer
        self.rules.append(DependencyRule("domain", "util"))
        self.rules.append(DependencyRule("application", "util"))
        self.rules.append(DependencyRule("adapter", "util"))
        self.rules.append(DependencyRule("api", "util"))

        # Same layer dependencies are allowed
        self.rules.append(DependencyRule("domain", "domain"))
        self.rules.append(DependencyRule("application", "application"))
        self.rules.append(DependencyRule("adapter", "adapter"))
        self.rules.append(DependencyRule("api", "api"))
        self.rules.append(DependencyRule("util", "util"))

    def scan_project(self):
        """
        Scan the project and extract module information.

        This method walks through the project directory, identifies Python
        modules, and extracts import information from them.
        """
        logger.info(f"Scanning project at {self.project_root}...")

        for root, _, files in os.walk(self.project_root):
            # Skip the venv directory
            if "venv" in root or ".venv" in root:
                continue

            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.project_root)

                    # Skip test files
                    if "test" in relative_path.lower():
                        continue

                    # Skip entry files
                    if "entrypoint" in relative_path.lower():
                        continue

                    # Determine the layer based on the file path
                    layer = self._determine_layer(relative_path)

                    # Parse the file and extract imports
                    imports = self._extract_imports(file_path)

                    # Create module info
                    module_name = self._path_to_module_name(relative_path)
                    self.modules[module_name] = ModuleInfo(
                        path=relative_path, layer=layer, imports=imports
                    )

        logger.info(f"Found {len(self.modules)} modules")

    def _determine_layer(self, file_path: str) -> str:
        """
        Determine the architectural layer of a module based on its file path.

        Args:
            file_path: The relative path of the module

        Returns:
            The layer name
        """
        parts = file_path.split(os.sep)

        if parts and parts[0] in ["domain", "application", "adapter", "api", "util"]:
            return parts[0]

        return "unknown"

    def _extract_imports(self, file_path: str) -> List[ImportInfo]:
        """
        Extract import statements from a Python file.

        Args:
            file_path: The path of the file to parse

        Returns:
            A list of import information
        """
        imports = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read(), file_path)

                    for node in ast.walk(tree):
                        # Handle 'import x' and 'import x as y' statements
                        if isinstance(node, ast.Import):
                            for name in node.names:
                                imports.append(
                                    ImportInfo(
                                        module=name.name,
                                        alias=name.asname,
                                        lineno=node.lineno,
                                    )
                                )

                        # Handle 'from x import y' and 'from x import y as z' statements
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                for name in node.names:
                                    imports.append(
                                        ImportInfo(
                                            module=node.module,
                                            name=name.name,
                                            alias=name.asname,
                                            lineno=node.lineno,
                                        )
                                    )
                except SyntaxError as e:
                    logger.error(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")

        return imports

    def _path_to_module_name(self, file_path: str) -> str:
        """
        Convert a file path to a Python module name.

        Args:
            file_path: The relative path of the module

        Returns:
            The module name
        """
        # Remove the '.py' extension
        if file_path.endswith(".py"):
            file_path = file_path[:-3]

        # Replace directory separators with dots
        module_name = file_path.replace(os.sep, ".")

        # Handle __init__.py files
        module_name = re.sub(r".__init__$", "", module_name)

        return module_name

    def _module_name_to_layer(self, module_name: str) -> str:
        """
        Determine the layer of a module based on its name.

        Args:
            module_name: The name of the module

        Returns:
            The layer name
        """
        parts = module_name.split(".")

        if parts and parts[0] in ["domain", "application", "adapter", "api", "util"]:
            return parts[0]

        # Standard library or external modules
        return "external"

    def check_dependencies(self) -> List[Tuple[ModuleInfo, ImportInfo, str]]:
        """
        Check if the dependencies between modules adhere to the rules.

        Returns:
            A list of violations (source module, import, message)
        """
        violations = []

        for module_name, module_info in self.modules.items():
            for import_info in module_info.imports:
                import_module_name = import_info.module

                # Skip standard library and external modules
                if not import_module_name.startswith(
                    ("domain", "application", "adapter", "api", "util")
                ):
                    continue

                # Check if the imported module exists in our map
                target_module_info = self.modules.get(import_module_name)

                if not target_module_info:
                    # Try to infer the layer
                    target_layer = self._module_name_to_layer(import_module_name)
                else:
                    target_layer = target_module_info.layer

                # Check if the dependency is allowed
                allowed = False
                for rule in self.rules:
                    if (
                        rule.source_layer == module_info.layer
                        and rule.target_layer == target_layer
                    ):
                        allowed = True
                        break

                if not allowed:
                    message = f"Dependency from {module_info.layer} to {target_layer} is not allowed"
                    violations.append((module_info, import_info, message))

        return violations

    def print_violations(self, violations: List[Tuple[ModuleInfo, ImportInfo, str]]):
        """
        Print the dependency violations.

        Args:
            violations: A list of violations (source module, import, message)
        """
        if not violations:
            logger.info(
                "No violations found. The project follows the Clean Architecture principles."
            )
            return

        logger.warning(f"Found {len(violations)} Clean Architecture violations:")

        for module_info, import_info, message in violations:
            logger.warning(
                f"- {module_info.path}:{import_info.lineno}: "
                f"Importing '{import_info.module}' - {message}"
            )

    def run(self) -> bool:
        """
        Run the architecture check.

        Returns:
            True if no violations were found, False otherwise
        """
        self.scan_project()
        violations = self.check_dependencies()
        self.print_violations(violations)

        return len(violations) == 0


def main():
    """
    Main entry point for the architecture checker.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Check if the project follows the Clean Architecture principles"
    )
    parser.add_argument("--root", default=".", help="The root directory of the project")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    checker = CleanArchChecker(args.root)
    result = checker.run()

    return 0 if result else 1


if __name__ == "__main__":
    exit(main())

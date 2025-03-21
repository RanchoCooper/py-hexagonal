# Architecture Checker

This tool checks if the project follows hexagonal architecture principles by validating that imports between different layers of the application respect the dependency rules.

## Hexagonal Architecture Rules

In hexagonal architecture, dependencies should flow from outer layers to inner layers:

1. **Domain Layer**: The innermost layer, can only import from itself.
2. **Application Layer**: Can import from the domain layer and itself.
3. **Adapter Layer**: Can import from the domain layer, application layer, and itself.
4. **API Layer**: Can import from the domain layer, application layer, and itself.
5. **Command Layer**: Can import from any layer.

The following dependencies are allowed:

- `domain` → `domain`
- `application` → `domain`, `application`
- `adapter` → `domain`, `application`, `adapter`
- `api` → `domain`, `application`, `api`
- `cmd` → `domain`, `application`, `adapter`, `api`, `cmd`, `config`, `util`
- `config` → `config`
- `util` → `util`

## Usage

You can run the architecture checker in several ways:

### As a standalone script

```bash
python util/check_arch.py
```

### As a Python module

```bash
python -m util.clean_arch
```

### From Python code

```python
from util.clean_arch import ArchitectureChecker

checker = ArchitectureChecker()
violations = checker.check_project()
checker.print_violations()
```

## Output

The tool will output any architecture violations it finds, including:

- The file where the violation occurred
- The source layer that has an invalid import
- The target layer that was imported incorrectly
- The specific import statement that caused the violation

Example output:

```
Architecture violation in adapter/http/example_controller.py:
  adapter should not import from cmd
  Import: cmd.server.app
```

If no violations are found, the tool will print:

```
No architecture violations found.
```

## Exit Code

The tool will exit with code 0 if no violations are found, and with code 1 if any violations are found. This makes it suitable for use in CI/CD pipelines. 
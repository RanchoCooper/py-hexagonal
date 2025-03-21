# py-hexagonal

Python framework based on Hexagonal Architecture.

## Architecture Features

- **Hexagonal Architecture**: Isolates the application core from external systems
- **Dependency Injection**: Uses dependency-injector for decoupling
- **Event-Driven**: Event bus based on PyDispatcher
- **Factory Pattern**: Factory classes for object creation
- **Interfaces and Abstractions**: Uses ABC module to define interfaces
- **Middleware Support**: Provides Flask middleware mechanism
- **Unified Error Handling**: Global exception handling
- **Configuration Management**: Configuration based on python-dotenv

## Directory Structure

- **adapter**: Adapter layer, connects the outside world to the application core
- **api**: API definitions and handlers
- **application**: Application layer, use case implementations
- **domain**: Domain layer, core business logic
- **config**: Configuration
- **util**: Utility classes

## Installation

```bash
pip install -r requirements.txt
```

Or using Makefile:

```bash
make install
```

## Running

```bash
python main.py
```

Or using Makefile:

```bash
make run
```

## Testing

```bash
pytest
```

Or using Makefile:

```bash
make test
```

## Code Quality Tools

This project integrates various code quality tools:

- **Flake8**: Code style checking
- **Black**: Code formatting
- **isort**: Import statement sorting
- **mypy**: Static type checking
- **pylint**: Code quality analysis

### Usage

Check code:

```bash
make lint
```

Format code:

```bash
make format
```

### Pre-commit Hooks

This project uses pre-commit to manage Git pre-commit hooks, ensuring code quality before commits:

```bash
# Install pre-commit
pip install pre-commit

# Install pre-commit hooks
pre-commit install
```

## Cleanup

Delete temporary files and caches:

```bash
make clean
```

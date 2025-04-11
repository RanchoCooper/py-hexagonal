# Python Hexagonal Architecture

![CI Status](https://github.com/RanchoCooper/py-hexagonal/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/RanchoCooper/py-hexagonal/branch/main/graph/badge.svg)](https://codecov.io/gh/RanchoCooper/py-hexagonal)

A Python application example based on hexagonal architecture (ports and adapters architecture). This project demonstrates how to separate business logic from technical implementation details to create maintainable, testable, and flexible applications.

## Features

- **Hexagonal Architecture**: Core business logic independent of external dependencies
- **Domain-Driven Design**: Code organized around business domain models
- **SOLID Principles**: Following Single Responsibility, Open-Closed principles and other software design principles
- **Dependency Injection**: Using `dependency-injector` for loose coupling
- **Multi-database Support**: Supporting MySQL and PostgreSQL, with flexible selection by domain service
- **Event-Driven**: Using event bus for component communication

## System Requirements

- Python 3.9+
- MySQL or PostgreSQL
- Redis

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/RanchoCooper/py-hexagonal.git
cd py-hexagonal
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Configuration:

```bash
cp config/config.yaml.example config/config.yaml
# Edit the config.yaml file to configure database connections, etc.
```

4. Run the application:

```bash
PYTHONPATH=. python entry/main.py
```

## Architecture Overview

The project is organized based on hexagonal architecture (also known as ports and adapters architecture), mainly divided into the following parts:

### Domain Layer

Contains business logic and entity models, the core of the application.

- `/domain/model/` - Business entities
- `/domain/service/` - Business service interfaces and implementations
- `/domain/repository/` - Repository interfaces
- `/domain/event/` - Domain events

### Application Layer

Coordinates domain objects to complete use cases, does not contain business rules.

- `/application/service/` - Application services
- `/application/event/` - Event handlers

### Adapter Layer

Connects the external world with the core application, divided into driving (API) and driven (database) adapters.

- `/adapter/http/` - HTTP API interfaces
- `/adapter/repository/` - Database implementations
- `/adapter/cache/` - Cache implementations
- `/adapter/event/` - Event bus implementations
- `/adapter/di/` - Dependency injection container

### Infrastructure

Provides technical support, such as logging, configuration, etc.

- `/config/` - Configuration files and loaders

## Database Adapters

The project supports multiple database backends, and different domain services can choose different databases:

```yaml
db:
  # Default database connection, options: 'mysql' or 'postgresql'
  default: mysql
  
  # Specify databases for different domain services
  examples_db: mysql  # Example service uses MySQL
  orders_db: postgresql  # Order service uses PostgreSQL
```

## Testing

Run tests:

```bash
PYTHONPATH=. pytest
```

## Contributing

Contributions are welcome! Please read the contribution guidelines first.

## License

MIT 
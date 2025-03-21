.PHONY: clean check-arch test lint format all

# Python command
PYTHON = python3

# Project variables
PROJECT_NAME = py-hexagonal

# Clean up generated files and caches
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	find . -name ".coverage" -delete
	find . -name "htmlcov" -type d -exec rm -rf {} +
	find . -name ".DS_Store" -delete

# Check architecture violations
check-arch:
	$(PYTHON) util/check_arch.py

# Run tests
test:
	$(PYTHON) -m pytest tests

# Run code linting
lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy .

# Format code
format:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

# Run all checks
all: format lint test check-arch

# Default target
default: all 
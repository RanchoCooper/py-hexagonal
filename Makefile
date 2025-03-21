.PHONY: help clean lint format test run install

# Default target
help:
	@echo "Available commands:"
	@echo "  make install           Install all dependencies"
	@echo "  make lint              Run all code checking tools"
	@echo "  make format            Format code"
	@echo "  make test              Run tests"
	@echo "  make run               Run application"
	@echo "  make clean             Clean temporary files"

# Install dependencies
install:
	pip install -r requirements.txt

# Code checking
lint:
	@echo "Running flake8..."
	flake8 .
	@echo "Running pylint..."
	pylint --rcfile=.pylintrc adapter application domain config util
	@echo "Running mypy..."
	mypy adapter application domain config util
	@echo "Checking import sorting..."
	isort --check --diff .

# Format code
format:
	@echo "Running black..."
	black .
	@echo "Reordering imports..."
	isort .

# Run tests
test:
	pytest -v tests/

# Run application
run:
	python main.py

# Clean temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

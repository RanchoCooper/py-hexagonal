"""
Clean Architecture validator package.

This package provides tools to validate that a project adheres to
Clean Architecture principles by analyzing dependencies between layers.
"""

from .clean_arch import (
    Layer,
    LayerMetadata,
    ValidationError,
    Validator,
    parse_layer_metadata,
)

__all__ = [
    "Layer",
    "LayerMetadata",
    "ValidationError",
    "Validator",
    "parse_layer_metadata",
]

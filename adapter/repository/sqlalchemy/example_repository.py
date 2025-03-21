"""
SQLAlchemy-based Example repository implementation.

This module provides a SQLAlchemy-based implementation of the Example repository.
"""
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from adapter.repository.sqlalchemy.base_repository import BaseSQLAlchemyRepository
from adapter.repository.sqlalchemy.models import ExampleModel
from domain.model.example import Example
from domain.repository.example_repository import ExampleRepository


class SQLAlchemyExampleRepository(BaseSQLAlchemyRepository, ExampleRepository):
    """
    SQLAlchemy-based implementation of the Example repository.
    
    This repository uses SQLAlchemy to persist Example entities to a
    relational database.
    """
    
    def __init__(self, db_name=None):
        """
        Initialize the repository.
        
        Args:
            db_name: 要使用的数据库名称，为None则使用默认数据库
        """
        super().__init__(db_name)
    
    def save(self, example: Example) -> Example:
        """
        Save an example to the repository.
        
        Args:
            example: The example entity to save
            
        Returns:
            The saved example with any updates
        """
        try:
            # Check if the example already exists
            existing_model = self._session.query(ExampleModel).filter_by(id=example.id).first()
            
            if existing_model:
                # Update the existing model
                existing_model.name = example.name
                existing_model.description = example.description
                existing_model.updated_at = example.updated_at
            else:
                # Create a new model
                model = ExampleModel(
                    id=example.id,
                    name=example.name,
                    description=example.description,
                    created_at=example.created_at,
                    updated_at=example.updated_at
                )
                self._session.add(model)
            
            self._commit()
            return example
        except SQLAlchemyError as e:
            self._rollback()
            raise e
    
    def find_by_id(self, example_id: str) -> Optional[Example]:
        """
        Find an example by its ID.
        
        Args:
            example_id: The ID of the example to find
            
        Returns:
            The found example entity or None if not found
        """
        model = self._session.query(ExampleModel).filter_by(id=example_id).first()
        return self._to_entity(model) if model else None
    
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name: The name of the example to find
            
        Returns:
            The found example entity or None if not found
        """
        model = self._session.query(ExampleModel).filter_by(name=name).first()
        return self._to_entity(model) if model else None
    
    def find_all(self) -> List[Example]:
        """
        Find all examples in the repository.
        
        Returns:
            A list of all example entities
        """
        models = self._session.query(ExampleModel).all()
        return [self._to_entity(model) for model in models]
    
    def delete(self, example_id: str) -> bool:
        """
        Delete an example from the repository.
        
        Args:
            example_id: The ID of the example to delete
            
        Returns:
            True if the example was deleted, False otherwise
        """
        try:
            model = self._session.query(ExampleModel).filter_by(id=example_id).first()
            if not model:
                return False
            
            self._session.delete(model)
            self._commit()
            return True
        except SQLAlchemyError as e:
            self._rollback()
            raise e
    
    def exists_by_name(self, name: str) -> bool:
        """
        Check if an example with the given name exists.
        
        Args:
            name: The name to check
            
        Returns:
            True if an example with the given name exists, False otherwise
        """
        return self._session.query(ExampleModel).filter_by(name=name).first() is not None
    
    def _to_entity(self, model: ExampleModel) -> Example:
        """
        Convert a database model to a domain entity.
        
        Args:
            model: The database model to convert
            
        Returns:
            The corresponding domain entity
        """
        return Example(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 
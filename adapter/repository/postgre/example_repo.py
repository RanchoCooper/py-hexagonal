"""
PostgreSQL example repository implementation.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from adapter.repository.error import (
    DuplicateEntityError,
    EntityNotFoundError,
    PostgreSQLError,
)
from adapter.repository.postgre.client import PostgreSQLClient
from adapter.repository.postgre.entity.example import ExampleEntity
from domain.model.example import Example
from domain.repo.example import ExampleRepository


class PostgreSQLExampleRepository(ExampleRepository):
    """PostgreSQL implementation of the example repository."""
    
    def __init__(self, postgresql_client: PostgreSQLClient):
        """
        Initialize the repository.
        
        Args:
            postgresql_client: The PostgreSQL client
        """
        self.postgresql_client = postgresql_client
    
    def find_by_id(self, example_id: UUID) -> Optional[Example]:
        """
        Find an example by its ID.
        
        Args:
            example_id: The ID of the example
            
        Returns:
            The example if found, None otherwise
            
        Raises:
            PostgreSQLError: If there's a problem with the database
        """
        try:
            with self.postgresql_client.session() as session:
                entity = session.query(ExampleEntity).filter(ExampleEntity.id == example_id).first()
                
                if entity is None:
                    return None
                    
                return entity.to_domain()
        except Exception as e:
            raise PostgreSQLError(f"Failed to find example by ID: {e}", e)
    
    def find_all(self) -> List[Example]:
        """
        Find all examples.
        
        Returns:
            A list of all examples
            
        Raises:
            PostgreSQLError: If there's a problem with the database
        """
        try:
            with self.postgresql_client.session() as session:
                entities = session.query(ExampleEntity).all()
                return [entity.to_domain() for entity in entities]
        except Exception as e:
            raise PostgreSQLError(f"Failed to find all examples: {e}", e)
    
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name: The name of the example
            
        Returns:
            The example if found, None otherwise
            
        Raises:
            PostgreSQLError: If there's a problem with the database
        """
        try:
            with self.postgresql_client.session() as session:
                entity = session.query(ExampleEntity).filter(ExampleEntity.name == name).first()
                
                if entity is None:
                    return None
                    
                return entity.to_domain()
        except Exception as e:
            raise PostgreSQLError(f"Failed to find example by name: {e}", e)
    
    def save(self, example: Example) -> Example:
        """
        Save an example.
        
        Args:
            example: The example to save
            
        Returns:
            The saved example
            
        Raises:
            DuplicateEntityError: If an example with the same name already exists
            PostgreSQLError: If there's a problem with the database
        """
        try:
            with self.postgresql_client.session() as session:
                # Check if the example already exists
                existing = session.query(ExampleEntity).filter(ExampleEntity.id == example.id).first()
                
                if existing:
                    # Update the existing entity
                    existing.name = example.name
                    existing.description = example.description
                    existing.is_active = example.is_active
                    existing.updated_at = example.updated_at
                else:
                    # Create a new entity
                    entity = ExampleEntity.from_domain(example)
                    session.add(entity)
                    
                try:
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    raise DuplicateEntityError("Example", "name", example.name)
                    
                return example
        except DuplicateEntityError:
            raise
        except Exception as e:
            raise PostgreSQLError(f"Failed to save example: {e}", e)
    
    def delete(self, example_id: UUID) -> None:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example
            
        Raises:
            EntityNotFoundError: If the example is not found
            PostgreSQLError: If there's a problem with the database
        """
        try:
            with self.postgresql_client.session() as session:
                deleted = session.query(ExampleEntity).filter(ExampleEntity.id == example_id).delete()
                session.commit()
                
                if deleted == 0:
                    raise EntityNotFoundError("Example", example_id)
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise PostgreSQLError(f"Failed to delete example: {e}", e) 
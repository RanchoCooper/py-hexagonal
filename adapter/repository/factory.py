"""
Repository factory for the adapter layer.
"""

from abc import ABC, abstractmethod

from domain.repo.example import ExampleRepository
from domain.repo.transaction import TransactionManager


class RepositoryFactory(ABC):
    """Repository factory interface."""
    
    @abstractmethod
    def create_example_repository(self) -> ExampleRepository:
        """
        Create an example repository.
        
        Returns:
            An implementation of the ExampleRepository interface.
        """
        pass
    
    @abstractmethod
    def create_transaction_manager(self) -> TransactionManager:
        """
        Create a transaction manager.
        
        Returns:
            An implementation of the TransactionManager interface.
        """
        pass

from adapter.repository.postgre.client import PostgreSQLClient
from adapter.repository.postgre.example_repo import PostgreSQLExampleRepository
from adapter.repository.postgre.transaction_manager import PostgreSQLTransactionManager


class PostgreSQLRepositoryFactory(RepositoryFactory):
    """PostgreSQL repository factory implementation."""

    def __init__(self, connection_string: str):
        """
        Initialize the factory.
        
        Args:
            connection_string: The PostgreSQL connection string
        """
        self.postgresql_client = PostgreSQLClient(connection_string)
    
    def create_example_repository(self) -> ExampleRepository:
        """
        Create a PostgreSQL example repository.
        
        Returns:
            A PostgreSQL implementation of the ExampleRepository interface
        """
        return PostgreSQLExampleRepository(self.postgresql_client)
    
    def create_transaction_manager(self) -> TransactionManager:
        """
        Create a PostgreSQL transaction manager.
        
        Returns:
            A PostgreSQL implementation of the TransactionManager interface
        """
        return PostgreSQLTransactionManager(self.postgresql_client) 
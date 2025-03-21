"""
PostgreSQL providers module for dependency injection.
"""

from typing import Any, Callable, Dict

from adapter.repository.postgre.client import PostgreSQLClient
from adapter.repository.postgre.example_repo import PostgreSQLExampleRepository
from adapter.repository.postgre.transaction_manager import PostgreSQLTransactionManager


class PostgreSQLClientProvider:
    """Provider for PostgreSQL client."""
    
    def __init__(self, connection_string: str):
        """
        Initialize the provider.
        
        Args:
            connection_string: The PostgreSQL connection string
        """
        self.connection_string = connection_string
    
    def __call__(self) -> PostgreSQLClient:
        """
        Provide a PostgreSQL client.
        
        Returns:
            A PostgreSQL client
        """
        return PostgreSQLClient(self.connection_string)


class PostgreSQLExampleRepositoryProvider:
    """Provider for PostgreSQL example repository."""
    
    def __init__(self, postgresql_client_provider: Callable[[], PostgreSQLClient]):
        """
        Initialize the provider.
        
        Args:
            postgresql_client_provider: A provider for a PostgreSQL client
        """
        self.postgresql_client_provider = postgresql_client_provider
    
    def __call__(self) -> PostgreSQLExampleRepository:
        """
        Provide a PostgreSQL example repository.
        
        Returns:
            A PostgreSQL example repository
        """
        return PostgreSQLExampleRepository(self.postgresql_client_provider())


class PostgreSQLTransactionManagerProvider:
    """Provider for PostgreSQL transaction manager."""
    
    def __init__(self, postgresql_client_provider: Callable[[], PostgreSQLClient]):
        """
        Initialize the provider.
        
        Args:
            postgresql_client_provider: A provider for a PostgreSQL client
        """
        self.postgresql_client_provider = postgresql_client_provider
    
    def __call__(self) -> PostgreSQLTransactionManager:
        """
        Provide a PostgreSQL transaction manager.
        
        Returns:
            A PostgreSQL transaction manager
        """
        return PostgreSQLTransactionManager(self.postgresql_client_provider()) 
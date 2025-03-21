"""
Transaction factory interface for the domain layer.
"""

from abc import ABC, abstractmethod

from domain.repo.transaction import TransactionManager


class TransactionFactory(ABC):
    """Transaction factory interface."""
    
    @abstractmethod
    def create_transaction_manager(self) -> TransactionManager:
        """
        Create a transaction manager.
        
        Returns:
            TransactionManager: A transaction manager
        """
        pass 
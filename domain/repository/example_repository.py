"""
Example repository interface module that defines the repository for Example entities.
"""

from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.model.example import Example
from domain.repository.repository import Repository


class ExampleRepository(Repository[Example]):
    """
    Repository interface for Example entities.
    This is a port in the hexagonal architecture terminology.
    """
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name (str): The name to search for.
            
        Returns:
            Optional[Example]: The found example, or None if not found.
        """
        pass
    
    @abstractmethod
    def find_active(self) -> List[Example]:
        """
        Find all active examples.
        
        Returns:
            List[Example]: A list of all active examples.
        """
        pass 
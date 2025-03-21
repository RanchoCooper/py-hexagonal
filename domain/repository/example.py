"""Example Repository Interfaces."""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model.example import Task, User


class UserRepository(ABC):
    """User Repository Interface."""

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Get all users."""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Save user."""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Delete user."""
        pass


class TaskRepository(ABC):
    """Task Repository Interface."""

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        pass

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[Task]:
        """Get all tasks."""
        pass

    @abstractmethod
    def list_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Task]:
        """Get all tasks for a user."""
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        """Save task."""
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Delete task."""
        pass

    @abstractmethod
    def count_by_user(self, user_id: str, is_completed: Optional[bool] = None) -> int:
        """Count user tasks."""
        pass

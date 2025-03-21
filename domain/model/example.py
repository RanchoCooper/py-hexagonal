"""Example Domain Model."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class BaseEntity:
    """Base Entity."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class User(BaseEntity):
    """User Entity."""

    username: str
    email: str
    password_hash: str
    full_name: Optional[str] = None
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = super().to_dict()
        data.update(
            {
                "username": self.username,
                "email": self.email,
                "full_name": self.full_name,
                "is_active": self.is_active,
            }
        )
        return data


@dataclass
class Task(BaseEntity):
    """Task Entity."""

    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    user_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = super().to_dict()
        data.update(
            {
                "title": self.title,
                "description": self.description,
                "is_completed": self.is_completed,
                "user_id": self.user_id,
            }
        )
        if self.due_date:
            data["due_date"] = self.due_date.isoformat()
        return data

    def complete(self) -> None:
        """Complete task."""
        self.is_completed = True
        self.updated_at = datetime.now()

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
    ) -> None:
        """Update task information."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        self.updated_at = datetime.now()

"""Example Use Case Module."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

# Use case input/output data structures


@dataclass
class CreateUserInput:
    """Create User Input."""

    username: str
    email: str
    password: str
    full_name: Optional[str] = None


@dataclass
class UserOutput:
    """User Output."""

    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime


@dataclass
class UpdateUserInput:
    """Update User Input."""

    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class CreateTaskInput:
    """Create Task Input."""

    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    user_id: Optional[str] = None


@dataclass
class TaskOutput:
    """Task Output."""

    id: str
    title: str
    description: Optional[str]
    is_completed: bool
    due_date: Optional[datetime]
    user_id: Optional[str]
    created_at: datetime


@dataclass
class UpdateTaskInput:
    """Update Task Input."""

    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

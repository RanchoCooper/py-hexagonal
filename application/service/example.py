"""Example Service Implementation."""
import hashlib
import logging
from datetime import datetime
from typing import List

from application.di.container import inject
from application.event.bus import publish
from application.event.events import (
    TaskCompletedEvent,
    TaskCreatedEvent,
    TaskDeletedEvent,
    TaskUpdatedEvent,
    UserCreatedEvent,
    UserDeletedEvent,
    UserUpdatedEvent,
)
from application.usecase.base import UseCase
from application.usecase.example import (
    CreateTaskInput,
    CreateUserInput,
    TaskOutput,
    UpdateTaskInput,
    UpdateUserInput,
    UserOutput,
)
from domain.model.example import Task, User
from domain.repository.example import TaskRepository, UserRepository
from util.errors import NotFoundError, ValidationError
from util.transaction import transactional

# Setup logging
logger = logging.getLogger(__name__)


class CreateUserUseCase(UseCase[CreateUserInput, UserOutput]):
    """Create User Use Case."""

    @inject("user_repository")
    @transactional
    def execute(
        self, input_data: CreateUserInput, user_repository: UserRepository = None
    ) -> UserOutput:
        """Execute create user use case."""
        # Check if username and email already exist
        if user_repository.get_by_username(input_data.username):
            raise ValidationError(message=f"Username '{input_data.username}' already exists")

        if user_repository.get_by_email(input_data.email):
            raise ValidationError(message=f"Email '{input_data.email}' already exists")

        # Password encryption
        password_hash = hashlib.sha256(input_data.password.encode()).hexdigest()

        # Create user entity
        user = User(
            username=input_data.username,
            email=input_data.email,
            password_hash=password_hash,
            full_name=input_data.full_name,
        )

        # Save user
        saved_user = user_repository.save(user)

        # Publish event
        publish(
            UserCreatedEvent(
                user_id=saved_user.id, username=saved_user.username, email=saved_user.email
            )
        )

        # Return output
        return UserOutput(
            id=saved_user.id,
            username=saved_user.username,
            email=saved_user.email,
            full_name=saved_user.full_name,
            is_active=saved_user.is_active,
            created_at=saved_user.created_at,
        )


class GetUserUseCase(UseCase[str, UserOutput]):
    """Get User Use Case."""

    @inject("user_repository")
    def execute(self, input_data: str, user_repository: UserRepository = None) -> UserOutput:
        """Execute get user use case."""
        user = user_repository.get_by_id(input_data)
        if not user:
            raise NotFoundError(message=f"User ID '{input_data}' not found")

        return UserOutput(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
        )


class UpdateUserUseCase(UseCase[UpdateUserInput, UserOutput]):
    """Update User Use Case."""

    @inject("user_repository")
    @transactional
    def execute(
        self, input_data: UpdateUserInput, user_repository: UserRepository = None
    ) -> UserOutput:
        """Execute update user use case."""
        # Get user
        user = user_repository.get_by_id(input_data.user_id)
        if not user:
            raise NotFoundError(message=f"User ID '{input_data.user_id}' not found")

        # Check if username already exists
        if input_data.username and input_data.username != user.username:
            existing = user_repository.get_by_username(input_data.username)
            if existing and existing.id != user.id:
                raise ValidationError(message=f"Username '{input_data.username}' already exists")
            user.username = input_data.username

        # Check if email already exists
        if input_data.email and input_data.email != user.email:
            existing = user_repository.get_by_email(input_data.email)
            if existing and existing.id != user.id:
                raise ValidationError(message=f"Email '{input_data.email}' already exists")
            user.email = input_data.email

        # Update other fields
        if input_data.full_name is not None:
            user.full_name = input_data.full_name

        if input_data.is_active is not None:
            user.is_active = input_data.is_active

        # Update timestamp
        user.updated_at = datetime.now()

        # Save user
        updated_user = user_repository.save(user)

        # Collect updated fields
        changes = {}
        if input_data.username:
            changes["username"] = input_data.username
        if input_data.email:
            changes["email"] = input_data.email
        if input_data.full_name is not None:
            changes["full_name"] = input_data.full_name
        if input_data.is_active is not None:
            changes["is_active"] = input_data.is_active

        # Publish event
        if changes:
            publish(UserUpdatedEvent(user_id=updated_user.id, changes=changes))

        # Return output
        return UserOutput(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            full_name=updated_user.full_name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
        )


class DeleteUserUseCase(UseCase[str, bool]):
    """Delete User Use Case."""

    @inject("user_repository")
    @transactional
    def execute(self, input_data: str, user_repository: UserRepository = None) -> bool:
        """Execute delete user use case."""
        # Check if user exists
        user = user_repository.get_by_id(input_data)
        if not user:
            raise NotFoundError(message=f"User ID '{input_data}' not found")

        # Delete user
        result = user_repository.delete(input_data)

        # Publish event
        if result:
            publish(UserDeletedEvent(user_id=input_data))

        return result


class CreateTaskUseCase(UseCase[CreateTaskInput, TaskOutput]):
    """Create Task Use Case."""

    @inject("task_repository")
    @inject("user_repository")
    @transactional
    def execute(
        self,
        input_data: CreateTaskInput,
        task_repository: TaskRepository = None,
        user_repository: UserRepository = None,
    ) -> TaskOutput:
        """Execute create task use case."""
        # If user is specified, check if user exists
        if input_data.user_id:
            user = user_repository.get_by_id(input_data.user_id)
            if not user:
                raise NotFoundError(message=f"User ID '{input_data.user_id}' not found")

        # Create task entity
        task = Task(
            title=input_data.title,
            description=input_data.description,
            due_date=input_data.due_date,
            user_id=input_data.user_id,
        )

        # Save task
        saved_task = task_repository.save(task)

        # Publish event
        publish(
            TaskCreatedEvent(
                task_id=saved_task.id, title=saved_task.title, user_id=saved_task.user_id
            )
        )

        # Return output
        return TaskOutput(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            is_completed=saved_task.is_completed,
            due_date=saved_task.due_date,
            user_id=saved_task.user_id,
            created_at=saved_task.created_at,
        )


class GetTaskUseCase(UseCase[str, TaskOutput]):
    """Get Task Use Case."""

    @inject("task_repository")
    def execute(self, input_data: str, task_repository: TaskRepository = None) -> TaskOutput:
        """Execute get task use case."""
        task = task_repository.get_by_id(input_data)
        if not task:
            raise NotFoundError(message=f"Task ID '{input_data}' not found")

        return TaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            due_date=task.due_date,
            user_id=task.user_id,
            created_at=task.created_at,
        )


class UpdateTaskUseCase(UseCase[UpdateTaskInput, TaskOutput]):
    """Update Task Use Case."""

    @inject("task_repository")
    @transactional
    def execute(
        self, input_data: UpdateTaskInput, task_repository: TaskRepository = None
    ) -> TaskOutput:
        """Execute update task use case."""
        # Get task
        task = task_repository.get_by_id(input_data.task_id)
        if not task:
            raise NotFoundError(message=f"Task ID '{input_data.task_id}' not found")

        # Collect updated fields
        changes = {}

        # Update fields
        if input_data.title is not None:
            task.title = input_data.title
            changes["title"] = input_data.title

        if input_data.description is not None:
            task.description = input_data.description
            changes["description"] = input_data.description

        if input_data.due_date is not None:
            task.due_date = input_data.due_date
            changes["due_date"] = input_data.due_date.isoformat() if input_data.due_date else None

        # Update timestamp
        task.updated_at = datetime.now()

        # Save task
        updated_task = task_repository.save(task)

        # Publish event
        if changes:
            publish(
                TaskUpdatedEvent(
                    task_id=updated_task.id, changes=changes, user_id=updated_task.user_id
                )
            )

        # Return output
        return TaskOutput(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            is_completed=updated_task.is_completed,
            due_date=updated_task.due_date,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at,
        )


class CompleteTaskUseCase(UseCase[str, TaskOutput]):
    """Complete Task Use Case."""

    @inject("task_repository")
    @transactional
    def execute(self, input_data: str, task_repository: TaskRepository = None) -> TaskOutput:
        """Execute complete task use case."""
        # Get task
        task = task_repository.get_by_id(input_data)
        if not task:
            raise NotFoundError(message=f"Task ID '{input_data}' not found")

        # Complete task
        task.complete()

        # Save task
        updated_task = task_repository.save(task)

        # Publish event
        publish(TaskCompletedEvent(task_id=updated_task.id, user_id=updated_task.user_id))

        # Return output
        return TaskOutput(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            is_completed=updated_task.is_completed,
            due_date=updated_task.due_date,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at,
        )


class DeleteTaskUseCase(UseCase[str, bool]):
    """Delete Task Use Case."""

    @inject("task_repository")
    @transactional
    def execute(self, input_data: str, task_repository: TaskRepository = None) -> bool:
        """Execute delete task use case."""
        # Get task
        task = task_repository.get_by_id(input_data)
        if not task:
            raise NotFoundError(message=f"Task ID '{input_data}' not found")

        user_id = task.user_id

        # Delete task
        result = task_repository.delete(input_data)

        # Publish event
        if result:
            publish(TaskDeletedEvent(task_id=input_data, user_id=user_id))

        return result


class ListUserTasksUseCase(UseCase[str, List[TaskOutput]]):
    """List User Tasks Use Case."""

    @inject("task_repository")
    @inject("user_repository")
    def execute(
        self,
        input_data: str,
        task_repository: TaskRepository = None,
        user_repository: UserRepository = None,
    ) -> List[TaskOutput]:
        """Execute list user tasks use case."""
        # Check if user exists
        user = user_repository.get_by_id(input_data)
        if not user:
            raise NotFoundError(message=f"User ID '{input_data}' not found")

        # Get user tasks
        tasks = task_repository.list_by_user(input_data)

        # Convert to output format
        return [
            TaskOutput(
                id=task.id,
                title=task.title,
                description=task.description,
                is_completed=task.is_completed,
                due_date=task.due_date,
                user_id=task.user_id,
                created_at=task.created_at,
            )
            for task in tasks
        ]

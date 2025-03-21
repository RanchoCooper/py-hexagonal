"""Unit Test Examples."""
import uuid
from datetime import datetime
from unittest.mock import MagicMock, patch

from application.service.example import CreateTaskUseCase, CreateUserUseCase
from application.usecase.example import CreateTaskInput, CreateUserInput
from domain.model.example import User


class TestUserUseCases:
    """User Use Case Tests."""

    def test_create_user(self):
        """Test create user use case."""
        # Create mock repository
        mock_repo = MagicMock()
        mock_repo.get_by_username.return_value = None
        mock_repo.get_by_email.return_value = None

        # Mock save operation
        user_id = str(uuid.uuid4())
        now = datetime.now()

        def mock_save(user):
            user.id = user_id
            user.created_at = now
            user.updated_at = now
            return user

        mock_repo.save.side_effect = mock_save

        # Create input
        input_data = CreateUserInput(
            username="testuser",
            email="test@example.com",
            password="password123",
            full_name="Test User",
        )

        # Execute use case
        with patch("application.service.example.publish") as mock_publish:
            usecase = CreateUserUseCase()
            result = usecase.execute(input_data, user_repository=mock_repo)

        # Verify results
        assert result.id == user_id
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.full_name == "Test User"
        assert result.is_active is True

        # Verify repository calls
        mock_repo.get_by_username.assert_called_once_with("testuser")
        mock_repo.get_by_email.assert_called_once_with("test@example.com")
        mock_repo.save.assert_called_once()

        # Verify event publishing
        mock_publish.assert_called_once()


class TestTaskUseCases:
    """Task Use Case Tests."""

    def test_create_task(self):
        """Test create task use case."""
        # Create mock repositories
        mock_task_repo = MagicMock()
        mock_user_repo = MagicMock()

        # Mock user exists
        user_id = str(uuid.uuid4())
        mock_user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            full_name="Test User",
        )
        mock_user_repo.get_by_id.return_value = mock_user

        # Mock save operation
        task_id = str(uuid.uuid4())
        now = datetime.now()

        def mock_save(task):
            task.id = task_id
            task.created_at = now
            task.updated_at = now
            return task

        mock_task_repo.save.side_effect = mock_save

        # Create input
        input_data = CreateTaskInput(
            title="Test Task", description="This is a test task", user_id=user_id
        )

        # Execute use case
        with patch("application.service.example.publish") as mock_publish:
            usecase = CreateTaskUseCase()
            result = usecase.execute(
                input_data, task_repository=mock_task_repo, user_repository=mock_user_repo
            )

        # Verify results
        assert result.id == task_id
        assert result.title == "Test Task"
        assert result.description == "This is a test task"
        assert result.is_completed is False
        assert result.user_id == user_id

        # Verify repository calls
        mock_user_repo.get_by_id.assert_called_once_with(user_id)
        mock_task_repo.save.assert_called_once()

        # Verify event publishing
        mock_publish.assert_called_once()

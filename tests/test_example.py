"""单元测试示例"""
import pytest
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime

from domain.model.example import User, Task
from application.service.example import CreateUserUseCase, CreateTaskUseCase
from application.usecase.example import CreateUserInput, CreateTaskInput


class TestUserUseCases:
    """用户用例测试"""
    
    def test_create_user(self):
        """测试创建用户用例"""
        # 创建模拟仓库
        mock_repo = MagicMock()
        mock_repo.get_by_username.return_value = None
        mock_repo.get_by_email.return_value = None
        
        # 模拟保存操作
        user_id = str(uuid.uuid4())
        now = datetime.now()
        
        def mock_save(user):
            user.id = user_id
            user.created_at = now
            user.updated_at = now
            return user
        
        mock_repo.save.side_effect = mock_save
        
        # 创建输入
        input_data = CreateUserInput(
            username="testuser",
            email="test@example.com",
            password="password123",
            full_name="Test User"
        )
        
        # 执行用例
        with patch('application.service.example.publish') as mock_publish:
            usecase = CreateUserUseCase()
            result = usecase.execute(input_data, user_repository=mock_repo)
        
        # 验证结果
        assert result.id == user_id
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.full_name == "Test User"
        assert result.is_active is True
        
        # 验证仓库调用
        mock_repo.get_by_username.assert_called_once_with("testuser")
        mock_repo.get_by_email.assert_called_once_with("test@example.com")
        mock_repo.save.assert_called_once()
        
        # 验证事件发布
        mock_publish.assert_called_once()


class TestTaskUseCases:
    """任务用例测试"""
    
    def test_create_task(self):
        """测试创建任务用例"""
        # 创建模拟仓库
        mock_task_repo = MagicMock()
        mock_user_repo = MagicMock()
        
        # 模拟用户存在
        user_id = str(uuid.uuid4())
        mock_user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            full_name="Test User"
        )
        mock_user_repo.get_by_id.return_value = mock_user
        
        # 模拟保存操作
        task_id = str(uuid.uuid4())
        now = datetime.now()
        
        def mock_save(task):
            task.id = task_id
            task.created_at = now
            task.updated_at = now
            return task
        
        mock_task_repo.save.side_effect = mock_save
        
        # 创建输入
        input_data = CreateTaskInput(
            title="Test Task",
            description="This is a test task",
            user_id=user_id
        )
        
        # 执行用例
        with patch('application.service.example.publish') as mock_publish:
            usecase = CreateTaskUseCase()
            result = usecase.execute(
                input_data, 
                task_repository=mock_task_repo,
                user_repository=mock_user_repo
            )
        
        # 验证结果
        assert result.id == task_id
        assert result.title == "Test Task"
        assert result.description == "This is a test task"
        assert result.is_completed is False
        assert result.user_id == user_id
        
        # 验证仓库调用
        mock_user_repo.get_by_id.assert_called_once_with(user_id)
        mock_task_repo.save.assert_called_once()
        
        # 验证事件发布
        mock_publish.assert_called_once()
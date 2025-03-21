"""示例服务实现"""
import logging
import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime

from domain.model.example import User, Task
from domain.repository.example import UserRepository, TaskRepository
from application.usecase.base import UseCase
from application.usecase.example import (
    CreateUserInput, UserOutput, UpdateUserInput,
    CreateTaskInput, TaskOutput, UpdateTaskInput
)
from application.di.container import inject
from application.event.bus import publish
from application.event.events import (
    UserCreatedEvent, UserUpdatedEvent, UserDeletedEvent,
    TaskCreatedEvent, TaskUpdatedEvent, TaskCompletedEvent, TaskDeletedEvent
)
from util.errors import NotFoundError, ValidationError
from util.transaction import transactional

# 设置日志
logger = logging.getLogger(__name__)


class CreateUserUseCase(UseCase[CreateUserInput, UserOutput]):
    """创建用户用例"""
    
    @inject('user_repository')
    @transactional
    def execute(self, input_data: CreateUserInput, user_repository: UserRepository = None) -> UserOutput:
        """执行创建用户用例"""
        # 检查用户名和邮箱是否已存在
        if user_repository.get_by_username(input_data.username):
            raise ValidationError(message=f"用户名 '{input_data.username}' 已存在")
        
        if user_repository.get_by_email(input_data.email):
            raise ValidationError(message=f"邮箱 '{input_data.email}' 已存在")
        
        # 密码加密
        password_hash = hashlib.sha256(input_data.password.encode()).hexdigest()
        
        # 创建用户实体
        user = User(
            username=input_data.username,
            email=input_data.email,
            password_hash=password_hash,
            full_name=input_data.full_name
        )
        
        # 保存用户
        saved_user = user_repository.save(user)
        
        # 发布事件
        publish(UserCreatedEvent(
            user_id=saved_user.id,
            username=saved_user.username,
            email=saved_user.email
        ))
        
        # 返回输出
        return UserOutput(
            id=saved_user.id,
            username=saved_user.username,
            email=saved_user.email,
            full_name=saved_user.full_name,
            is_active=saved_user.is_active,
            created_at=saved_user.created_at
        )


class GetUserUseCase(UseCase[str, UserOutput]):
    """获取用户用例"""
    
    @inject('user_repository')
    def execute(self, input_data: str, user_repository: UserRepository = None) -> UserOutput:
        """执行获取用户用例"""
        user = user_repository.get_by_id(input_data)
        if not user:
            raise NotFoundError(message=f"用户 ID '{input_data}' 不存在")
        
        return UserOutput(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at
        )


class UpdateUserUseCase(UseCase[UpdateUserInput, UserOutput]):
    """更新用户用例"""
    
    @inject('user_repository')
    @transactional
    def execute(self, input_data: UpdateUserInput, user_repository: UserRepository = None) -> UserOutput:
        """执行更新用户用例"""
        # 获取用户
        user = user_repository.get_by_id(input_data.user_id)
        if not user:
            raise NotFoundError(message=f"用户 ID '{input_data.user_id}' 不存在")
        
        # 检查用户名是否已存在
        if input_data.username and input_data.username != user.username:
            existing = user_repository.get_by_username(input_data.username)
            if existing and existing.id != user.id:
                raise ValidationError(message=f"用户名 '{input_data.username}' 已存在")
            user.username = input_data.username
        
        # 检查邮箱是否已存在
        if input_data.email and input_data.email != user.email:
            existing = user_repository.get_by_email(input_data.email)
            if existing and existing.id != user.id:
                raise ValidationError(message=f"邮箱 '{input_data.email}' 已存在")
            user.email = input_data.email
        
        # 更新其他字段
        if input_data.full_name is not None:
            user.full_name = input_data.full_name
        
        if input_data.is_active is not None:
            user.is_active = input_data.is_active
        
        # 更新时间
        user.updated_at = datetime.now()
        
        # 保存用户
        updated_user = user_repository.save(user)
        
        # 收集更新的字段
        changes = {}
        if input_data.username:
            changes['username'] = input_data.username
        if input_data.email:
            changes['email'] = input_data.email
        if input_data.full_name is not None:
            changes['full_name'] = input_data.full_name
        if input_data.is_active is not None:
            changes['is_active'] = input_data.is_active
        
        # 发布事件
        if changes:
            publish(UserUpdatedEvent(
                user_id=updated_user.id,
                changes=changes
            ))
        
        # 返回输出
        return UserOutput(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            full_name=updated_user.full_name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at
        )


class DeleteUserUseCase(UseCase[str, bool]):
    """删除用户用例"""
    
    @inject('user_repository')
    @transactional
    def execute(self, input_data: str, user_repository: UserRepository = None) -> bool:
        """执行删除用户用例"""
        # 检查用户是否存在
        user = user_repository.get_by_id(input_data)
        if not user:
            raise NotFoundError(message=f"用户 ID '{input_data}' 不存在")
        
        # 删除用户
        result = user_repository.delete(input_data)
        
        # 发布事件
        if result:
            publish(UserDeletedEvent(user_id=input_data))
        
        return result


class CreateTaskUseCase(UseCase[CreateTaskInput, TaskOutput]):
    """创建任务用例"""
    
    @inject('task_repository')
    @inject('user_repository')
    @transactional
    def execute(
        self, 
        input_data: CreateTaskInput, 
        task_repository: TaskRepository = None,
        user_repository: UserRepository = None
    ) -> TaskOutput:
        """执行创建任务用例"""
        # 如果指定了用户，检查用户是否存在
        if input_data.user_id:
            user = user_repository.get_by_id(input_data.user_id)
            if not user:
                raise NotFoundError(message=f"用户 ID '{input_data.user_id}' 不存在")
        
        # 创建任务实体
        task = Task(
            title=input_data.title,
            description=input_data.description,
            due_date=input_data.due_date,
            user_id=input_data.user_id
        )
        
        # 保存任务
        saved_task = task_repository.save(task)
        
        # 发布事件
        publish(TaskCreatedEvent(
            task_id=saved_task.id,
            title=saved_task.title,
            user_id=saved_task.user_id
        ))
        
        # 返回输出
        return TaskOutput(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            is_completed=saved_task.is_completed,
            due_date=saved_task.due_date,
            user_id=saved_task.user_id,
            created_at=saved_task.created_at
        )


class GetTaskUseCase(UseCase[str, TaskOutput]):
    """获取任务用例"""
    
    @inject('task_repository')
    def execute(self, input_data: str, task_repository: TaskRepository = None) -> TaskOutput:
        """执行获取任务用例"""
        task = task_repository.get_by_id(input_data)
        if not task:
            raise NotFoundError(message=f"任务 ID '{input_data}' 不存在")
        
        return TaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            due_date=task.due_date,
            user_id=task.user_id,
            created_at=task.created_at
        )


class UpdateTaskUseCase(UseCase[UpdateTaskInput, TaskOutput]):
    """更新任务用例"""
    
    @inject('task_repository')
    @transactional
    def execute(self, input_data: UpdateTaskInput, task_repository: TaskRepository = None) -> TaskOutput:
        """执行更新任务用例"""
        # 获取任务
        task = task_repository.get_by_id(input_data.task_id)
        if not task:
            raise NotFoundError(message=f"任务 ID '{input_data.task_id}' 不存在")
        
        # 收集更新的字段
        changes = {}
        
        # 更新字段
        if input_data.title is not None:
            task.title = input_data.title
            changes['title'] = input_data.title
        
        if input_data.description is not None:
            task.description = input_data.description
            changes['description'] = input_data.description
        
        if input_data.due_date is not None:
            task.due_date = input_data.due_date
            changes['due_date'] = input_data.due_date.isoformat() if input_data.due_date else None
        
        # 更新时间
        task.updated_at = datetime.now()
        
        # 保存任务
        updated_task = task_repository.save(task)
        
        # 发布事件
        if changes:
            publish(TaskUpdatedEvent(
                task_id=updated_task.id,
                changes=changes,
                user_id=updated_task.user_id
            ))
        
        # 返回输出
        return TaskOutput(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            is_completed=updated_task.is_completed,
            due_date=updated_task.due_date,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at
        )


class CompleteTaskUseCase(UseCase[str, TaskOutput]):
    """完成任务用例"""
    
    @inject('task_repository')
    @transactional
    def execute(self, input_data: str, task_repository: TaskRepository = None) -> TaskOutput:
        """执行完成任务用例"""
        # 获取任务
        task = task_repository.get_by_id(input_data)
        if not task:
            raise NotFoundError(message=f"任务 ID '{input_data}' 不存在")
        
        # 完成任务
        task.complete()
        
        # 保存任务
        updated_task = task_repository.save(task)
        
        # 发布事件
        publish(TaskCompletedEvent(
            task_id=updated_task.id,
            user_id=updated_task.user_id
        ))
        
        # 返回输出
        return TaskOutput(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            is_completed=updated_task.is_completed,
            due_date=updated_task.due_date,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at
        )


class DeleteTaskUseCase(UseCase[str, bool]):
    """删除任务用例"""
    
    @inject('task_repository')
    @transactional
    def execute(self, input_data: str, task_repository: TaskRepository = None) -> bool:
        """执行删除任务用例"""
        # 获取任务
        task = task_repository.get_by_id(input_data)
        if not task:
            raise NotFoundError(message=f"任务 ID '{input_data}' 不存在")
        
        user_id = task.user_id
        
        # 删除任务
        result = task_repository.delete(input_data)
        
        # 发布事件
        if result:
            publish(TaskDeletedEvent(
                task_id=input_data,
                user_id=user_id
            ))
        
        return result


class ListUserTasksUseCase(UseCase[str, List[TaskOutput]]):
    """列出用户任务用例"""
    
    @inject('task_repository')
    @inject('user_repository')
    def execute(
        self, 
        input_data: str,
        task_repository: TaskRepository = None,
        user_repository: UserRepository = None
    ) -> List[TaskOutput]:
        """执行列出用户任务用例"""
        # 检查用户是否存在
        user = user_repository.get_by_id(input_data)
        if not user:
            raise NotFoundError(message=f"用户 ID '{input_data}' 不存在")
        
        # 获取用户任务
        tasks = task_repository.list_by_user(input_data)
        
        # 转换为输出格式
        return [
            TaskOutput(
                id=task.id,
                title=task.title,
                description=task.description,
                is_completed=task.is_completed,
                due_date=task.due_date,
                user_id=task.user_id,
                created_at=task.created_at
            )
            for task in tasks
        ] 
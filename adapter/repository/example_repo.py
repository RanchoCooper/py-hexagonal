"""示例仓库实现"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, delete, func

from domain.repository.example import UserRepository, TaskRepository
from domain.model.example import User, Task
from util.errors import NotFoundError, DatabaseError

# SQLAlchemy模型定义
Base = declarative_base()

class UserModel(Base):
    """用户数据库模型"""
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    @classmethod
    def from_entity(cls, user: User) -> 'UserModel':
        """从实体创建模型"""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    def to_entity(self) -> User:
        """转换为实体"""
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            full_name=self.full_name,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


class TaskModel(Base):
    """任务数据库模型"""
    __tablename__ = 'tasks'
    
    id = Column(String(36), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime)
    user_id = Column(String(36), ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    @classmethod
    def from_entity(cls, task: Task) -> 'TaskModel':
        """从实体创建模型"""
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            due_date=task.due_date,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    
    def to_entity(self) -> Task:
        """转换为实体"""
        return Task(
            id=self.id,
            title=self.title,
            description=self.description,
            is_completed=self.is_completed,
            due_date=self.due_date,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy用户仓库实现"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        return user.to_entity() if user else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        user = self.session.query(UserModel).filter(UserModel.username == username).first()
        return user.to_entity() if user else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        user = self.session.query(UserModel).filter(UserModel.email == email).first()
        return user.to_entity() if user else None
    
    def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        users = self.session.query(UserModel).limit(limit).offset(offset).all()
        return [user.to_entity() for user in users]
    
    def save(self, user: User) -> User:
        try:
            existing = self.session.query(UserModel).filter(UserModel.id == user.id).first()
            if existing:
                # 更新现有用户
                existing.username = user.username
                existing.email = user.email
                existing.password_hash = user.password_hash
                existing.full_name = user.full_name
                existing.is_active = user.is_active
                existing.updated_at = user.updated_at
                self.session.add(existing)
                self.session.flush()
                return existing.to_entity()
            else:
                # 创建新用户
                user_model = UserModel.from_entity(user)
                self.session.add(user_model)
                self.session.flush()
                return user_model.to_entity()
        except Exception as e:
            raise DatabaseError(message=f"保存用户失败: {str(e)}")
    
    def delete(self, user_id: str) -> bool:
        try:
            result = self.session.query(UserModel).filter(UserModel.id == user_id).delete()
            self.session.flush()
            return result > 0
        except Exception as e:
            raise DatabaseError(message=f"删除用户失败: {str(e)}")


class SQLAlchemyTaskRepository(TaskRepository):
    """SQLAlchemy任务仓库实现"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        task = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        return task.to_entity() if task else None
    
    def list_all(self, limit: int = 100, offset: int = 0) -> List[Task]:
        tasks = self.session.query(TaskModel).limit(limit).offset(offset).all()
        return [task.to_entity() for task in tasks]
    
    def list_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Task]:
        tasks = self.session.query(TaskModel).filter(
            TaskModel.user_id == user_id
        ).limit(limit).offset(offset).all()
        return [task.to_entity() for task in tasks]
    
    def save(self, task: Task) -> Task:
        try:
            existing = self.session.query(TaskModel).filter(TaskModel.id == task.id).first()
            if existing:
                # 更新现有任务
                existing.title = task.title
                existing.description = task.description
                existing.is_completed = task.is_completed
                existing.due_date = task.due_date
                existing.user_id = task.user_id
                existing.updated_at = task.updated_at
                self.session.add(existing)
                self.session.flush()
                return existing.to_entity()
            else:
                # 创建新任务
                task_model = TaskModel.from_entity(task)
                self.session.add(task_model)
                self.session.flush()
                return task_model.to_entity()
        except Exception as e:
            raise DatabaseError(message=f"保存任务失败: {str(e)}")
    
    def delete(self, task_id: str) -> bool:
        try:
            result = self.session.query(TaskModel).filter(TaskModel.id == task_id).delete()
            self.session.flush()
            return result > 0
        except Exception as e:
            raise DatabaseError(message=f"删除任务失败: {str(e)}")
    
    def count_by_user(self, user_id: str, is_completed: Optional[bool] = None) -> int:
        query = self.session.query(func.count(TaskModel.id)).filter(TaskModel.user_id == user_id)
        if is_completed is not None:
            query = query.filter(TaskModel.is_completed == is_completed)
        return query.scalar() or 0 
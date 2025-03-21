"""示例仓库接口"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from domain.model.example import User, Task


class UserRepository(ABC):
    """用户仓库接口"""
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        pass
    
    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """获取所有用户"""
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        """保存用户"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """删除用户"""
        pass


class TaskRepository(ABC):
    """任务仓库接口"""
    
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        pass
    
    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[Task]:
        """获取所有任务"""
        pass
    
    @abstractmethod
    def list_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Task]:
        """获取用户的所有任务"""
        pass
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """保存任务"""
        pass
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """删除任务"""
        pass
    
    @abstractmethod
    def count_by_user(self, user_id: str, is_completed: Optional[bool] = None) -> int:
        """统计用户任务数量"""
        pass 
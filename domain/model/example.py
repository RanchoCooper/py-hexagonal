"""示例领域模型"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


@dataclass
class BaseEntity:
    """基础实体"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class User(BaseEntity):
    """用户实体"""
    username: str
    email: str
    password_hash: str
    full_name: Optional[str] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data.update({
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active
        })
        return data


@dataclass
class Task(BaseEntity):
    """任务实体"""
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    user_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
            "user_id": self.user_id
        })
        if self.due_date:
            data["due_date"] = self.due_date.isoformat()
        return data
    
    def complete(self) -> None:
        """完成任务"""
        self.is_completed = True
        self.updated_at = datetime.now()
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None,
              due_date: Optional[datetime] = None) -> None:
        """更新任务信息"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        self.updated_at = datetime.now() 
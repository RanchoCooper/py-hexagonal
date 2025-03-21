"""事件定义模块"""
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class Event:
    """基础事件类"""
    event_type: str
    timestamp: datetime = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class UserEvent(Event):
    """用户相关事件"""
    user_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data["user_id"] = self.user_id
        return data


@dataclass
class UserCreatedEvent(UserEvent):
    """用户创建事件"""
    username: str
    email: str
    
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(
            event_type="user.created",
            user_id=user_id
        )
        self.username = username
        self.email = email
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data.update({
            "username": self.username,
            "email": self.email
        })
        return data


@dataclass
class UserUpdatedEvent(UserEvent):
    """用户更新事件"""
    changes: Dict[str, Any]
    
    def __init__(self, user_id: str, changes: Dict[str, Any]):
        super().__init__(
            event_type="user.updated",
            user_id=user_id
        )
        self.changes = changes
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data["changes"] = self.changes
        return data


@dataclass
class UserDeletedEvent(UserEvent):
    """用户删除事件"""
    
    def __init__(self, user_id: str):
        super().__init__(
            event_type="user.deleted",
            user_id=user_id
        )


@dataclass
class TaskEvent(Event):
    """任务相关事件"""
    task_id: str
    user_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data["task_id"] = self.task_id
        if self.user_id:
            data["user_id"] = self.user_id
        return data


@dataclass
class TaskCreatedEvent(TaskEvent):
    """任务创建事件"""
    title: str
    
    def __init__(self, task_id: str, title: str, user_id: Optional[str] = None):
        super().__init__(
            event_type="task.created",
            task_id=task_id,
            user_id=user_id
        )
        self.title = title
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data["title"] = self.title
        return data


@dataclass
class TaskUpdatedEvent(TaskEvent):
    """任务更新事件"""
    changes: Dict[str, Any]
    
    def __init__(self, task_id: str, changes: Dict[str, Any], user_id: Optional[str] = None):
        super().__init__(
            event_type="task.updated",
            task_id=task_id,
            user_id=user_id
        )
        self.changes = changes
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = super().to_dict()
        data["changes"] = self.changes
        return data


@dataclass
class TaskCompletedEvent(TaskEvent):
    """任务完成事件"""
    
    def __init__(self, task_id: str, user_id: Optional[str] = None):
        super().__init__(
            event_type="task.completed",
            task_id=task_id,
            user_id=user_id
        )


@dataclass
class TaskDeletedEvent(TaskEvent):
    """任务删除事件"""
    
    def __init__(self, task_id: str, user_id: Optional[str] = None):
        super().__init__(
            event_type="task.deleted",
            task_id=task_id,
            user_id=user_id
        ) 
"""示例用例模块"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

# 用例输入/输出数据结构


@dataclass
class CreateUserInput:
    """创建用户输入"""
    username: str
    email: str
    password: str
    full_name: Optional[str] = None


@dataclass
class UserOutput:
    """用户输出"""
    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime


@dataclass
class UpdateUserInput:
    """更新用户输入"""
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class CreateTaskInput:
    """创建任务输入"""
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    user_id: Optional[str] = None


@dataclass
class TaskOutput:
    """任务输出"""
    id: str
    title: str
    description: Optional[str]
    is_completed: bool
    due_date: Optional[datetime]
    user_id: Optional[str]
    created_at: datetime


@dataclass
class UpdateTaskInput:
    """更新任务输入"""
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

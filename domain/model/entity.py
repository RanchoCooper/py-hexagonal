"""
定义基础实体结构的基础实体模块。
"""

from abc import ABC
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Entity(ABC):
    """
    所有领域实体都应该继承的基础实体类。
    提供通用的实体行为和属性。
    """

    def __init__(self, entity_id: Optional[UUID] = None, created_at: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None):
        """
        初始化一个新实体。
        
        参数:
            entity_id (Optional[UUID]): 实体ID。默认为生成的UUID。
            created_at (Optional[datetime]): 实体创建时间戳。默认为当前时间。
            updated_at (Optional[datetime]): 实体最后更新时间戳。默认为当前时间。
        """
        self._id = entity_id or uuid4()
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
    
    @property
    def id(self) -> UUID:
        """获取实体ID。"""
        return self._id
    
    @property
    def created_at(self) -> datetime:
        """获取实体创建时间戳。"""
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        """获取实体最后更新时间戳。"""
        return self._updated_at
    
    def update(self) -> None:
        """更新实体的最后更新时间戳。"""
        self._updated_at = datetime.utcnow()
        
    def __eq__(self, other):
        """
        比较两个实体是否相等。
        如果两个实体的ID相同，则它们相等。
        """
        if not isinstance(other, Entity):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """基于实体ID生成哈希值。"""
        return hash(self.id) 
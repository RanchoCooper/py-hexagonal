"""
领域层的示例模型。
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Example:
    """示例实体。"""
    
    id: UUID
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create(cls, name: str, description: Optional[str] = None) -> 'Example':
        """
        创建新的示例。
        
        参数:
            name: 示例的名称
            description: 示例的描述
            
        返回:
            一个新的示例
        """
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now
        )
    
    def update(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        更新示例。
        
        参数:
            name: 示例的新名称
            description: 示例的新描述
        """
        if name is not None:
            self.name = name
        
        if description is not None:
            self.description = description
            
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """激活示例。"""
        if self.is_active:
            return
            
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """停用示例。"""
        if not self.is_active:
            return
            
        self.is_active = False
        self.updated_at = datetime.utcnow() 
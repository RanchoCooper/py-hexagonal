"""
示例应用服务模块，处理示例的应用层操作。
"""

from typing import List, Optional
from uuid import UUID

from domain.event.event_bus import EventBus
from domain.event.example_events import (
    ExampleCreatedEvent,
    ExampleDeletedEvent,
    ExampleUpdatedEvent,
)
from domain.model.example import Example
from domain.service.example_service import ExampleService as DomainExampleService


class ExampleApplicationService:
    """
    示例实体的应用服务。
    编排使用领域服务的应用层操作。
    """
    
    def __init__(self, domain_service: DomainExampleService, event_bus: EventBus):
        """
        初始化示例应用服务。
        
        参数:
            domain_service (DomainExampleService): 示例实体的领域服务。
            event_bus (EventBus): 用于发布事件的事件总线。
        """
        self._domain_service = domain_service
        self._event_bus = event_bus
    
    def create_example(self, name: str, description: str) -> Example:
        """
        创建新的示例。
        
        参数:
            name (str): 新示例的名称。
            description (str): 新示例的描述。
            
        返回:
            Example: 创建的示例。
        """
        # 使用领域服务创建示例
        example = self._domain_service.create_example(name, description)
        
        # 发布创建事件
        self._event_bus.publish(ExampleCreatedEvent(example.id, example.name))
        
        return example
    
    def get_example(self, example_id: UUID) -> Optional[Example]:
        """
        通过ID获取示例。
        
        参数:
            example_id (UUID): 要获取的示例的ID。
            
        返回:
            Optional[Example]: 找到的示例，如果未找到则为None。
        """
        return self._domain_service.get_example(example_id)
    
    def get_all_examples(self) -> List[Example]:
        """
        获取所有示例。
        
        返回:
            List[Example]: 所有示例的列表。
        """
        return self._domain_service.get_all_examples()
    
    def get_active_examples(self) -> List[Example]:
        """
        获取所有活动的示例。
        
        返回:
            List[Example]: 所有活动示例的列表。
        """
        return self._domain_service.get_active_examples()
    
    def update_example(self, example_id: UUID, name: Optional[str] = None,
                      description: Optional[str] = None) -> Optional[Example]:
        """
        更新示例的详细信息。
        
        参数:
            example_id (UUID): 要更新的示例的ID。
            name (Optional[str]): 新名称，如果有的话。
            description (Optional[str]): 新描述，如果有的话。
            
        返回:
            Optional[Example]: 更新后的示例，如果未找到则为None。
        """
        # 使用领域服务更新示例
        example = self._domain_service.update_example(example_id, name, description)
        
        # 如果找到并更新了示例，则发布更新事件
        if example:
            self._event_bus.publish(ExampleUpdatedEvent(example.id, example.name))
        
        return example
    
    def activate_example(self, example_id: UUID) -> Optional[Example]:
        """
        激活示例。
        
        参数:
            example_id (UUID): 要激活的示例的ID。
            
        返回:
            Optional[Example]: 激活的示例，如果未找到则为None。
        """
        return self._domain_service.activate_example(example_id)
    
    def deactivate_example(self, example_id: UUID) -> Optional[Example]:
        """
        停用示例。
        
        参数:
            example_id (UUID): 要停用的示例的ID。
            
        返回:
            Optional[Example]: 停用的示例，如果未找到则为None。
        """
        return self._domain_service.deactivate_example(example_id)
    
    def delete_example(self, example_id: UUID) -> bool:
        """
        删除示例。
        
        参数:
            example_id (UUID): 要删除的示例的ID。
            
        返回:
            bool: 如果删除了示例则为True，如果未找到则为False。
        """
        # 在删除之前获取示例（以便为事件提供数据）
        example = self._domain_service.get_example(example_id)
        if not example:
            return False
        
        # 使用领域服务删除示例
        result = self._domain_service.delete_example(example_id)
        
        # 如果找到并删除了示例，则发布删除事件
        if result:
            self._event_bus.publish(ExampleDeletedEvent(example.id))
        
        return result 
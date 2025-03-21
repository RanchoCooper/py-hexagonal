"""
依赖注入容器。
"""

from dependency_injector import containers, providers

from adapter.event.memory_event_bus import MemoryEventBus
from adapter.repository.memory_example_repository import MemoryExampleRepository
from application.event.example_event_handlers import (
    ExampleCreatedEventHandler,
    ExampleDeletedEventHandler,
    ExampleUpdatedEventHandler,
)
from application.service.example_service import ExampleApplicationService
from domain.event.example_events import (
    ExampleCreatedEvent,
    ExampleDeletedEvent,
    ExampleUpdatedEvent,
)
from domain.service.example_service import ExampleService


class Container(containers.DeclarativeContainer):
    """
    依赖注入容器。
    """
    
    # 配置
    config = providers.Configuration()
    
    # 仓储
    example_repository = providers.Singleton(MemoryExampleRepository)
    
    # 领域服务
    example_domain_service = providers.Singleton(
        ExampleService,
        example_repository=example_repository
    )
    
    # 事件总线
    event_bus = providers.Singleton(MemoryEventBus)
    
    # 事件处理器
    example_created_handler = providers.Factory(ExampleCreatedEventHandler)
    example_updated_handler = providers.Factory(ExampleUpdatedEventHandler)
    example_deleted_handler = providers.Factory(ExampleDeletedEventHandler)
    
    # 应用服务
    example_app_service = providers.Singleton(
        ExampleApplicationService,
        domain_service=example_domain_service,
        event_bus=event_bus,
    )
    
    # 连接事件处理器
    wire_events = providers.Resource(
        _wire_events,
        event_bus=event_bus,
        example_created_handler=example_created_handler,
        example_updated_handler=example_updated_handler,
        example_deleted_handler=example_deleted_handler,
    )


def _wire_events(
    event_bus,
    example_created_handler,
    example_updated_handler,
    example_deleted_handler,
):
    """
    将事件处理器连接到事件总线。
    """
    event_bus.subscribe(ExampleCreatedEvent, example_created_handler)
    event_bus.subscribe(ExampleUpdatedEvent, example_updated_handler)
    event_bus.subscribe(ExampleDeletedEvent, example_deleted_handler)
    
    return event_bus 
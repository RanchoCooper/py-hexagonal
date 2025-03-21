"""事件总线模块"""
from typing import Callable, Dict, List, Any
import logging
from functools import wraps
from pydispatch import dispatcher

from application.event.events import Event

# 设置日志
logger = logging.getLogger(__name__)


class EventBus:
    """事件总线，基于PyDispatcher实现"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
    
    def publish(self, event: Event) -> None:
        """发布事件
        
        Args:
            event: 要发布的事件
        """
        event_type = event.event_type
        logger.debug(f"发布事件: {event_type}")
        
        # 使用PyDispatcher发送事件
        dispatcher.send(signal=event_type, sender=self, event=event)
    
    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """订阅事件
        
        Args:
            event_type: 事件类型
            handler: 事件处理函数
        """
        logger.debug(f"订阅事件: {event_type}")
        
        # 添加到内部处理器字典
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        
        # 使用PyDispatcher连接事件处理器
        dispatcher.connect(
            receiver=self._dispatch_handler(handler),
            signal=event_type,
            sender=self
        )
    
    def _dispatch_handler(self, handler: Callable) -> Callable:
        """包装处理器以适配PyDispatcher"""
        @wraps(handler)
        def wrapper(sender, event, **kwargs):
            try:
                handler(event)
            except Exception as e:
                logger.error(f"事件处理失败: {e}")
        return wrapper
    
    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """取消订阅
        
        Args:
            event_type: 事件类型
            handler: 事件处理函数
        """
        logger.debug(f"取消订阅事件: {event_type}")
        
        # 从内部处理器字典移除
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
        
        # 断开PyDispatcher连接
        dispatcher.disconnect(
            receiver=self._dispatch_handler(handler),
            signal=event_type,
            sender=self
        )


# 全局事件总线单例
event_bus = EventBus()


def publish(event: Event) -> None:
    """发布事件到全局事件总线
    
    Args:
        event: 要发布的事件
    """
    event_bus.publish(event)


def subscribe(event_type: str) -> Callable:
    """事件订阅装饰器
    
    用法:
    @subscribe("user.created")
    def handle_user_created(event):
        # 处理事件
    
    Args:
        event_type: 要订阅的事件类型
    """
    def decorator(handler: Callable[[Event], None]) -> Callable:
        event_bus.subscribe(event_type, handler)
        return handler
    return decorator 
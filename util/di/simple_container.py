"""
简化的依赖注入容器，作为dependency-injector的替代。
此容器在Python 3.12上运行良好。
"""

from typing import Any, Callable, Dict, Optional, TypeVar

T = TypeVar('T')


class SimpleContainer:
    """
    简化的依赖注入容器，用于管理对象实例和工厂函数。
    """
    
    def __init__(self):
        """初始化容器"""
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[..., Any]] = {}
        self._configs: Dict[str, Any] = {}
    
    def register_singleton(self, name: str, instance: Any) -> None:
        """
        注册单例实例。
        
        Args:
            name: 实例的名称
            instance: 要存储的实例
        """
        self._singletons[name] = instance
    
    def register_factory(self, name: str, factory: Callable[..., T]) -> None:
        """
        注册工厂函数。
        
        Args:
            name: 工厂的名称
            factory: 创建实例的工厂函数
        """
        self._factories[name] = factory
    
    def get(self, name: str) -> Any:
        """
        获取注册的实例。
        
        Args:
            name: 要获取的实例的名称
            
        Returns:
            注册的实例
            
        Raises:
            KeyError: 如果找不到指定名称的实例
        """
        if name in self._singletons:
            return self._singletons[name]
        elif name in self._factories:
            return self._factories[name]()
        else:
            raise KeyError(f"No dependency registered with name: {name}")
    
    def set_config(self, key: str, value: Any) -> None:
        """
        设置配置值。
        
        Args:
            key: 配置键
            value: 配置值
        """
        self._configs[key] = value
    
    def get_config(self, key: str, default: Optional[Any] = None) -> Any:
        """
        获取配置值。
        
        Args:
            key: 配置键
            default: 如果键不存在，返回的默认值
            
        Returns:
            配置值或默认值
        """
        return self._configs.get(key, default)
    
    def from_dict(self, config_dict: Dict[str, Any]) -> None:
        """
        从字典加载配置。
        
        Args:
            config_dict: 包含配置的字典
        """
        for key, value in config_dict.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    self.set_config(f"{key}.{subkey}", subvalue)
            else:
                self.set_config(key, value) 
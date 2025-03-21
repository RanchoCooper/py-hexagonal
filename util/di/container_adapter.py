"""
容器适配器，提供与dependency-injector类似的API
"""

import sys
from typing import Any, Callable, Dict, Optional, TypeVar

from .simple_container import SimpleContainer

T = TypeVar('T')


class Provider:
    """提供者基类，模拟dependency-injector的提供者API"""
    
    def __init__(self):
        self._factory = None
    
    def __call__(self, *args, **kwargs):
        """
        调用提供者以获取实例
        """
        print(f"Provider.__call__: factory={self._factory}, args={args}, kwargs={kwargs}")
        # 始终调用provide方法，不管_factory是否被设置
        return self.provide(*args, **kwargs)
    
    def provide(self, *args, **kwargs) -> Any:
        """
        提供实例的方法（由子类实现）
        """
        raise NotImplementedError("Subclasses must implement provide method")


class Singleton(Provider):
    """
    单例提供者，类似于dependency-injector的Singleton
    """
    
    def __init__(self, factory: Callable[..., T], *args, **kwargs):
        """
        初始化单例提供者
        
        Args:
            factory: 用于创建实例的工厂函数或类
            *args: 传递给工厂的位置参数
            **kwargs: 传递给工厂的关键字参数
        """
        super().__init__()
        self._factory = factory
        self._args = args
        self._kwargs = kwargs
        self._instance = None
        print(f"Singleton.__init__: factory={factory}, args={args}, kwargs={kwargs}")
    
    def provide(self, *args, **kwargs) -> Any:
        """
        提供单例实例
        
        Returns:
            单例实例
        """
        print(f"Singleton.provide: instance={self._instance}, args={args}, kwargs={kwargs}")
        if self._instance is None:
            # 获取所有参数
            all_kwargs = {}
            for key, value in self._kwargs.items():
                # 如果值是lambda函数，则执行它
                if callable(value) and not isinstance(value, type):
                    print(f"  Calling callable kwarg: {key}={value}")
                    try:
                        all_kwargs[key] = value()
                    except Exception as e:
                        print(f"  Error calling {key}: {e}", file=sys.stderr)
                        raise
                else:
                    all_kwargs[key] = value
                    
            # 合并传入的关键字参数
            all_kwargs.update(kwargs)
            
            # 处理位置参数
            all_args = []
            for arg in self._args:
                if callable(arg) and not isinstance(arg, type):
                    print(f"  Calling callable arg: {arg}")
                    try:
                        all_args.append(arg())
                    except Exception as e:
                        print(f"  Error calling arg {arg}: {e}", file=sys.stderr)
                        raise
                else:
                    all_args.append(arg)
                    
            # 合并传入的位置参数
            if args:
                all_args.extend(args)
                
            print(f"  Creating instance with: factory={self._factory}, args={all_args}, kwargs={all_kwargs}")
            self._instance = self._factory(*all_args, **all_kwargs)
        return self._instance


class Factory(Provider):
    """
    工厂提供者，类似于dependency-injector的Factory
    """
    
    def __init__(self, factory: Callable[..., T], *args, **kwargs):
        """
        初始化工厂提供者
        
        Args:
            factory: 用于创建实例的工厂函数或类
            *args: 传递给工厂的位置参数
            **kwargs: 传递给工厂的关键字参数
        """
        super().__init__()
        self._factory = factory
        self._args = args
        self._kwargs = kwargs
        print(f"Factory.__init__: factory={factory}, args={args}, kwargs={kwargs}")
    
    def provide(self, *args, **kwargs) -> Any:
        """
        提供新实例
        
        Returns:
            新创建的实例
        """
        print(f"Factory.provide: args={args}, kwargs={kwargs}")
        # 获取所有参数
        all_kwargs = {}
        for key, value in self._kwargs.items():
            # 如果值是lambda函数，则执行它
            if callable(value) and not isinstance(value, type):
                print(f"  Calling callable kwarg: {key}={value}")
                try:
                    all_kwargs[key] = value()
                except Exception as e:
                    print(f"  Error calling {key}: {e}", file=sys.stderr)
                    raise
            else:
                all_kwargs[key] = value
                
        # 合并传入的关键字参数
        all_kwargs.update(kwargs)
        
        # 处理位置参数
        all_args = []
        for arg in self._args:
            if callable(arg) and not isinstance(arg, type):
                print(f"  Calling callable arg: {arg}")
                try:
                    all_args.append(arg())
                except Exception as e:
                    print(f"  Error calling arg {arg}: {e}", file=sys.stderr)
                    raise
            else:
                all_args.append(arg)
                
        # 合并传入的位置参数
        if args:
            all_args.extend(args)
            
        print(f"  Creating instance with: factory={self._factory}, args={all_args}, kwargs={all_kwargs}")
        return self._factory(*all_args, **all_kwargs)


class Resource(Provider):
    """
    资源提供者，类似于dependency-injector的Resource
    """
    
    def __init__(self, factory: Callable[..., T], *args, **kwargs):
        """
        初始化资源提供者
        
        Args:
            factory: 用于创建资源的工厂函数
            *args: 传递给工厂的位置参数
            **kwargs: 传递给工厂的关键字参数
        """
        super().__init__()
        self._factory = factory
        self._args = args
        self._kwargs = kwargs
        self._resource = None
        print(f"Resource.__init__: factory={factory}, args={args}, kwargs={kwargs}")
    
    def provide(self, *args, **kwargs) -> Any:
        """
        提供资源实例
        
        Returns:
            资源实例
        """
        print(f"Resource.provide: resource={self._resource}, args={args}, kwargs={kwargs}")
        if self._resource is None:
            # 获取所有参数
            all_kwargs = {}
            for key, value in self._kwargs.items():
                # 如果值是lambda函数，则执行它
                if callable(value) and not isinstance(value, type):
                    print(f"  Calling callable kwarg: {key}={value}")
                    try:
                        all_kwargs[key] = value()
                    except Exception as e:
                        print(f"  Error calling {key}: {e}", file=sys.stderr)
                        raise
                else:
                    all_kwargs[key] = value
                    
            # 合并传入的关键字参数
            all_kwargs.update(kwargs)
            
            # 处理位置参数
            all_args = []
            for arg in self._args:
                if callable(arg) and not isinstance(arg, type):
                    print(f"  Calling callable arg: {arg}")
                    try:
                        all_args.append(arg())
                    except Exception as e:
                        print(f"  Error calling arg {arg}: {e}", file=sys.stderr)
                        raise
                else:
                    all_args.append(arg)
                    
            # 合并传入的位置参数
            if args:
                all_args.extend(args)
                
            print(f"  Creating resource with: factory={self._factory}, args={all_args}, kwargs={all_kwargs}")
            self._resource = self._factory(*all_args, **all_kwargs)
        return self._resource


class Configuration:
    """
    配置提供者，类似于dependency-injector的Configuration
    """
    
    def __init__(self):
        """初始化配置提供者"""
        self._values = {}
    
    def from_dict(self, config: Dict[str, Any]) -> None:
        """
        从字典加载配置
        
        Args:
            config: 包含配置的字典
        """
        print(f"Configuration.from_dict: config={config}")
        self._values.update(config)
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        value = self._values.get(key, default)
        print(f"Configuration.get: key={key}, default={default}, value={value}")
        return value
    
    def __getitem__(self, key: str) -> Any:
        """
        使用字典语法获取配置值
        
        Args:
            key: 配置键
            
        Returns:
            配置值
            
        Raises:
            KeyError: 如果找不到配置键
        """
        if key in self._values:
            value = self._values[key]
            print(f"Configuration.__getitem__: key={key}, value={value}")
            return value
        print(f"Configuration.__getitem__: key={key} not found")
        raise KeyError(f"Configuration key '{key}' not found")


class Container:
    """
    依赖注入容器，与dependency-injector的Container类似
    """
    
    def __init__(self):
        """初始化容器"""
        self._providers = {}
        self._simple_container = SimpleContainer()
        self.config = Configuration()
        print(f"Container.__init__")
    
    def __getattr__(self, name: str) -> Any:
        """
        获取提供者或实例
        
        Args:
            name: 提供者或实例的名称
            
        Returns:
            提供者或实例
            
        Raises:
            AttributeError: 如果找不到提供者或实例
        """
        print(f"Container.__getattr__: name={name}, providers={list(self._providers.keys())}")
        if name in self._providers:
            print(f"  Found provider: {name}")
            return self._providers[name]
        
        # 检查是否是providers字典中的键，如果是返回实例
        for key, provider in self._providers.items():
            if name == key:
                print(f"  Calling provider: {name}")
                return provider()
        
        print(f"  Provider '{name}' not found")
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def register_provider(self, name: str, provider: Provider) -> None:
        """
        注册提供者
        
        Args:
            name: 提供者名称
            provider: 提供者实例
        """
        print(f"Container.register_provider: name={name}, provider={provider}")
        self._providers[name] = provider 
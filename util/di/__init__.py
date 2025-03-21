"""
依赖注入模块。
"""

# 在Python 3.12中，dependency-injector存在兼容性问题
# 因此我们提供了一个简化的替代容器实现

# 再导入适配器
from .container_adapter import Container, Factory, Resource, Singleton

# 先导入简单容器
from .simple_container import SimpleContainer


# 创建模拟providers命名空间
class _Providers:
    """提供者命名空间类"""
    
    Singleton = Singleton
    Factory = Factory
    Resource = Resource

# 模拟dependency-injector的providers命名空间
providers = _Providers()

__all__ = ["SimpleContainer", "Container", "providers"] 

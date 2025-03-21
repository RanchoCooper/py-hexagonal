"""
提供者模块，导出各种依赖注入提供者
"""

from .container_adapter import Factory, Provider, Resource, Singleton

__all__ = [
    "Singleton", 
    "Factory", 
    "Resource", 
    "Provider"
] 

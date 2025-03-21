"""依赖注入容器"""
from typing import Callable
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dependency_injector import containers, providers

from config.settings import get_config
from domain.repository.example import UserRepository, TaskRepository
from adapter.repository.example_repo import (
    SQLAlchemyUserRepository, SQLAlchemyTaskRepository, Base
)

# 设置日志
logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    """依赖注入容器"""
    
    # 配置
    config = providers.Singleton(get_config)
    
    # 数据库引擎
    engine = providers.Singleton(
        lambda config: create_engine(config.DB_URI),
        config=config
    )
    
    # 会话工厂
    session_factory = providers.Singleton(
        lambda engine: scoped_session(sessionmaker(bind=engine)),
        engine=engine
    )
    
    # 初始化数据库
    db_init = providers.Resource(
        lambda engine: Base.metadata.create_all(engine),
        engine=engine
    )
    
    # 仓库
    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session=session_factory
    )
    
    task_repository = providers.Factory(
        SQLAlchemyTaskRepository,
        session=session_factory
    )


# 全局容器实例
container = Container()


def get_container() -> Container:
    """获取全局容器实例"""
    return container


def inject(dependency_name: str) -> Callable:
    """依赖注入装饰器
    
    用法:
    @inject('user_repository')
    def some_function(user_repository, ...):
        # 使用user_repository
    
    Args:
        dependency_name: 要注入的依赖名称
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if dependency_name not in kwargs:
                # 从容器中获取依赖
                dependency = getattr(container, dependency_name)()
                kwargs[dependency_name] = dependency
            return func(*args, **kwargs)
        return wrapper
    return decorator 
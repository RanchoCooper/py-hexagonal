"""事务管理模块"""
from typing import Any, Callable, TypeVar, cast
from functools import wraps
import contextlib
from sqlalchemy.orm import Session

from util.errors import DatabaseError

T = TypeVar('T')


@contextlib.contextmanager
def transaction_context(session: Session):
    """事务上下文管理器
    
    用法:
    with transaction_context(session) as tx:
        # 执行数据库操作
    """
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise DatabaseError(message=f"事务执行失败: {str(e)}", details={"error": str(e)})


def transactional(func: Callable[..., T]) -> Callable[..., T]:
    """事务装饰器
    
    用法:
    @transactional
    def some_function(session, ...):
        # 执行数据库操作
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # 查找session参数
        session = None
        
        # 从位置参数中查找session
        for arg in args:
            if isinstance(arg, Session):
                session = arg
                break
        
        # 从关键字参数中查找session
        if session is None:
            session = kwargs.get('session')
        
        if session is None:
            raise ValueError("未找到Session参数，无法执行事务")
        
        with transaction_context(session):
            return func(*args, **kwargs)
    
    return cast(Callable[..., T], wrapper) 
"""
Base repository implementation for SQLAlchemy.

This module provides a base class for SQLAlchemy-based repositories
that can dynamically choose which database to use.
"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from adapter.repository import db_registry


class BaseSQLAlchemyRepository:
    """
    基础SQLAlchemy仓储实现
    
    提供基本的数据库操作和动态选择数据库的能力
    """
    
    def __init__(self, db_name=None):
        """
        初始化仓储
        
        Args:
            db_name: 要使用的数据库名称，为None则使用默认数据库
        """
        self._db_name = db_name
    
    @property
    def _session(self) -> Session:
        """
        获取当前会话
        
        Returns:
            SQLAlchemy Session实例
        """
        return db_registry.get_session(self._db_name)
    
    def _commit(self):
        """提交事务"""
        try:
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e
    
    def _rollback(self):
        """回滚事务"""
        self._session.rollback() 
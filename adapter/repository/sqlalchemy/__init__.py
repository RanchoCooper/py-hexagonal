"""SQLAlchemy repository adapters for data persistence."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from adapter.repository.sqlalchemy.models import Base


def create_mysql_engine(url, echo=False):
    """
    创建MySQL数据库引擎
    
    Args:
        url: MySQL数据库连接URL
        echo: 是否输出SQL语句（调试用）
        
    Returns:
        SQLAlchemy Engine实例
    """
    return create_engine(url, echo=echo)


def create_postgresql_engine(url, echo=False):
    """
    创建PostgreSQL数据库引擎
    
    Args:
        url: PostgreSQL数据库连接URL
        echo: 是否输出SQL语句（调试用）
        
    Returns:
        SQLAlchemy Engine实例
    """
    return create_engine(url, echo=echo)


def create_session_factory(engine):
    """
    创建数据库会话工厂
    
    Args:
        engine: SQLAlchemy引擎实例
        
    Returns:
        SQLAlchemy会话工厂
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_scoped_session(session_factory):
    """
    创建线程安全的数据库会话
    
    Args:
        session_factory: SQLAlchemy会话工厂
        
    Returns:
        线程安全的SQLAlchemy会话
    """
    return scoped_session(session_factory)


def initialize_database(engine):
    """
    初始化数据库架构
    
    Args:
        engine: SQLAlchemy引擎实例
    """
    Base.metadata.create_all(engine) 
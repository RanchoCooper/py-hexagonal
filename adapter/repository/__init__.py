"""
Repository adapters package.

This package contains adapter implementations for the domain repositories.
"""

class DatabaseRegistry:
    """数据库注册表，管理不同的数据库连接"""

    def __init__(self):
        self._engines = {}
        self._sessions = {}
        self._default = None

    def register(self, name, engine, session):
        """
        注册一个数据库连接
        
        Args:
            name: 数据库连接名称
            engine: SQLAlchemy Engine实例
            session: SQLAlchemy Session实例
        """
        self._engines[name] = engine
        self._sessions[name] = session
        if self._default is None:
            self._default = name

    def set_default(self, name):
        """
        设置默认数据库连接
        
        Args:
            name: 数据库连接名称
        """
        if name not in self._engines:
            raise ValueError(f"No database registered with name '{name}'")
        self._default = name

    def get_engine(self, name=None):
        """
        获取数据库引擎
        
        Args:
            name: 数据库连接名称，为None则返回默认连接
            
        Returns:
            SQLAlchemy Engine实例
        """
        if name is None:
            name = self._default
        if name not in self._engines:
            raise ValueError(f"No database registered with name '{name}'")
        return self._engines[name]

    def get_session(self, name=None):
        """
        获取数据库会话
        
        Args:
            name: 数据库连接名称，为None则返回默认连接
            
        Returns:
            SQLAlchemy Session实例
        """
        if name is None:
            name = self._default
        if name not in self._sessions:
            raise ValueError(f"No database registered with name '{name}'")
        return self._sessions[name]


# 创建全局数据库注册表实例
db_registry = DatabaseRegistry()

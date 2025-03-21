"""
MySQL数据库连接适配器。

提供与MySQL数据库的连接和查询功能。
"""

import sys
from typing import Any, Dict, List, Optional


class MySQLConnection:
    """MySQL数据库连接类"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: str = "",
        charset: str = "utf8mb4",
        pool_size: int = 5,
        pool_recycle: int = 3600,
    ):
        """
        初始化MySQL连接
        
        Args:
            host: 数据库主机地址
            port: 数据库端口
            user: 用户名
            password: 密码
            database: 数据库名
            charset: 字符集
            pool_size: 连接池大小
            pool_recycle: 连接重用时间(秒)
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.pool_size = pool_size
        self.pool_recycle = pool_recycle
        self._engine = None
        
        print(f"初始化MySQL连接: {host}:{port}/{database} (用户: {user})")
    
    def connect(self) -> None:
        """连接到MySQL数据库"""
        try:
            # 尝试导入所需的模块
            import sqlalchemy
            from sqlalchemy import create_engine
            
            connection_str = (
                f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
                f"?charset={self.charset}"
            )
            self._engine = create_engine(
                connection_str,
                pool_size=self.pool_size,
                pool_recycle=self.pool_recycle
            )
            print(f"已连接到MySQL: {self.host}:{self.port}/{self.database}")
        except ImportError:
            print("错误: 无法导入sqlalchemy或pymysql模块。请使用pip安装: pip install sqlalchemy pymysql", file=sys.stderr)
            raise
        except Exception as e:
            print(f"连接MySQL时出错: {e}", file=sys.stderr)
            raise
    
    def execute(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        执行SQL查询
        
        Args:
            sql: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果
        """
        if self._engine is None:
            self.connect()
            
        if params is None:
            params = {}
            
        try:
            with self._engine.connect() as connection:
                if sql.strip().lower().startswith("select"):
                    # 处理SELECT查询
                    result = connection.execute(sql, params)
                    return [dict(row) for row in result]
                else:
                    # 处理其他类型的查询
                    connection.execute(sql, params)
                    return []
        except Exception as e:
            print(f"执行SQL时出错: {e}", file=sys.stderr)
            raise
    
    def close(self) -> None:
        """关闭数据库连接"""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            print(f"已关闭MySQL连接: {self.host}:{self.port}/{self.database}") 
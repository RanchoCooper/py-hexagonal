"""
数据库提供者模块，为依赖注入容器提供MySQL和Redis连接提供者。
"""

from typing import Optional

from util.di.container_adapter import Resource

from .mysql import MySQLConnection
from .redis import RedisConnection


class MySQLProvider(Resource):
    """MySQL数据库连接提供者"""
    
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
        初始化MySQL提供者
        
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
        super().__init__(
            MySQLConnection,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            pool_size=pool_size,
            pool_recycle=pool_recycle,
        )


class RedisProvider(Resource):
    """Redis连接提供者"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5,
    ):
        """
        初始化Redis提供者
        
        Args:
            host: Redis主机地址
            port: Redis端口
            db: Redis数据库索引
            password: Redis密码
            decode_responses: 是否解码响应
            socket_timeout: Socket超时时间
            socket_connect_timeout: Socket连接超时时间
        """
        super().__init__(
            RedisConnection,
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
        ) 
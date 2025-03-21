"""
Redis数据库连接适配器。

提供与Redis数据库的连接和操作功能。
"""

import sys
from typing import Any, Optional


class RedisConnection:
    """Redis连接类"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5,
        connection_pool: Optional[Any] = None,
    ):
        """
        初始化Redis连接
        
        Args:
            host: Redis主机地址
            port: Redis端口
            db: Redis数据库索引
            password: Redis密码
            decode_responses: 是否解码响应
            socket_timeout: Socket超时时间
            socket_connect_timeout: Socket连接超时时间
            connection_pool: 连接池对象
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout
        self.connection_pool = connection_pool
        self._client = None
        
        print(f"初始化Redis连接: {host}:{port} 数据库: {db}")
    
    def connect(self) -> None:
        """连接到Redis服务器"""
        try:
            # 尝试导入redis模块
            import redis
            
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=self.decode_responses,
                socket_timeout=self.socket_timeout,
                socket_connect_timeout=self.socket_connect_timeout,
                connection_pool=self.connection_pool,
            )
            
            # 测试连接
            self._client.ping()
            print(f"已连接到Redis: {self.host}:{self.port} 数据库: {self.db}")
        except ImportError:
            print("错误: 无法导入redis模块。请使用pip安装: pip install redis", file=sys.stderr)
            raise
        except Exception as e:
            print(f"连接Redis时出错: {e}", file=sys.stderr)
            raise
    
    def get(self, key: str) -> Any:
        """
        获取键值
        
        Args:
            key: 键名
            
        Returns:
            键值
        """
        if self._client is None:
            self.connect()
            
        return self._client.get(key)
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        设置键值
        
        Args:
            key: 键名
            value: 键值
            ex: 过期时间(秒)
            
        Returns:
            操作是否成功
        """
        if self._client is None:
            self.connect()
            
        return self._client.set(key, value, ex=ex)
    
    def delete(self, key: str) -> int:
        """
        删除键
        
        Args:
            key: 键名
            
        Returns:
            删除的键数量
        """
        if self._client is None:
            self.connect()
            
        return self._client.delete(key)
    
    def hash_get(self, name: str, key: str) -> Any:
        """
        获取哈希表中的字段值
        
        Args:
            name: 哈希表名
            key: 字段名
            
        Returns:
            字段值
        """
        if self._client is None:
            self.connect()
            
        return self._client.hget(name, key)
    
    def hash_set(self, name: str, key: str, value: Any) -> int:
        """
        设置哈希表中的字段值
        
        Args:
            name: 哈希表名
            key: 字段名
            value: 字段值
            
        Returns:
            1表示新创建字段，0表示更新字段
        """
        if self._client is None:
            self.connect()
            
        return self._client.hset(name, key, value)
    
    def publish(self, channel: str, message: str) -> int:
        """
        发布消息到频道
        
        Args:
            channel: 频道名
            message: 消息内容
            
        Returns:
            接收消息的客户端数量
        """
        if self._client is None:
            self.connect()
            
        return self._client.publish(channel, message)
    
    def close(self) -> None:
        """关闭Redis连接"""
        if self._client is not None:
            self._client.close()
            self._client = None
            print(f"已关闭Redis连接: {self.host}:{self.port} 数据库: {self.db}") 
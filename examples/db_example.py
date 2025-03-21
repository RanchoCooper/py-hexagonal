"""
数据库连接示例

演示如何使用MySQL和Redis连接适配器
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from adapter.repository.mysql import MySQLConnection
from adapter.repository.providers import MySQLProvider, RedisProvider
from adapter.repository.redis import RedisConnection
from util.di import Container, providers


# 创建一个用于存储用户数据的简单服务
class UserService:
    """用户服务，演示如何使用MySQL和Redis"""
    
    def __init__(self, mysql_connection: MySQLConnection, redis_connection: RedisConnection):
        """
        初始化用户服务
        
        Args:
            mysql_connection: MySQL连接
            redis_connection: Redis连接
        """
        self.mysql = mysql_connection
        self.redis = redis_connection
        print("用户服务已初始化")
    
    def get_user(self, user_id: int) -> dict:
        """
        获取用户信息
        
        首先尝试从Redis缓存获取，如果没有再从MySQL数据库获取并缓存
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户信息
        """
        # 尝试从缓存获取
        cache_key = f"user:{user_id}"
        cached_user = self.redis.get(cache_key)
        
        if cached_user:
            print(f"从缓存获取用户 {user_id}")
            return {"id": user_id, "name": cached_user, "source": "cache"}
        
        # 模拟从数据库获取
        print(f"从数据库获取用户 {user_id}")
        user_data = {"id": user_id, "name": f"用户_{user_id}", "source": "database"}
        
        # 存入缓存
        self.redis.set(cache_key, user_data["name"], ex=3600)  # 1小时过期
        
        return user_data


# 创建并配置容器
def create_container():
    """创建并配置依赖注入容器"""
    container = Container()
    
    # 配置
    container.config.from_dict({
        "database": {
            "mysql": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "password",
                "database": "users_db"
            },
            "redis": {
                "host": "localhost",
                "port": 6379,
                "db": 0
            }
        }
    })
    
    # 注册MySQL提供者
    container.register_provider(
        "mysql",
        MySQLProvider(
            host=container.config["database"]["mysql"]["host"],
            port=container.config["database"]["mysql"]["port"],
            user=container.config["database"]["mysql"]["user"],
            password=container.config["database"]["mysql"]["password"],
            database=container.config["database"]["mysql"]["database"]
        )
    )
    
    # 注册Redis提供者
    container.register_provider(
        "redis",
        RedisProvider(
            host=container.config["database"]["redis"]["host"],
            port=container.config["database"]["redis"]["port"],
            db=container.config["database"]["redis"]["db"]
        )
    )
    
    # 注册用户服务
    container.register_provider(
        "user_service",
        providers.Singleton(
            UserService,
            mysql_connection=lambda: container.mysql(),
            redis_connection=lambda: container.redis()
        )
    )
    
    return container


def main():
    """主函数，模拟应用程序入口"""
    print("初始化应用...")
    
    # 创建一个模拟的环境（不实际连接数据库和Redis）
    container = create_container()
    
    try:
        # 获取用户服务
        print("\n获取用户服务...")
        user_service = container.user_service()
        
        # 模拟获取用户
        print("\n第一次获取用户（应从数据库获取）:")
        user1 = user_service.get_user(42)
        print(f"获取到用户: {user1}")
        
        print("\n第二次获取同一用户（应从缓存获取）:")
        user2 = user_service.get_user(42)
        print(f"获取到用户: {user2}")
        
        print("\n获取另一个用户（应从数据库获取）:")
        user3 = user_service.get_user(100)
        print(f"获取到用户: {user3}")
        
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n应用已完成")


if __name__ == "__main__":
    main() 
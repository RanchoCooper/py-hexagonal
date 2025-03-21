"""
依赖注入示例模块。

演示如何使用我们自定义的依赖注入容器（Python 3.12兼容版本）。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict, List

from util.di import Container, providers


# 定义一些示例类
class Database:
    """示例数据库类"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        print(f"Connecting to database: {connection_string}")
    
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """执行查询"""
        print(f"Executing SQL query: {sql}")
        return [{"id": 1, "name": "Example"}]


class Repository:
    """示例仓库类"""
    
    def __init__(self, database: Database):
        self.database = database
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有记录"""
        return self.database.query("SELECT * FROM examples")


class Service:
    """示例服务类"""
    
    def __init__(self, repository: Repository):
        self.repository = repository
    
    def get_all_examples(self) -> List[Dict[str, Any]]:
        """获取所有示例"""
        return self.repository.get_all()


class DbProvider:
    """数据库提供者类，用于解决循环依赖"""
    
    def __init__(self, container):
        """
        初始化数据库提供者
        
        Args:
            container: 容器实例
        """
        self.container = container
    
    def __call__(self) -> Database:
        """
        提供数据库实例
        
        Returns:
            数据库实例
        """
        return self.container.database()


class RepoProvider:
    """仓库提供者类，用于解决循环依赖"""
    
    def __init__(self, container):
        """
        初始化仓库提供者
        
        Args:
            container: 容器实例
        """
        self.container = container
    
    def __call__(self) -> Repository:
        """
        提供仓库实例
        
        Returns:
            仓库实例
        """
        return self.container.repository()


# 创建并配置容器
class AppContainer(Container):
    """应用程序容器"""
    
    def __init__(self):
        super().__init__()
        
        # 配置
        self.config.from_dict({
            "database": {
                "connection_string": "postgres://user:password@localhost:5432/examples"
            }
        })
        
        # 注册提供者
        self.register_provider(
            "database",
            providers.Singleton(
                Database,
                connection_string=self.config["database"]["connection_string"]
            )
        )
        
        # 创建提供者
        db_provider = DbProvider(self)
        
        self.register_provider(
            "repository",
            providers.Singleton(
                Repository,
                database=db_provider
            )
        )
        
        # 创建提供者
        repo_provider = RepoProvider(self)
        
        self.register_provider(
            "service",
            providers.Singleton(
                Service,
                repository=repo_provider
            )
        )


# 使用示例
def main():
    """主函数"""
    # 创建和配置容器
    container = AppContainer()
    
    # 获取服务
    service = container.service()
    
    # 使用服务
    examples = service.get_all_examples()
    print(f"Found examples: {examples}")


if __name__ == "__main__":
    main() 
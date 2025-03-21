"""
基本依赖注入示例。

展示依赖注入容器的简单用法。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.di import Container, providers


# 定义一些简单的类
class Logger:
    """简单的日志记录器"""
    
    def __init__(self, prefix: str = ""):
        self.prefix = prefix
    
    def log(self, message: str) -> None:
        """记录消息"""
        print(f"{self.prefix}[日志] {message}")


class Config:
    """配置类"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
    
    def is_debug(self) -> bool:
        """是否处于调试模式"""
        return self.debug


class UserService:
    """用户服务"""
    
    def __init__(self, logger: Logger, config: Config):
        self.logger = logger
        self.config = config
    
    def get_user(self, user_id: int) -> dict:
        """获取用户信息"""
        self.logger.log(f"获取用户ID: {user_id}")
        if self.config.is_debug():
            self.logger.log("调试模式: 返回模拟数据")
        
        # 模拟数据
        return {"id": user_id, "name": f"用户_{user_id}", "age": 30}


# 创建容器
container = Container()

# 添加配置
container.config.from_dict({
    "app": {
        "debug": True,
        "log_prefix": "[应用] "
    }
})

# 注册日志记录器
container.register_provider(
    "logger",
    providers.Singleton(
        Logger,
        prefix=lambda: container.config["app"]["log_prefix"]
    )
)

# 注册配置
container.register_provider(
    "app_config",  # 重命名为app_config以避免与container.config混淆
    providers.Singleton(
        Config,
        debug=lambda: container.config["app"]["debug"]
    )
)

# 注册用户服务
container.register_provider(
    "user_service",
    providers.Singleton(
        UserService,
        logger=lambda: container.logger(),
        config=lambda: container.app_config()  # 使用app_config而不是config
    )
)


# 使用示例
def main():
    """主函数"""
    # 从容器获取服务
    user_service = container.user_service()
    
    # 使用服务
    user = user_service.get_user(42)
    print(f"获取到用户: {user}")


if __name__ == "__main__":
    main() 
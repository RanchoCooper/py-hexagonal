"""
简单DI测试脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.di import Container, providers


# 定义一个简单的类
class Simple:
    def __init__(self, value: str):
        self.value = value
        print(f"创建Simple实例，值为：{value}")
    
    def get_value(self):
        return self.value


# 创建并配置容器
container = Container()

# 添加一些配置
container.config.from_dict({
    "app": {
        "value": "测试值"
    }
})

# 注册提供者 - 直接使用值
container.register_provider(
    "simple1",
    providers.Singleton(
        Simple,
        value="直接值"
    )
)

# 注册提供者 - 使用配置值
container.register_provider(
    "simple2",
    providers.Singleton(
        Simple,
        value=lambda: container.config["app"]["value"]
    )
)

# 主函数
def main():
    print("获取实例1")
    instance1 = container.simple1()
    print(f"实例1的值：{instance1.get_value()}")
    
    print("\n获取实例2")
    instance2 = container.simple2()
    print(f"实例2的值：{instance2.get_value()}")


if __name__ == "__main__":
    main() 
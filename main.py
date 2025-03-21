"""主程序入口"""
import os
import logging

from adapter.api.rest import create_app
from config.settings import get_config
import adapter.event.handlers  # 导入事件处理器，使其注册

# 获取配置
config = get_config()

# 设置根日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """程序主入口"""
    # 创建Flask应用
    app = create_app()
    
    # 运行应用
    logger.info(f"启动应用于 {config.HOST}:{config.PORT}, 环境: {config.ENV}")
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )


if __name__ == "__main__":
    main()

"""REST API适配器"""
import logging
from flask import Flask
from flask.logging import default_handler

from config.settings import get_config
from api.routes import api_blueprint
from api.middleware import error_handler, request_logger
from application.di.container import container

# 获取配置
config = get_config()

# 设置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """创建Flask应用
    
    Returns:
        配置好的Flask应用实例
    """
    # 创建应用
    app = Flask(__name__)
    
    # 配置应用
    app.config.from_object(config)
    
    # 注册中间件
    error_handler(app)
    request_logger(app)
    
    # 注册蓝图
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # 初始化数据库
    with app.app_context():
        container.db_init()
    
    # 路由信息日志
    logger.info("已注册的路由:")
    for rule in app.url_map.iter_rules():
        logger.info(f"{rule.endpoint}: {rule.rule} {rule.methods}")
    
    return app

import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 应用配置
class Config:
    """应用配置类"""
    # 基础配置
    ENV = os.getenv('ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # 服务配置
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    
    # 数据库配置
    DB_URI = os.getenv('DB_URI', 'sqlite:///app.db')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 环境特定配置
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DB_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # 必须设置

# 配置映射
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# 获取当前配置
def get_config():
    """获取当前环境配置"""
    env = os.getenv('ENV', 'development')
    return config_by_name[env] 
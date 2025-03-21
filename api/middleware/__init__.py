"""API中间件模块"""
import time
import logging
from functools import wraps
from typing import Callable, Dict, Any
from flask import request, jsonify, g

from util.errors import AppError, AuthenticationError

# 设置日志
logger = logging.getLogger(__name__)


def error_handler(app):
    """错误处理中间件
    
    Args:
        app: Flask应用实例
    """
    @app.errorhandler(AppError)
    def handle_app_error(error):
        """处理应用异常"""
        logger.error(f"应用错误: {error.message}")
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """处理通用异常"""
        logger.error(f"未处理的异常: {str(error)}", exc_info=True)
        app_error = AppError.from_exception(error)
        response = jsonify(app_error.to_dict())
        response.status_code = app_error.status_code
        return response


def request_logger(app):
    """请求日志中间件
    
    Args:
        app: Flask应用实例
    """
    @app.before_request
    def log_request():
        """记录请求开始"""
        g.start_time = time.time()
        logger.info(f"开始请求: {request.method} {request.path}")
        
    @app.after_request
    def log_response(response):
        """记录请求结束"""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            logger.info(f"结束请求: {request.method} {request.path} - "
                      f"状态码: {response.status_code}, 耗时: {elapsed:.4f}s")
        return response


def auth_required(func: Callable) -> Callable:
    """认证中间件装饰器
    
    用法:
    @auth_required
    def some_route():
        # 受保护的路由
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 从请求头获取令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationError(message="缺少认证令牌")
        
        # 检查令牌格式
        try:
            auth_type, token = auth_header.split(None, 1)
        except ValueError:
            raise AuthenticationError(message="认证令牌格式无效")
        
        if auth_type.lower() != 'bearer':
            raise AuthenticationError(message="认证类型必须为Bearer")
        
        # 验证令牌 (实际项目中应实现真正的JWT验证)
        if not token or token == 'invalid':
            raise AuthenticationError(message="认证令牌无效")
        
        # 令牌有效，可以在g对象中存储用户信息
        g.user_id = "user-123"  # 示例用户ID，实际应从令牌中解析
        
        return func(*args, **kwargs)
    return wrapper 
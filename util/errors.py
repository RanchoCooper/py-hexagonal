"""错误处理模块"""
from typing import Dict, Any, Optional
import traceback
import logging

# 设置日志
logger = logging.getLogger(__name__)

class AppError(Exception):
    """应用基础异常"""
    def __init__(
        self, 
        message: str = "发生了应用错误", 
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转化为字典表示"""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }
    
    @classmethod
    def from_exception(cls, exc: Exception) -> 'AppError':
        """从异常创建AppError"""
        logger.error(f"捕获异常: {exc}")
        logger.debug(traceback.format_exc())
        if isinstance(exc, AppError):
            return exc
        return cls(message=str(exc))


class NotFoundError(AppError):
    """资源未找到异常"""
    def __init__(
        self, 
        message: str = "资源未找到", 
        code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, code=code, status_code=404, details=details)


class ValidationError(AppError):
    """数据验证错误"""
    def __init__(
        self, 
        message: str = "数据验证失败", 
        code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, code=code, status_code=400, details=details)


class AuthenticationError(AppError):
    """认证错误"""
    def __init__(
        self, 
        message: str = "认证失败", 
        code: str = "AUTHENTICATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, code=code, status_code=401, details=details)


class AuthorizationError(AppError):
    """授权错误"""
    def __init__(
        self, 
        message: str = "没有操作权限", 
        code: str = "AUTHORIZATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, code=code, status_code=403, details=details)


class DatabaseError(AppError):
    """数据库错误"""
    def __init__(
        self, 
        message: str = "数据库操作失败", 
        code: str = "DATABASE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, code=code, status_code=500, details=details) 
"""用例基类"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict, Any

# 定义输入和输出类型变量
I = TypeVar('I')  # 输入参数类型
O = TypeVar('O')  # 输出结果类型


class UseCase(Generic[I, O], ABC):
    """用例基类，定义用例接口"""
    
    @abstractmethod
    def execute(self, input_data: I) -> O:
        """执行用例
        
        Args:
            input_data: 用例输入数据
            
        Returns:
            用例输出结果
        """
        pass 
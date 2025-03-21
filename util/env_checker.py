"""
环境变量检查工具。
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set


class EnvChecker:
    """
    环境变量检查器。
    检查必需的环境变量是否已设置。
    """
    
    def __init__(self, env_file: Optional[Path] = None, env_example_file: Optional[Path] = None):
        """
        初始化环境检查器。
        
        参数:
            env_file (Optional[Path]): .env 文件的路径。默认为 None。
            env_example_file (Optional[Path]): .env.example 文件的路径。默认为 None。
        """
        self.env_file = env_file
        self.env_example_file = env_example_file
        
        if self.env_file is None and self.env_example_file is None:
            # 相对于此文件的默认路径
            config_dir = Path(__file__).parent.parent / "config"
            self.env_file = config_dir / ".env"
            self.env_example_file = config_dir / ".env.example"
    
    def get_required_vars(self) -> Set[str]:
        """
        从 .env.example 文件获取必需的环境变量。
        
        返回:
            Set[str]: 必需环境变量名称的集合。
        """
        required_vars = set()
        
        # 首先尝试 .env.example
        if self.env_example_file and self.env_example_file.exists():
            with open(self.env_example_file, "r") as f:
                for line in f:
                    line = line.strip()
                    # 跳过注释和空行
                    if not line or line.startswith("#"):
                        continue
                    
                    # 提取变量名
                    if "=" in line:
                        var_name = line.split("=", 1)[0].strip()
                        required_vars.add(var_name)
        
        return required_vars
    
    def check_env_vars(self, required_vars: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        检查必需的环境变量是否已设置。
        
        参数:
            required_vars (Optional[List[str]]): 必需环境变量的列表。
                如果为 None，则从 .env.example 中提取必需变量。
            
        返回:
            Dict[str, bool]: 将变量名映射到它们是否已设置的字典。
        """
        if required_vars is None:
            required_vars = list(self.get_required_vars())
        
        result = {}
        for var in required_vars:
            result[var] = var in os.environ
        
        return result
    
    def get_missing_vars(self, required_vars: Optional[List[str]] = None) -> List[str]:
        """
        获取缺失的环境变量列表。
        
        参数:
            required_vars (Optional[List[str]]): 必需环境变量的列表。
                如果为 None，则从 .env.example 中提取必需变量。
            
        返回:
            List[str]: 缺失的环境变量名称列表。
        """
        check_result = self.check_env_vars(required_vars)
        return [var for var, is_set in check_result.items() if not is_set]
    
    def check_and_exit(self, required_vars: Optional[List[str]] = None) -> None:
        """
        检查必需的环境变量是否已设置，如果有任何缺失则退出。
        
        参数:
            required_vars (Optional[List[str]]): 必需环境变量的列表。
                如果为 None，则从 .env.example 中提取必需变量。
        """
        missing_vars = self.get_missing_vars(required_vars)
        
        if missing_vars:
            print(f"错误: 缺少必需的环境变量: {', '.join(missing_vars)}")
            
            # 提供指导
            if self.env_file:
                if self.env_file.exists():
                    print(f"请检查并更新 {self.env_file} 文件。")
                else:
                    print(f"请创建一个包含必需变量的 {self.env_file} 文件。")
                    
                    if self.env_example_file and self.env_example_file.exists():
                        print(f"您可以使用 {self.env_example_file} 作为模板。")
            
            sys.exit(1)


def check_environment(required_vars: Optional[List[str]] = None) -> None:
    """
    检查必需的环境变量是否已设置，如果有任何缺失则退出。
    
    参数:
        required_vars (Optional[List[str]]): 必需环境变量的列表。
            如果为 None，则从 .env.example 中提取必需变量。
    """
    checker = EnvChecker()
    checker.check_and_exit(required_vars) 
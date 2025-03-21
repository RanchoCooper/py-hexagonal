"""
架构验证工具，确保项目遵循六边形架构原则。

该模块提供功能来检查应用程序不同部分之间的导入是否
遵守六边形架构的依赖规则。
"""

import os
import re
import sys
from typing import Dict, List, Set, Tuple


class ArchitectureChecker:
    """
    检查项目是否遵循六边形架构原则。
    """

    # 按从内到外的顺序定义层
    LAYERS = ["domain", "application", "adapter", "api", "cmd"]
    
    # 定义层之间允许的依赖关系
    # 每一层只允许从索引较低或相同的层导入
    ALLOWED_DEPENDENCIES = {
        "domain": ["domain"],
        "application": ["domain", "application"],
        "adapter": ["domain", "application", "adapter"],
        "api": ["domain", "application", "api"],
        "cmd": ["domain", "application", "adapter", "api", "cmd", "config", "util"],
        "config": ["config"],
        "util": ["util"],
    }
    
    # 从检查中排除的文件
    EXCLUDE_PATTERNS = [
        r"__pycache__",
        r"\.git",
        r"\.venv",
        r"\.pytest_cache",
        r"\.mypy_cache",
        r"\.idea",
        r"\.vscode",
    ]
    
    def __init__(self, project_root: str = None):
        """
        初始化架构检查器。
        
        参数:
            project_root (str, optional): 要检查的项目的根目录。
                如果未提供，则使用当前工作目录。
        """
        self.project_root = project_root or os.getcwd()
        self.violations: List[str] = []
    
    def is_excluded(self, path: str) -> bool:
        """
        检查路径是否应从检查中排除。
        
        参数:
            path (str): 要检查的路径。
            
        返回:
            bool: 如果路径应被排除则为True，否则为False。
        """
        return any(re.search(pattern, path) for pattern in self.EXCLUDE_PATTERNS)
    
    def get_layer_from_path(self, path: str) -> str:
        """
        从文件路径获取层。
        
        参数:
            path (str): Python文件的路径。
            
        返回:
            str: 层名称，如果路径不匹配任何层则为None。
        """
        relative_path = os.path.relpath(path, self.project_root)
        parts = relative_path.split(os.path.sep)
        
        if parts and parts[0] in self.ALLOWED_DEPENDENCIES:
            return parts[0]
        return None
    
    def extract_imports(self, file_path: str) -> List[str]:
        """
        从Python文件中提取导入。
        
        参数:
            file_path (str): Python文件的路径。
            
        返回:
            List[str]: 导入模块的列表。
        """
        imports = []
        import_pattern = re.compile(r'^from\s+(\S+)\s+import\s+|^import\s+(\S+)')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = import_pattern.match(line.strip())
                if match:
                    # 获取非None的组
                    module = match.group(1) or match.group(2)
                    imports.append(module)
        
        return imports
    
    def get_layer_from_import(self, import_stmt: str) -> str:
        """
        从导入语句获取层。
        
        参数:
            import_stmt (str): 导入语句（例如，'domain.model.entity'）。
            
        返回:
            str: 层名称，如果导入不匹配任何层则为None。
        """
        parts = import_stmt.split('.')
        if parts and parts[0] in self.ALLOWED_DEPENDENCIES:
            return parts[0]
        return None
    
    def check_file(self, file_path: str) -> None:
        """
        检查单个Python文件是否存在架构违规。
        
        参数:
            file_path (str): Python文件的路径。
        """
        # 跳过排除的文件
        if self.is_excluded(file_path):
            return
        
        # 只检查Python文件
        if not file_path.endswith('.py'):
            return
        
        source_layer = self.get_layer_from_path(file_path)
        if not source_layer:
            return
        
        imports = self.extract_imports(file_path)
        for import_stmt in imports:
            target_layer = self.get_layer_from_import(import_stmt)
            
            # 跳过不属于我们项目的导入
            if not target_layer:
                continue
            
            # 检查导入是否允许
            if target_layer not in self.ALLOWED_DEPENDENCIES[source_layer]:
                violation = (
                    f"架构违规，位于 {file_path}:\n"
                    f"  {source_layer} 不应该从 {target_layer} 导入\n"
                    f"  导入: {import_stmt}"
                )
                self.violations.append(violation)
    
    def check_project(self) -> List[str]:
        """
        检查整个项目是否存在架构违规。
        
        返回:
            List[str]: 架构违规的列表。
        """
        self.violations = []
        
        for root, _, files in os.walk(self.project_root):
            if self.is_excluded(root):
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                self.check_file(file_path)
        
        return self.violations
    
    def print_violations(self) -> None:
        """打印所有架构违规。"""
        if not self.violations:
            print("未发现架构违规。")
            return
        
        print(f"发现 {len(self.violations)} 个架构违规:")
        for violation in self.violations:
            print(f"\n{violation}")


def main() -> int:
    """
    架构检查器的主入口点。
    
    返回:
        int: 退出代码（如果没有违规则为0，否则为1）。
    """
    # 使用提供的路径或当前目录
    project_root = sys.argv[1] if len(sys.argv) > 1 else None
    
    checker = ArchitectureChecker(project_root)
    violations = checker.check_project()
    
    checker.print_violations()
    
    # 如果发现违规则返回非零退出代码
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main()) 
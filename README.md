# py-hexagonal

基于六边形架构（Hexagonal Architecture）的Python框架。

## 架构特点

- **六边形架构**：将应用核心与外部系统隔离
- **依赖注入**：使用dependency-injector实现解耦
- **事件驱动**：基于PyDispatcher的事件总线
- **工厂模式**：创建对象的工厂类
- **接口与抽象**：使用ABC模块定义接口
- **中间件支持**：提供Flask中间件机制
- **统一错误处理**：全局异常处理
- **配置管理**：基于python-dotenv的配置

## 目录结构

- **adapter**：适配器层，连接外部世界与应用核心
- **api**：API定义和处理
- **application**：应用层，用例实现
- **domain**：领域层，核心业务逻辑
- **config**：配置
- **util**：工具类

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 测试

```bash
pytest
```

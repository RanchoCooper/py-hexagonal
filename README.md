# Python Hexagonal Architecture

![CI Status](https://github.com/yourusername/py-hexagonal/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/yourusername/py-hexagonal/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/py-hexagonal)

一个基于六边形架构（端口与适配器架构）的 Python 应用程序示例。该项目展示了如何将业务逻辑与技术实现细节分离，以创建可维护、可测试和灵活的应用程序。

## 功能特点

- **六边形架构**：核心业务逻辑独立于外部依赖
- **领域驱动设计**：围绕业务领域模型组织代码
- **SOLID 原则**：遵循单一职责、开闭原则等软件设计原则
- **依赖注入**：使用 `dependency-injector` 实现松散耦合
- **多数据库支持**：支持 MySQL 和 PostgreSQL，可按领域服务灵活选择
- **事件驱动**：使用事件总线实现组件间通信

## 系统要求

- Python 3.9+
- MySQL 或 PostgreSQL
- Redis

## 快速开始

1. 克隆仓库:

```bash
git clone https://github.com/RanchoCooper/py-hexagonal.git
cd py-hexagonal
```

2. 创建虚拟环境并安装依赖:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. 配置:

```bash
cp config/config.yaml.example config/config.yaml
# 编辑 config.yaml 文件，配置数据库连接等
```

4. 运行应用:

```bash
PYTHONPATH=. python cmd/main.py
```

## 架构概览

项目基于六边形架构（也称为端口与适配器架构）组织，主要分为以下几个部分：

### 领域层 (Domain)

包含业务逻辑和实体模型，是应用的核心。

- `/domain/model/` - 业务实体
- `/domain/service/` - 业务服务接口和实现
- `/domain/repository/` - 仓储接口
- `/domain/event/` - 领域事件

### 应用层 (Application)

协调领域对象完成用例，不包含业务规则。

- `/application/service/` - 应用服务
- `/application/event/` - 事件处理器

### 适配器层 (Adapter)

连接外部世界与核心应用，分为驱动型（API）和被驱动型（数据库）适配器。

- `/adapter/http/` - HTTP API 接口
- `/adapter/repository/` - 数据库实现
- `/adapter/cache/` - 缓存实现
- `/adapter/event/` - 事件总线实现
- `/adapter/di/` - 依赖注入容器

### 基础设施 (Infrastructure)

提供技术支持，如日志、配置等。

- `/config/` - 配置文件和加载器

## 数据库适配

项目支持多种数据库后端，可以为不同领域服务选择不同的数据库：

```yaml
db:
  # 默认数据库连接，可选 'mysql' 或 'postgresql'
  default: mysql
  
  # 为不同领域服务指定数据库
  examples_db: mysql  # Example服务使用MySQL
  orders_db: postgresql  # 订单服务使用PostgreSQL
```

## 测试

运行测试:

```bash
PYTHONPATH=. pytest
```

## 贡献

欢迎贡献！请先阅读贡献指南。

## 许可

MIT 
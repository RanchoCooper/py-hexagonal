# Python 六边形架构示例项目

这是一个使用六边形架构（Hexagonal Architecture，也称为端口和适配器架构）构建的Python应用程序示例。

## 项目结构

项目按照六边形架构的理念组织，具有以下主要部分：

```
.
├── adapter/                  # 适配器层 - 实现端口的具体技术适配器
│   ├── cache/                # 缓存适配器
│   ├── dto/                  # 数据传输对象
│   ├── event/                # 事件总线适配器
│   ├── http/                 # HTTP控制器
│   └── repository/           # 存储库实现
├── api/                      # API定义
│   ├── dto/                  # API的数据传输对象
│   └── rest/                 # REST API定义
├── application/              # 应用层 - 用例和服务
│   ├── event/                # 事件处理器
│   └── service/              # 应用服务
├── cmd/                      # 应用程序入口点
│   ├── main.py               # 主入口点
│   └── server/               # HTTP服务器
├── config/                   # 配置
├── domain/                   # 领域层 - 业务逻辑和实体
│   ├── event/                # 领域事件
│   ├── model/                # 领域模型/实体
│   ├── repository/           # 存储库接口
│   ├── aggregate/            # 聚合
│   ├── vo/                   # 值对象
│   ├── service/              # 领域服务
│   └── repo/                 # 仓储接口
├── examples/                 # 示例代码
├── tests/                    # 测试
└── util/                     # 工具类
    ├── clean_arch/           # 架构验证工具
    └── di/                   # 依赖注入容器
```

## 开发环境设置

### 前提条件

- Python 3.9 或更高版本
- pip (Python包管理器)

### 安装

1. 克隆此仓库
```
git clone https://github.com/RanchoCooper/py-hexagonal.git
cd py-hexagonal
```

2. 创建并激活虚拟环境
```
python -m venv venv
source venv/bin/activate  # 在Windows上是 venv\Scripts\activate
```

3. 安装依赖项
```
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

4. 设置预提交钩子
```
pre-commit install
```

## 运行应用程序

```
python -m app
```

## 运行测试

```
pytest
```

## 类型检查

该项目使用mypy进行静态类型检查：

```
mypy app tests
```

## 依赖注入

本项目实现了一个简化的依赖注入容器，它在Python 3.12上与标准`dependency-injector`库兼容。位于`util/di`目录下。

### 基本用法

```python
from util.di import Container, providers

# 创建容器
container = Container()

# 配置容器
container.config.from_dict({
    "database": {
        "connection_string": "postgres://user:password@localhost:5432/examples"
    }
})

# 注册单例
container.register_provider(
    "database",
    providers.Singleton(
        Database,
        connection_string=container.config["database"]["connection_string"]
    )
)

# 注册带依赖的组件
container.register_provider(
    "repository",
    providers.Singleton(
        Repository,
        database=lambda: container.database()
    )
)

# 获取实例
repository = container.repository()
```

### 示例

可以在`examples/di_example.py`和`examples/di_simple_test.py`中查看完整示例。

## 数据库支持

本项目包含对MySQL、PostgreSQL和Redis数据库的支持，位于`adapter/repository`目录下。

### MySQL支持

提供了与MySQL数据库的连接和操作功能。

```python
from adapter.repository.mysql import MySQLConnection

# 创建连接
mysql = MySQLConnection(
    host="localhost",
    port=3306,
    user="root",
    password="password",
    database="app_db"
)

# 执行查询
results = mysql.execute("SELECT * FROM users WHERE id = :user_id", {"user_id": 1})
print(results)
```

### PostgreSQL支持

提供了与PostgreSQL数据库的连接和操作功能。

```python
from adapter.repository.postgre import PostgreSQLClient

# 创建连接
pg_client = PostgreSQLClient("postgresql://user:password@localhost:5432/app_db")

# 执行会话操作
with pg_client.session() as session:
    # 使用SQLAlchemy进行查询
    results = session.execute("SELECT * FROM users WHERE id = :user_id", {"user_id": 1})
    for row in results:
        print(row)
```

### Redis支持

提供了与Redis数据库的连接和操作功能。

```python
from adapter.repository.redis import RedisConnection

# 创建连接
redis = RedisConnection(
    host="localhost",
    port=6379,
    db=0
)

# 基本操作
redis.set("key", "value", ex=3600)  # 设置键值，1小时过期
value = redis.get("key")            # 获取键值
redis.delete("key")                 # 删除键

# 哈希表操作
redis.hash_set("user:1", "name", "张三")
redis.hash_set("user:1", "age", "30")
name = redis.hash_get("user:1", "name")

# 发布消息
redis.publish("channel", "message")
```

### 与依赖注入集成

数据库连接可以通过依赖注入容器进行管理：

```python
from util.di import Container
from adapter.repository.mysql.providers import MySQLClientProvider
from adapter.repository.postgre.providers import PostgreSQLClientProvider
from adapter.repository.redis.providers import RedisClientProvider

# 创建容器
container = Container()

# 注册MySQL提供者
container.register_provider(
    "mysql",
    MySQLClientProvider(
        host="localhost",
        port=3306,
        user="root",
        password="password",
        database="app_db"
    )
)

# 注册PostgreSQL提供者
container.register_provider(
    "postgresql",
    PostgreSQLClientProvider(
        "postgresql://user:password@localhost:5432/app_db"
    )
)

# 注册Redis提供者
container.register_provider(
    "redis",
    RedisClientProvider(
        host="localhost",
        port=6379,
        db=0
    )
)

# 使用数据库连接
mysql = container.mysql()
postgresql = container.postgresql()
redis = container.redis()
```

更多示例请查看 `examples/db_example.py`。

## 代码风格和质量

项目使用以下工具确保代码质量：

- black (格式化)
- isort (导入排序)
- flake8 (代码质量)
- mypy (类型检查)

所有这些工具都可以通过pre-commit自动运行：

```
pre-commit run --all-files
```

## 架构验证

此项目包括一个架构验证工具，确保项目遵循六边形架构原则。该工具检查不同层之间的导入是否遵守依赖规则。

要运行验证：

```bash
make check-arch
```

或直接：

```bash
python util/check_arch.py
```

允许的依赖关系是：

- `domain` → `domain`
- `application` → `domain`, `application`
- `adapter` → `domain`, `application`, `adapter`
- `api` → `domain`, `application`, `api`
- `cmd` → `domain`, `application`, `adapter`, `api`, `cmd`, `config`, `util`
- `config` → `config`
- `util` → `util`

## 项目结构

```
.
├── adapter/                  # 适配器层 - 实现端口的具体技术适配器
│   ├── cache/                # 缓存适配器
│   ├── dto/                  # 数据传输对象
│   ├── event/                # 事件总线适配器
│   ├── http/                 # HTTP控制器
│   └── repository/           # 存储库实现
├── api/                      # API定义
│   ├── dto/                  # API的数据传输对象
│   └── rest/                 # REST API定义
├── application/              # 应用层 - 用例和服务
│   ├── event/                # 事件处理器
│   └── service/              # 应用服务
├── cmd/                      # 应用程序入口点
│   ├── main.py               # 主入口点
│   └── server/               # HTTP服务器
├── config/                   # 配置
├── domain/                   # 领域层 - 业务逻辑和实体
│   ├── event/                # 领域事件
│   ├── model/                # 领域模型/实体
│   ├── repository/           # 存储库接口
│   ├── aggregate/            # 聚合
│   ├── vo/                   # 值对象
│   ├── service/              # 领域服务
│   └── repo/                 # 仓储接口
├── examples/                 # 示例代码
├── tests/                    # 测试
└── util/                     # 工具类
    ├── clean_arch/           # 架构验证工具
    └── di/                   # 依赖注入容器
```

## 获取开始

### 前提条件

- Python 3.9 或更高版本
- pip (Python包管理器)

### 安装

1. 克隆此仓库
```bash
git clone https://github.com/yourusername/py-hexagonal.git
cd py-hexagonal
```

2. 创建并激活虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. 安装依赖项
```bash
pip install -r requirements.txt
```

4. 创建一个 `.env` 文件在 `config` 目录中：
```bash
cp config/.env.example config/.env
```

5. 编辑 `.env` 文件以进行配置。

### 运行应用程序

```bash
python cmd/main.py
```

服务器将在 `http://localhost:5000` 启动。

## API 端点

### 示例 API

- `GET /api/examples`: 获取所有示例
- `GET /api/examples/active`: 获取所有活动示例
- `GET /api/examples/{id}`: 按 ID 获取示例
- `POST /api/examples`: 创建新示例
- `PUT /api/examples/{id}`: 更新示例
- `PUT /api/examples/{id}/activate`: 激活示例
- `PUT /api/examples/{id}/deactivate`: 停用示例
- `DELETE /api/examples/{id}`: 删除示例

## 开发

该项目包括几个用于开发的 make 命令：

```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test

# Check architecture
make check-arch

# Run all of the above
make all
```

## 测试

```bash
pytest
```

## 许可证

此项目根据 MIT 许可证进行许可 - 查看 LICENSE 文件以获取详细信息。

## 致谢

- 此项目基于 Alistair Cockburn 提出的六边形架构模式
- 受 Go Hexagonal 的启发：https://github.com/RanchoCooper/go-hexagonal

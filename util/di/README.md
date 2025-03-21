# 依赖注入容器

这个模块提供了一个轻量级的依赖注入容器，用于管理应用程序的依赖关系。它是`dependency-injector`库的简化替代品，专门为Python 3.12及以上版本设计，解决了标准库在新版Python中的兼容性问题。

## 主要组件

### Container

`Container`是依赖注入容器的主类，负责管理所有依赖项。

```python
from util.di import Container, providers

# 创建容器实例
container = Container()
```

### Providers

提供者负责创建和管理依赖项的实例。主要有以下几种：

#### Singleton

单例提供者确保在整个应用程序生命周期中只创建一个依赖项实例。

```python
# 注册单例
container.register_provider(
    "database",
    providers.Singleton(
        Database,
        connection_string="postgres://user:password@localhost:5432/db"
    )
)
```

#### Factory

工厂提供者每次请求时都会创建新的实例。

```python
# 注册工厂
container.register_provider(
    "request",
    providers.Factory(
        Request,
        headers={"Content-Type": "application/json"}
    )
)
```

#### Resource

资源提供者类似于单例，但专门用于需要管理生命周期的资源。

```python
# 注册资源
container.register_provider(
    "connection_pool",
    providers.Resource(
        ConnectionPool,
        max_connections=10
    )
)
```

### Configuration

容器包含一个配置组件，用于管理应用程序配置。

```python
# 从字典加载配置
container.config.from_dict({
    "database": {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "password"
    },
    "api": {
        "port": 8000,
        "debug": True
    }
})

# 访问配置
db_host = container.config["database"]["host"]  # 使用字典语法
api_port = container.config.get("api.port", 8080)  # 使用get方法
```

#### 重要提示

`container.config`是一个`Configuration`对象，不是`Provider`对象，因此不能使用`container.config()`调用它。如果需要将配置注入到类中，应该创建一个专门的配置提供者：

```python
# 注册配置提供者
container.register_provider(
    "app_config",  # 使用不同的名称，避免与container.config混淆
    providers.Singleton(
        Config,
        debug=lambda: container.config["app"]["debug"]
    )
)

# 注册服务
container.register_provider(
    "service",
    providers.Singleton(
        Service,
        config=lambda: container.app_config()  # 使用app_config而不是config
    )
)
```

## 依赖注入模式

### 构造函数注入

最常见的依赖注入模式是通过构造函数注入依赖项。

```python
class UserRepository:
    def __init__(self, database):
        self.database = database

# 注册仓库
container.register_provider(
    "user_repository",
    providers.Singleton(
        UserRepository,
        database=lambda: container.database()
    )
)
```

### 处理循环依赖

处理循环依赖需要创建专门的提供者类。

```python
class DatabaseProvider:
    def __init__(self, container):
        self.container = container
    
    def __call__(self):
        return self.container.database()

# 创建提供者
db_provider = DatabaseProvider(container)

# 注册依赖项
container.register_provider(
    "service",
    providers.Singleton(
        Service,
        database=db_provider
    )
)
```

## 完整示例

以下是一个完整的依赖注入设置示例：

```python
from util.di import Container, providers

# 定义一些类
class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        print(f"Connecting to {connection_string}")
    
    def query(self, sql):
        print(f"Executing: {sql}")
        return [{"id": 1, "name": "Example"}]

class Repository:
    def __init__(self, database):
        self.database = database
    
    def get_all(self):
        return self.database.query("SELECT * FROM examples")

class Service:
    def __init__(self, repository):
        self.repository = repository
    
    def get_all_examples(self):
        return self.repository.get_all()

# 创建容器
container = Container()

# 配置
container.config.from_dict({
    "database": {
        "connection_string": "postgres://user:password@localhost:5432/examples"
    }
})

# 注册提供者
container.register_provider(
    "database",
    providers.Singleton(
        Database,
        connection_string=container.config["database"]["connection_string"]
    )
)

container.register_provider(
    "repository",
    providers.Singleton(
        Repository,
        database=lambda: container.database()
    )
)

container.register_provider(
    "service",
    providers.Singleton(
        Service,
        repository=lambda: container.repository()
    )
)

# 使用容器
service = container.service()
examples = service.get_all_examples()
print(f"Found examples: {examples}")
```

## 更多示例

可以在`examples`目录下查看更多示例：

- `di_basic_example.py` - 基本使用示例
- `di_simple_test.py` - 简单测试脚本
- `di_example.py` - 更复杂的示例，包含循环依赖解决方案

## API参考

### Container

- `__init__()`: 初始化容器。
- `register_provider(name: str, provider: Provider)`: 注册提供者。
- `__getattr__(name: str)`: 获取提供者或实例。

### Provider

- `__init__()`: 初始化提供者。
- `__call__(*args, **kwargs)`: 调用提供者以获取实例。
- `provide(*args, **kwargs)`: 提供实例的方法（由子类实现）。

### Singleton

- `__init__(factory: Callable[..., T], *args, **kwargs)`: 初始化单例提供者。
- `provide(*args, **kwargs)`: 提供单例实例。

### Factory

- `__init__(factory: Callable[..., T], *args, **kwargs)`: 初始化工厂提供者。
- `provide(*args, **kwargs)`: 提供新实例。

### Resource

- `__init__(factory: Callable[..., T], *args, **kwargs)`: 初始化资源提供者。
- `provide(*args, **kwargs)`: 提供资源实例。

### Configuration

- `__init__()`: 初始化配置提供者。
- `from_dict(config: Dict[str, Any])`: 从字典加载配置。
- `get(key: str, default: Optional[Any] = None)`: 获取配置值。
- `__getitem__(key: str)`: 使用字典语法获取配置值。 
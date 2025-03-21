# 仓储适配器（Repository Adapters）

本目录包含仓储适配器的实现，用于连接各种数据存储系统。

## MySQL 适配器

`mysql.py` 提供了与 MySQL 数据库的连接和交互功能。它使用 SQLAlchemy 作为底层实现，支持连接池和事务管理。

基本用法：

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

# 执行更新
mysql.execute("UPDATE users SET name = :name WHERE id = :user_id", 
              {"name": "新名称", "user_id": 1})

# 关闭连接
mysql.close()
```

## Redis 适配器

`redis.py` 提供了与 Redis 数据库的连接和交互功能。它支持基本的键值操作、哈希表和发布订阅。

基本用法：

```python
from adapter.repository.redis import RedisConnection

# 创建连接
redis = RedisConnection(
    host="localhost",
    port=6379,
    db=0
)

# 设置键值
redis.set("key", "value", ex=3600)  # 1小时过期

# 获取键值
value = redis.get("key")
print(value)

# 哈希表操作
redis.hash_set("user:1", "name", "张三")
redis.hash_set("user:1", "age", "30")
name = redis.hash_get("user:1", "name")
print(name)

# 发布消息
redis.publish("channel", "message")

# 关闭连接
redis.close()
```

## 依赖注入集成

`providers.py` 提供了与依赖注入容器集成的提供者类，便于在应用程序中使用数据库连接。

```python
from util.di import Container
from adapter.repository.providers import MySQLProvider, RedisProvider

# 创建容器
container = Container()

# 配置
container.config.from_dict({
    "database": {
        "mysql": {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "password",
            "database": "app_db"
        },
        "redis": {
            "host": "localhost",
            "port": 6379,
            "db": 0
        }
    }
})

# 注册MySQL提供者
container.register_provider(
    "mysql",
    MySQLProvider(
        host=container.config["database"]["mysql"]["host"],
        port=container.config["database"]["mysql"]["port"],
        user=container.config["database"]["mysql"]["user"],
        password=container.config["database"]["mysql"]["password"],
        database=container.config["database"]["mysql"]["database"]
    )
)

# 注册Redis提供者
container.register_provider(
    "redis",
    RedisProvider(
        host=container.config["database"]["redis"]["host"],
        port=container.config["database"]["redis"]["port"],
        db=container.config["database"]["redis"]["db"]
    )
)

# 在服务中使用
class UserService:
    def __init__(self, mysql, redis):
        self.mysql = mysql
        self.redis = redis

container.register_provider(
    "user_service",
    Container.providers.Singleton(
        UserService,
        mysql=lambda: container.mysql(),
        redis=lambda: container.redis()
    )
)

# 获取服务
service = container.user_service()
```

## 依赖项

使用这些适配器需要安装以下依赖：

```
# MySQL
sqlalchemy>=1.4.0
pymysql>=1.0.0

# Redis
redis>=4.5.0
```

可以通过以下命令安装：

```bash
pip install -r requirements-dev.txt
``` 
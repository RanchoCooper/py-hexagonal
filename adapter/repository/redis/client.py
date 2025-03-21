"""
Redis client module.
"""

import sys
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from adapter.repository.error import RedisError
from domain.repo.transaction import Transaction


class RedisClient:
    """Redis client wrapper."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5,
    ):
        """
        Initialize the Redis client.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password
            decode_responses: Whether to decode responses from Redis
            socket_timeout: Socket timeout in seconds
            socket_connect_timeout: Socket connect timeout in seconds
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout
        self._client = None
    
    def connect(self) -> None:
        """
        Connect to the Redis server.
        
        Raises:
            RedisError: If the connection fails
        """
        try:
            # Import Redis here to avoid requiring it if not used
            import redis
            
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=self.decode_responses,
                socket_timeout=self.socket_timeout,
                socket_connect_timeout=self.socket_connect_timeout,
            )
            
            # Test the connection
            self._client.ping()
        except ImportError:
            raise RedisError("Redis module not installed. Please run: pip install redis")
        except Exception as e:
            raise RedisError(f"Failed to connect to Redis: {e}", e)
    
    def _get_client(self):
        """Get the client, connecting if needed."""
        if self._client is None:
            self.connect()
        return self._client
    
    def get(self, key: str) -> Any:
        """
        Get a value from Redis.
        
        Args:
            key: The key to get
            
        Returns:
            The value, or None if the key doesn't exist
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return client.get(key)
        except Exception as e:
            raise RedisError(f"Failed to get key {key}: {e}", e)
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        Set a value in Redis.
        
        Args:
            key: The key to set
            value: The value to set
            ex: Expiration time in seconds
            
        Returns:
            True if successful
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return bool(client.set(key, value, ex=ex))
        except Exception as e:
            raise RedisError(f"Failed to set key {key}: {e}", e)
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False if it didn't exist
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return bool(client.delete(key))
        except Exception as e:
            raise RedisError(f"Failed to delete key {key}: {e}", e)
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.
        
        Args:
            key: The key to check
            
        Returns:
            True if the key exists, False otherwise
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return bool(client.exists(key))
        except Exception as e:
            raise RedisError(f"Failed to check if key {key} exists: {e}", e)
    
    def hget(self, name: str, key: str) -> Any:
        """
        Get a value from a hash in Redis.
        
        Args:
            name: The name of the hash
            key: The key within the hash
            
        Returns:
            The value, or None if the key doesn't exist
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return client.hget(name, key)
        except Exception as e:
            raise RedisError(f"Failed to get hash key {name}:{key}: {e}", e)
    
    def hset(self, name: str, key: str, value: Any) -> bool:
        """
        Set a value in a hash in Redis.
        
        Args:
            name: The name of the hash
            key: The key within the hash
            value: The value to set
            
        Returns:
            True if a new field was created, False if the field was updated
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return bool(client.hset(name, key, value))
        except Exception as e:
            raise RedisError(f"Failed to set hash key {name}:{key}: {e}", e)
    
    def hgetall(self, name: str) -> Dict[str, Any]:
        """
        Get all fields and values from a hash in Redis.
        
        Args:
            name: The name of the hash
            
        Returns:
            A dictionary of all fields and values in the hash
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return client.hgetall(name)
        except Exception as e:
            raise RedisError(f"Failed to get all hash keys for {name}: {e}", e)
    
    def pipeline(self) -> 'RedisPipeline':
        """
        Get a Redis pipeline.
        
        Returns:
            A Redis pipeline
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            client = self._get_client()
            return RedisPipeline(client.pipeline())
        except Exception as e:
            raise RedisError(f"Failed to create Redis pipeline: {e}", e)
    
    def close(self) -> None:
        """
        Close the Redis connection.
        
        Raises:
            RedisError: If the operation fails
        """
        if self._client is not None:
            try:
                self._client.close()
                self._client = None
            except Exception as e:
                raise RedisError(f"Failed to close Redis connection: {e}", e)


class RedisPipeline:
    """Redis pipeline wrapper."""
    
    def __init__(self, pipeline):
        """
        Initialize the pipeline.
        
        Args:
            pipeline: The Redis pipeline
        """
        self._pipeline = pipeline
    
    def get(self, key: str) -> 'RedisPipeline':
        """
        Add a GET command to the pipeline.
        
        Args:
            key: The key to get
            
        Returns:
            The pipeline
        """
        self._pipeline.get(key)
        return self
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> 'RedisPipeline':
        """
        Add a SET command to the pipeline.
        
        Args:
            key: The key to set
            value: The value to set
            ex: Expiration time in seconds
            
        Returns:
            The pipeline
        """
        self._pipeline.set(key, value, ex=ex)
        return self
    
    def delete(self, key: str) -> 'RedisPipeline':
        """
        Add a DELETE command to the pipeline.
        
        Args:
            key: The key to delete
            
        Returns:
            The pipeline
        """
        self._pipeline.delete(key)
        return self
    
    def hget(self, name: str, key: str) -> 'RedisPipeline':
        """
        Add an HGET command to the pipeline.
        
        Args:
            name: The name of the hash
            key: The key within the hash
            
        Returns:
            The pipeline
        """
        self._pipeline.hget(name, key)
        return self
    
    def hset(self, name: str, key: str, value: Any) -> 'RedisPipeline':
        """
        Add an HSET command to the pipeline.
        
        Args:
            name: The name of the hash
            key: The key within the hash
            value: The value to set
            
        Returns:
            The pipeline
        """
        self._pipeline.hset(name, key, value)
        return self
    
    def execute(self) -> List[Any]:
        """
        Execute the pipeline.
        
        Returns:
            The results of the commands
            
        Raises:
            RedisError: If the operation fails
        """
        try:
            return self._pipeline.execute()
        except Exception as e:
            raise RedisError(f"Failed to execute Redis pipeline: {e}", e)


class RedisTransaction(Transaction):
    """Redis transaction implementation."""
    
    def __init__(self, client: RedisClient):
        """
        Initialize the transaction.
        
        Args:
            client: The Redis client
        """
        self.client = client
        self._pipeline = None
    
    def __enter__(self) -> 'RedisTransaction':
        """Enter the transaction context."""
        client = self.client._get_client()
        self._pipeline = client.pipeline()
        return self
    
    def commit(self) -> None:
        """
        Commit the transaction.
        
        Raises:
            RedisError: If the commit fails
        """
        try:
            if self._pipeline is not None:
                self._pipeline.execute()
                self._pipeline = None
        except Exception as e:
            self.rollback()
            raise RedisError(f"Failed to commit transaction: {e}", e)
    
    def rollback(self) -> None:
        """
        Rollback the transaction.
        
        Raises:
            RedisError: If the rollback fails
        """
        try:
            if self._pipeline is not None:
                self._pipeline.reset()
                self._pipeline = None
        except Exception as e:
            raise RedisError(f"Failed to rollback transaction: {e}", e) 
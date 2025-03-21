"""
Redis cache adapter.

This module provides a Redis-based cache implementation.
"""
import json
import logging
from datetime import timedelta
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

import redis

from domain.model.example import Example

logger = logging.getLogger(__name__)
T = TypeVar('T')


class RedisCache:
    """
    Redis cache implementation.
    
    This class provides a simple interface to interact with Redis for caching
    purposes, with support for serialization and deserialization of values.
    """
    
    def __init__(self, redis_client: redis.Redis, prefix: str = "cache:"):
        """
        Initialize the Redis cache.
        
        Args:
            redis_client: The Redis client to use
            prefix: The prefix to use for all cache keys
        """
        self._redis = redis_client
        self._prefix = prefix
    
    def get(self, key: str) -> Optional[str]:
        """
        Get a value from the cache.
        
        Args:
            key: The key to get the value for
            
        Returns:
            The cached value or None if not found
        """
        full_key = self._prefix + key
        try:
            value = self._redis.get(full_key)
            return value.decode('utf-8') if value else None
        except redis.RedisError as e:
            logger.error(f"Error getting value for key {full_key}: {e}")
            return None
    
    def set(self, key: str, value: str, ttl: Optional[timedelta] = None) -> bool:
        """
        Set a value in the cache.
        
        Args:
            key: The key to set the value for
            value: The value to cache
            ttl: Optional time-to-live for the cache entry
            
        Returns:
            True if the value was set successfully, False otherwise
        """
        full_key = self._prefix + key
        try:
            if ttl:
                return self._redis.setex(full_key, ttl, value)
            else:
                return self._redis.set(full_key, value)
        except redis.RedisError as e:
            logger.error(f"Error setting value for key {full_key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the value was deleted, False otherwise
        """
        full_key = self._prefix + key
        try:
            return bool(self._redis.delete(full_key))
        except redis.RedisError as e:
            logger.error(f"Error deleting key {full_key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.
        
        Args:
            key: The key to check
            
        Returns:
            True if the key exists, False otherwise
        """
        full_key = self._prefix + key
        try:
            return bool(self._redis.exists(full_key))
        except redis.RedisError as e:
            logger.error(f"Error checking existence of key {full_key}: {e}")
            return False


class ExampleRedisCache:
    """
    Redis cache adapter for Example entities.
    
    This class provides a specialized cache interface for Example entities,
    handling serialization and deserialization.
    """
    
    def __init__(self, redis_cache: RedisCache):
        """
        Initialize the Example Redis cache.
        
        Args:
            redis_cache: The Redis cache to use
        """
        self._cache = redis_cache
    
    def get_by_id(self, example_id: str) -> Optional[Example]:
        """
        Get an Example by its ID from the cache.
        
        Args:
            example_id: The ID of the Example to get
            
        Returns:
            The cached Example or None if not found
        """
        key = f"example:{example_id}"
        json_str = self._cache.get(key)
        
        if not json_str:
            return None
        
        try:
            data = json.loads(json_str)
            return Example.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error deserializing Example from cache: {e}")
            return None
    
    def save(self, example: Example, ttl: Optional[timedelta] = None) -> bool:
        """
        Save an Example to the cache.
        
        Args:
            example: The Example to cache
            ttl: Optional time-to-live for the cache entry
            
        Returns:
            True if the Example was cached successfully, False otherwise
        """
        key = f"example:{example.id}"
        try:
            json_str = json.dumps(example.to_dict())
            return self._cache.set(key, json_str, ttl)
        except (TypeError, ValueError) as e:
            logger.error(f"Error serializing Example to cache: {e}")
            return False
    
    def delete(self, example_id: str) -> bool:
        """
        Delete an Example from the cache.
        
        Args:
            example_id: The ID of the Example to delete
            
        Returns:
            True if the Example was deleted, False otherwise
        """
        key = f"example:{example_id}"
        return self._cache.delete(key)
    
    def exists(self, example_id: str) -> bool:
        """
        Check if an Example exists in the cache.
        
        Args:
            example_id: The ID of the Example to check
            
        Returns:
            True if the Example exists in the cache, False otherwise
        """
        key = f"example:{example_id}"
        return self._cache.exists(key) 
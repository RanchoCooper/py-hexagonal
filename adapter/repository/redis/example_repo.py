"""
Redis example repository implementation.
"""

import json
import pickle
from typing import Dict, List, Optional
from uuid import UUID

from adapter.repository.error import RedisError
from adapter.repository.redis.client import RedisClient
from domain.model.example import Example
from domain.repo.example import ExampleRepository


class RedisExampleRepository(ExampleRepository):
    """Redis implementation of the example repository."""
    
    def __init__(self, redis_client: RedisClient, prefix: str = "example"):
        """
        Initialize the repository.
        
        Args:
            redis_client: The Redis client
            prefix: The key prefix for all examples
        """
        self.redis_client = redis_client
        self.prefix = prefix
    
    def _get_key(self, example_id: UUID) -> str:
        """Get the Redis key for an example."""
        return f"{self.prefix}:{str(example_id)}"
    
    def _get_name_key(self, name: str) -> str:
        """Get the Redis key for an example name index."""
        return f"{self.prefix}:name:{name}"
    
    def _get_all_key(self) -> str:
        """Get the Redis key for the set of all example IDs."""
        return f"{self.prefix}:all"
    
    def _serialize(self, example: Example) -> str:
        """
        Serialize an example to JSON.
        
        Args:
            example: The example to serialize
            
        Returns:
            The serialized example as a JSON string
        """
        data = {
            "id": str(example.id),
            "name": example.name,
            "description": example.description,
            "is_active": example.is_active,
            "created_at": example.created_at.isoformat(),
            "updated_at": example.updated_at.isoformat()
        }
        return json.dumps(data)
    
    def _deserialize(self, data_str: str) -> Example:
        """
        Deserialize an example from JSON.
        
        Args:
            data_str: The JSON string to deserialize
            
        Returns:
            The deserialized example
            
        Raises:
            RedisError: If deserialization fails
        """
        try:
            from datetime import datetime
            
            data = json.loads(data_str)
            return Example(
                id=UUID(data["id"]),
                name=data["name"],
                description=data["description"],
                is_active=data["is_active"],
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            )
        except Exception as e:
            raise RedisError(f"Failed to deserialize example: {e}", e)
    
    def find_by_id(self, example_id: UUID) -> Optional[Example]:
        """
        Find an example by its ID.
        
        Args:
            example_id: The ID of the example
            
        Returns:
            The example if found, None otherwise
            
        Raises:
            RedisError: If there's a problem with Redis
        """
        try:
            key = self._get_key(example_id)
            data = self.redis_client.get(key)
            
            if data is None:
                return None
                
            return self._deserialize(data)
        except RedisError:
            raise
        except Exception as e:
            raise RedisError(f"Failed to find example by ID: {e}", e)
    
    def find_all(self) -> List[Example]:
        """
        Find all examples.
        
        Returns:
            A list of all examples
            
        Raises:
            RedisError: If there's a problem with Redis
        """
        try:
            all_key = self._get_all_key()
            example_ids = self.redis_client.hgetall(all_key)
            
            if not example_ids:
                return []
                
            examples = []
            for example_id in example_ids.values():
                key = self._get_key(UUID(example_id))
                data = self.redis_client.get(key)
                if data is not None:
                    examples.append(self._deserialize(data))
            
            return examples
        except RedisError:
            raise
        except Exception as e:
            raise RedisError(f"Failed to find all examples: {e}", e)
    
    def find_by_name(self, name: str) -> Optional[Example]:
        """
        Find an example by its name.
        
        Args:
            name: The name of the example
            
        Returns:
            The example if found, None otherwise
            
        Raises:
            RedisError: If there's a problem with Redis
        """
        try:
            name_key = self._get_name_key(name)
            example_id = self.redis_client.get(name_key)
            
            if example_id is None:
                return None
                
            key = self._get_key(UUID(example_id))
            data = self.redis_client.get(key)
            
            if data is None:
                # Inconsistent state, remove the name index
                self.redis_client.delete(name_key)
                return None
                
            return self._deserialize(data)
        except RedisError:
            raise
        except Exception as e:
            raise RedisError(f"Failed to find example by name: {e}", e)
    
    def save(self, example: Example) -> Example:
        """
        Save an example.
        
        Args:
            example: The example to save
            
        Returns:
            The saved example
            
        Raises:
            RedisError: If there's a problem with Redis
        """
        try:
            # Get keys
            key = self._get_key(example.id)
            name_key = self._get_name_key(example.name)
            all_key = self._get_all_key()
            
            # Check if name conflicts with a different example
            existing_id = self.redis_client.get(name_key)
            if existing_id is not None and existing_id != str(example.id):
                existing_example = self.find_by_id(UUID(existing_id))
                if existing_example is not None:
                    from domain.repo.error import DuplicateEntityError
                    raise DuplicateEntityError("Example", "name", example.name)
            
            # Serialize the example
            data = self._serialize(example)
            
            # Use a pipeline to ensure atomic operations
            pipeline = self.redis_client.pipeline()
            
            # Save the example
            pipeline.set(key, data)
            
            # Update the name index
            pipeline.set(name_key, str(example.id))
            
            # Update the all index
            pipeline.hset(all_key, str(example.id), str(example.id))
            
            # Execute the pipeline
            pipeline.execute()
            
            return example
        except RedisError:
            raise
        except Exception as e:
            raise RedisError(f"Failed to save example: {e}", e)
    
    def delete(self, example_id: UUID) -> None:
        """
        Delete an example.
        
        Args:
            example_id: The ID of the example
            
        Raises:
            EntityNotFoundError: If the example is not found
            RedisError: If there's a problem with Redis
        """
        try:
            # Find the example first
            example = self.find_by_id(example_id)
            
            if example is None:
                from domain.repo.error import EntityNotFoundError
                raise EntityNotFoundError("Example", example_id)
                
            # Get keys
            key = self._get_key(example_id)
            name_key = self._get_name_key(example.name)
            all_key = self._get_all_key()
            
            # Use a pipeline to ensure atomic operations
            pipeline = self.redis_client.pipeline()
            
            # Delete the example
            pipeline.delete(key)
            
            # Delete the name index
            pipeline.delete(name_key)
            
            # Remove from the all index
            pipeline.delete(f"{all_key}:{str(example_id)}")
            
            # Execute the pipeline
            pipeline.execute()
        except RedisError:
            raise
        except Exception as e:
            if isinstance(e, RedisError) or hasattr(e, "__cause__") and isinstance(e.__cause__, RedisError):
                raise
            from domain.repo.error import EntityNotFoundError
            if isinstance(e, EntityNotFoundError):
                raise
            raise RedisError(f"Failed to delete example: {e}", e) 
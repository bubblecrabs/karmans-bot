import json
from typing import Any

from redis.asyncio import Redis

from app.core.config import settings


class RedisCache:
    def __init__(self, url: str) -> None:
        self.redis: Redis = Redis.from_url(url=url)

    async def get(self, key: str) -> Any | None:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        value: Any = await self.redis.get(name=key)
        if value is None:
            return None

        try:
            return json.loads(s=value)
        except json.JSONDecodeError:
            return value

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        Returns:
            True if successful
        """
        serialized: str = json.dumps(obj=value)

        if ttl:
            return await self.redis.setex(name=key, value=serialized, time=ttl)

        return await self.redis.set(name=key, value=serialized)

    async def delete(self, *keys: str) -> int:
        """
        Delete one or more keys.

        Args:
            keys: Keys to delete

        Returns:
            Number of keys deleted
        """
        return await self.redis.delete(*keys)

    async def exists(self, *keys: str) -> int:
        """
        Check if keys exist.

        Args:
            keys: Keys to check

        Returns:
            Number of existing keys
        """
        return await self.redis.exists(*keys)

    async def expire(self, key: str, ttl: int) -> bool:
        """
        Set expiration time for a key.

        Args:
            key: Cache key
            ttl: Time to live in seconds

        Returns:
            True if successful
        """
        return await self.redis.expire(name=key, time=ttl)

    async def close(self) -> None:
        """
        Close Redis connection.
        """
        await self.redis.aclose()


redis_cache = RedisCache(url=settings.REDIS_DSN)

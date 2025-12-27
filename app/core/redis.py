from redis.asyncio import Redis

from app.core.config import settings

redis: Redis = Redis.from_url(url=settings.REDIS_DSN)

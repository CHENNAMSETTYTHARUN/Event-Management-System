import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        self.client = None
        self._local_cache = {}
        if settings.REDIS_ENABLED:
            try:
                import redis
                self.client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                self.client.ping()
                logger.info("Successfully connected to Redis cache.")
            except Exception as e:
                logger.warning(f"Could not connect to Redis. Falling back to simple in-memory cache: {e}")
                self.client = None

    def get(self, key: str) -> Optional[str]:
        if self.client:
            try:
                return self.client.get(key)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        return self._local_cache.get(key)

    def set(self, key: str, value: str, expire_seconds: int = 300) -> bool:
        if self.client:
            try:
                self.client.set(key, value, ex=expire_seconds)
                return True
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        self._local_cache[key] = value
        return True

    def delete(self, key: str) -> bool:
        if self.client:
            try:
                self.client.delete(key)
                return True
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
        if key in self._local_cache:
            del self._local_cache[key]
        return True

cache = RedisCache()

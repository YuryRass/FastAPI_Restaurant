from aioredis import ConnectionPool as AsyncConnectionPool, Redis as AsyncRedis
from redis import ConnectionPool, Redis  # type: ignore

from app.config import settings


class RedisCacher:
    """Нереляционная база данных Redis."""

    async_pool: AsyncConnectionPool = AsyncConnectionPool.from_url(settings.REDIS_URL)
    pool: ConnectionPool = ConnectionPool.from_url(settings.REDIS_URL)

    @classmethod
    def get_async_cacher(cls) -> AsyncRedis:
        """Получение асинхр. Redis."""
        return AsyncRedis(connection_pool=cls.async_pool)

    @classmethod
    def get_cacher(cls) -> Redis:
        """Получение синхр. Redis."""
        return Redis(connection_pool=cls.pool)


redis_cacher: AsyncRedis = RedisCacher.get_async_cacher()
sync_redis_cacher: Redis = RedisCacher.get_cacher()

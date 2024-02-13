from redis import ConnectionPool, Redis  # type: ignore

from app.config import settings


class RedisCacher:
    """Нереляционная база данных Redis."""
    pool: ConnectionPool = ConnectionPool.from_url(settings.REDIS_URL)

    @classmethod
    def get_cacher(cls) -> Redis:
        """Получение Redis."""
        return Redis(connection_pool=cls.pool)


redis_cacher: Redis = RedisCacher.get_cacher()

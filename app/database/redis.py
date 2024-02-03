from aioredis import ConnectionPool, Redis

from app.config import settings


class RedisCacher:
    pool: ConnectionPool = ConnectionPool.from_url(settings.REDIS_URL)

    @classmethod
    def get_cacher(cls) -> Redis:
        return Redis(connection_pool=cls.pool)


redis_cacher: Redis = RedisCacher.get_cacher()

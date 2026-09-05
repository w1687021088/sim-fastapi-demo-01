# import redis
# from settings import app_settings
#
# redis_client = redis.Redis(
#     host=app_settings.REDIS_HOST,
#     port=app_settings.REDIS_PORT,
#     password=app_settings.REDIS_PASSWORD,
#     decode_responses=True,
#     max_connections=app_settings.REDIS_MAX_CONNECTIONS,
# )
from contextlib import asynccontextmanager
from redis.asyncio import Redis, ConnectionPool

class RedisManager:
    def __init__(self):
        self.pool = None
        self.client = None

    async def connect(self):
        self.pool = ConnectionPool.from_url(
            "redis://localhost:6379",
            max_connections=50,           # 核心：连接池大小
            decode_responses=True,
        )
        self.client = Redis(connection_pool=self.pool)
        await self.client.ping()

    async def disconnect(self):
        if self.client:
            await self.client.aclose()
        if self.pool:
            await self.pool.aclose()

    def get_client(self):
        return self.client

redis_manager = RedisManager()
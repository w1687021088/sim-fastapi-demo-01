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

from redis.asyncio import Redis, ConnectionPool
from settings import app_settings


def _build_redis_url() -> str:
    """根据配置构建 Redis 连接 URL"""
    host = app_settings.REDIS_HOST
    port = app_settings.REDIS_PORT
    db = app_settings.REDIS_DB
    password = app_settings.REDIS_PASSWORD

    if password:
        # 如果有密码，格式：redis://:password@host:port/0
        return f"redis://:{password}@{host}:{port}/{db}"
    else:
        # 无密码
        return f"redis://{host}:{port}/{db}"


class RedisManager:
    def __init__(self):
        self.pool = None
        self.client = None

    async def connect(self):
        """初始化连接池"""
        url = _build_redis_url()
        max_conn = app_settings.REDIS_MAX_CONNECTIONS

        self.pool = ConnectionPool.from_url(
            url,
            max_connections=max_conn,
            decode_responses=True,
            # 可选的超时设置（按需添加）
            # socket_timeout=5,
            # socket_connect_timeout=3,
            # retry_on_timeout=True,
        )
        self.client = Redis(connection_pool=self.pool)

        # 验证连接
        await self.client.ping()
        print(f"✅ Redis 连接成功 (host={app_settings.REDIS_HOST})")

    async def disconnect(self):
        """关闭连接池"""
        if self.client:
            await self.client.aclose()
        if self.pool:
            await self.pool.aclose()
        print("🛑 Redis 连接已释放")

    def get_client(self) -> Redis:
        """获取 Redis 客户端实例"""
        if self.client is None:
            raise RuntimeError("Redis 未初始化，请先调用 connect()")
        return self.client


# 全局单例
redis_manager = RedisManager()

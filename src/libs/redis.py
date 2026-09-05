import redis

# 全局连接池（只创建一次）
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    password='123456',
    decode_responses=True,
    max_connections=10,
)

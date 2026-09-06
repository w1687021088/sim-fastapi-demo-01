from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.apps import register_routes
from src.libs.redis_client import app_redis
from src.libs.log import logger
from src.libs import (
    register_middleware,
    register_exception,
    register_db,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """应用启动时执行"""
    try:
        await app_redis.connect()  # 链接 redis
        print("✅ 所有服务连接成功")
    except Exception as e:
        logger.error(f"❌ 服务连接失败，应用无法启动: {e}")
        raise

    yield

    # 关闭时尽量保证都释放，即使某个报错也不影响其他的
    try:
        await app_redis.disconnect()  # 关闭 redis 连接
    except Exception as e:
        logger.error(f"⚠️ Redis 关闭异常: {e}")

    print("🛑 所有连接已释放")


def create_app() -> FastAPI:
    """创建FastAPI应用程序"""

    app = FastAPI(lifespan=lifespan)

    # 注册路由
    register_routes(app)
    # 注册中间件
    register_middleware(app)
    # 注册异常处理
    register_exception(app)
    # 注册数据库
    register_db(app)

    return app

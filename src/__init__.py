from fastapi import FastAPI
from contextlib import asynccontextmanager
from .apps import register_routes
from tortoise import Tortoise

from .libs import (
    register_middleware,
    register_exception,
    init_db,
    redis_manager
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await redis_manager.connect() # 链接 redis
        await init_db() # 初始化数据库
        print("✅ 所有服务连接成功")
    except Exception as e:
        print(f"❌ 服务连接失败，应用无法启动: {e}")
        raise

    yield

    # 关闭时尽量保证都释放，即使某个报错也不影响其他的
    try:
        await Tortoise.close_connections() # 关闭数据库连接
    except Exception as e:
        print(f"⚠️ 数据库关闭异常: {e}")

    try:
        await redis_manager.disconnect() # 关闭 redis 连接
    except Exception as e:
        print(f"⚠️ Redis 关闭异常: {e}")

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

    return app

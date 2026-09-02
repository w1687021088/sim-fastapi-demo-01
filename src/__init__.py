from fastapi import FastAPI
from .apps import register_routes
from .libs import (
    register_middleware,
    register_exception,
    register_db
)


def create_app() -> FastAPI:
    """创建FastAPI应用程序"""

    app = FastAPI()

    # 注册路由
    register_routes(app)
    # 注册中间件
    register_middleware(app)
    # 注册异常处理
    register_exception(app)
    # 注册数据库
    register_db(app)

    return app

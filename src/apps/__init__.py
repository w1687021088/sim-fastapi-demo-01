from fastapi import FastAPI
from .home import home_router
from .system import system_router
from .auth import auth_router


def register_routes(app: FastAPI):
    """
    注册路由
    :param app: FastAPI
    :return: None
    """

    # 添加路径前缀
    router_path = lambda path: f"/api/v1/{path}"

    # 注册鉴权路由
    app.include_router(auth_router, prefix=router_path("auth"))

    # 注册首页路由
    app.include_router(home_router, prefix=router_path("home"))

    # 注册系统路由
    app.include_router(system_router, prefix=router_path("system"))

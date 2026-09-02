from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .visit_log import visit_log_middleware


def register_middleware(app: FastAPI):
    """
    注册中间件
    :param app: FastAPI
    :return: None
    """

    # cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 访问日志
    visit_log_middleware(app)

# settings.py
from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class AppConfigSettings(BaseSettings):
    """应用程序设置"""
    # 基础配置
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8080

    # 基础目录
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent

    # 数据库配置
    DB_HOST: str = ""
    DB_PORT: int
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_URL: str = ''

    # jwt
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    # redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_MAX_CONNECTIONS: int = 100
    REDIS_DB: int

    # 雪花算法
    SNOWFLAKE_WORKER_ID: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",  # 指定文件（相对于当前文件路径）
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略 .env 里多余的变量
        case_sensitive=True,  # 推荐保持默认 True，让字段名和 .env 完全一致
    )


app_settings = AppConfigSettings()

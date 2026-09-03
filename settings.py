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

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",  # 指定文件（相对于当前文件路径）
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略 .env 里多余的变量
        case_sensitive=True,  # 推荐保持默认 True，让字段名和 .env 完全一致
    )


app_settings = AppConfigSettings()

# settings.py
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



class AppConfigSettings(BaseSettings):

    """应用程序设置"""
    # 基础配置
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8080

    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent

    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "py_dome_001"
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",  # 指定文件（相对于当前文件路径）
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略 .env 里多余的变量
        case_sensitive=True,  # 推荐保持默认 True，让字段名和 .env 完全一致
    )


app_settings = AppConfigSettings()

# 数据库配置
TORTOISE_ORM = {
    # 数据库连接配置
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",  # 使用 mysql 驱动
            "credentials": {
                "host": app_settings.DB_HOST,  # 数据库主机
                "port": app_settings.DB_PORT,  # 数据库端口
                "user": app_settings.DB_USER,  # 数据库用户
                "password": app_settings.DB_PASSWORD,  # 数据库密码
                "database": app_settings.DB_NAME,  # 数据库名称
                "charset": "utf8mb4",  # 支持完整 Unicode
            },
            # 连接池参数
            "minsize": 1,  # 最小连接数
            "maxsize": 10,  # 最大连接数
            "echo": False,  # 生产环境关闭
        }
    },
    # 应用模型映射
    "apps": {
        "models": {
            "models": ["src.apps.models"],
            "default_connection": "default",
            "migrations": "src.apps.migrations",  # 新增：指定迁移文件存放路径
        },
    },
    # 全局配置（可选）
    "use_tz": False,  # 使用本地时区，关闭时区转换
    "timezone": "Asia/Shanghai",  # 时区配置
}

# aerich init -t settings.TORTOISE_ORM # 在项目根目录生成 pyproject.toml（或 aerich.ini），记录配置路径。

# aerich init-db 连接数据库，并创建 aerich 表（用于记录哪些迁移已执行）。

# aerich migrate 生成迁移文件（.py 文件），只写文件，不动数据库。 也可以 aerich migrate --name "描述本次改动"

# aerich upgrade 将尚未执行的迁移文件（生成的脚本）应用到数据库，修改表结构。

# aerich heads 列出当前所有已生成的迁移文件版本号（即代码里的最新文件列表）。

# aerich history 显示当前数据库已执行的迁移历史记录。

# aerich merge 合并迁移文件 (当你在一个分支上生成了 0003_a，同时同事在另一个分支上生成了 0003_b，直接 upgrade 会报错。此时需要使用 merge 将两个迁移文件合并成一个新的文件，然后再执行 aerich upgrade)

# aerich check 用于检查当前模型定义与最后一次迁移记录是否有差异。它不会生成文件，只告诉你“有没有变动”，适合在提交代码前检查是否忘记生成迁移文件

# aerich downgrade 回滚迁移 aerich downgrade -1  aerich downgrade 0001_initial <-回退到指定的具体版本号


"""
# 1. 改完模型后，生成迁移文件
aerich migrate --name 描述本次改动

# 2. 检查本地版本（可选）
aerich heads

# 3. 提交给数据库执行
aerich upgrade

如果发现 upgrade 错了，立刻执行 aerich downgrade -1 回滚
"""

"""
init 
tortoise init 
为已配置的应用创建迁移包。这确保了每个应用都有一个 migrations 模块

makemigrations
tortoise makemigrations 检测 所有已注册的应用（apps） 的模型变化。自动生成包含模型变化的迁移文件（如新增字段、删除表等）
tortoise makemigrations --name add_posts_table 生成名为 add_posts_table 的迁移文件
tortoise makemigrations users 为 users 应用生成迁移文件
tortoise makemigrations --empty users 为 users 应用生成空迁移文件


tortoise migrate 或 tortoise upgrade
应用迁移。migrate 可以根据目标向前或向后迁移。upgrade 仅限向前迁移，拒绝回滚

tortoise history
显示当前数据库已执行的迁移历史记录。

tortoise heads
列出当前所有已生成的迁移文件版本号（即代码里的最新文件列表）。

tortoise downgrade
取消特定应用的已应用迁移。downgrade 仅限向后迁移，拒绝应用新的迁移。如果未提供迁移名称，它将针对该应用的第一个迁移。
"""

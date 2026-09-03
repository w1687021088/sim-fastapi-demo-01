import jwt
from datetime import datetime, timedelta, UTC
from settings import app_settings


def create_access_token(data: dict) -> str:
    """创建访问令牌"""

    # 复制数据
    to_encode = data.copy()

    # 添加过期时间
    expire = datetime.now(UTC) + timedelta(minutes=app_settings.JWT_EXPIRE_MINUTES)

    # 更新数据
    to_encode.update({"exp": expire})

    # 创建令牌
    return jwt.encode(to_encode, app_settings.JWT_SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """解码访问令牌"""
    try:
        # 解码令牌
        payload = jwt.decode(token, app_settings.JWT_SECRET_KEY, algorithms=[app_settings.JWT_ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None

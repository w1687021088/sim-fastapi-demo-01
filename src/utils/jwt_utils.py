import uuid
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
    to_encode.update({
        "exp": expire,
        "jti": str(uuid.uuid4())
    })

    # 创建令牌
    return jwt.encode(to_encode, app_settings.JWT_SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, str]:
    """
    解码并验证 token
    如果 token 过期 → 抛出 ExpiredSignatureError
    如果 token 无效（签名错误、格式错误等）→ 抛出 InvalidTokenError
    """
    return jwt.decode(
        token,
        app_settings.JWT_SECRET_KEY,
        algorithms=[app_settings.JWT_ALGORITHM]
        # verify_exp=True 是默认行为，过期时自动抛 ExpiredSignatureError
    )
    # """解码访问令牌"""
    # try:
    #     # 解码令牌
    #     payload = jwt.decode(token, app_settings.JWT_SECRET_KEY, algorithms=[app_settings.JWT_ALGORITHM])
    #     return payload  # {'user_id': str, 'exp': int, 'jti': str}
    # except jwt.InvalidTokenError:
    #     return None


def access_token_blocklist_key_prefix(jti: str) -> str:
    """获取访问令牌黑名单key前缀"""
    return f"auth:access-token:{jti}"


def get_access_token_remaining_seconds(token: str) -> int:
    """获取访问令牌剩余有效期"""
    payload = decode_access_token(token)
    if payload is None:
        return 0
    exp = int(payload.get("exp", 0))
    now = int(datetime.now(UTC).timestamp())
    remaining_seconds = max(0, exp - now)
    return remaining_seconds

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from redis.exceptions import RedisError  # 导入 Redis 异常

from src.utils import decode_access_token, access_token_blocklist_key_prefix
from src.libs import app_redis, raise_biz_error
from src.config import BizCode

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/account/login",
    auto_error=False
)


async def require_auth(token: str = Depends(oauth2_scheme)):
    """ 鉴权依赖 """
    # 1. 检查是否提供了 token
    if not token:
        raise_biz_error(
            code=BizCode.TOKEN_MISSING,
            http_status_code=401
        )

    # 2. 解码并验证 token
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError:
        raise_biz_error(
            code=BizCode.TOKEN_EXPIRED,
            http_status_code=401
        )
    except InvalidTokenError:
        raise_biz_error(
            code=BizCode.TOKEN_INVALID,
            http_status_code=401
        )
    else:
        # 只有 token 解码成功时才执行这里
        # 3. 检查 jti
        jti = payload.get("jti")
        if not jti:
            raise_biz_error(
                code=BizCode.TOKEN_MISSING_JTI,
                http_status_code=401
            )

        # 4. 检查黑名单
        blacklist_key = access_token_blocklist_key_prefix(jti)
        try:
            is_blacklisted = await app_redis.client.exists(blacklist_key)
        except RedisError:
            # Redis 异常时降级处理：认为 token 不在黑名单（避免把用户全拦了）
            is_blacklisted = False

        if is_blacklisted:
            raise_biz_error(
                code=BizCode.TOKEN_BLACKLISTED,
                http_status_code=401
            )

        # 5. 返回用户信息
        return {"user_id": payload.get("user_id")}

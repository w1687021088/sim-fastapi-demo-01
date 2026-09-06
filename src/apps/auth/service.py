from datetime import datetime, UTC
from typing import Any
from src.config import BizCode
from src.libs.redis_client import app_redis
from src.libs.exception import raise_biz_error
from src.models import UserInfoModel
from src.utils.bcrypt_utils import hash_password, verify_password
from src.utils.jwt_utils import create_access_token, access_token_blocklist_key_prefix
from src.utils.snowflake_utils import generate_snowflake_id
from src.apps.auth.schemas import (
    AuthRegisterBody,
    AuthLoginBody,
    AuthLoginResponse,
    AuthChangePasswordBody,
    UserInfoResponse
)


async def handle_register(body: AuthRegisterBody):
    """ 处理注册逻辑 """

    # 1. 检查用户名是否已存在
    if await UserInfoModel.filter(username=body.username).exists():
        raise_biz_error(BizCode.USERNAME_ALREADY_EXISTS)

    # 2. 检查手机号（若提供）是否已存在
    if body.phone and await UserInfoModel.filter(phone=body.phone).exists():
        raise_biz_error(BizCode.PHONE_ALREADY_EXISTS)

    # 3. 检查邮箱（若提供）是否已存在
    if body.email and await UserInfoModel.filter(email=body.email).exists():
        raise_biz_error(BizCode.EMAIL_ALREADY_EXISTS)

    hashed_password = hash_password(body.password)

    # id
    user_id = generate_snowflake_id()

    # 5. 创建用户
    user = await UserInfoModel.create(
        user_id=user_id,
        username=body.username,
        password=hashed_password,
        phone=body.phone,
        email=body.email,
    )

    # 6. 生成 JWT Token
    token = create_access_token(data={"sub": user.username, "user_id": str(user.user_id)})

    return {
        "token": token,
    }


async def handle_login(body: AuthLoginBody) -> dict[str, Any]:
    # 1. 查找用户
    user: UserInfoModel = await UserInfoModel.get_or_none(username=body.username)
    if not user:
        raise_biz_error(BizCode.USER_NOT_FOUND)
        # raise AppException(BizCode.USER_NOT_FOUND)

    # 2. 验证密码
    if not verify_password(body.password, user.password):
        raise_biz_error(BizCode.USER_PASSWORD_ERROR)
        # raise AppException(BizCode.USER_PASSWORD_ERROR)

    # 3. 生成 token
    token = create_access_token(data={"sub": user.username, "user_id": str(user.user_id)})

    # 4. 构造响应
    return AuthLoginResponse(
        token=token,
        user_id=str(user.user_id),
        username=user.username,
        phone=user.phone,
        email=user.email,
        avatar=user.avatar,
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
        enabled=user.enabled,
    ).model_dump()


async def handle_change_password(body: AuthChangePasswordBody, current_user: dict):
    """处理修改密码逻辑"""
    user_id = current_user.get("user_id")
    jti = current_user.get("jti")
    exp = current_user.get("exp")

    if not jti:
        raise_biz_error(BizCode.TOKEN_MISSING_JTI)

    # 1. 获取用户
    user = await UserInfoModel.get(user_id=user_id)
    if not user:
        raise_biz_error(BizCode.USER_NOT_FOUND)

    # 2. 验证旧密码
    if not verify_password(body.old_password, user.password):
        raise_biz_error(BizCode.USER_PASSWORD_ERROR)

    # 3. 更新密码
    user.password = hash_password(body.new_password)
    await user.save(update_fields=["password", "updated_at"])

    # 4. 将当前 token 加入黑名单（强制登出）
    blacklist_key = access_token_blocklist_key_prefix(jti)
    if exp:
        ttl = int(exp - datetime.now().timestamp())
        if ttl > 0:
            await app_redis.client.setex(blacklist_key, ttl, "1")
        else:
            # token 已过期但为了安全仍保留 60 秒
            await app_redis.client.setex(blacklist_key, 60, "1")
    else:
        # 无 exp 则默认保留 1 小时
        await app_redis.client.setex(blacklist_key, 3600, "1")


async def handle_logout(current_user: dict):
    """ 处理登出逻辑 """
    jti = current_user.get("jti")
    exp = current_user.get("exp")
    if not jti:
        raise_biz_error(BizCode.TOKEN_MISSING_JTI)
    blacklist_key = access_token_blocklist_key_prefix(jti)

    if exp:
        ttl = int(exp - datetime.now().timestamp())
        if ttl > 0:
            await app_redis.client.setex(blacklist_key, ttl, "1")
        else:
            # token 已过期但为了安全仍保留 60 秒
            await app_redis.client.setex(blacklist_key, 60, "1")
    else:
        # 无 exp 则默认保留 1 小时
        await app_redis.client.setex(blacklist_key, 3600, "1")


async def handle_get_user_info(current_user: dict) -> dict:
    """ 处理获取用户信息逻辑 """
    user_id = current_user.get("user_id")

    user = await UserInfoModel.get(user_id=user_id)
    if not user:
        raise_biz_error(BizCode.USER_NOT_FOUND)

    # 使用 Pydantic 模型构造返回数据
    user_info = UserInfoResponse(
        user_id=str(user.user_id),
        username=user.username,
        phone=user.phone,
        email=user.email,
        avatar=user.avatar,
        created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        enabled=user.enabled,
    )
    return user_info.model_dump()

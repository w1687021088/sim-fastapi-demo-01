from typing import Any

from config import BizCode
from src.libs.exception import raise_biz_error
from src.models import UserInfoModel
from src.utils import hash_password, create_access_token
from apps.auth.schemas import (
    AuthRegisterBody,
    AuthLoginBody,
    AuthLoginResponse
)
from utils import verify_password


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

    # 5. 创建用户
    user = await UserInfoModel.create(
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

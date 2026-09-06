from fastapi import APIRouter, Body, Depends
from typing import Annotated
from src.apps.auth.schemas import (
    AuthRegisterBody,
    AuthRegisterResponse,
    AuthLoginBody,
    AuthLoginResponse,
    AuthChangePasswordBody,
    UserInfoResponse
)
from src.config import AppResponse, CommonResponseModel
from src.apps.auth.service import (
    handle_register,
    handle_login,
    handle_change_password,
    handle_logout,
    handle_get_user_info

)
from src.apps.dependencies import require_auth

router = APIRouter()


@router.post("/login", description="用户登录", response_model=CommonResponseModel[AuthLoginResponse])
async def login(body: AuthLoginBody):
    result = await handle_login(body)
    return AppResponse(data=result)


@router.post("/register", description="用户注册", response_model=CommonResponseModel[AuthRegisterResponse])
async def register(body: Annotated[AuthRegisterBody, Body()]):
    result = await handle_register(body)
    return AppResponse(data=result)


@router.post("/change-password", description="用户修改密码", response_model=CommonResponseModel)
async def change_password(body: AuthChangePasswordBody, current_user: dict = Depends(require_auth)):
    await handle_change_password(body, current_user)
    return AppResponse(message="密码修改成功，请重新登录")


@router.post("/logout", description="登出", response_model=CommonResponseModel)
async def logout(current_user: dict = Depends(require_auth)):
    await handle_logout(current_user)
    return AppResponse(message="登出成功")


@router.get("/user-info", description="获取用户信息", response_model=CommonResponseModel[UserInfoResponse])
async def get_user_info(current_user: dict = Depends(require_auth)):
    info = await handle_get_user_info(current_user)
    return AppResponse(data=info)

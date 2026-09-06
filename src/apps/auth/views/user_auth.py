from fastapi import APIRouter, Body
from typing import Annotated
from apps.auth.schemas import (
    AuthRegisterBody,
    AuthRegisterResponse,
    AuthLoginBody,
    AuthLoginResponse,
)
from src.config import AppResponse, CommonResponseModel
from apps.auth.service import (
    handle_register,
    handle_login,
)

router = APIRouter()


@router.post("/login", description="用户登录", response_model=CommonResponseModel[AuthLoginResponse])
async def login(body: AuthLoginBody):
    result = await handle_login(body)
    return AppResponse(data=result)


@router.post("/register", description="用户注册", response_model=CommonResponseModel[AuthRegisterResponse])
async def register(body: Annotated[AuthRegisterBody, Body()]):
    result = await handle_register(body)
    return AppResponse(data=result)


@router.post("/change-password", description="用户修改密码")
async def change_password():
    pass


@router.post("/logout", description="登出")
async def logout():
    pass

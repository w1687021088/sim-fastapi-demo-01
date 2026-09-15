from fastapi import APIRouter, Body, Depends
from typing import Annotated
from src.apps.auth.schemas import AuthRegisterBody, AuthRegisterResponse, AuthLoginBody, AuthLoginResponse
from src.config.response import AppResponse, AppResponseModel
from src.apps.auth.service import handle_register, handle_login, handle_logout
from src.apps.dependencies import require_auth

router = APIRouter()


@router.post("/login", description="用户登录", response_model=AppResponseModel[AuthLoginResponse])
async def login(body: AuthLoginBody):
    result = await handle_login(body)
    return AppResponse(data=result)


@router.post("/register", description="用户注册", response_model=AppResponseModel[AuthRegisterResponse])
async def register(body: Annotated[AuthRegisterBody, Body()]):
    result = await handle_register(body)
    return AppResponse(data=result)


@router.post("/logout", description="登出", response_model=AppResponseModel)
async def logout(current_user: dict = Depends(require_auth)):
    await handle_logout(current_user)
    return AppResponse(message="登出成功")

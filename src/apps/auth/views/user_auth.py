from fastapi import APIRouter, Body

from apps.auth.schemas import AuthRegisterBody, AuthRegisterResponse
from typing import Annotated
from src.config import AppResponse, CommonResponseModel

router = APIRouter()


@router.post("/login", description="用户登录")
async def login():
    pass


@router.post("/register", description="用户注册", response_model=CommonResponseModel[AuthRegisterResponse])
async def register(body: Annotated[AuthRegisterBody, Body()]):
    return AppResponse(data={"message": "注册成功"})



@router.post("/change-password", description="用户修改密码")
async def change_password():
    pass


@router.post("/logout", description="登出")
async def logout():
    pass

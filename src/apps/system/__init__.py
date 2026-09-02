from fastapi import APIRouter
from .views.auth import router as auth_router
from .views.user import router as user_router

system_router = APIRouter()

# 注册认证路由
system_router.include_router(auth_router, prefix="/auth", tags=["认证"])

# 注册用户路由
system_router.include_router(user_router, prefix="/user", tags=["用户"])

from fastapi import APIRouter
from .views.user import router as user_router

system_router = APIRouter()

# 注册用户路由
system_router.include_router(user_router, prefix="/user", tags=["用户"])

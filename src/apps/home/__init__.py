from fastapi import APIRouter
from .views.view import router as main_router

home_router = APIRouter()

# 首页核心
home_router.include_router(main_router, prefix="/main", tags=["首页核心"])

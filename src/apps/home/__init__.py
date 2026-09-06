from fastapi import APIRouter, Depends
from .views.view import router as main_router
from src.apps.dependencies import require_auth

home_router = APIRouter(dependencies=[Depends(require_auth)])

# 首页核心
home_router.include_router(main_router, prefix="/main", tags=["首页核心"])

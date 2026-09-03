from fastapi import APIRouter
from .views.user_auth import router as user_auth_router

auth_router = APIRouter()

# auth
auth_router.include_router(user_auth_router, prefix="/auth", tags=["认证"])

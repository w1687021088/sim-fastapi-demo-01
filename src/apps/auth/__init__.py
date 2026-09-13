from fastapi import APIRouter
from src.apps.auth.views.user_auth import router as user_auth_router
from src.apps.auth.views.user import router as user_router

auth_router = APIRouter()

# auth
auth_router.include_router(user_auth_router, prefix="/account", tags=["认证"])

# user
auth_router.include_router(user_router, prefix="/user", tags=["用户"])

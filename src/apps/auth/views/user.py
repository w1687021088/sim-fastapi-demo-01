from fastapi import APIRouter, Depends
from src.apps.auth.views.user_auth import require_auth
from src.apps.auth.schemas import UserInfoResponse, AuthChangePasswordBody
from src.config.response import AppResponse, CommonResponseModel
from src.apps.auth.service import handle_get_user_info, handle_change_password

router = APIRouter()


@router.get("/info", description="获取用户信息", response_model=CommonResponseModel[UserInfoResponse])
async def get_user_info(current_user: dict = Depends(require_auth)):
    print(current_user)
    info = await handle_get_user_info(current_user)
    return AppResponse(data=info)


@router.post("/change-password", description="用户修改密码", response_model=CommonResponseModel)
async def change_password(body: AuthChangePasswordBody, current_user: dict = Depends(require_auth)):
    await handle_change_password(body, current_user)
    return AppResponse(message="密码修改成功，请重新登录")
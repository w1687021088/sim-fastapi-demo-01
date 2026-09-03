from fastapi import APIRouter
from src.models.User import UserInfoModel
from pydantic import BaseModel

router = APIRouter()


@router.get("/info")
async def info():
    user_info = await UserInfoModel.get_or_none(id=1)

    if user_info:
        print(user_info.username)

    await UserInfoModel.create(username="test", password="test")
    return "info111"

from fastapi import APIRouter
from src.libs import logger

router = APIRouter()


@router.get("/info")
async def info():
    logger.info("info, 我来啦")
    return "info111"

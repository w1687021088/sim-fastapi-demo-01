from fastapi import APIRouter
router = APIRouter()


@router.get("/info")
async def info():
    1 / 0
    return "info111"

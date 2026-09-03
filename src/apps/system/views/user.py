from fastapi import APIRouter

router = APIRouter()


@router.post("/login", description="用户登录")
async def login():
    return {"message": "Login successful"}


@router.get("/register", description="用户注册")
async def register():
    return {"message": "Register successful"}

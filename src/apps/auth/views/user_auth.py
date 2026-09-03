from fastapi import APIRouter

router = APIRouter()


@router.post("/login", description="用户登录")
async def login():
    pass


@router.post("/register", description="用户注册")
async def register():
    pass


@router.post("/change-password", description="用户修改密码")
async def change_password():
    pass


@router.post("/logout", description="登出")
async def logout():
    pass

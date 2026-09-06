from .base import BaseModel
from tortoise import fields
from passlib.context import CryptContext

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserInfoModel(BaseModel):
    # def __init__(self, **kwargs: Any):
    #     super().__init__(**kwargs)
    #     self.online_user: OnlineUserModel = None

    """
    用户信息表
    """
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField(unique=True, description="用户公开唯一标识（雪花ID）")
    username = fields.CharField(unique=True, max_length=100, description="用户名称")
    password = fields.CharField(max_length=100, description="用户密码")
    email = fields.CharField(max_length=255, unique=True, null=True, description="用户邮箱")
    phone = fields.CharField(max_length=20, unique=True, null=True, description="用户手机号")
    enabled = fields.BooleanField(default=False, description="用户状态是否启用？1启用 0禁用")
    avatar = fields.CharField(max_length=255, null=True, description="用户头像")

    class Meta:
        # 表名
        table = "user_info"
        # 默认排序
        ordering = ["-created_at"]

    # @classmethod
    # def make_password(cls, login_password: str) -> str:
    #     """
    #     密码加密
    #     :param login_password:str
    #     :return: str
    #     """
    #     return pwd_context.hash(login_password)
    #
    # def verify_password(self, login_password: str):
    #     """
    #      验证密码
    #     :param login_password: str
    #     :return: bool
    #     """
    #     return pwd_context.verify(login_password, self.password)


class OnlineUserModel(BaseModel):
    """
    在线用户表
    """
    id = fields.BigIntField(pk=True)
    browser = fields.CharField(max_length=255, null=True, description="浏览器信息")
    os = fields.CharField(max_length=255, null=True, description="操作系统信息")
    ip = fields.CharField(max_length=20, null=True, description="用户IP")
    client = fields.CharField(max_length=255, null=True, description="客户端类型：pc、android、ios")
    user = fields.ForeignKeyField(
        "models.UserInfoModel",
        related_name="online_user",
        null=True,
        on_delete=fields.CASCADE,
        db_constraint=True
    )

    class Meta:
        # 表名
        table = "online_user"
        # 默认排序
        ordering = ["-created_at"]

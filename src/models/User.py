from .base import BaseModel
from tortoise import fields
import uuid


class UserInfoModel(BaseModel):
    id = fields.BigIntField(pk=True)
    user_uuid = fields.UUIDField(unique=True, default=uuid.uuid4, description="用户公开唯一标识")
    username = fields.CharField(unique=True, max_length=100, description="用户名称")
    password = fields.CharField(max_length=100, description="用户密码")
    email = fields.CharField(max_length=255, unique=True, null=True, description="用户邮箱")
    phone = fields.CharField(max_length=20, unique=True, null=True, description="用户手机号")

    class Meta:
        # 表名
        table = "user_info"
        # 默认排序
        ordering = ["-created_at"]

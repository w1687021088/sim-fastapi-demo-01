from .base import BaseModel
from tortoise import fields


class UserInfoModel(BaseModel):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(unique=True, max_length=100, description="用户名称")

    class Meta:
        # 表名
        table = "user_info"
        # 默认排序
        ordering = ["-created_at"]

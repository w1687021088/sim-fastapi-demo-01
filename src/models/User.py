from tortoise.models import Model
from tortoise import fields


class UserInfoModel(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(unique=True, max_length=100, description="用户名称")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "user_info"

        ordering = ["-created_at"]

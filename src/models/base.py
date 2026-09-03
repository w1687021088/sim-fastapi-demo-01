from tortoise.models import Model
from tortoise import fields

class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True  # 关键：告诉 Tortoise 这只是基类，不创建表

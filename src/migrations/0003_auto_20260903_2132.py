from tortoise import migrations
from tortoise.migrations import operations as ops
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0002_auto_20260903_2124')]

    initial = False

    operations = [
        ops.AddField(
            model_name='UserInfoModel',
            name='user_uuid',
            field=fields.UUIDField(default=uuid4, unique=True, description='用户公开唯一标识'),
        ),
    ]

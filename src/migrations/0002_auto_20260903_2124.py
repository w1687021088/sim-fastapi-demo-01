from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_init_user_info')]

    initial = False

    operations = [
        ops.AddField(
            model_name='UserInfoModel',
            name='updated_at',
            field=fields.DatetimeField(description='更新时间', auto_now=True, auto_now_add=False),
        ),
    ]

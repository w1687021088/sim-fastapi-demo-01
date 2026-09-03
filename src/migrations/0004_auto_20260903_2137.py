from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0003_auto_20260903_2132')]

    initial = False

    operations = [
        ops.AddField(
            model_name='UserInfoModel',
            name='email',
            field=fields.CharField(null=True, unique=True, description='用户邮箱', max_length=255),
        ),
        ops.AddField(
            model_name='UserInfoModel',
            name='password',
            field=fields.CharField(description='用户密码', max_length=100),
        ),
        ops.AddField(
            model_name='UserInfoModel',
            name='phone',
            field=fields.CharField(null=True, unique=True, description='用户手机号', max_length=20),
        ),
    ]

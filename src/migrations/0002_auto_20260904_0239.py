from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_initial')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='OnlineUserModel',
            name='browser',
            field=fields.CharField(null=True, description='浏览器信息', max_length=255),
        ),
        ops.AlterField(
            model_name='OnlineUserModel',
            name='ip',
            field=fields.CharField(null=True, description='用户IP', max_length=20),
        ),
        ops.AlterField(
            model_name='OnlineUserModel',
            name='os',
            field=fields.CharField(null=True, description='操作系统信息', max_length=255),
        ),
        ops.AddField(
            model_name='OnlineUserModel',
            name='client',
            field=fields.CharField(null=True, description='客户端类型：pc、android、ios', max_length=255),
        ),
    ]

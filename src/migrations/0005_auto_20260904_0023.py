from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0004_auto_20260903_2137')]

    initial = False

    operations = [
        ops.CreateModel(
            name='OnlineUserModel',
            fields=[
                ('created_at', fields.DatetimeField(description='创建时间', auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(description='更新时间', auto_now=True, auto_now_add=False)),
                ('id', fields.BigIntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('browser', fields.CharField(description='浏览器信息', max_length=255)),
                ('os', fields.CharField(description='操作系统信息', max_length=255)),
                ('ip', fields.CharField(description='用户IP', max_length=20)),
                ('user', fields.ForeignKeyField('models.UserInfoModel', source_field='user_id', null=True, db_constraint=True, to_field='id', related_name='User_info', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'online_user', 'app': 'models', 'pk_attr': 'id', 'table_description': '在线用户表'},
            bases=['BaseModel'],
        ),
        ops.AlterModelOptions(
            name='UserInfoModel',
            options={'table': 'user_info', 'app': 'models', 'pk_attr': 'id', 'table_description': '用户信息表'},
        ),
        ops.AddField(
            model_name='UserInfoModel',
            name='avatar',
            field=fields.CharField(null=True, description='用户头像', max_length=255),
        ),
        ops.AddField(
            model_name='UserInfoModel',
            name='enabled',
            field=fields.BooleanField(default=False, description='用户状态是否启用？1启用 0禁用'),
        ),
    ]

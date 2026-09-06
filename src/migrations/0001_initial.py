from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='UserInfoModel',
            fields=[
                ('created_at', fields.DatetimeField(description='创建时间', auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(description='更新时间', auto_now=True, auto_now_add=False)),
                ('id', fields.BigIntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('user_id', fields.BigIntField(unique=True, description='用户公开唯一标识（雪花ID）')),
                ('username', fields.CharField(unique=True, description='用户名称', max_length=100)),
                ('password', fields.CharField(description='用户密码', max_length=100)),
                ('email', fields.CharField(null=True, unique=True, description='用户邮箱', max_length=255)),
                ('phone', fields.CharField(null=True, unique=True, description='用户手机号', max_length=20)),
                ('enabled', fields.BooleanField(default=False, description='用户状态是否启用？1启用 0禁用')),
                ('avatar', fields.CharField(null=True, description='用户头像', max_length=255)),
            ],
            options={'table': 'user_info', 'app': 'models', 'pk_attr': 'id', 'table_description': '用户信息表'},
            bases=['BaseModel'],
        ),
        ops.CreateModel(
            name='OnlineUserModel',
            fields=[
                ('created_at', fields.DatetimeField(description='创建时间', auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(description='更新时间', auto_now=True, auto_now_add=False)),
                ('id', fields.BigIntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('browser', fields.CharField(null=True, description='浏览器信息', max_length=255)),
                ('os', fields.CharField(null=True, description='操作系统信息', max_length=255)),
                ('ip', fields.CharField(null=True, description='用户IP', max_length=20)),
                ('client', fields.CharField(null=True, description='客户端类型：pc、android、ios', max_length=255)),
                ('user', fields.ForeignKeyField('models.UserInfoModel', source_field='user_id', null=True, db_constraint=True, to_field='id', related_name='online_user', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'online_user', 'app': 'models', 'pk_attr': 'id', 'table_description': '在线用户表'},
            bases=['BaseModel'],
        ),
    ]

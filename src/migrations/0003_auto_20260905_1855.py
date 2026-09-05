from tortoise import migrations
from tortoise.migrations import operations as ops

class Migration(migrations.Migration):
    dependencies = [('models', '0002_auto_20260904_0239')]

    initial = False

    operations = [
        ops.AlterModelOptions(
            name='UserInfoModel',
            options={'table': 'user_info', 'app': 'models', 'pk_attr': 'id'},
        ),
    ]

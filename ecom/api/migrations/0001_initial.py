from django.db import migrations

from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name='ganesh', email="ganicoit1998@gmail.com",
                          is_staff=True, is_superuser=True, phone="7349209179", gender="Male")

        user.set_password('1234')
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]

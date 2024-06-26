# Generated by Django 4.2.13 on 2024-05-24 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import marketplace.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0015_marketplaceprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplaceprofile',
            name='user',
            field=models.ForeignKey(default=marketplace.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.13 on 2024-05-24 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0013_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketplaceprofile',
            name='user',
        ),
    ]
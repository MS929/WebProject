# Generated by Django 4.2.13 on 2024-06-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0020_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-03 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santapp', '0003_auto_20201129_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='data_available_time',
        ),
        migrations.AddField(
            model_name='user',
            name='friend_available',
            field=models.BooleanField(default=False),
        ),
    ]

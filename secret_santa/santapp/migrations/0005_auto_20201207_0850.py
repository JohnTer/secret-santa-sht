# Generated by Django 3.1.3 on 2020-12-07 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santapp', '0004_auto_20201203_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='wishlist',
            field=models.CharField(default=None, max_length=2048, null=True),
        ),
    ]
